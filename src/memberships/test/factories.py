import factory
from django.contrib.auth import get_user_model

from src.images.tests.factories import PermissionFactory
from src.memberships.models import Membership, Plan


class PlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Plan

    name = factory.Sequence(lambda n: f"Plan {n}")
    description = factory.Faker("sentence")
    default = False


class MembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Membership

    user = factory.SubFactory(get_user_model())
    plan = factory.SubFactory(PlanFactory)

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for permission in extracted:
                self.plan.permissions.add(permission)
        else:
            permission = PermissionFactory()
            self.plan.permissions.add(permission)
