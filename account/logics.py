from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from account.forms import UserRegistrationForm, UserEditForm, ProfileEditForm

#用户登录
from account.models import Profile
from actions.utils import create_action


def user_auth(request,form):
    '''
    用户登录验证功能:
    1.验证表单的数据格式是否合法
    2.取出数据并使用django的验证框架进行验证
    3.验证通过说明数据库中有该条记录,然后验证用户的is_active字段是否为True
    4.若通过了步骤3,则调用login()方法,在绘画中设置用户信息
    '''
    if form.is_valid():
        datas = form.cleaned_data
        user = authenticate(request,username=datas['username'],password=datas['password'])
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponse('验证成功')
            else:
                return HttpResponse('该用户不存在')
        else:
            return HttpResponse('用户名或者密码不正确')
    else:
        return HttpResponse('输入的格式有误')

#用户注册
def user_register(request):
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
        #建立新数据对象但并不写入数据库
        new_user = form.save(commit=False)
        #验证两次输入的密码是否相同
        password = form.clean_password2()
        #将密码和其他信息一起存入数据库
        new_user.set_password(password)
        new_user.save()
        Profile.objects.create(user=new_user)
        create_action(new_user,'注册了账号')
        return new_user
#编辑个人信息
def user_edit(request):
    user_form = UserEditForm(request.POST)
    profile_form = ProfileEditForm(request.POST)
    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        create_action(request.user,'修改了个人信息')
        messages.success(request,'个人信息更新成功')
        return user_form,profile_form
    else:
        messages.error(request,'个人信息更新失败')