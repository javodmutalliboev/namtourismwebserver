import os
import shutil
from django.db import models
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver


def news_image_upload_path(instance, filename):
    # Use the instance's ID to construct the upload path for NewsImage
    return f"news/{instance.news.id}/images/{filename}"


def news_main_image_upload_path(instance, filename):
    # Use the instance's ID to construct the upload path for the main image in News
    if instance.id:
        return f"news/{instance.id}/image/{filename}"
    return f"news/temp/{filename}"


class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=news_main_image_upload_path)
    video_i_frame = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"

    def save(self, *args, **kwargs):
        # Save the instance first to ensure it has an ID
        super().save(*args, **kwargs)
        if "image" in self.__dict__:
            image_path = news_main_image_upload_path(self, self.image.name)
            if self.image.path != image_path:
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                shutil.move(self.image.path, image_path)
                self.image.name = image_path
                super().save(update_fields=["image"])

    def delete(self, *args, **kwargs):
        # Delete the main image file
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        # Delete the directory containing the images
        image_dir = os.path.join("news", str(self.id))
        if os.path.isdir(image_dir):
            shutil.rmtree(image_dir)
        super().delete(*args, **kwargs)


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
    # Delete the image file
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_delete, sender=News)
def delete_news_images(sender, instance, **kwargs):
    # Delete all related NewsImage instances
    for news_image in instance.images.all():
        news_image.delete()


class Holiday(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="holidays/")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Bayram"
        verbose_name_plural = "Bayramlar"
