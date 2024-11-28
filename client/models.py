import os
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from datetime import datetime


def news_image_upload_path(instance, filename):
    # Generate the filename with the current time including milliseconds
    current_time = datetime.now().strftime("%Y%m%d%H%M%S%f")
    filename = f"{current_time}_{filename}"
    return os.path.join("news", filename)


def festival_image_upload_path(instance, filename):
    # Generate the filename with the current time including milliseconds
    current_time = datetime.now().strftime("%Y%m%d%H%M%S%f")
    filename = f"{current_time}_{filename}"
    return os.path.join("festivals", filename)


def social_media_icon_upload_path(instance, filename):
    # Generate the filename with the current time including milliseconds
    current_time = datetime.now().strftime("%Y%m%d%H%M%S%f")
    filename = f"{current_time}_{filename}"
    return os.path.join("social_media_icons", filename)


def sponsor_logo_upload_path(instance, filename):
    # Generate the filename with the current time including milliseconds
    current_time = datetime.now().strftime("%Y%m%d%H%M%S%f")
    filename = f"{current_time}_{filename}"
    return os.path.join("sponsors", filename)


def about_us_image_upload_path(instance, filename):
    # Generate the filename with the current time including milliseconds
    current_time = datetime.now().strftime("%Y%m%d%H%M%S%f")
    filename = f"{current_time}_{filename}"
    return os.path.join("about_us", filename)


def photo_gallery_image_upload_path(instance, filename):
    # Generate the filename with the current time including milliseconds
    current_time = datetime.now().strftime("%Y%m%d%H%M%S%f")
    filename = f"{current_time}_{filename}"
    return os.path.join("photo_gallery", filename)


class NewsCategory(models.Model):
    name_uz = models.CharField(max_length=100, blank=True, null=True)
    name_en = models.CharField(max_length=100, blank=True, null=True)
    name_ru = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name_uz or ""

    class Meta:
        verbose_name = "Yangilik katigoriyasi"
        verbose_name_plural = "Yangilik kategoriyalari"


class FestivalCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Festival katigoriyasi"
        verbose_name_plural = "Festival kategoriyalari"


class Festival(models.Model):
    name_uz = models.CharField(max_length=255, blank=True, null=True)
    name_en = models.CharField(max_length=255, blank=True, null=True)
    name_ru = models.CharField(max_length=255, blank=True, null=True)
    description_uz = models.TextField(blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)
    description_ru = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    banner = models.ImageField(
        upload_to=festival_image_upload_path, blank=True, null=True
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    address_uz = models.CharField(max_length=255, blank=True, null=True)
    address_en = models.CharField(max_length=255, blank=True, null=True)
    address_ru = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        FestivalCategory,
        related_name="festivals",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    video_i_frame = models.TextField(blank=True, null=True)
    location_i_frame = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name_uz or ""

    class Meta:
        verbose_name = "Festival"
        verbose_name_plural = "Festivallar"


class FestivalImage(models.Model):
    festival = models.ForeignKey(
        Festival, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to=festival_image_upload_path)

    def __str__(self):
        return f"Image for {self.festival.name_uz or ''}"

    class Meta:
        verbose_name = "Festival rasm"
        verbose_name_plural = "Festival rasmlari"


@receiver(pre_save, sender=Festival)
def delete_old_banner_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_banner = Festival.objects.get(pk=instance.pk).banner
    except Festival.DoesNotExist:
        return False

    new_banner = instance.banner
    if old_banner and old_banner != new_banner:
        if os.path.isfile(old_banner.path):
            os.remove(old_banner.path)


@receiver(post_delete, sender=Festival)
def delete_festival_banner_file(sender, instance, **kwargs):
    # Delete the banner file when the festival object is deleted
    if instance.banner:
        if os.path.isfile(instance.banner.path):
            os.remove(instance.banner.path)


@receiver(post_delete, sender=FestivalImage)
def delete_festival_image_file(sender, instance, **kwargs):
    # Delete the image file when the festival image object is deleted
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class News(models.Model):
    title_uz = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255, blank=True, null=True)
    title_ru = models.CharField(max_length=255, blank=True, null=True)
    content_uz = models.TextField()
    content_en = models.TextField(blank=True, null=True)
    content_ru = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=news_image_upload_path)
    video_i_frame = models.TextField(blank=True, null=True)
    location_i_frame = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        NewsCategory, related_name="news", on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return self.title_uz or ""

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"


