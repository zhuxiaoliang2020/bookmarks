from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.urls import reverse
from django.utils.text import slugify


class Image(models.Model):
    user = models.ForeignKey(User,related_name='images',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True,db_index=True)
    users_like = models.ManyToManyField(User,related_name='images_liked',blank=True)
    total_likes = models.PositiveIntegerField(db_index=True,default=0)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.slug:
            self.slug = slugify(self.title)

    def get_absolute_url(self):
        return reverse('images:detail',args=[self.id,self.slug])