
from django import forms

from Cardapio.models import ProdutoGrupoCombo


class ProdutoGrupoComboForm(forms.ModelForm):

    class Meta:

        model = ProdutoGrupoCombo

        fields = [
            "obrigatorio",
            "minimo",
            "maximo",
            "ordem",
        ]

        widgets = {

            "obrigatorio": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),

            "minimo": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                }
            ),

            "maximo": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),

            "ordem": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        minimo = cleaned_data.get("minimo")
        maximo = cleaned_data.get("maximo")

        if (
            minimo is not None
            and maximo is not None
            and minimo > maximo
        ):
            raise forms.ValidationError(
                "O mínimo não pode ser maior que o máximo."
            )

        return cleaned_data

