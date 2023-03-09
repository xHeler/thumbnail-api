from copy import deepcopy

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.images.serializers import ImageUploadSerializer
from src.images.services import ImageUploadService


class UploadPicture(APIView):
    serializer_class = ImageUploadSerializer

    def post(self, request):
        data = deepcopy(request.data)
        serializer = ImageUploadSerializer(data=data)

        if serializer.is_valid():
            service = ImageUploadService(request.user, request.FILES["image_file"])
            info = service.create()
            return Response(info, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
