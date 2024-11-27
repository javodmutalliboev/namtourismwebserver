from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import News, NewsImage, Festival, FestivalImage, NewsCategory
from .serializers import (
    NewsSerializer,
    NewsImageSerializer,
    FestivalSerializer,
    NewsCategorySerializer,
)
from .pagination import CustomPagination
from urllib.parse import unquote
from rest_framework.pagination import PageNumberPagination
import os
from django.views import View


# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the client index.")


class NewsList(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    pagination_class = CustomPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class NewsDetailByTitle(generics.RetrieveAPIView):
    serializer_class = NewsSerializer

    def get_object(self):
        title = self.kwargs.get("title")
        title = unquote(title).replace("-", " ").replace("~", "-").lower()
        request = self.request
        accept_language = request.headers.get("Accept-Language", "en")

        if accept_language == "uz":
            title_field = "title_uz"
        elif accept_language == "ru":
            title_field = "title_ru"
        else:
            title_field = "title_en"

        filter_kwargs = {f"{title_field}__iexact": title}

        try:
            return News.objects.get(**filter_kwargs)
        except News.DoesNotExist:
            raise NotFound("News item not found")


class NewsImageDetailByFilename(View):
    def get(self, request, filename):
        filename = unquote(filename)
        try:
            # Iterate through all NewsImage objects and match the filename
            for news_image in NewsImage.objects.all():
                if os.path.basename(news_image.image.name) == filename:
                    image_path = news_image.image.path
                    return FileResponse(
                        open(image_path, "rb"), content_type="image/jpeg"
                    )
            raise NewsImage.DoesNotExist
        except NewsImage.DoesNotExist:
            raise Http404("News image not found")


class FestivalImageDetailByFilename(View):
    def get(self, request, filename):
        filename = unquote(filename)
        try:
            # Iterate through all Festival objects and match the filename
            for festival in FestivalImage.objects.all():
                if os.path.basename(festival.image.name) == filename:
                    image_path = festival.image.path
                    return FileResponse(
                        open(image_path, "rb"), content_type="image/jpeg"
                    )
            raise Http404("Image not found")
        except Festival.DoesNotExist:
            raise Http404("Festival item not found")


class NewsBannerImage(View):
    def get(self, request, filename):
        filename = unquote(filename)
        try:
            # Iterate through all News objects and match the filename
            for news in News.objects.all():
                if os.path.basename(news.image.name) == filename:
                    image_path = news.image.path
                    return FileResponse(
                        open(image_path, "rb"), content_type="image/jpeg"
                    )
            raise Http404("Image not found")
        except News.DoesNotExist:
            raise Http404("News item not found")


class FestivalBannerImage(View):
    def get(self, request, filename):
        filename = unquote(filename)
        try:
            # Iterate through all Festival objects and match the filename
            for festival in Festival.objects.all():
                if os.path.basename(festival.banner.name) == filename:
                    image_path = festival.banner.path
                    return FileResponse(
                        open(image_path, "rb"), content_type="image/jpeg"
                    )
            raise Http404("Image not found")
        except Festival.DoesNotExist:
            raise Http404("Festival item not found")


class FestivalList(generics.ListCreateAPIView):
    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer
    pagination_class = CustomPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class FestivalDetail(generics.RetrieveAPIView):
    serializer_class = FestivalSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_object(self):
        name = self.kwargs.get("name")
        name = unquote(name).replace("-", " ").replace("~", "-").lower()
        request = self.request
        accept_language = request.headers.get("Accept-Language", "en")

        if accept_language == "uz":
            name_field = "name_uz"
        elif accept_language == "ru":
            name_field = "name_ru"
        else:
            name_field = "name_en"

        filter_kwargs = {f"{name_field}__iexact": name}

        try:
            return Festival.objects.get(**filter_kwargs)
        except Festival.DoesNotExist:
            raise NotFound("Festival item not found")


class NewsCategoryList(generics.ListAPIView):
    queryset = NewsCategory.objects.all()
    serializer_class = NewsCategorySerializer
    pagination_class = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class NewsListByCategoryName(generics.ListAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        category_name = self.kwargs.get("category_name")
        request = self.request
        accept_language = request.headers.get("Accept-Language", "en")

        if accept_language == "uz":
            category_field = "name_uz"
        elif accept_language == "ru":
            category_field = "name_ru"
        else:
            category_field = "name_en"

        filter_kwargs = {f"{category_field}__iexact": category_name}

        try:
            category = NewsCategory.objects.get(**filter_kwargs)
        except NewsCategory.DoesNotExist:
            raise NotFound("News category not found")

        return News.objects.filter(category=category)
