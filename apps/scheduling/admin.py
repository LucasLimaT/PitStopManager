from django.contrib import admin

from apps.core.admin import BaseModelAdmin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(BaseModelAdmin):
    list_display = [
        "get_vehicle_plate",
        "get_service_order_id",
        "data_do_agendamento",
        "responsavel",
        "created_at",
        "updated_at",
    ]

    list_filter = ["data_do_agendamento", "responsavel", "created_at", "updated_at"]

    search_fields = ["pk_id_carro__placa", "pk_id_ordem_de_servico__id", "responsavel"]

    autocomplete_fields = ["pk_id_carro", "pk_id_ordem_de_servico"]

    fieldsets = [
        (
            "Informações Principais",
            {
                "fields": [
                    "pk_id_carro",
                    "pk_id_ordem_de_servico",
                    "data_do_agendamento",
                    "responsavel",
                ]
            },
        ),
        (
            "Metadados do Sistema",
            {
                "fields": ["uuid_id", "created_at", "updated_at"],
                "classes": ["collapse"],
            },
        ),
    ]

    @admin.display(description="Placa do Veículo")
    def get_vehicle_plate(self, obj):
        if obj.pk_id_carro:
            return obj.pk_id_carro.placa
        return "N/A"

    @admin.display(description="ID da Ordem de Serviço")
    def get_service_order_id(self, obj):
        if obj.pk_id_ordem_de_servico:
            return obj.pk_id_ordem_de_servico.id
        return "N/A"
