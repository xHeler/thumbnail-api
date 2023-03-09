from django.conf import settings
from rest_framework import serializers

from .models.image import Image
from .models.thumbnail import Thumbnail
from .utils import get_image_validators


class ImageUploadSerializer(serializers.ModelSerializer):
    image_file = serializers.ImageField(validators=[get_image_validators()])

    class Meta:
        model = Thumbnail
        fields = (
            "id",
            "image_file",
        )


class ImageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = (
            "id",
            "created_at",
            "updated_at",
            "urls_dict",
        )


class ExpiringLinkSerializer(serializers.Serializer):
    url = serializers.URLField(allow_blank=False)
    time = serializers.IntegerField(
        min_value=settings.EXPIRING_LINK__TIME_MIN,
        max_value=settings.EXPIRING_LINK__TIME_MAX,
    )
