from django import forms

from apps.core.forms import BaseBootstrapForm

from .models import Product


class ProductForm(BaseBootstrapForm):
    estoque = forms.IntegerField(
        min_value=0,
        widget=forms.TextInput(
            attrs={
                "placeholder": "0",
                "inputmode": "numeric",
                "pattern": "^[0-9]+$",
                "title": "Insira apenas números inteiros positivos",
            },
        ),
    )

    class Meta:
        model = Product
        fields = [
            "nome",
            "estoque",
        ]

        help_texts = {
            "nome": "Nome da peça ou do material.",
            "estoque": "Quantidade atual em estoque.",
        }

        widgets = {
            "nome": forms.TextInput(
                attrs={"placeholder": "Insira o nome da peça ou material"}
            ),
        }
