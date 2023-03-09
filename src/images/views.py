from copy import deepcopy

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.images.models.image import Image
from src.images.serializers import ImageDetailSerializer, ImageUploadSerializer
from src.images.services import ImageUploadService


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
