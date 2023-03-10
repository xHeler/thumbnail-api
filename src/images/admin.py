from django.contrib import admin
from django.forms import ModelForm

from .models.image import Image
from .models.size import Size
from .models.thumbnail import Thumbnail


class SizeForm(ModelForm):
    class Meta:
        model = Size
        fields = ("height",)


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "codename",
    )

    form = SizeForm

    ordering = ["height"]


@admin.register(Thumbnail)
class ThumbnailAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_height",
        "url",
    )

    search_fields = ("orginal_image__id",)

    def get_height(self, thumbnail):
        if thumbnail.height == 0:
            return "Original"
        return thumbnail.height


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
    )

    search_fields = ("owner__username",)
