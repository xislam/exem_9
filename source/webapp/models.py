from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Sum


def get_admin():
    return User.objects.get(username='admin').pk


class Photo (models.Model):
    img = models.ImageField(null=True, blank=True, upload_to='img', verbose_name='Фото')
    subscription = models.TextField(max_length=3000, null=False, blank=False, verbose_name='Подпесь')
    date_ct = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    created = models.ForeignKey(User, default=get_admin, verbose_name='Автор',
                                on_delete=models.PROTECT, related_name='img_created')
    like = models.IntegerField(default=0, verbose_name="Лайки")
    # votes = GenericRelation('LikeDislike', related_query_name='img')

    def __str__(self):
        return self.subscription


class Comment(models.Model):
    text = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Текст')
    images = models.ForeignKey(Photo, verbose_name='Фото', on_delete=models.PROTECT, related_name='img_comment')
    created_by = models.ForeignKey(User, default=get_admin, verbose_name='Автор',
                                   on_delete=models.PROTECT, related_name='img_comment')
    date_ct = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # Забираем queryset с записями больше 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # Забираем queryset с записями меньше 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        # Забираем суммарный рейтинг
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

    def articles(self):
        return self.get_queryset().filter(content_type__model='img').order_by('-img__pub_date')


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    vote = models.SmallIntegerField(verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()