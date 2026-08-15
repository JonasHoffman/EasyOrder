from django import forms

from Cardapio.models import Produto


class ComboForm(forms.ModelForm):

    class Meta:
        model = Produto
        fields = [
            "categoria",
            "nome",
            "descricao",
            "preco",
            "imagem",
            "tempo_preparo",
            "codigo",
            "ordem",
            "disponivel",
            "destaque",
        ]

        labels = {
            "categoria": "Categoria",
            "nome": "Nome do Combo",
            "descricao": "Descrição",
            "preco": "Preço do Combo",
            "imagem": "Imagem",
            "tempo_preparo": "Tempo de preparo (minutos)",
            "codigo": "Código",
            "ordem": "Ordem",
            "disponivel": "Disponível",
            "destaque": "Destaque",
        }

        widgets = {
            "categoria": forms.Select(attrs={
                "class": "form-select"
            }),

            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex.: Combo Família"
            }),

            "descricao": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Descrição do combo"
            }),

            "preco": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "0,00"
            }),

            "imagem": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),

            "tempo_preparo": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "20"
            }),

            "codigo": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Código interno"
            }),

            "ordem": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "disponivel": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

            "destaque": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }