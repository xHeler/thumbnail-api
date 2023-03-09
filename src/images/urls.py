from django.urls import path

from src.images.views import (
    ExpiringLink,
    GenerateExpiringLink,
    PictureList,
    PictureUpload,
)

urlpatterns = [
    path("", PictureList.as_view()),
    path("upload/", PictureUpload.as_view()),
    path("expiring_link/", ExpiringLink.as_view(), name="media-view"),
    path("generate_expiring_link/", GenerateExpiringLink.as_view()),
]
