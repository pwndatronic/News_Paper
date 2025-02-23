from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    # author__author__username
    '''Не должно быть выбора автора. Дополнить admin?..
    Поле Author - не пишет username. Идей нет.'''
    class Meta:
        model = Post
        fields = [
            'post_title',
            'post_body',
            'author'
        ]
