from django.conf import settings
from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from .models.thumbnail import Thumbnail


class ImageUploadSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=settings.IMAGES_ALLOWED_EXTENSIONS
            )
        ]
    )

    class Meta:
        model = Thumbnail
        fields = (
            "id",
            "image",
        )
