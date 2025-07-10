from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):
    readonly_fields = ["uuid_id", "created_at", "updated_at"]
    list_per_page = 25

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj))

        has_system_section = any(
            "Sistema" in str(section[0]) or "Metadados" in str(section[0])
            for section in fieldsets
        )

        if not has_system_section:
            fieldsets.append(
                [
                    "Metadados do Sistema",
                    {
                        "fields": ["uuid_id", "created_at", "updated_at"],
                        "classes": ["collapse"],
                    },
                ]
            )

        return fieldsets
