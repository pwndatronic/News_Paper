from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import PostForm
from .filters import NewsFilter
from .models import Post, User, Author

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['categories'] = post.postcategory_set.select_related('category')
        return context


@login_required()
def subscribe_to_categories(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    categories = post.categories.all()
    for category in categories:
        if not category.subscribers.filter(id=user.id).exists():
            category.subscribers.add(user)
    return redirect('/')


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    permission_required = 'news.add_post'
    template_name = 'post_edit.html'

    def form_valid(self, form):
        new = form.save(commit=False)
        new.post_content = self.model.news
        new.author = get_object_or_404(Author, author=self.request.user)
        new.save()
        super().form_valid(form)
        return self.send_to_subcribers(new)

    def send_to_subcribers(self, new):
        categories = new.categories.all()
        subscribers = User.objects.filter(subscribed_categories__in=categories).distinct()
        for subscriber in subscribers:
            html_content = render_to_string(
                'subscription_info.html',
                {'new': new, 'subscriber': subscriber}
            )
            msg = EmailMultiAlternatives(
                subject=f'Здравствуй, {subscriber.username}. Новая статья в твоём любимом разделе!',
                body='',
                from_email='pwndatronic@yandex.ru',
                to=[subscriber.email]
            )
            msg.attach_alternative(html_content, 'text/html')
            try:
                msg.send(fail_silently=False)
            except Exception as e:
                print(f'Ошибка: {e}')
        return redirect('/')


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    permission_required = 'news.change_post'
    pk_url_kwarg = 'id'
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')


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
