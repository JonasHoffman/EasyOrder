from django import forms

from Cardapio.models import Ingrediente


class IngredienteForm(forms.ModelForm):

    class Meta:
        model = Ingrediente
        fields = [
            "nome",
            "ordem",
            "ativo",
        ]
        widgets = {

            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex.: Cebola",
            }),

            "ordem": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Ex.: 0",
            }),

            "ativo": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),

        }