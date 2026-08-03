from django import forms

from Cardapio.models import ProdutoSabor


class ProdutoSaborForm(forms.ModelForm):

    class Meta:
        model = ProdutoSabor

        fields = [
            "produto",
            "sabor",
            "ordem",
            "ativo",
        ]

        widgets = {

            "produto": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "sabor": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "ordem": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "ativo": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }


    def __init__(self, *args, **kwargs):

        loja = kwargs.pop("loja", None)

        super().__init__(*args, **kwargs)


        if loja:

            self.fields["produto"].queryset = (
                self.fields["produto"]
                .queryset
                .filter(loja=loja)
            )

            self.fields["sabor"].queryset = (
                self.fields["sabor"]
                .queryset
                .filter(loja=loja)
            )