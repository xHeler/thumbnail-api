from django.contrib.auth import get_user_model
from django.db import models

from src.images.models.base import BaseModel


class Image(BaseModel):
    owner = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        # TODO check user permissions and create thubnails depends on it
        super(Image, self).save(*args, **kwargs)

    @property
    def urls_dict(self):
        return [thumbnail.url_dict for thumbnail in self.thumbnail_set.all()]

    @property
    def urls(self):
        return [thumbnail.url for thumbnail in self.thumbnail_set.all()]

    @property
    def get_thumbnails(self):
        return self.thumbnail_set.all()

    class Meta:
        permissions = [
            ("custom_generate_expired_link", "can generate expired link"),
        ]
