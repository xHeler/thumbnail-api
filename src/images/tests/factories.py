import factory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from src.images.models.size import Size


class PermissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Permission

    name = factory.Faker("word")
    content_type = ContentType.objects.get_for_model(Size)
    codename = factory.Faker("word")


class SizeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Size

    height = factory.Faker("random_int", min_value=0, max_value=1000)

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for permission in extracted:
                self.permissions.add(permission)
        else:
            permission = PermissionFactory.create()
            self.permissions.add(permission)
