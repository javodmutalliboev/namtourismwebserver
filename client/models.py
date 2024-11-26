import os
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from datetime import datetime


def news_image_upload_path(instance, filename):
    # Generate the filename with the current time including milliseconds
    current_time = datetime.now().strftime("%Y%m%d%H%M%S%f")
    filename = f"{current_time}_{filename}"
    return os.path.join("news", filename)


class NewsCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Yangilik katigoriyasi"
        verbose_name_plural = "Yangilik kategoriyalari"


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=news_image_upload_path)
    video_i_frame = models.TextField(blank=True, null=True)
    location_i_frame = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        NewsCategory, related_name="news", on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"


@receiver(post_delete, sender=News)
def delete_news_image_file(sender, instance, **kwargs):
    # Delete the image file
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class NewsImage(models.Model):
    news = models.ForeignKey(News, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=news_image_upload_path)

    def __str__(self):
        return f"Image for {self.news.title}"

    class Meta:
        verbose_name = "Yangilik Rasmi"
        verbose_name_plural = "Yangilik Rasmlari"


@receiver(post_delete, sender=NewsImage)
def delete_news_image_file(sender, instance, **kwargs):
    # Delete the image file when the news image object is deleted
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
