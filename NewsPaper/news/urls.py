from django.urls import path
from .views import NewsList, NewsDetail


urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:id>', NewsDetail.as_view())
]
