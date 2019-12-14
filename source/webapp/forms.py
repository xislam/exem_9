from django import forms

from webapp.models import Comment


class PhotoCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['created_by', 'text', 'images']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['date_ct']
