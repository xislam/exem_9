from django.urls import path
from .views import *

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/create/', PhotoCreateView.as_view(), name='photo_create'),
    path('product/<int:pk>/', PhotoView.as_view(), name='photo_detail'),
    path('product/<int:pk>/update/', PhotoUpdateView.as_view(), name='photo_update'),
    path('product/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo_delete'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('comment/add/', CommentCreateView.as_view(), name='comment_add'),
   ]
