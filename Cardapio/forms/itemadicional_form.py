from django import forms
from Cardapio.models import ItemAdicional


class ItemAdicionalForm(forms.ModelForm):

    class Meta:
        model = ItemAdicional
        fields = [
            "grupo",
            "nome",
            "descricao",
            "preco",
            "imagem",
            "ordem",
            "ativo",
        ]

        widgets = {
            "grupo": forms.Select(attrs={
                "class": "form-select"
            }),

            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex.: Bacon Crocante"
            }),

            "descricao": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,"placeholder": "Ex.: Descrição do adicional (opcional)"
            }),

            "preco": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01"
            }),

            "imagem": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),

            "ordem": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "ativo": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

        labels = {
            "grupo": "Grupo",
            "nome": "Nome",
            "descricao": "Descrição",
            "preco": "Preço",
            "imagem": "Imagem",
            "ordem": "Ordem",
            "ativo": "Ativo",
        }