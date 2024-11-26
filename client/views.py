from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import News, NewsImage, Festival
from .serializers import NewsSerializer, NewsImageSerializer, FestivalSerializer
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


class NewsDetailByTitle(generics.RetrieveAPIView):
    serializer_class = NewsSerializer

    def get_object(self):
        title = self.kwargs.get("title")
        title = unquote(title).replace("-", " ").lower()
        try:
            return News.objects.get(title__iexact=title)
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


class FestivalList(generics.ListCreateAPIView):
    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer


class FestivalDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer
    pagination_class = CustomPagination
