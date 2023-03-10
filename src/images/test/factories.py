import factory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from src.images.models.image import Image
from src.images.models.size import Size
from src.users.test.factories import UserFactory


class PermissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Permission

    name = factory.Faker("word")
    content_type = ContentType.objects.get_for_model(Size)
    codename = factory.Faker("word")


class SizeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Size

    height = factory.Faker("pyint", min_value=0, max_value=1000)


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image

    owner = factory.SubFactory(UserFactory)
