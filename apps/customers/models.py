import uuid

from django.db import models

from apps.core.models import SoftDeleteModel
from apps.core.utils import format_phone


class Customer(SoftDeleteModel):
    uuid_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name="UUID"
    )

    nome = models.CharField(
        max_length=100, verbose_name="Nome", help_text="Nome do cliente"
    )

    telefone = models.CharField(
        max_length=15, verbose_name="Telefone", help_text="Telefone de contato"
    )

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["nome"]
        db_table = "customers_customer"

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if self.telefone:
            self.telefone = format_phone(self.telefone)
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        return self.nome
