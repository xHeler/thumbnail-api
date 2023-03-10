from copy import deepcopy

from src.images.models.image import Image
from src.images.models.size import Size
from src.images.models.thumbnail import Thumbnail
from src.images.serializers import ImageDetailSerializer
from src.memberships.models import Membership


class ImageUploadService:
    def __init__(self, user, image_data):
        self.user = user
        self.image_data = image_data

    def _get_sizes(self, permissions):
        sizes = []
        for p in permissions:
            try:
                size = Size.objects.filter(codename=p.codename)
            except Size.DoesNotExist:
                size = None
            if len(size) > 0:
                sizes.append(size[0])
        return sizes

    def _create_image(self, sizes):
        image = Image(owner=self.user)
        image.save()

        for size in sizes:
            thumbnail = Thumbnail(
                image_file=deepcopy(self.image_data),
                orginal_image=image,
                height=size.height,
                width=size.height,
            )
            thumbnail.save()

        return image

    def create(self):
        permissions = Membership.get_user_permissions(self.user)
        if not permissions:
            return None
        image = self._create_image(self._get_sizes(permissions))
        image_serializer = ImageDetailSerializer(image)
        return image_serializer.data
