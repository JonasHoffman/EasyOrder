
from django import forms
from .models import Loja,Endereco
from django.utils.text import slugify

from django import forms
from django.utils.text import slugify

from .models import Loja, Endereco


class LojaForm(forms.ModelForm):

    class Meta:
        model = Loja
        fields = [
            "nome",
            "razao_social",
            "cnpj",
            "inscricao_estadual",
            "inscricao_municipal",
            "slug",
            "logo",
            "telefone",
            "whatsapp",
            "email",
            "responsavel",
            "site",
            "instagram",
            "facebook",
            "ativa",
        ]

        widgets = {
            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nome fantasia"
            }),
            "razao_social": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Razão social"
            }),
            "cnpj": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "00.000.000/0000-00"
            }),
            "inscricao_estadual": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Inscrição Estadual"
            }),
            "inscricao_municipal": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Inscrição Municipal"
            }),
            "slug": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "url-da-loja"
            }),
            "telefone": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "whatsapp": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),
            "responsavel": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nome do responsável"
            }),
            "site": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://www.seusite.com.br"
            }),
            "instagram": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "@instagram"
            }),
            "facebook": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "facebook.com/suapagina"
            }),
            "ativa": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if not slug:
            slug = slugify(self.cleaned_data.get("nome"))
        return slug

    def clean_logo(self):
        logo = self.cleaned_data.get("logo")

        if logo:
            # Limite de 2MB
            if logo.size > 2 * 1024 * 1024:
                raise forms.ValidationError(
                    "A logo deve ter no máximo 2MB."
                )

            # Verifica extensão
            extensoes_permitidas = [
                "jpg",
                "jpeg",
                "png",
                "webp"
            ]

            extensao = logo.name.split(".")[-1].lower()

            if extensao not in extensoes_permitidas:
                raise forms.ValidationError(
                    "Formato inválido. Use JPG, PNG ou WEBP."
                )

        return logo
        
class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = [
            "cep",
            "logradouro",
            "numero",
            "complemento",
            "bairro",
            "cidade",
            "estado",
        ]

        widgets = {
            "cep": forms.TextInput(attrs={
                "class": "form-control",
                "id": "id_cep"
            }),
            "logradouro": forms.TextInput(attrs={
                "class": "form-control",
                "id": "id_logradouro"
            }),
            "numero": forms.TextInput(attrs={
                "class": "form-control",
                "id": "id_numero"
            }),
            "complemento": forms.TextInput(attrs={
                "class": "form-control",
                "id": "id_complemento"
            }),
            "bairro": forms.TextInput(attrs={
                "class": "form-control",
                "id": "id_bairro"
            }),
            "cidade": forms.TextInput(attrs={
                "class": "form-control",
                "id": "id_cidade"
            }),
            "estado": forms.TextInput(attrs={
                "class": "form-control",
                "id": "id_estado"
            }),
}