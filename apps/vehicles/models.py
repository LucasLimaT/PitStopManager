import uuid

from django.db import models

from apps.core.models import SoftDeleteModel
from apps.customers.models import Customer


class Vehicle(SoftDeleteModel):
    uuid_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="UUID",
    )

    pk_id_cliente = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="vehicles",
        verbose_name="Cliente",
    )

    marca = models.CharField(
        max_length=50,
        verbose_name="Marca",
        help_text="Marca do veículo",
    )

    modelo = models.CharField(
        max_length=50,
        verbose_name="Modelo",
        help_text="Modelo do veículo",
    )

    ano = models.PositiveIntegerField(
        verbose_name="Ano",
        help_text="Ano do veículo",
    )

    placa = models.CharField(
        max_length=8,
        unique=True,
        verbose_name="Placa",
        help_text="Placa do veículo",
    )

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"
        ordering = ["placa"]
        db_table = "vehicles_vehicle"

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"

    @property
    def display_name(self):
        return f"{self.marca} {self.modelo} {self.ano}"

    def reactivate(self):
        self.is_active = True
        self.deleted_at = None
        self.save()
