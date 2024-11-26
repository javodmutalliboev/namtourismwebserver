from django.urls import path
from . import views
from .views import (
    NewsList,
    NewsDetailByTitle,
    NewsImageDetailByFilename,
    NewsBannerImage,
    FestivalList,
    FestivalDetail,
)

urlpatterns = [
    path("", views.index, name="index"),
    path("api/news/", NewsList.as_view(), name="news-list"),
    path(
        "api/news/<str:title>/",
        NewsDetailByTitle.as_view(),
        name="news-detail-by-title",
    ),
    path(
        "api/news/image/<str:filename>/",
        NewsImageDetailByFilename.as_view(),
        name="news-image-detail-by-filename",
    ),
    path(
        "api/news/banner/<str:filename>/",
        NewsBannerImage.as_view(),
        name="news-banner-image",
    ),
    path("api/festivals/", FestivalList.as_view(), name="festival-list"),
    path("api/festivals/<int:pk>/", FestivalDetail.as_view(), name="festival-detail"),
]
