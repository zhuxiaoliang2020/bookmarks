from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from actions.utils import create_action
from common.decorators import ajax_required
from images.models import Image
import redis
from django.conf import settings

# Create your views here.

#创建图片
from images.forms import ImageCreateForm
from images.logics import image_create_logic

r = redis.Redis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)

@login_required
def image_created(request):
    if request.method == 'POST':
        form = ImageCreateForm(request.POST)
        image_create_logic(request,form)
    else:
        #根据GET请求传入的参数建立表单
        form = ImageCreateForm(data=request.GET)
    return render(request,'images/image/create.html',{'section':'images','form':form})

def image_detail(request,id,slug):
    image = get_object_or_404(Image,id=id,slug=slug)
    #浏览数+1
    total_views = r.incr('image:{}:views'.format(image.id))
    #在有序集合image_ranking里,把image.id的分数增加1
    r.zincrby('image_ranking',image.id,1)
    return render(request,'images/image/detail.html',{'section':'images','image':image,'total_views':total_views})

@login_required
def image_ranking(request):
    #获得排名前十的图片id列表
    image_ranking = r.zrange('image_ranking',0,-1,desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    #取排名最高的图片然后排序
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x:image_ranking_ids.index(x.id))
    return render(request,'images/image/ranking.html',{'section':'images','most_viewed':most_viewed })


#第三者喜欢和不喜欢分享的图片的动作
@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        image = get_object_or_404(Image,id=image_id)
        if action == 'like':
            image.users_like.add(request.user)
            create_action(request.user,'点赞了',image)
        else:
            image.users_like.remove(request.user)
            create_action(request.user,'取消点赞',image)
        return JsonResponse({'status':'ok'})
    else:
        pass
    return JsonResponse({'status':'ko'})


#图片列表分页
@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images,2)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        #如果页数不是一个整数就返回第一页
        images = paginator.page(1)
    except EmptyPage:
        #如果页数草果范围.显示最后一页
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,'images/image/list_ajax.html',{'section':'images','images':images})
    return render(request,'images/image/list.html',{'section':'images','images':images})