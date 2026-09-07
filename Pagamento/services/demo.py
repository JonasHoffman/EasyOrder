from Pagamento.services.pagamento import confirmar_pagamento


def aprovar_pagamento_demo(pagamento):
    confirmar_pagamento(pagamento)

    return pagamento