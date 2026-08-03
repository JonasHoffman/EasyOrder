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

        labels = {
            
            "nome": "Nome",
            "descricao": "Descrição",
            "obrigatorio": "Obrigatório",
            "minimo": "Mínimo",
            "maximo": "Máximo",
            "ordem": "Ordem",
            "ativo": "Ativo",
        }

        widgets = {

            "nome": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex.: Molhos",
                }
            ),

            "descricao": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Descrição do grupo (opcional)",
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

            "obrigatorio": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "ativo": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }