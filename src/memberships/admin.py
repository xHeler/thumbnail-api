from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import Membership, Plan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "default")

    list_filter = ("default",)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "permissions":
            kwargs["queryset"] = Permission.objects.filter(codename__contains="custom")

        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Membership)
class MembershipPlan(admin.ModelAdmin):
    list_display = (
        "user",
        "plan",
    )

    list_filter = ("user", "plan")

    search_fields = ("user__username",)
