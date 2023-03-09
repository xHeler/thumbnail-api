from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import Membership, Plan


class PlanModelAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "permissions":
            kwargs["queryset"] = Permission.objects.filter(codename__contains="custom")

        return super().formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Plan, PlanModelAdmin)
admin.site.register(Membership)
