from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver

from src.images.models.base import BaseModel
from src.images.models.image import Image
from src.images.utils import (
    file_generate_upload_path,
    get_image_validators,
    get_resized_image,
)


class Thumbnail(BaseModel):
    image_file = models.ImageField(
        upload_to=file_generate_upload_path, validators=[get_image_validators()]
    )

    orginal_image = models.ForeignKey(Image, null=True, on_delete=models.CASCADE)

    uploaded_by = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL
    )

    height = models.PositiveIntegerField(default=0, blank=True, null=True)
    width = models.PositiveIntegerField(default=0, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.uploaded_by = self.orginal_image.owner
        size = (self.width, self.height)
        if size[0] > 0 and size[1] > 0:
            resized_image = get_resized_image(self.image_file, size)
            self.image_file.delete(False)
            self.image_file = resized_image
        super(Thumbnail, self).save(*args, **kwargs)

    @property
    def url(self):
        # TODO ADD S3 URL
        url = f"{settings.APP_DOMAIN}{self.image_file.url}"
        if self.height > 0:
            key = f"{self.width}x{self.height}"
            return {key: url}
        return {"orginal": url}


@receiver(models.signals.post_delete, sender=Thumbnail)
def delete_image_file(sender, instance, **kwargs):
    instance.image_file.delete(False)
