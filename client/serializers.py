from rest_framework import serializers
from .models import News, NewsImage


class NewsSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = "__all__"

    def get_slug(self, obj):
        return obj.title.lower().replace(" ", "-")

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None


class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ["image"]
