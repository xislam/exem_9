from django.contrib.auth.models import User
from django.db import models


def get_admin():
    return User.objects.get(username='admin').pk


class Photo (models.Model):
    img = models.ImageField(null=True, blank=True, upload_to='img', verbose_name='Фото')
    subscription = models.TextField(max_length=3000, null=False, blank=False, verbose_name='Подпесь')
    date_ct = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    created = models.ForeignKey(User, default=get_admin, verbose_name='Автор', on_delete=models.PROTECT, related_name='img_created')

    def __str__(self):
        return self.subscription


class Comment(models.Model):
    text = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Текст')
    images = models.ForeignKey(Photo, verbose_name='Фото', on_delete=models.PROTECT, related_name='img_comment')
    created_by = models.ForeignKey(User, default=get_admin, verbose_name='Автор', on_delete=models.PROTECT, related_name='img_comment')
    date_ct = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


class Like(models.Model):
    pass
