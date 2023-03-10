from copy import deepcopy

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.images.models.image import Image
from src.images.serializers import (
    ExpiringLinkSerializer,
    ImageDetailSerializer,
    ImageUploadSerializer,
)
from src.images.services.expiring_link import ExpiringLinkService
from src.images.services.image import ImageUploadService
from src.images.utils import generate_expiring_link
from src.memberships.models import Membership


class PictureUpload(APIView):
    serializer_class = ImageUploadSerializer

    def post(self, request):
        data = deepcopy(request.data)
        serializer = ImageUploadSerializer(data=data)

        if serializer.is_valid():
            service = ImageUploadService(request.user, request.FILES["image_file"])
            info = service.create()
            if not info:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
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
        permissions = Membership.get_user_permissions(request.user)

        if not permissions.filter(codename="custom_generate_expired_link"):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = ExpiringLinkSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        link = generate_expiring_link(
            request, serializer.data["url"], serializer.data["time"]
        )

        return Response({"expiring_link": link})


class ExpiringLink(APIView):
    def get(self, request):
        encoded_data = request.query_params.get("encoded_data", None)
        if not encoded_data:
            return Response("Not encoded_data", status=status.HTTP_400_NOT_FOUND)
        service = ExpiringLinkService(encoded_data)
        response = service.encode_link()

        if not response:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return response
