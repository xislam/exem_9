from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from .views import LogoutView, CommentViewSet, RateUpView
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from . import views
from webapp.models import LikeDislike, Photo

router = routers.DefaultRouter()
router.register(r'comment', CommentViewSet)
app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='obtain_auth_token'),
    path('logout/', LogoutView.as_view(), name='delete_auth_token'),
    path('<int:pk>/like/', RateUpView.as_view(),
         name='img_like'),
    # url(r'^img/<int:pk>/dislike/$',
    #     login_required(views.VotesView.as_view(model=Photo, vote_type=LikeDislike.DISLIKE)),
    #     name='img_dislike'),
]