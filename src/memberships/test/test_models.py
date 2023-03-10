from django.test import TestCase

from src.images.tests.factories import PermissionFactory
from src.memberships.models import Membership, Plan
from src.users.test.factories import UserFactory

from .factories import MembershipFactory, PlanFactory


class PlanTestCase(TestCase):
    def test_plan_creation(self):
        plan = PlanFactory()
        self.assertIsInstance(plan, Plan)
        self.assertFalse(plan.default)

    def test_default_plan(self):
        default_plan = PlanFactory(default=True)
        plan = Plan.get_default_plan()
        self.assertEqual(default_plan, plan)


class MembershipTestCase(TestCase):
    def test_default_membership_creation(self):
        plan = PlanFactory(default=True)
        user = UserFactory()
        membership = Membership.objects.get(user=user)
        self.assertIsInstance(membership, Membership)
        self.assertEqual(str(membership.user), str(user))
        self.assertEqual(membership.plan, plan)

    def test_membership_permissions(self):
        user = UserFactory()
        plan = PlanFactory()
        permission = PermissionFactory()
        MembershipFactory(user=user, plan=plan, permissions=[permission])
        user_permissions = Membership.get_user_permissions(user)
        self.assertIn(permission, user_permissions.all())
