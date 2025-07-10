import uuid

from django.db import models

from apps.core.models import SoftDeleteModel


class Product(SoftDeleteModel):
    uuid_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name="UUID"
    )

    nome = models.CharField(
        max_length=200, verbose_name="Nome", help_text="Nome da peça ou material"
    )

    estoque = models.IntegerField(
        default=0, verbose_name="Estoque", help_text="Quantidade em estoque"
    )

    class Meta:
        verbose_name = "Peça/Material"
        verbose_name_plural = "Peças e Materiais"
        ordering = ["nome"]
        db_table = "inventory_product"

    def __str__(self):
        return f"{self.nome} (Estoque: {self.estoque})"

    def update_stock(self, quantity, operation="add"):
        if operation == "add":
            self.estoque += quantity
        elif operation == "subtract":
            if self.estoque >= quantity:
                self.estoque -= quantity
            else:
                raise ValueError("Estoque insuficiente")
        self.save()
