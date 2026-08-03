from django import forms
from Cardapio.models import Sabor
from Cardapio.utils.validar_imgs import validar_imagem



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
            "grupo": forms.Select(attrs={
                "class": "form-control",
                "placeholder": "Escolha o grupo de sabores",
            }),

            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex.: Calabresa",
            }),

            "descricao": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Ingredientes ou observações",
            }),

            "valor_adicional": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Ex.: 5,00",
            }),

            "ordem": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Ex.: 0",
            }),
}
    def clean_imagem(self):
    
            imagem = self.cleaned_data.get("imagem")
    
            if imagem:
                validar_imagem(imagem)
    
            return imagem
    def __init__(self, *args, **kwargs):
        loja = kwargs.pop("loja", None)

        super().__init__(*args, **kwargs)

        if loja:
            self.fields["grupo"].queryset = (
                self.fields["grupo"]
                .queryset
                .filter(loja=loja, ativo=True)
            )