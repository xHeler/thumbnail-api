from src.images.models.base import BaseModel


class Image(BaseModel):
    def save(self, *args, **kwargs):
        # TODO check user permissions and create thubnails depends on it
        super(Image, self).save(*args, **kwargs)

    @property
    def urls(self):
        # TODO return thumbnails urls as dict
        thumbnails = self.thumbnail_set.all()
        for thumbnail in thumbnails:
            print(thumbnail.url)

    class Meta:
        permissions = [
            ("custom_generate_expired_link", "can generate expired link"),
        ]
