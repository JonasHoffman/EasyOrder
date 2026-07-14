from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from Cardapio.models import Produto,Promocao


class PromocaoForm(forms.ModelForm):

    class Meta:

        model = Promocao

        exclude = (
            "loja",
            "created_at",
            "updated_at",
        )

        widgets = {

            "nome": forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Ex.: Promoção da Semana"
            }),

            "produto": forms.Select(attrs={
                "class":"form-select",
                "id":"id_produto"
            }),

            "preco_promocional": forms.NumberInput(attrs={
                "class":"form-control",
                "step":"0.01",
                "min":"0.01"
            }),

            "descricao": forms.Textarea(attrs={
                "class":"form-control",
                "rows":3
            }),

            "data_inicio": forms.DateTimeInput(attrs={
                "class":"form-control",
                "type":"datetime-local"
            }),

            "data_fim": forms.DateTimeInput(attrs={
                "class":"form-control",
                "type":"datetime-local"
            }),

            "ativa": forms.CheckboxInput(attrs={
                "class":"form-check-input"
            }),

            "destaque": forms.CheckboxInput(attrs={
                "class":"form-check-input"
            })

        }

    def __init__(self, *args, loja=None, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["produto"].queryset = Produto.objects.none()

        if loja:

            self.fields["produto"].queryset = Produto.objects.filter(
                loja=loja,
                disponivel=True
            )

        self.loja = loja

    def clean(self):

        cleaned = super().clean()

        produto = cleaned.get("produto")
        preco = cleaned.get("preco_promocional")

        inicio = cleaned.get("data_inicio")
        fim = cleaned.get("data_fim")

        if produto and preco:

            if preco >= produto.preco:

                raise ValidationError(
                    "O preço promocional deve ser menor que o preço original."
                )

        if inicio and fim:

            if fim <= inicio:

                raise ValidationError(
                    "A data final deve ser maior que a inicial."
                )

        return cleaned