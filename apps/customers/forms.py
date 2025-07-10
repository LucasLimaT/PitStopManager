from django import forms

from apps.core.forms import BaseBootstrapForm

from .models import Customer


class CustomerForm(BaseBootstrapForm):
    class Meta:
        model = Customer
        fields = [
            "nome",
            "telefone",
        ]

        labels = {
            "nome": "Nome",
            "telefone": "Telefone",
        }

        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Nome do cliente"}),
            "telefone": forms.TextInput(
                attrs={
                    "placeholder": "(11) 99999-9999",
                    "minlength": "10",
                    "maxlength": "15",
                    "inputmode": "numeric",
                    "title": "Digite um telefone com 10 ou 11 números",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nome"].required = True
        self.fields["telefone"].required = True

    def clean_telefone(self):
        telefone = self.cleaned_data.get("telefone")
        if telefone:
            telefone_numerico = "".join(filter(str.isdigit, telefone))
            if len(telefone_numerico) < 10 or len(telefone_numerico) > 11:
                raise forms.ValidationError(
                    "O telefone deve ter entre 10 e 11 dígitos."
                )
            return telefone_numerico
        return telefone
