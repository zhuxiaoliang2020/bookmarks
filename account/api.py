
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from account.logics import user_auth, user_register, user_edit

# Create your views here.
from account.forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm



from account.models import Contact
from actions.models import Actions
from actions.utils import create_action
from common.decorators import ajax_required

#用户登录视图
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        #用户验证
        user_auth(request,form)
    else:
        form = LoginForm()
    return render(request,'account/login.html',{'form':form})


#主页视图
@login_required
def dashboard(request):
    #默认展示所有行为,不包含当前用户
    actions = Actions.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',flat=True)

    if following_ids:
        #如果当前用户有关注到用户,近展示用户的行为
        actions = actions.objects.filter(user_id__in=following_ids)
        # actions = actions[:10]
        actions = actions.select_related('user','user__profile').prefetch_related('target')[:10]
    return render(request,'account/dashboard.html',{'section':'dashboard','actions':actions})


#用户注册
def register(request):
    if request.method == 'POST':
        new_user = user_register(request)
        return render(request,'account/register_done.html',{'new_user':new_user})
    else:
        form = UserRegistrationForm()
        return render(request,'account/register.html',{'user_form':form})

#编辑个人信息
@login_required
def edit(request):
    if request.method == 'POST':
        user_form,profile_form = user_edit(request)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'account/edit.html',{'user_form':user_form,'profile_form':profile_form})


#用户列表
@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,'account/user/list.html',{'section':'people','username':users})

@login_required
def user_detail(request,username):
    user = get_object_or_404(User,username=username,is_active=True)
    return render(request, 'account/user/list.html')


#用户关注
@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,user_to=user)
                create_action(request.user,'关注了',user)
            else:
                Contact.objects.filter(user_from=request.user,user_to=user).delete()
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})

