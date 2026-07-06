
from django import forms

from Cardapio.models import GrupoDeSabores


class GrupoDeSaboresForm(forms.ModelForm):

    class Meta:
        model = GrupoDeSabores

        fields = [
            "nome",
            "ordem",
            "ativo",
        ]

        widgets = {
            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nome do grupo"
            }),

            "ordem": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "ativo": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }