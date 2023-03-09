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
    username = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Image
        fields = (
            "id",
            "username",
            "urls",
        )
