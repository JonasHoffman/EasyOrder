from django import forms
from Cardapio.models import Produto
from Cardapio.utils.validar_imgs import validar_imagem


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
            "possui_sabores",
            "permite_multiplos_sabores",
            "maximo_sabores",
            "tempo_preparo",
            "ordem",
        ]

        widgets = {
            "categoria": forms.Select(attrs={"class": "form-control","placeholder":"Escolha qual a categoria do seu produto"}),
            "nome": forms.TextInput(attrs={"class": "form-control","placeholder":"Ex.: X-Burguer Especial"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3,"placeholder":"Ingredientes ou descrição do produto"}),
            "preco": forms.NumberInput(attrs={"class": "form-control","placeholder":"Ex.: 29,90"}),
            "ordem": forms.NumberInput(attrs={"class": "form-control","placeholder":"Ex 0, quanto menor o numero, primeiro sera na ordem."}),
            "tempo_preparo": forms.NumberInput(attrs={"class": "form-control","placeholder":"Ex 20 Minutos"}),
        }

        labels = {
        "categoria": "Escolha a categoria do produto",
    }
    def clean_imagem(self):

        imagem = self.cleaned_data.get("imagem")

        if imagem:
            validar_imagem(imagem)

        return imagem