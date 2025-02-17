# Generated by Django 5.1.2 on 2024-11-28 15:39

import client.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0026_alter_photogallery_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='FestivalPoster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_uz', models.CharField(blank=True, max_length=255, null=True)),
                ('title_en', models.CharField(blank=True, max_length=255, null=True)),
                ('title_ru', models.CharField(blank=True, max_length=255, null=True)),
                ('description_uz', models.TextField(blank=True, null=True)),
                ('description_en', models.TextField(blank=True, null=True)),
                ('description_ru', models.TextField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to=client.models.festival_poster_logo_upload_path)),
                ('video', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Festival Poster',
                'verbose_name_plural': 'Festival Poster',
            },
        ),
    ]
