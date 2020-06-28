from django.urls import path
from images.api import  *


app_name = 'images'
urlpatterns = [
    path(r'create/',image_created,name='create'),
    path(r'detail/<int:id>/<slug:slug>/',image_detail,name='detail'),
    path(r'like/',image_like,name='like'),
    path('ranking',image_ranking,name='image_ranking'),
    path('',image_list,name='list'),
]
