from django import forms

from Cardapio.models import ProdutoComboGrupo


class ProdutoComboGrupoForm(forms.ModelForm):

    class Meta:

        model = ProdutoComboGrupo

        fields = [
            "nome",
            "descricao",
            "ativo",
            "ordem",
        ]


        widgets = {

            "nome": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex.: Bebidas"
                }
            ),


            "descricao": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Descrição do grupo"
                }
            ),


            "ativo": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),


            "ordem": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0
                }
            ),
        }