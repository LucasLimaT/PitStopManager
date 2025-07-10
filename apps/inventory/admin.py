from django.contrib import admin

from apps.core.admin import BaseModelAdmin

from .models import Product


@admin.register(Product)
class ProductAdmin(BaseModelAdmin):
    list_display = ["nome", "estoque", "status_estoque", "created_at", "updated_at"]

    list_filter = ["created_at", "updated_at"]

    list_editable = ["estoque"]

    search_fields = ["nome"]

    fieldsets = [
        ("Produto", {"fields": ["nome", "estoque"]}),
        (
            "Metadados do Sistema",
            {
                "fields": ["uuid_id", "created_at", "updated_at"],
                "classes": ["collapse"],
            },
        ),
    ]

    @admin.display(description="Status do Estoque")
    def status_estoque(self, obj):
        if obj.estoque == 0:
            return "Sem estoque"
        elif obj.estoque < 10:
            return "Estoque baixo"
        return "Disponível"
