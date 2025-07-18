# Generated by Django 5.2 on 2025-05-29 11:39

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Criado em"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Atualizado em"),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Ativo")),
                (
                    "deleted_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Deletado em"
                    ),
                ),
                (
                    "uuid_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        unique=True,
                        verbose_name="UUID",
                    ),
                ),
                (
                    "nome",
                    models.CharField(
                        help_text="Nome do cliente", max_length=100, verbose_name="Nome"
                    ),
                ),
                (
                    "telefone",
                    models.CharField(
                        help_text="Telefone de contato",
                        max_length=20,
                        verbose_name="Telefone",
                    ),
                ),
            ],
            options={
                "verbose_name": "Cliente",
                "verbose_name_plural": "Clientes",
                "db_table": "customers_customer",
                "ordering": ["nome"],
            },
        ),
    ]
