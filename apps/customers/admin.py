from django.contrib import admin

from apps.core.admin import BaseModelAdmin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(BaseModelAdmin):
    list_display = ["nome", "telefone", "created_at", "updated_at"]

    list_filter = ["created_at", "updated_at"]

    search_fields = ["nome", "telefone"]

    fieldsets = [
        ("Informações Principais", {"fields": ["nome", "telefone"]}),
        (
            "Metadados do Sistema",
            {
                "fields": ["uuid_id", "created_at", "updated_at"],
                "classes": ["collapse"],
            },
        ),
    ]
