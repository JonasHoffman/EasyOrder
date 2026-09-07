from Pedidos.models import PedidoStatus


def criar_status_padrao(loja):

    status_padrao = [

        {
            "nome": "Recebido",
            "codigo": "recebido",
            "ordem": 1,
            "ativo": True,
            "aparece_kanban": True,
            "finalizador": False,
            "cancelamento": False,
            "sistema": True,
        },

        {
            "nome": "Em preparo",
            "codigo": "em-preparo",
            "ordem": 2,
            "ativo": True,
            "aparece_kanban": True,
            "finalizador": False,
            "cancelamento": False,
            "sistema": True,
        },

        {
            "nome": "Pronto",
            "codigo": "pronto",
            "ordem": 3,
            "ativo": True,
            "aparece_kanban": True,
            "finalizador": False,
            "cancelamento": False,
            "sistema": True,
        },

        {
            "nome": "Entregue",
            "codigo": "entregue",
            "ordem": 4,
            "ativo": True,
            "aparece_kanban": True,
            "finalizador": True,
            "cancelamento": False,
            "sistema": True,
        },

        {
            "nome": "Cancelado",
            "codigo": "cancelado",
            "ordem": 5,
            "ativo": True,
            "aparece_kanban": False,
            "finalizador": False,
            "cancelamento": True,
            "sistema": True,
        },

    ]

    for dados in status_padrao:

        PedidoStatus.objects.get_or_create(
            loja=loja,
            codigo=dados["codigo"],
            defaults=dados,
        )