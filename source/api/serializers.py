from rest_framework.serializers import ModelSerializer
from webapp.models import Comment, LikeDislike


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_by', 'images']


class LikeSerializer(ModelSerializer):
    class Meta:
        model = LikeDislike
        fields = ['id', 'vote', 'user', 'content_type', 'object_id']



