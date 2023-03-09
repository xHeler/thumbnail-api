import sys
import uuid
from io import BytesIO

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import FileExtensionValidator
from django.db import models
from django.dispatch import receiver
from PIL import Image

from src.images.utils import file_generate_upload_path


class Thumbnail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    image = models.ImageField(
        upload_to=file_generate_upload_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=settings.IMAGES_ALLOWED_EXTENSIONS
            )
        ],
    )

    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    uploaded_by = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL
    )

    def save(self, *args, **kwargs):
        im = Image.open(self.image)
        output = BytesIO()
        im = im.resize((100, 100))
        im.save(output, format="JPEG", quality=100)
        output.seek(0)
        self.image = InMemoryUploadedFile(
            output,
            "ImageField",
            "%s.jpg" % self.image.name.split(".")[0],
            "image/jpeg",
            sys.getsizeof(output),
            None,
        )

        super(Thumbnail, self).save(*args, **kwargs)


@receiver(models.signals.post_delete, sender=Thumbnail)
def delete_image_file(sender, instance, **kwargs):
    instance.image.delete(False)
