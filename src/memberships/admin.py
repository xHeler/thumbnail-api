from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Plan, Membership


class PlanModelAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "permissions":
            content_type = ContentType.objects.get_for_model(Membership)
            kwargs["queryset"] = Permission.objects.filter(content_type=content_type, codename__contains="custom")
        
        return super().formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(Plan, PlanModelAdmin)
admin.site.register(Membership)