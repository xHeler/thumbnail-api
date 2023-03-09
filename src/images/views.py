from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from copy import deepcopy


from src.images.serializers import ImageUploadSerializer, ImageDetailSerializer
from src.images.models.image import Image


class UploadPicture(APIView):
    serializer_class = ImageUploadSerializer

    def post(self, request):
        orginal_data = request.data
        print(request.FILES.get('image_file'))
        serializer = ImageUploadSerializer(data=deepcopy(orginal_data))
        serializer2 = ImageUploadSerializer(data=deepcopy(orginal_data))

        if serializer.is_valid():
            image = Image(owner=request.user)
            image.save()

            thumbnail_1 = serializer.save(
                orginal_image=image,
                uploaded_by=request.user,
                height=200,
                width=200
            )

            serializer2.is_valid()
            thumbnail_2 = serializer2.save(
                orginal_image=image,
                uploaded_by=request.user,
                height=300,
                width=300
            )
            image_serializer = ImageDetailSerializer(image)
            return Response(image_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
