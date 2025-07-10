from django.contrib import admin

from apps.core.admin import BaseModelAdmin

from .models import ServiceOrder


@admin.register(ServiceOrder)
class ServiceOrderAdmin(BaseModelAdmin):
    list_display = [
        "id",
        "pk_id_carro",
        "data_de_entrada",
        "data_de_entrega",
        "status",
        "orcamento_reais",
        "quilometragem",
        "created_at",
        "updated_at",
        "deleted_at",
    ]

    list_filter = [
        "status",
        "data_de_entrada",
        "data_de_entrega",
        "created_at",
        "updated_at",
    ]

    search_fields = [
        "pk_id_carro__placa",
        "pk_id_carro__modelo__nome",
        "pk_id_carro__marca__nome",
        "descricao_problema",
    ]

    readonly_fields = BaseModelAdmin.readonly_fields + ["deleted_at"]

    fieldsets = [
        ("Informações Principais", {"fields": ["pk_id_carro", "status"]}),
        ("Datas", {"fields": ["data_de_entrada", "data_de_entrega"]}),
        (
            "Detalhes do Serviço",
            {
                "fields": [
                    "quilometragem",
                    "orcamento",
                    "descricao_problema",
                    "descricao_concerto",
                ]
            },
        ),
        (
            "Metadados do Sistema",
            {
                "fields": ["uuid_id", "created_at", "updated_at", "deleted_at"],
                "classes": ["collapse"],
            },
        ),
    ]

    def get_queryset(self, request):
        return ServiceOrder.all_objects

    @admin.display(description="Orçamento (R$)")
    def orcamento_reais(self, obj):
        return f"R$ {obj.orcamento / 100:.2f}"
