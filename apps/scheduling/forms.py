from django import forms

from apps.core.forms import BaseBootstrapForm
from apps.services.models import ServiceOrder
from apps.vehicles.models import Vehicle

from .models import Appointment


class AppointmentForm(BaseBootstrapForm):
    class Meta:
        model = Appointment
        fields = [
            "pk_id_carro",
            "pk_id_ordem_de_servico",
            "data_do_agendamento",
            "responsavel",
        ]

        labels = {
            "pk_id_carro": "Veiculo",
            "pk_id_ordem_de_servico": "Ordem de Serviço",
            "data_do_agendamento": "Agendamento Data/Hora",
            "responsavel": "Responsável",
        }

        help_texts = {
            "pk_id_carro": "Selecione o veiculo para o agendamento.",
            "pk_id_ordem_de_servico": "Link para uma ordem de serviço existente (opcional).",
            "data_do_agendamento": "Data e hora do agendamento.",
            "responsavel": "Pessoa responsável pelo agendamento (e.g., Mecânico ou Staff responsável pelo agendamento).",
        }

        widgets = {
            "data_do_agendamento": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
            "responsavel": forms.TextInput(
                attrs={"placeholder": "Nome do responsável pelo agendamento"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["pk_id_carro"].queryset = Vehicle.objects.all()
        self.fields["pk_id_ordem_de_servico"].queryset = ServiceOrder.objects.all()
        self.fields["pk_id_ordem_de_servico"].required = False
