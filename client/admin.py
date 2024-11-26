from django.contrib import admin

from .models import News, NewsImage, NewsCategory, Festival, FestivalImage


class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1  # Number of empty forms to display


class FestivalImageInline(admin.TabularInline):
    model = FestivalImage
    extra = 1  # Number of empty forms to display


class FestivalAdmin(admin.ModelAdmin):
    inlines = [FestivalImageInline]


admin.site.register(Festival, FestivalAdmin)


class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsImageInline]


admin.site.register(NewsCategory)
admin.site.register(News, NewsAdmin)


admin.site.site_header = "Nam Tourism"
admin.site.site_title = "Admin Panel"
admin.site.index_title = "Bosh sahifa"
