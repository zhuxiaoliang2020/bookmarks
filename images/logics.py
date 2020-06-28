from django.contrib import messages
from django.shortcuts import redirect

from actions.utils import create_action
from images.forms import ImageCreateForm


def image_create_logic(request,form):
    #判断表单数据是否通过验证
    if form.is_valid():
        #表单数据
        form_data = form.cleaned_data
        new_image = form.save(commit=False)
        #需要一并存入user的信息
        new_image.user = request.user
        new_image.save()
        create_action(request.user,'添加了一张图片',new_image)
        messages.success(request,'图片添加成功')
        #重定向到新创键的数据对象的详情视图
        return redirect(new_image.get_absolute_url())




