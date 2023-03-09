from django.urls import path

from src.images.views import PictureList, PictureUpload

urlpatterns = [
    path("", PictureList.as_view()),
    path("upload/", PictureUpload.as_view()),
]
