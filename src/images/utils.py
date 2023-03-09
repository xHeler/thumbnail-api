import base64
import pathlib
import sys
from datetime import datetime, timedelta
from io import BytesIO
from uuid import uuid4

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import FileExtensionValidator
from django.urls import reverse
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


def generate_expiring_link(request, media_file_url, time):
    length = len(settings.APP_DOMAIN) + 1
    url = media_file_url[length:]
    current_time = datetime.utcnow()
    exp_time = current_time + timedelta(seconds=time)
    encoded_data = base64.urlsafe_b64encode(
        f"{url}|{exp_time.isoformat()}".encode()
    ).decode()
    return request.build_absolute_uri(
        reverse("media-view") + f"?encoded_data={encoded_data}"
    )
