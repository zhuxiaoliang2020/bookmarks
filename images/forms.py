from urllib import request

from django import forms
from django.core.files.base import ContentFile

from images.models import *

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title','url','description')
        labels = {
            'title':'标题',
            'url':'链接',
            'description':'描述'
        }
        #所务信息的调用
        # error_messages = {
        #     'title':{'required':'title必填',},
        #     'description':{'reduired':'必填项',},
        # }
        widgets = {
            'url':forms.HiddenInput,
        }

    def save(self,force_insert=False,force_update=False,commit=True):
        image = super(ImageCreateForm,self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_extensions = image_url.split('.')[-1]
        image_name = slugify(self.title)+'.'+image_extensions

        #根据url下载图片
        response = request.urlopen(image_url)
        image.image.save(image_name,ContentFile(response.read()),save=False)
        if commit:
            image.save()
        return image


    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg','jpeg']
        url_extensions = url.split('.')[-1].lower()
        if url_extensions not in valid_extensions:
            raise forms.ValidationError('该链接不是图片url')
        return url
