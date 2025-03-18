from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


@login_required()
def become_author(request):
    user = request.user
    author_group = Group.objects.get(name='Author')
    if not request.user.groups.filter(name='Author').exists():
        author_group.user_set.add(user)
    return redirect('/')


# @login_required()
# def become_subscriber(request):
#     user = request.user
#     categories = Post.objects.filter(categorie=)
