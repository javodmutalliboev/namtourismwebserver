# validators.py
from django.core.exceptions import ValidationError
import mimetypes


def validate_image_size(image):
    max_size_mb = 20  # 20MB
    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Image size should not exceed {max_size_mb}MB")


def validate_video_size(video):
    max_size_mb = 100  # 100MB
    if video.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Video size should not exceed {max_size_mb}MB")


def validate_video_file(file):
    valid_mime_types = ['video/mp4', 'video/avi', 'video/mpeg', 'video/quicktime']
    mime_type, _ = mimetypes.guess_type(file.name)
    if mime_type not in valid_mime_types:
        raise ValidationError('Unsupported file type. Please upload a video file.')
