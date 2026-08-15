from django import forms

from Cardapio.models import (
    ProdutoGrupoAdicional,
    Produto,
    GrupoAdicional
)


class ProdutoGrupoAdicionalForm(forms.ModelForm):


    class Meta:

        model = ProdutoGrupoAdicional

        fields = [
            "produto",
            "grupo",
        ]


        widgets = {


            "grupo": forms.Select(
                attrs={
                    "class":"form-select"
                }
            ),
            "produto": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "id_produto",
                }
            ),

        }



    def __init__(
        self,
        *args,
        loja=None,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )


        self.fields["produto"].queryset = Produto.objects.none()

        self.fields["grupo"].queryset = GrupoAdicional.objects.none()



        if loja:


            self.fields["produto"].queryset = Produto.objects.filter(
                loja=loja
            ).order_by(
                "nome"
            )


            self.fields["grupo"].queryset = GrupoAdicional.objects.filter(
                loja=loja
            ).order_by(
                "nome"
            )