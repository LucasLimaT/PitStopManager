import uuid

from django.db import models

from apps.core.models import SoftDeleteModel
from apps.vehicles.models import Vehicle


class ServiceOrder(SoftDeleteModel):
    STATUS_CHOICES = [
        ("PENDENTE", "Pendente"),
        ("EM_ANDAMENTO", "Em Andamento"),
        ("CONCLUIDA", "Concluída"),
        ("ENTREGUE", "Entregue"),
        ("CANCELADA", "Cancelada"),
    ]

    uuid_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name="UUID"
    )

    pk_id_carro = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="service_orders",
        verbose_name="Veículo",
    )

    data_de_entrada = models.DateField(
        verbose_name="Data de Entrada",
        help_text="Data de entrada do veículo na oficina",
    )

    data_de_entrega = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data de Entrega",
        help_text="Data prevista/efetiva de entrega do veículo",
    )

    orcamento = models.IntegerField(
        default=0, verbose_name="Orçamento", help_text="Valor do orçamento em centavos"
    )

    descricao_problema = models.TextField(
        blank=True,
        default="",
        verbose_name="Descrição do Problema",
        help_text="Descrição do problema relatado pelo cliente",
    )

    descricao_concerto = models.TextField(
        blank=True,
        default="",
        verbose_name="Descrição do Conserto",
        help_text="Descrição detalhada do serviço realizado",
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="PENDENTE", verbose_name="Status"
    )

    quilometragem = models.IntegerField(
        verbose_name="Quilometragem", help_text="Quilometragem atual do veículo"
    )

    class Meta:
        verbose_name = "Ordem de Serviço"
        verbose_name_plural = "Ordens de Serviço"
        ordering = ["-data_de_entrada"]
        db_table = "services_serviceorder"

    def __str__(self):
        return f"OS {self.id} - {self.pk_id_carro.placa}"

    @property
    def orcamento_reais(self):
        return self.orcamento / 100.0
