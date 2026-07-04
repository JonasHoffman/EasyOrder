from django import forms
from Cardapio.models import Categoria


class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = [
            "nome",
            "descricao",
            "imagem",
            "ordem",
            "ativa",
        ]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "ordem": forms.NumberInput(attrs={"class": "form-control"}),
            "ativa": forms.CheckboxInput(),
        }