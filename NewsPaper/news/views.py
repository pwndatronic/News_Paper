from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    queryset = Post.objects.filter(
        post_content='NEWS'
    )
    ordering = '-post_creation_datetime'
    template_name = 'newslist.html'
    context_object_name = 'newslist'


class NewsDetail(DetailView):
    model = Post
    queryset = Post.objects.filter(
        post_content='NEWS'
    )
    template_name = 'newsdetail.html'
    pk_url_kwarg = 'id'
    context_object_name = 'newsdetail'
