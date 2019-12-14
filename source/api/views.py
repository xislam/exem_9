from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

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

    @action(methods=['post'], detail=True)
    def rate_up(self, request, pk=None):
        photo_pk = request.data.get('photo')
        img = Photo.objects.get(pk=photo_pk)
        if self.queryset.filter(photo=img):
            return Response({'error': 'You have already liked it'}, status=400)
        img.likenum += 1
        img.save()

    @action(methods=['post'], detail=True)
    def rate_down(self, request, pk=None):
        photo_pk = request.data.get('photo')
        img = Photo.objects.get(pk=photo_pk)
        if self.queryset.filter(photo=img):
            return Response({'error': 'No let likes '}, status=400)
        img.likenum -= 1
        img.save()
