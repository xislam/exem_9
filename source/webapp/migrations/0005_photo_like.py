# Generated by Django 2.2 on 2019-12-16 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20191215_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='like',
            field=models.IntegerField(default=0, verbose_name='Лайки'),
        ),
    ]
