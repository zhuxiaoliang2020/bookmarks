from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='用户')
    date_of_birth = models.DateField(blank=True,null=True,verbose_name='出生日期')
    photo = models.ImageField(upload_to='user/%Y/%m/%d/',blank=True,verbose_name='照片')

    def __str__(self):
        return "Profile for user {}".format(self.user.username)

    class Meta:
        db_table = 'profile'
        verbose_name = '个人信息'
        verbose_name_plural = verbose_name


class Contact(models.Model):
    user_from = models.ForeignKey(User,related_name='rel_from_set',on_delete=models.CASCADE)
    user_to = models.ForeignKey(User,related_name='rel_to_set',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{}关注了{}'.format(self.user_from,self.user_to)

User.add_to_class('following',models.ManyToManyField('self',through=Contact,related_name='followers',symmetrical=False))


