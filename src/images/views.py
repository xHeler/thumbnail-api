from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.images.serializers import ImageUploadSerializer


class UploadPicture(APIView):
    serializer_class = ImageUploadSerializer

    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(uploaded_by=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
