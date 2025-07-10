import uuid

from django.db import models

from apps.core.models import SoftDeleteModel
from apps.vehicles.models import Vehicle


class Appointment(SoftDeleteModel):
    uuid_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name="UUID"
    )

    pk_id_ordem_de_servico = models.ForeignKey(
        "services.ServiceOrder",
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="Ordem de Serviço",
    )

    pk_id_carro = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="Veículo",
    )

    data_do_agendamento = models.DateTimeField(
        verbose_name="Data do Agendamento", help_text="Data e hora do agendamento"
    )

    responsavel = models.CharField(
        max_length=100,
        verbose_name="Responsável",
        help_text="Nome do responsável pelo agendamento",
    )

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ["data_do_agendamento"]
        db_table = "scheduling_appointment"

    def __str__(self):
        return f"Agendamento {self.id} - {self.pk_id_carro.placa} - {self.data_do_agendamento.strftime('%d/%m/%Y %H:%M')}"
