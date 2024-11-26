# Generated by Django 5.1.2 on 2024-11-26 09:36

import client.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_alter_news_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='FestivalCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Festival katigoriyasi',
                'verbose_name_plural': 'Festival kategoriyalari',
            },
        ),
        migrations.CreateModel(
            name='Festival',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('banner', models.ImageField(blank=True, null=True, upload_to=client.models.festival_image_upload_path)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('address', models.CharField(max_length=255)),
                ('video_i_frame', models.TextField(blank=True, null=True)),
                ('location_i_frame', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='festivals', to='client.festivalcategory')),
            ],
            options={
                'verbose_name': 'Festival',
                'verbose_name_plural': 'Festivals',
            },
        ),
    ]