from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import reverse, get_object_or_404
from webapp.forms import PhotoCommentForm, CommentForm
from webapp.models import Photo, Comment



class IndexView(ListView):
    model = Photo
    template_name = 'index.html'

    def get_queryset(self):
        return Photo.objects.order_by('-created')


class PhotoView(DetailView):
    model = Photo
    template_name = 'photo_detail.html'


class PhotoCreateView(PermissionRequiredMixin, CreateView):
    model = Photo
    template_name = 'photo_create.html'
    fields = ('img', 'subscription', 'created')
    permission_required = 'webapp.add_photo'
    permission_denied_message = '403 Доступ запрещён!'

    def get_success_url(self):
        return reverse('webapp:photo_detail', kwargs={'pk': self.object.pk})


class PhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    template_name = 'photo_update.html'
    fields = ('img', 'subscription', 'created')
    context_object_name = 'photo'

    def get_success_url(self):
        return reverse('webapp:photo_detail', kwargs={'pk': self.object.pk})


class PhotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    template_name = 'photo_delete.html'
    success_url = reverse_lazy('webapp:index')
    context_object_name = 'photo'


class CommentListView(ListView):
    context_object_name = 'comments'
    model = Comment
    template_name = 'photo_detail.html'
    ordering = ['-created_at']
    paginate_by = 10
    paginate_orphans = 3


class CommentForArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'comment_create.html'
    form_class = PhotoCommentForm

    def get_article(self):
        photo_pk = self.kwargs.get('pk')
        return get_object_or_404(Photo, pk=photo_pk)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'comment_create.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('webapp:photo_detail', kwargs={'pk': self.object.photo.pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:photo_detail', kwargs={'pk': self.object.photo.pk})


