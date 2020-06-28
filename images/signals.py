from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from images.models import Image

@receiver(m2m_changed,sender=Image.users_like.though)
def users_like_changed(sender,**kwargs):
    kwargs['instance'].total_likes = kwargs['instance'].users_like.count()
    kwargs['instance'].save()