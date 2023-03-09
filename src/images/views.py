import base64
import mimetypes
import os
from copy import deepcopy
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.http import Http404, HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.images.models.image import Image
from src.images.serializers import (
    ExpiringLinkSerializer,
    ImageDetailSerializer,
    ImageUploadSerializer,
)
from src.images.services import ImageUploadService
from src.images.utils import generate_expiring_link


class PictureUpload(APIView):
    serializer_class = ImageUploadSerializer

    def post(self, request):
        data = deepcopy(request.data)
        serializer = ImageUploadSerializer(data=data)

        if serializer.is_valid():
            service = ImageUploadService(request.user, request.FILES["image_file"])
            info = service.create()
            return Response(info, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PictureList(APIView):
    def get(self, request):
        images = Image.objects.filter(owner=request.user)
        if not images:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ImageDetailSerializer(images, many=True)
        return Response(serializer.data)


class GenerateExpiringLink(APIView):
    def post(self, request):
        serializer = ExpiringLinkSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print(serializer.data["time"])
        link = generate_expiring_link(
            request, serializer.data["url"], serializer.data["time"]
        )

        return Response({"expiring_link": link})


class ExpiringLink(APIView):
    def get(self, request):
        encoded_data = request.query_params.get("encoded_data", None)
        if encoded_data is None:
            raise Http404
        try:
            media_file_url, exp_time = (
                base64.urlsafe_b64decode(encoded_data.encode()).decode().split("|")
            )
            exp_time = datetime.fromisoformat(exp_time)
            if exp_time < datetime.utcnow():
                raise Http404
        except (ValueError, TypeError):
            raise Http404

        try:
            media_file = default_storage.open(media_file_url)
        except ObjectDoesNotExist:
            raise Http404

        content_type, encoding = mimetypes.guess_type(media_file_url)
        response = HttpResponse(media_file, content_type=content_type)
        response[
            "Content-Disposition"
        ] = f'attachment; filename="{os.path.basename(media_file_url)}"'
        return response
