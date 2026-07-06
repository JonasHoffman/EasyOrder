from django import forms
from Cardapio.models import Sabor


class SaborForm(forms.ModelForm):

    class Meta:
        model = Sabor
        fields = [
            "grupo",
            "nome",
            "descricao",
            "imagem",
            "valor_adicional",
            "ordem",
            "ativo",
        ]

        widgets = {
            "descricao": forms.Textarea(attrs={
                "rows": 3
            }),
        }

    def __init__(self, *args, **kwargs):
        loja = kwargs.pop("loja", None)

        super().__init__(*args, **kwargs)

        if loja:
            self.fields["grupo"].queryset = (
                self.fields["grupo"]
                .queryset
                .filter(loja=loja, ativo=True)
            )