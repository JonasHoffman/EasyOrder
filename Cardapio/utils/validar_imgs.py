from django.core.exceptions import ValidationError


def validar_imagem(imagem):

    extensoes = [
        "jpg",
        "jpeg",
        "png",
        "webp"
    ]

    extensao = imagem.name.split(".")[-1].lower()

    if extensao not in extensoes:
        raise ValidationError(
            "Formato de imagem inválido."
        )


    if imagem.size > 2 * 1024 * 1024:
        raise ValidationError(
            "A imagem deve ter no máximo 2MB."
        )
