from rest_framework import serializers
from .models import News, NewsImage, NewsCategory, Festival, FestivalCategory
import os


class NewsImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = NewsImage
        fields = ["image"]

    def get_image(self, obj):
        return os.path.basename(obj.image.name)


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ["id", "name"]


class NewsSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()
    images = NewsImageSerializer(many=True, read_only=True)
    category = NewsCategorySerializer(read_only=True)

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

    def get_slug(self, obj):
        return obj.title.lower().replace(" ", "-")

    def get_banner(self, obj):
        if obj.image:
            return os.path.basename(obj.image.name)
        return None


class FestivalCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FestivalCategory
        fields = ["id", "name"]


class FestivalSerializer(serializers.ModelSerializer):
    category = FestivalCategorySerializer(read_only=True)

    class Meta:
        model = Festival
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "end_date",
            "location",
            "category",
            "image",
        ]
