from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import PostForm
from .filters import NewsFilter
from .models import Post

'''Создать PostList, NewsList @ ArticleList от него.'''


class NewsList(ListView):
    model = Post
    queryset = Post.objects.filter(
        post_content='NEWS'
    )
    ordering = '-post_creation_datetime'
    template_name = 'newslist.html'
    context_object_name = 'newslist'
    paginate_by = 10


class NewsSearch(NewsList):
    context_object_name = 'news_search'
    template_name = 'news_search.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    pk_url_kwarg = 'id'
    context_object_name = 'post_detail'


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    permission_required = 'news.add_post'
    template_name = 'post_edit.html'

    def form_valid(self, form):
        new = form.save(commit=False)
        new.post_content = self.model.news
        '''admin is not an instance of Author. ??
        request.user.username'''
        # new.author = self.request.user
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    permission_required = 'news.change_post'
    pk_url_kwarg = 'id'
    template_name = 'post_edit.html'


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    pk_url_kwarg = 'id'
    template_name = 'post_delete.html'
    permission_required = 'news.delete_post'
    success_url = reverse_lazy('news_list')


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    permission_required = 'news.add_post'
    template_name = 'post_edit.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.post_content = self.model.article
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    permission_required = 'news.delete_post'
    pk_url_kwarg = 'id'
    template_name = 'post_edit.html'


class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    pk_url_kwarg = 'id'
    permission_required = 'news.delete_post'
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')
