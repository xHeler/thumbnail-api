from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Size(Permission):
    height = models.PositiveIntegerField(default=0, blank=True, null=True, unique=True)

    def save(self, *args, **kwargs):
        self.content_type = ContentType.objects.get_for_model(Size)
        if self.height > 0:
            self.name = f"Image sizes {self.height}x{self.height}"
            self.codename = f"custom_image_size_{self.height}x{self.height}"
        else:
            self.name = "Image original size"
            self.codename = "custom_image_size_original"
        super(Size, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Size {self.name}"
