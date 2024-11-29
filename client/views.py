from django.http import HttpResponse, FileResponse, Http404, StreamingHttpResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import (
    News,
    NewsImage,
    Festival,
    FestivalImage,
    NewsCategory,
    SocialMedia,
    Sponsor,
    AboutUs,
    PhotoGallery,
    PhotoGalleryImage,
    FestivalCategory,
    PhotoGalleryCategory,
    FestivalPoster,
    Contact,
)
from .serializers import (
    NewsSerializer,
    FestivalSerializer,
    NewsCategorySerializer,
    SocialMediaSerializer,
    SponsorSerializer,
    AboutUsSerializer,
    PhotoGallerySerializer,
    PhotoGalleryCategorySerializer,
    FestivalPosterSerializer,
    ContactSerializer,
)
from .pagination import CustomPagination
from urllib.parse import unquote
from rest_framework.pagination import PageNumberPagination
import os
from django.views import View
from django.db.models import Q
import re
import mimetypes


# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the client index.")


class NewsList(generics.ListAPIView):
    serializer_class = NewsSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = News.objects.all()
        search = self.request.query_params.get("search", None)
        category_name = self.request.query_params.get("category", None)
        accept_language = self.request.headers.get("Accept-Language", "en")

        if accept_language == "uz":
            title_field = "title_uz"
            content_field = "content_uz"
            category_field = "name_uz"
        elif accept_language == "ru":
            title_field = "title_ru"
            content_field = "content_ru"
            category_field = "name_ru"
        else:
            title_field = "title_en"
            content_field = "content_en"
            category_field = "name_en"

        if search:
            queryset = queryset.filter(
                Q(**{f"{title_field}__icontains": search})
                | Q(**{f"{content_field}__icontains": search})
            )

        if category_name:
            try:
                category = NewsCategory.objects.get(
                    **{f"{category_field}__iexact": category_name}
                )
                queryset = queryset.filter(category=category)
            except NewsCategory.DoesNotExist:
                queryset = queryset.none()

        return queryset

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
    queryset = Festival.objects.all().order_by("start_date")
    serializer_class = FestivalSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Festival.objects.all().order_by("start_date")
        search = self.request.query_params.get("search", None)
        category_name = self.request.query_params.get("category", None)
        accept_language = self.request.headers.get("Accept-Language", "en")

        if accept_language == "uz":
            name_field = "name_uz"
            description_field = "description_uz"
            address_field = "address_uz"
        elif accept_language == "ru":
            name_field = "name_ru"
            description_field = "description_ru"
            address_field = "address_ru"
        else:
            name_field = "name_en"
            description_field = "description_en"
            address_field = "address_en"

        if search:
            queryset = queryset.filter(
                Q(**{f"{name_field}__icontains": search})
                | Q(**{f"{description_field}__icontains": search})
                | Q(**{f"{address_field}__icontains": search})
            )

        if category_name:
            try:
                category = FestivalCategory.objects.get(name__iexact=category_name)
                queryset = queryset.filter(category=category)
            except FestivalCategory.DoesNotExist:
                queryset = queryset.none()

        return queryset

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


