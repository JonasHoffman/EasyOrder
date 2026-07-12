from django import forms
from Cardapio.models import GrupoAdicional


class GrupoAdicionalForm(forms.ModelForm):

    class Meta:
        model = GrupoAdicional
        fields = [
            "nome",
            "descricao",
            "obrigatorio",
            "minimo",
            "maximo",
            "ordem",
            "ativo",
        ]

        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 3}),
            "nome":forms.TextInput(attrs={

                "placeholder": "Ex.: Molhos"
            }),
        }