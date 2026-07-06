from django import forms
from Cardapio.models import Produto


class ProdutoForm(forms.ModelForm):

    class Meta:
        model = Produto

        fields = [
            "categoria",
            "nome",
            "descricao",
            "preco",
            "imagem",
            "disponivel",
            "destaque",
            "permite_multiplos_sabores",
            "maximo_sabores",
            "tempo_preparo",
            "ordem",
        ]

        widgets = {
            "categoria": forms.Select(attrs={"class": "form-control"}),
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "preco": forms.NumberInput(attrs={"class": "form-control"}),
            "ordem": forms.NumberInput(attrs={"class": "form-control"}),
            "tempo_preparo": forms.NumberInput(attrs={"class": "form-control"}),
        }