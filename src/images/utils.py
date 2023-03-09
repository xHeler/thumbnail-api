import pathlib
import sys
from io import BytesIO
from uuid import uuid4

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import FileExtensionValidator
from PIL import Image


def file_generate_name(original_file_name):
    extension = pathlib.Path(original_file_name).suffix
    return f"{uuid4().hex}{extension}"


def file_generate_upload_path(instance, original_file_name):
    file_name = file_generate_name(original_file_name)
    return f"{instance.uploaded_by.id}/{file_name}"


def get_image_validators():
    return FileExtensionValidator(allowed_extensions=settings.IMAGES_ALLOWED_EXTENSIONS)


def get_resized_image(orginal, size):
    image = Image.open(orginal)
    output = BytesIO()
    image = image.resize(size)
    image.save(output, format="JPEG", quality=100)
    output.seek(0)
    return InMemoryUploadedFile(
        output,
        "ImageField",
        "%s.jpg" % orginal.name.split(".")[0],
        "image/jpeg",
        sys.getsizeof(output),
        None,
    )
