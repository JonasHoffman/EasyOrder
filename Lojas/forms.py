
from django import forms
from .models import Loja,Endereco
from django.utils.text import slugify

class LojaForm(forms.ModelForm):

    class Meta:
        model = Loja
        fields = [
            "nome",
            "slug",
            "logo",
            "telefone",
            "whatsapp",
            "email",
            "ativa",
        ]

        widgets = {
            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nome da loja"
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
            
            "ativa": forms.CheckboxInput(),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if not slug:
            slug = slugify(self.cleaned_data.get("nome"))
        return slug
        
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
            "cep": forms.TextInput(attrs={"class": "form-control"}),
            "logradouro": forms.TextInput(attrs={"class": "form-control"}),
            "numero": forms.TextInput(attrs={"class": "form-control"}),
            "complemento": forms.TextInput(attrs={"class": "form-control"}),
            "bairro": forms.TextInput(attrs={"class": "form-control"}),
            "cidade": forms.TextInput(attrs={"class": "form-control"}),
            "estado": forms.TextInput(attrs={"class": "form-control"}),
        }