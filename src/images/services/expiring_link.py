import base64
import mimetypes
import os
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.http import HttpResponse


class ExpiringLinkService:
    def __init__(self, encoded_data) -> None:
        self.encoded_data = encoded_data

    def _get_media_file(self, url):
        try:
            media_file = default_storage.open(url)
        except ObjectDoesNotExist:
            media_file = None
        return media_file

    def _decode_data(self):
        try:
            url, exp_time = (
                base64.urlsafe_b64decode(self.encoded_data.encode()).decode().split("|")
            )
            exp_time = datetime.fromisoformat(exp_time)

            if exp_time < datetime.utcnow():
                return None
        except (ValueError, TypeError):
            return None
        return url

    def encode_link(self):
        url = self._decode_data()
        if not url:
            return None

        media_file = self._get_media_file(url)
        if not media_file:
            return None

        content_type, _ = mimetypes.guess_type(url)
        response = HttpResponse(media_file, content_type=content_type)
        response[
            "Content-Disposition"
        ] = f'attachment; filename="{os.path.basename(url)}"'
        return response
