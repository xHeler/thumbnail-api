from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db import models


class Plan(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(blank=True, max_length=100)
    default = models.BooleanField(default=None, unique=True, null=True)
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
    )

    def __str__(self):
        if self.default:
            return f"Plan (DEFAULT) {self.name}"
        return f"Plan {self.name}"


class Membership(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    def get_user_permissions(user):
        try:
            membership = Membership.objects.get(user=user)
        except Membership.DoesNotExist:
            membership = None
            return None
        plan = membership.plan
        if plan:
            return plan.permissions.all()
        return None

    def __str__(self):
        return f"Membership ({self.plan.name}) {self.user}"
