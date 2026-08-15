from django import forms

from Cardapio.models import Produto, ProdutoComboGrupoItem


class ProdutoComboGrupoItemForm(forms.ModelForm):

    class Meta:
        model = ProdutoComboGrupoItem

        fields = [
            "produto",
            "quantidade",
            "ordem",
        ]

        labels = {
            "produto": "Produto",
            "quantidade": "Quantidade",
            "ordem": "Ordem",
        }

        widgets = {

            "produto": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "quantidade": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "value": 1,
                }
            ),

            "ordem": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),

        }

    def __init__(self, *args, loja=None, **kwargs):

        super().__init__(*args, **kwargs)

        if loja:

            self.fields["produto"].queryset = Produto.objects.filter(
                loja=loja,
                tipo="SIMPLES",
                disponivel=True
            ).order_by("nome")

        self.fields["produto"].empty_label = "Selecione um produto"

    def clean_quantidade(self):

        quantidade = self.cleaned_data["quantidade"]

        if quantidade < 1:

            raise forms.ValidationError(
                "A quantidade deve ser maior que zero."
            )

        return quantidade

    def clean_ordem(self):

        ordem = self.cleaned_data["ordem"]

        if ordem < 1:

            raise forms.ValidationError(
                "A ordem deve ser maior que zero."
            )

        return ordem