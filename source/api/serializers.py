from rest_framework.serializers import ModelSerializer
from webapp.models import Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_by']