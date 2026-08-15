from django import forms
from Cardapio.models import Categoria
from django.core.exceptions import ValidationError
from Cardapio.utils.validar_imgs import validar_imagem





class CategoriaForm(forms.ModelForm):
    imagem = forms.ImageField(
        validators=[validar_imagem],
        required=False
    )
    
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
            "nome": forms.TextInput(attrs={"class": "form-control","placeholder":"Exemplo, Pizza, Refrigerante, Sobremesa..."}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "ordem": forms.NumberInput(attrs={"class": "form-control","placeholder":"Ex 0, quanto menor o numero, primeiro sera na ordem."}),
            "ativa": forms.CheckboxInput(),
            "imagem": forms.FileInput(attrs={
                "class": "form-control"
            }),
        }