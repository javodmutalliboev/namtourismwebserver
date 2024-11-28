from rest_framework import serializers
from .models import (
    News,
    NewsImage,
    NewsCategory,
    Festival,
    FestivalCategory,
    FestivalImage,
    SocialMedia,
    Sponsor,
    AboutUs,
    PhotoGallery,
    PhotoGalleryImage,
    PhotoGalleryCategory,
    FestivalPoster,
    Contact,
)
import os


class NewsImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = NewsImage
        fields = ["image"]

    def get_image(self, obj):
        return os.path.basename(obj.image.name)


class NewsCategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = NewsCategory
        fields = ["id", "name"]

    def get_name(self, obj):
        request = self.context.get("request")
        if request:
            accept_language = request.headers.get("Accept-Language", "en")
            if accept_language == "uz":
                return obj.name_uz
            elif accept_language == "ru":
                return obj.name_ru
        return obj.name_en


class NewsSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()
    images = NewsImageSerializer(many=True, read_only=True)
    category = NewsCategorySerializer(read_only=True)
    title = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "content",
            "created_at",
            "updated_at",
            "banner",
            "video_i_frame",
            "location_i_frame",
            "slug",
            "images",
            "category",
        ]

    def get_title(self, obj):
        request = self.context.get("request")
        if request:
            accept_language = request.headers.get("Accept-Language", "en")
            if accept_language == "uz":
                return obj.title_uz
            elif accept_language == "ru":
                return obj.title_ru
        return obj.title_en

    def get_content(self, obj):
        request = self.context.get("request")
        if request:
            accept_language = request.headers.get("Accept-Language", "en")
            if accept_language == "uz":
                return obj.content_uz
            elif accept_language == "ru":
                return obj.content_ru
        return obj.content_en

    def get_slug(self, obj):
        request = self.context.get("request")
        if request:
            accept_language = request.headers.get("Accept-Language", "en")
            if accept_language == "uz":
                return obj.title_uz.lower().replace("-", "~").replace(" ", "-")
            elif accept_language == "ru":
                return obj.title_ru.lower().replace("-", "~").replace(" ", "-")
        return obj.title_en.lower().replace("-", "~").replace(" ", "-")

    def get_banner(self, obj):
        if obj.image:
            return os.path.basename(obj.image.name)
        return None


class FestivalImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = FestivalImage
        fields = ["image"]

    def get_image(self, obj):
        return os.path.basename(obj.image.name)


class FestivalCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FestivalCategory
        fields = ["id", "name"]


class FestivalSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()
    category = FestivalCategorySerializer(read_only=True)
    images = FestivalImageSerializer(many=True, read_only=True)
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = Festival
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "created_at",
            "updated_at",
            "banner",
            "start_date",
            "end_date",
            "address",
            "images",
            "video_i_frame",
            "category",
            "location_i_frame",
        ]

    def get_name(self, obj):
        request = self.context.get("request")
        if request:
            accept_language = request.headers.get("Accept-Language", "en")
            if accept_language == "uz":
                return obj.name_uz
            elif accept_language == "ru":
                return obj.name_ru
        return obj.name_en

    def get_slug(self, obj):
        request = self.context.get("request")
        if request:
            accept_language = request.headers.get("Accept-Language", "en")
            if accept_language == "uz":
                return obj.name_uz.lower().replace("-", "~").replace(" ", "-")
            elif accept_language == "ru":
                return obj.name_ru.lower().replace("-", "~").replace(" ", "-")
        return obj.name_en.lower().replace("-", "~").replace(" ", "-")

    def get_description(self, obj):
        request = self.context.get("request")
        if request:
            accept_language = request.headers.get("Accept-Language", "en")
            if accept_language == "uz":
                return obj.description_uz
            elif accept_language == "ru":
                return obj.description_ru
        return obj.description_en

    def get_address(self, obj):
        request = self.context.get("request")
        if request:
            accept_language = request.headers.get("Accept-Language", "en")
            if accept_language == "uz":
                return obj.address_uz
            elif accept_language == "ru":
                return obj.address_ru
        return obj.address_en

    def get_banner(self, obj):
        if obj.banner:
            return os.path.basename(obj.banner.name)
        return None


class SocialMediaSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    # icon = serializers.SerializerMethodField()

    class Meta:
        model = SocialMedia
        fields = ["id", "name", "url"]

    def get_name(self, obj):
        request = self.context.get("request")
        if request:
            accept_language = request.headers.get("Accept-Language", "en")
            if accept_language == "uz":
                return obj.name_uz
            elif accept_language == "ru":
                return obj.name_ru
        return obj.name_en

    """
    def get_icon(self, obj):
        return os.path.basename(obj.icon.name)
    """


class SponsorSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Sponsor
        fields = ["id", "name", "url", "logo"]

    def get_logo(self, obj):
        return os.path.basename(obj.logo.name)


class AboutUsSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = AboutUs
        fields = ["id", "title", "content", "image"]

    def get_title(self, obj):
        request = self.context.get("request")
        if request:
            accept_language = request.headers.get("Accept-Language", "en")
            if accept_language == "uz":
                return obj.title_uz
            elif accept_language == "ru":
                return obj.title_ru
        return obj.title_en

    def get_content(self, obj):
        request = self.context.get("request")
        if request:
            accept_language = request.headers.get("Accept-Language", "en")
            if accept_language == "uz":
                return obj.content_uz
            elif accept_language == "ru":
                return obj.content_ru
        return obj.content_en

    def get_image(self, obj):
        if obj.image:
            return os.path.basename(obj.image.name)
        return None


class PhotoGalleryImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = PhotoGalleryImage
        fields = ["image"]

    def get_image(self, obj):
        if obj.image:
            return os.path.basename(obj.image.name)
        return None


class PhotoGalleryCategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = PhotoGalleryCategory
        fields = ["id", "name"]

    def get_name(self, obj):
        request = self.context.get("request")
        if request:
            accept_language = request.headers.get("Accept-Language", "en")
            if accept_language == "uz":
                return obj.name_uz
            elif accept_language == "ru":
                return obj.name_ru
        return obj.name_en


class PhotoGallerySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    category = PhotoGalleryCategorySerializer(read_only=True)
    images = PhotoGalleryImageSerializer(many=True, read_only=True)
    address = serializers.SerializerMethodField()

    class Meta:
        model = PhotoGallery
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "category",
            "address",
            "location_i_frame",
            "video_i_frame",
            "images",
        ]

    def get_title(self, obj):
        request = self.context.get("request")
        if request:
            accept_language = request.headers.get("Accept-Language", "en")
            if accept_language == "uz":
                return obj.title_uz
            elif accept_language == "ru":
                return obj.title_ru
        return obj.title_en

    def get_description(self, obj):
        request = self.context.get("request")
        if request:
            accept_language = request.headers.get("Accept-Language", "en")
            if accept_language == "uz":
                return obj.description_uz
            elif accept_language == "ru":
                return obj.description_ru
        return obj.description_en

    def get_address(self, obj):
        request = self.context.get("request")
        if request:
            accept_language = request.headers.get("Accept-Language", "en")
            if accept_language == "uz":
                return obj.address_uz
            elif accept_language == "ru":
                return obj.address_ru
        return obj.address_en

    def get_slug(self, obj):
        request = self.context.get("request")
        if request:
            accept_language = request.headers.get("Accept-Language", "en")
            if accept_language == "uz":
                return obj.title_uz.lower().replace("-", "~").replace(" ", "-")
            elif accept_language == "ru":
                return obj.title_ru.lower().replace("-", "~").replace(" ", "-")
        return obj.title_en.lower().replace("-", "~").replace(" ", "-")


class FestivalPosterSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()

    class Meta:
        model = FestivalPoster
        fields = ["id", "title", "slug", "description", "logo", "video"]

    def get_title(self, obj):
        request = self.context.get("request")
        if request:
            accept_language = request.headers.get("Accept-Language", "en")
            if accept_language == "uz":
                return obj.title_uz
            elif accept_language == "ru":
                return obj.title_ru
        return obj.title_en

    def get_slug(self, obj):
        request = self.context.get("request")
        if request:
            accept_language = request.headers.get("Accept-Language", "en")
            if accept_language == "uz":
                return obj.title_uz.lower().replace("-", "~").replace(" ", "-")
            elif accept_language == "ru":
                return obj.title_ru.lower().replace("-", "~").replace(" ", "-")
        return obj.title_en.lower().replace("-", "~").replace(" ", "-")

    def get_description(self, obj):
        request = self.context.get("request")
        if request:
            accept_language = request.headers.get("Accept-Language", "en")
            if accept_language == "uz":
                return obj.description_uz
            elif accept_language == "ru":
                return obj.description_ru
        return obj.description_en

    def get_logo(self, obj):
        if obj.logo:
            return os.path.basename(obj.logo.name)
        return None

    def get_video(self, obj):
        if obj.video:
            return os.path.basename(obj.video.name)
        return None


class ContactSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = [
            "id",
            "phone",
            "additional_phone",
            "address",
            "location_i_frame",
            "postal_index",
            "email",
        ]

    def get_address(self, obj):
        request = self.context.get("request")
        if request:
            accept_language = request.headers.get("Accept-Language", "en")
            if accept_language == "uz":
                return obj.address_uz
            elif accept_language == "ru":
                return obj.address_ru
        return obj.address_en
