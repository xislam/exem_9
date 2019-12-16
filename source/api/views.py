from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import json
from django.http import HttpResponse
from django.views import View
from django.contrib.contenttypes.models import ContentType
from webapp.models import LikeDislike
from api.serializers import CommentSerializer
from webapp.models import Comment, Photo


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            user.auth_token.delete()
        return Response({'status': 'ok'})


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.none()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action not in ['update', 'partial_update', 'destroy']:
            return [AllowAny()]
        return [IsAuthenticated()]


class RateUpView(APIView):

    # model = Photo  # Модель данных
    # vote_type = LikeDislike  # Тип комментария Like/Dislike

    # @action(methods=['post'], detail=True)
    def post(self, request, pk=None):
        photo_pk = request.data.get('obj')
        img = Photo.objects.get(pk=photo_pk)
        # if self.queryset.filter(photo=img):
        #     return Response({'error': 'You have already liked it'}, status=400)
        img.like += 1
        img.save()
        return Response({'id': img.pk})

    # @action(methods=['post'], detail=True)
    # def rate_down(self, request, pk=None):
    #     photo_pk = request.data.get('photo')
    #     img = Photo.objects.get(pk=photo_pk)
    #     if self.queryset.filter(photo=img):
    #         return Response({'error': 'No let likes '}, status=400)
    #     img.likenum -= 1
    #     img.save()

    # def post(self, request, pk):
    #     obj = self.model.objects.get(pk=pk)
    #     # GenericForeignKey не поддерживает метод get_or_create
    #     try:
    #         likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
    #                                               user=request.user)
    #         if likedislike.vote is not self.vote_type:
    #             likedislike.vote = self.vote_type
    #             likedislike.save(update_fields=['vote'])
    #             result = True
    #         else:
    #             likedislike.delete()
    #             result = False
    #     except LikeDislike.DoesNotExist:
    #         obj.votes.create(user=request.user, vote=self.vote_type)
    #         result = True
    #
    #     return HttpResponse(
    #         json.dumps({
    #             "id": obj.img.id(),
    #             "result": result,
    #             "like_count": obj.votes.likes().count(),
    #             "dislike_count": obj.votes.dislikes().count(),
    #             "sum_rating": obj.votes.sum_rating()
    #         }),
    #         content_type="application/json"
    #     )