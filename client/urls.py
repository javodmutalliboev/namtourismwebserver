from django.urls import path
from . import views
from .views import NewsList, NewsDetailByTitle

urlpatterns = [
    path("", views.index, name="index"),
    path("api/news", NewsList.as_view(), name="news-list"),
    path(
        "api/news/<str:title>",
        NewsDetailByTitle.as_view(),
        name="news-detail-by-title",
    ),
]
