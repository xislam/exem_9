from django.contrib import admin

from webapp.models import Comment, Photo

admin.site.register(Photo)
admin.site.register(Comment)

