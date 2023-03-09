from django.contrib.auth import get_user_model
from django.db import models

from src.images.models.base import BaseModel


class Image(BaseModel):
    owner = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        # TODO check user permissions and create thubnails depends on it
        super(Image, self).save(*args, **kwargs)

    @property
    def urls(self):
        # TODO return thumbnails urls as dict
        urls = []
        thumbnails = self.thumbnail_set.all()
        for thumbnail in thumbnails:
            urls.append(thumbnail.url)
        return urls

    class Meta:
        permissions = [
            ("custom_generate_expired_link", "can generate expired link"),
        ]
