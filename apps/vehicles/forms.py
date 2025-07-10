from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError

from apps.core.forms import BaseBootstrapForm
from apps.customers.models import Customer

from .models import Vehicle


class VehicleForm(BaseBootstrapForm):
    class Meta:
        model = Vehicle
        fields = [
            "pk_id_cliente",
            "marca",
            "modelo",
            "ano",
            "placa",
        ]

        labels = {
            "pk_id_cliente": "Cliente",
            "marca": "Marca",
            "modelo": "Modelo",
            "ano": "Ano",
            "placa": "Placa",
        }

        help_texts = {
            "pk_id_cliente": "Selecione o proprietário do veículo.",
            "marca": "Marca do veiculo.",
            "modelo": "Modelo do veiculo.",
            "ano": "Ano de fabricação do veículo (e.g., 2023).",
            "placa": "Placa do veiculo (e.g., ABC-1234).",
        }

        widgets = {
            "marca": forms.TextInput(attrs={"placeholder": "Ex: Honda"}),
            "modelo": forms.TextInput(attrs={"placeholder": "Ex: Civic"}),
            "ano": forms.TextInput(
                attrs={
                    "placeholder": "Ex: 2023",
                    "inputmode": "numeric",
                    "pattern": "[0-9]*",
                    "maxlength": "4",
                }
            ),
            "placa": forms.TextInput(attrs={"placeholder": "Ex: ABC-1234"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deleted_vehicle = None
        self.fields["pk_id_cliente"].queryset = Customer.active_objects.all()

    def clean_placa(self):
        placa = self.cleaned_data.get("placa")
        if placa:
            placa = placa.upper()

            if hasattr(self.instance, "pk") and self.instance.pk:
                if self.instance.placa == placa:
                    return placa

            active_vehicle = Vehicle.active_objects.filter(placa=placa).first()
            if active_vehicle:
                raise ValidationError("Já existe um veículo ativo com essa placa.")

            deleted_vehicle = Vehicle.objects.filter(
                placa=placa, is_active=False
            ).first()
            if deleted_vehicle:
                self.deleted_vehicle = deleted_vehicle
                raise ValidationError(f"DELETED_VEHICLE_EXISTS:{deleted_vehicle.pk}")

            return placa
        return placa

    def clean_ano(self):
        ano = self.cleaned_data.get("ano")
        if ano:
            ano_str = str(ano).replace(",", "").replace(".", "").replace(" ", "")

            try:
                ano_int = int(float(ano_str))
            except (ValueError, TypeError):
                raise ValidationError("O ano deve ser um número válido.")

            current_year = datetime.now().year
            if ano_int < 1900 or ano_int > current_year + 1:
                raise ValidationError(
                    f"O ano deve estar entre 1900 e {current_year + 1}."
                )

            return ano_int
        return ano
