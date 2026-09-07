from django import forms

from Pedidos.models import PedidoStatus


class PedidoStatusForm(forms.ModelForm):

    class Meta:
        model = PedidoStatus

        fields = [
            "nome",
            "ordem",
            "ativo",
            "aparece_kanban",
        ]

        widgets = {

            "nome": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex.: Em preparo",
                }
            ),

            "ordem": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                }
            ),

            "ativo": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "aparece_kanban": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def __init__(self, *args, loja=None, **kwargs):

        self.loja = loja

        super().__init__(*args, **kwargs)

        # =====================================================
        # STATUS DO SISTEMA
        # =====================================================

        if (
            self.instance
            and self.instance.pk
            and self.instance.sistema
        ):

            codigo = self.instance.codigo

            # =================================================
            # RECEBIDO
            #
            # É a porta de entrada dos pedidos.
            # Deve obrigatoriamente permanecer:
            #
            # ativo = True
            # aparece_kanban = True
            # =================================================

            if codigo == "recebido":

                self.fields["ativo"].disabled = True
                self.fields["aparece_kanban"].disabled = True

            # =================================================
            # ENTREGUE
            #
            # É o destino dos pedidos finalizados.
            # Não aparece como coluna normal do Kanban.
            # =================================================

            elif codigo == "entregue":

                self.fields["ativo"].disabled = True
                

    def clean(self):

        cleaned_data = super().clean()

        status = self.instance

        # =====================================================
        # STATUS DO SISTEMA
        # =====================================================

        if status and status.pk and status.sistema:

            codigo = status.codigo

            # =================================================
            # RECEBIDO
            #
            # Sempre ativo e sempre no Kanban.
            # =================================================

            if codigo == "recebido":

                cleaned_data["ativo"] = True
                cleaned_data["aparece_kanban"] = True

            # =================================================
            # ENTREGUE
            #
            # Destino dos pedidos finalizados.
            # =================================================

            elif codigo == "entregue":

                cleaned_data["ativo"] = True
                

            # =================================================
            # DEMAIS STATUS DO SISTEMA
            #
            # Aguardando pagamento
            # Em preparo
            # Pronto
            # Cancelado
            #
            # Podem ter ativo e Kanban configurados.
            # =================================================

        return cleaned_data