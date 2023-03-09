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
class ImageAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "codename",
    ]

    form = SizeForm

    ordering = ["height"]


admin.site.register(Image)
# DELETE MUST
admin.site.register(Thumbnail)
