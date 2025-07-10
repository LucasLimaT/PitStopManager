from django.contrib import admin

from apps.core.admin import BaseModelAdmin

from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(BaseModelAdmin):
    list_display = [
        "placa",
        "marca",
        "modelo",
        "ano",
        "pk_id_cliente",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "marca",
        "modelo",
        "ano",
        "pk_id_cliente",
        "created_at",
        "updated_at",
    ]

    search_fields = ["placa", "marca", "modelo", "pk_id_cliente__nome"]

    readonly_fields = BaseModelAdmin.readonly_fields + ["deleted_at"]

    fieldsets = [
        ("Informações Principais", {"fields": ["pk_id_cliente", "placa"]}),
        ("Detalhes do Veículo", {"fields": ["marca", "modelo", "ano"]}),
        (
            "Metadados do Sistema",
            {
                "fields": ["uuid_id", "created_at", "updated_at", "deleted_at"],
                "classes": ["collapse"],
            },
        ),
    ]

    ordering = ["-created_at"]

    def get_queryset(self, request):
        return Vehicle.all_objects