class SocialMediaList(generics.ListCreateAPIView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer
    pagination_class = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class SocialMediaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class SponsorList(generics.ListCreateAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class SponsorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class SponsorLogoDetail(View):
    def get(self, request, filename):
        filename = unquote(filename)
        try:
            # Iterate through all Sponsor objects and match the filename
            for sponsor in Sponsor.objects.all():
                if os.path.basename(sponsor.logo.name) == filename:
                    image_path = sponsor.logo.path
                    return FileResponse(
                        open(image_path, "rb"), content_type="image/jpeg"
                    )
            raise Http404("Logo not found")
        except Sponsor.DoesNotExist:
            raise Http404("Sponsor not found")


class AboutUsList(generics.ListCreateAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    pagination_class = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class AboutUsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class AboutUsImageDetailByFilename(View):
    def get(self, request, filename):
        filename = unquote(filename)
        try:
            # Iterate through all AboutUs objects and match the filename
            for about_us in AboutUs.objects.all():
                if os.path.basename(about_us.image.name) == filename:
                    image_path = about_us.image.path
                    return FileResponse(
                        open(image_path, "rb"), content_type="image/jpeg"
                    )
            raise Http404("Image not found")
        except AboutUs.DoesNotExist:
            raise Http404("About Us item not found")


class PhotoGalleryList(generics.ListCreateAPIView):
    queryset = PhotoGallery.objects.all()
    serializer_class = PhotoGallerySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = PhotoGallery.objects.all()
        search = self.request.query_params.get("search", None)
        category_name = self.request.query_params.get("category", None)
        accept_language = self.request.headers.get("Accept-Language", "en")

        if accept_language == "uz":
            title_field = "title_uz"
            description_field = "description_uz"
            address_field = "address_uz"
            category_field = "name_uz"
        elif accept_language == "ru":
            title_field = "title_ru"
            description_field = "description_ru"
            address_field = "address_ru"
            category_field = "name_ru"
        else:
            title_field = "title_en"
            description_field = "description_en"
            address_field = "address_en"
            category_field = "name_en"

        if search:
            queryset = queryset.filter(
                Q(**{f"{title_field}__icontains": search})
                | Q(**{f"{description_field}__icontains": search})
                | Q(**{f"{address_field}__icontains": search})
            )

        if category_name:
            try:
                category = PhotoGalleryCategory.objects.get(
                    **{f"{category_field}__iexact": category_name}
                )
                queryset = queryset.filter(category=category)
            except PhotoGalleryCategory.DoesNotExist:
                queryset = queryset.none()

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class PhotoGalleryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PhotoGallery.objects.all()
    serializer_class = PhotoGallerySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class PhotoGalleryDetailByTitle(generics.RetrieveAPIView):
    serializer_class = PhotoGallerySerializer

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
            return PhotoGallery.objects.get(**filter_kwargs)
        except PhotoGallery.DoesNotExist:
            raise NotFound("Photo gallery item not found")


class PhotoGalleryImageDetailByFilename(View):
    def get(self, request, filename):
        filename = unquote(filename)
        try:
            # Iterate through all PhotoGalleryImage objects and match the filename
            for photo_gallery_image in PhotoGalleryImage.objects.all():
                if os.path.basename(photo_gallery_image.image.name) == filename:
                    image_path = photo_gallery_image.image.path
                    return FileResponse(
                        open(image_path, "rb"), content_type="image/jpeg"
                    )
            raise Http404("Image not found")
        except PhotoGalleryImage.DoesNotExist:
            raise Http404("Photo gallery image not found")


class PhotoGalleryCategoryList(generics.ListAPIView):
    queryset = PhotoGalleryCategory.objects.all()
    serializer_class = PhotoGalleryCategorySerializer
    pagination_class = None


class FestivalPosterList(generics.ListCreateAPIView):
    queryset = FestivalPoster.objects.all()
    serializer_class = FestivalPosterSerializer
    pagination_class = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class FestivalPosterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FestivalPoster.objects.all()
    serializer_class = FestivalPosterSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class FestivalPosterDetailByTitle(generics.RetrieveAPIView):
    serializer_class = FestivalPosterSerializer

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
            return FestivalPoster.objects.get(**filter_kwargs)
        except FestivalPoster.DoesNotExist:
            raise NotFound("Festival poster item not found")


class FestivalPosterLogoDetail(View):
    def get(self, request, filename):
        filename = unquote(filename)
        try:
            # Iterate through all FestivalPoster objects and match the filename
            for festival_poster in FestivalPoster.objects.all():
                if os.path.basename(festival_poster.logo.name) == filename:
                    image_path = festival_poster.logo.path
                    return FileResponse(
                        open(image_path, "rb"), content_type="image/jpeg"
                    )
            raise Http404("Logo not found")
        except FestivalPoster.DoesNotExist:
            raise Http404("Festival poster not found")


class FestivalPosterVideoDetail(View):
    def get(self, request, filename):
        filename = unquote(filename)
        try:
            # Iterate through all FestivalPoster objects and match the filename
            for festival_poster in FestivalPoster.objects.all():
                if os.path.basename(festival_poster.video.name) == filename:
                    video_path = festival_poster.video.path
                    return self.serve_video(request, video_path)
            raise Http404("Video not found")
        except FestivalPoster.DoesNotExist:
            raise Http404("Festival poster not found")

    def serve_video(self, request, path):
        range_header = request.headers.get("Range", "").strip()
        range_match = re.match(r"bytes=(\d+)-(\d+)?", range_header)
        size = os.path.getsize(path)
        content_type, _ = mimetypes.guess_type(path)
        content_type = content_type or "application/octet-stream"

        if range_match:
            first_byte, last_byte = range_match.groups()
            first_byte = int(first_byte)
            last_byte = int(last_byte) if last_byte else size - 1
            length = last_byte - first_byte + 1
            response = StreamingHttpResponse(
                self.file_iterator(path, offset=first_byte, length=length),
                status=206,
                content_type=content_type,
            )
            response["Content-Range"] = f"bytes {first_byte}-{last_byte}/{size}"
        else:
            response = StreamingHttpResponse(
                self.file_iterator(path), content_type=content_type
            )
            response["Content-Length"] = size

        response["Accept-Ranges"] = "bytes"
        return response

    def file_iterator(self, path, offset=0, length=None, chunk_size=8192):
        with open(path, "rb") as f:
            f.seek(offset, os.SEEK_SET)
            remaining = length
            while remaining is None or remaining > 0:
                chunk_size = min(chunk_size, remaining) if remaining else chunk_size
                data = f.read(chunk_size)
                if not data:
                    break
                if remaining:
                    remaining -= len(data)
                yield data


class ContactList(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    pagination_class = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class PhotoGalleryBannerImageDetail(View):
    def get(self, request, filename):
        filename = unquote(filename)
        try:
            # Iterate through all PhotoGallery objects and match the filename
            for photo_gallery in PhotoGallery.objects.all():
                if os.path.basename(photo_gallery.banner.name) == filename:
                    image_path = photo_gallery.banner.path
                    return FileResponse(
                        open(image_path, "rb"), content_type="image/jpeg"
                    )
            raise Http404("Banner image not found")
        except PhotoGallery.DoesNotExist:
            raise Http404("Photo gallery not found")