@receiver(pre_save, sender=News)
def delete_old_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_image = News.objects.get(pk=instance.pk).image
    except News.DoesNotExist:
        return False

    new_image = instance.image
    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)


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
        return f"Image for {self.news.title_uz or ''}"

    class Meta:
        verbose_name = "Yangilik Rasmi"
        verbose_name_plural = "Yangilik Rasmlari"


@receiver(post_delete, sender=NewsImage)
def delete_news_image_file(sender, instance, **kwargs):
    # Delete the image file when the news image object is deleted
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class SocialMedia(models.Model):
    name_uz = models.CharField(max_length=100, blank=True, null=True)
    name_en = models.CharField(max_length=100, blank=True, null=True)
    name_ru = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField()
    """
    icon = models.ImageField(
        upload_to=social_media_icon_upload_path, blank=True, null=True
    )
    """

    def __str__(self):
        return self.name_uz  # Default to Uzbek name for display

    class Meta:
        verbose_name = "Ijtimoiy tarmoq"
        verbose_name_plural = "Ijtimoiy tarmoqlar"


"""
@receiver(pre_save, sender=SocialMedia)
def delete_old_icon_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_icon = SocialMedia.objects.get(pk=instance.pk).icon
    except SocialMedia.DoesNotExist:
        return False

    new_icon = instance.icon
    if old_icon and old_icon != new_icon:
        if os.path.isfile(old_icon.path):
            os.remove(old_icon.path)

@receiver(post_delete, sender=SocialMedia)
def delete_social_media_icon_file(sender, instance, **kwargs):
    # Delete the icon file when the social media object is deleted
    if instance.icon:
        if os.path.isfile(instance.icon.path):
            os.remove(instance.icon.path)
"""


class Sponsor(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to=sponsor_logo_upload_path, blank=True, null=True)

    def __str__(self):
        return self.name or ""

    class Meta:
        verbose_name = "Homiy"
        verbose_name_plural = "Homiylar"


@receiver(pre_save, sender=Sponsor)
def delete_old_logo_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_logo = Sponsor.objects.get(pk=instance.pk).logo
    except Sponsor.DoesNotExist:
        return False

    new_logo = instance.logo
    if old_logo and old_logo != new_logo:
        if os.path.isfile(old_logo.path):
            os.remove(old_logo.path)


@receiver(post_delete, sender=Sponsor)
def delete_sponsor_logo_file(sender, instance, **kwargs):
    # Delete the logo file when the sponsor object is deleted
    if instance.logo:
        if os.path.isfile(instance.logo.path):
            os.remove(instance.logo.path)


class AboutUs(models.Model):
    title_uz = models.CharField(max_length=200, blank=True, null=True)
    title_en = models.CharField(max_length=200, blank=True, null=True)
    title_ru = models.CharField(max_length=200, blank=True, null=True)
    content_uz = models.TextField(blank=True, null=True)
    content_en = models.TextField(blank=True, null=True)
    content_ru = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to=about_us_image_upload_path, blank=True, null=True
    )

    def __str__(self):
        return self.title_uz

    class Meta:
        verbose_name = "Biz haqimizda"
        verbose_name_plural = "Biz haqimizda"


@receiver(pre_save, sender=AboutUs)
def delete_old_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_image = AboutUs.objects.get(pk=instance.pk).image
    except AboutUs.DoesNotExist:
        return False

    new_image = instance.image
    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)


@receiver(post_delete, sender=AboutUs)
def delete_about_us_image_file(sender, instance, **kwargs):
    # Delete the image file when the about us object is deleted
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class PhotoGallery(models.Model):
    title_uz = models.CharField(max_length=200, blank=True, null=True)
    title_en = models.CharField(max_length=200, blank=True, null=True)
    title_ru = models.CharField(max_length=200, blank=True, null=True)
    description_uz = models.TextField(blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)
    description_ru = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100)
    address_uz = models.CharField(max_length=255, blank=True, null=True)
    address_en = models.CharField(max_length=255, blank=True, null=True)
    address_ru = models.CharField(max_length=255, blank=True, null=True)
    location_i_frame = models.TextField(blank=True, null=True)
    video_i_frame = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title_en or self.title_uz or self.title_ru

    class Meta:
        verbose_name = "Fotogalereya"
        verbose_name_plural = "Fotogalereya"


class PhotoGalleryImage(models.Model):
    photo_gallery = models.ForeignKey(
        PhotoGallery, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to=photo_gallery_image_upload_path)

    def __str__(self):
        return f"{self.photo_gallery.title_uz} uchun rasm"

    class Meta:
        verbose_name = "Fotogalereya Rasm"
        verbose_name_plural = "Fotogalereya Rasmlar"
