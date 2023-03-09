from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver

from src.images.models.base import BaseModel
from src.images.utils import (
    file_generate_upload_path,
    get_image_validators,
    get_resized_image,
)


class Thumbnail(BaseModel):
    image = models.ImageField(
        upload_to=file_generate_upload_path, validators=[get_image_validators()]
    )

    uploaded_by = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL
    )

    height = models.PositiveIntegerField(default=0, blank=True, null=True)
    width = models.PositiveIntegerField(default=0, blank=True, null=True)

    def save(self, *args, **kwargs):
        size = (self.width, self.height)
        if size[0] > 0 and size[1] > 0:
            resized_image = get_resized_image(self.image, size)
            self.image.delete(False)
            self.image = resized_image
        super(Thumbnail, self).save(*args, **kwargs)


@receiver(models.signals.post_delete, sender=Thumbnail)
def delete_image_file(sender, instance, **kwargs):
    instance.image.delete(False)
