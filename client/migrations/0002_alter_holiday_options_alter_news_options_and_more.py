# Generated by Django 5.1.2 on 2024-11-24 08:44

import client.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='holiday',
            options={'verbose_name': 'Bayram', 'verbose_name_plural': 'Bayramlar'},
        ),
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': 'Yangilik', 'verbose_name_plural': 'Yangiliklar'},
        ),
        migrations.AddField(
            model_name='news',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='news',
            name='video_i_frame',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(upload_to=client.models.news_main_image_upload_path),
        ),
        migrations.CreateModel(
            name='NewsImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=client.models.news_image_upload_path)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='client.news')),
            ],
            options={
                'verbose_name': 'Yangilik Rasmi',
                'verbose_name_plural': 'Yangilik Rasmlari',
            },
        ),
    ]
