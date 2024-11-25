from rest_framework import serializers
from .models import News, NewsImage


class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ["image"]


class NewsSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    images = NewsImageSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "content",
            "created_at",
            "updated_at",
            "image",
            "video_i_frame",
            "location",
            "slug",
            "images",
        ]

    def get_slug(self, obj):
        return obj.title.lower().replace(" ", "-")

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None
