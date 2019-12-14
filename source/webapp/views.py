from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import reverse, redirect, get_object_or_404

from webapp.forms import PhotoCommentForm, CommentForm
from webapp.mixins import StatsMixin
from webapp.models import Photo, Comment


class IndexView(StatsMixin, ListView):
    model = Photo
    template_name = 'index.html'

    def get_queryset(self):
        return Photo.objects.order_by('-created')


class PhotoView(StatsMixin, DetailView):
    model = Photo
    template_name = 'photo_detail.html'


class PhotoCreateView(PermissionRequiredMixin, StatsMixin, CreateView):
    model = Photo
    template_name = 'photo_create.html'
    fields = ('img', 'subscription', 'created')
    permission_required = 'webapp.add_photo'
    permission_denied_message = '403 Доступ запрещён!'

    def get_success_url(self):
        return reverse('webapp:photo_detail', kwargs={'pk': self.object.pk})


class PhotoUpdateView(LoginRequiredMixin, StatsMixin, UpdateView):
    model = Photo
    template_name = 'photo_update.html'
    fields = ('img', 'subscription', 'created')
    context_object_name = 'photo'

    def get_success_url(self):
        return reverse('webapp:photo_detail', kwargs={'pk': self.object.pk})


class PhotoDeleteView(LoginRequiredMixin, StatsMixin, DeleteView):
    model = Photo
    template_name = 'photo_delete.html'
    success_url = reverse_lazy('webapp:index')
    context_object_name = 'photo'

    def delete(self, request, *args, **kwargs):
        photo = self.object = self.get_object()
        photo.in_order = False
        photo.save()
        return HttpResponseRedirect(self.get_success_url())


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

    def dispatch(self, request, *args, **kwargs):
        self.photo = self.get_article()
        if self.photo.is_archived:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.photo.comments.create(**form.cleaned_data)
        return redirect('webapp:article_view', pk=self.photo.pk)

    def get_article(self):
        photo_pk = self.kwargs.get('pk')
        return get_object_or_404(Photo, pk=photo_pk)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'comment_create.html'
    form_class = CommentForm

    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class)
    #     form.fields['article'].queryset = Article.objects.filter(status=STATUS_ACTIVE)
    #     return form

    def get_success_url(self):
        return reverse('webapp:article_view', kwargs={'pk': self.object.article.pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.article.is_archived:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:article_view', kwargs={'pk': self.object.article.pk})