from django import forms

from apps.core.forms import BaseBootstrapForm
from apps.vehicles.models import Vehicle

from .models import ServiceOrder


class ServiceOrderForm(BaseBootstrapForm):
    orcamento = forms.IntegerField(
        min_value=0,
        widget=forms.TextInput(
            attrs={
                "placeholder": "0",
                "inputmode": "numeric",
                "pattern": "^[0-9]+$",
                "title": "Insira apenas números inteiros positivos (em centavos)",
            },
        ),
        help_text="Valor em centavos. Ex: 15000 para R$150,00",
    )
    quilometragem = forms.IntegerField(
        min_value=0,
        widget=forms.TextInput(
            attrs={
                "placeholder": "0",
                "inputmode": "numeric",
                "pattern": "^[0-9]+$",
                "title": "Insira apenas números inteiros positivos",
            },
        ),
        help_text="Quilometragem atual do veículo.",
    )

    class Meta:
        model = ServiceOrder
        fields = [
            "pk_id_carro",
            "data_de_entrada",
            "data_de_entrega",
            "orcamento",
            "descricao_problema",
            "descricao_concerto",
            "status",
            "quilometragem",
        ]

        widgets = {
            "data_de_entrada": forms.DateInput(attrs={"type": "date"}),
            "data_de_entrega": forms.DateInput(attrs={"type": "date"}),
            "descricao_problema": forms.Textarea(attrs={"rows": 3}),
            "descricao_concerto": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["pk_id_carro"].queryset = Vehicle.active_objects.all()
        self.fields["data_de_entrega"].required = False
        self.fields["orcamento"].help_text = (
            "Valor em centavos. Ex: 15000 para R$150,00"
        )

    def clean(self):
        cleaned_data = super().clean()
        data_de_entrada = cleaned_data.get("data_de_entrada")
        data_de_entrega = cleaned_data.get("data_de_entrega")

        if data_de_entrada and data_de_entrega:
            if data_de_entrega < data_de_entrada:
                self.add_error(
                    "data_de_entrega",
                    "A data de entrega não pode ser anterior à data de entrada.",
                )

        return cleaned_data
