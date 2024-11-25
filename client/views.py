from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import News
from .serializers import NewsSerializer
from urllib.parse import unquote
from rest_framework.pagination import PageNumberPagination


# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the client index.")


class NewsList(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    pagination_class = PageNumberPagination


class NewsDetailByTitle(generics.RetrieveAPIView):
    serializer_class = NewsSerializer

    def get_object(self):
        title = self.kwargs.get("title")
        title = unquote(title).replace("-", " ").lower()
        try:
            return News.objects.get(title__iexact=title)
        except News.DoesNotExist:
            raise NotFound("News item not found")
