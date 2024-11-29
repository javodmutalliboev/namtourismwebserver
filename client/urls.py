from django.urls import path
from . import views
from .views import (
    NewsList,
    NewsDetailByTitle,
    NewsImageDetailByFilename,
    NewsBannerImage,
    FestivalList,
    FestivalDetail,
    FestivalBannerImage,
    FestivalImageDetailByFilename,
    NewsCategoryList,
    NewsListByCategoryName,
    SocialMediaList,
    SponsorList,
    SponsorLogoDetail,
    AboutUsList,
    AboutUsImageDetailByFilename,
    PhotoGalleryList,
    PhotoGalleryDetailByTitle,
    PhotoGalleryImageDetailByFilename,
    PhotoGalleryCategoryList,
    FestivalPosterList,
    FestivalPosterDetailByTitle,
    FestivalPosterLogoDetail,
    FestivalPosterVideoDetail,
    ContactList,
    PhotoGalleryBannerImageDetail,
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
    path(
        "api/festival/<str:name>/",
        FestivalDetail.as_view(),
        name="festival-detail-by-name",
    ),
    path(
        "api/festival/banner/<str:filename>/",
        FestivalBannerImage.as_view(),
        name="festival-banner-image",
    ),
    path(
        "api/festival/image/<str:filename>/",
        FestivalImageDetailByFilename.as_view(),
        name="festival-image-detail-by-filename",
    ),
    path("api/news-categories/", NewsCategoryList.as_view(), name="news-category-list"),
    path(
        "api/news/category/<str:category_name>/",
        NewsListByCategoryName.as_view(),
        name="news-list-by-category-name",
    ),
    path("api/social-media/", SocialMediaList.as_view(), name="social-media-list"),
    path("api/sponsors/", SponsorList.as_view(), name="sponsor-list"),
    path(
        "api/sponsors/logo/<str:filename>/",
        SponsorLogoDetail.as_view(),
        name="sponsor-logo-detail",
    ),
    path("api/about-us/", AboutUsList.as_view(), name="about-us-list"),
    path(
        "api/about-us/image/<str:filename>/",
        AboutUsImageDetailByFilename.as_view(),
        name="about-us-image-detail-by-filename",
    ),
    path(
        "api/photo-gallery-list/", PhotoGalleryList.as_view(), name="photo-gallery-list"
    ),
    path(
        "api/photo-gallery/<str:title>/",
        PhotoGalleryDetailByTitle.as_view(),
        name="photo-gallery-detail-by-title",
    ),
    path(
        "api/photo-gallery/image/<str:filename>/",
        PhotoGalleryImageDetailByFilename.as_view(),
        name="photo-gallery-image-detail-by-filename",
    ),
    path(
        "api/photo-gallery-categories/",
        PhotoGalleryCategoryList.as_view(),
        name="photo-gallery-category-list",
    ),
    path(
        "api/festival-poster-list/",
        FestivalPosterList.as_view(),
        name="festival-poster-list",
    ),
    path(
        "api/festival-poster/<str:title>/",
        FestivalPosterDetailByTitle.as_view(),
        name="festival-poster-detail-by-title",
    ),
    path(
        "api/festival-poster/logo/<str:filename>/",
        FestivalPosterLogoDetail.as_view(),
        name="festival-poster-logo-detail",
    ),
    path(
        "api/festival-poster/video/<str:filename>/",
        FestivalPosterVideoDetail.as_view(),
        name="festival-poster-video-detail",
    ),
    path("api/contacts/", ContactList.as_view(), name="contact-list"),
    path(
        "api/photo-gallery/banner/<str:filename>/",
        PhotoGalleryBannerImageDetail.as_view(),
        name="photo-gallery-banner-image-detail",
    ),
]
