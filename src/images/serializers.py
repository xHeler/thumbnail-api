from rest_framework import serializers

from .models.thumbnail import Thumbnail
from .utils import get_image_validators


class ImageUploadSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(validators=[get_image_validators()])

    class Meta:
        model = Thumbnail
        fields = (
            "id",
            "image",
        )
