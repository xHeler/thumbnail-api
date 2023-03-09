from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver

from src.images.utils import (
    file_generate_upload_path,
    get_image_validators,
    get_resized_image,
)


class Thumbnail(models.Model):
    image = models.ImageField(
        upload_to=file_generate_upload_path, validators=[get_image_validators()]
    )

    uploaded_by = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL
    )

    def save(self, *args, **kwargs):
        size = (125, 125)
        self.image = get_resized_image(self.image, size)
        super(Thumbnail, self).save(*args, **kwargs)


@receiver(models.signals.post_delete, sender=Thumbnail)
def delete_image_file(sender, instance, **kwargs):
    instance.image.delete(False)
