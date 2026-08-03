from django.http import JsonResponse
from django.db.models import Q
from Cardapio.models import Categoria, Produto
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

def buscar_sugestoes(request):
    termo = request.GET.get('q', '').strip()
    resultados = []

    if len(termo) >= 2:  # só busca a partir de 2 caracteres
        produtos = Produto.objects.filter(
            Q(nome__icontains=termo) | Q(categoria__nome__icontains=termo)
        ).select_related('categoria')[:5]  # limita a 5 sugestões

        categorias = Categoria.objects.filter(
            nome__icontains=termo
        )[:3]

        for c in categorias:

            resultados.append({
                'tipo': 'categoria',
                'nome': c.nome,
                'url': reverse('categorias:categoria_detalhe', args=[c.slug]),  # ajuste conforme o name real no seu urls.py
            })

        for p in produtos:
            resultados.append({
                'tipo': 'produto',
                'nome': p.nome,
                'categoria': p.categoria.nome,
                'preco': str(p.preco),
                'imagem': p.imagem.url if p.imagem else '',
                'url': reverse('produtos:produto_detalhe', args=[p.slug]),
            })

    return JsonResponse({'resultados': resultados})


@login_required
def produto_info(request, produto_id):

    loja = request.user.perfil.loja

    produto = get_object_or_404(
        Produto,
        id=produto_id,
        loja=loja
    )


    return JsonResponse({

        "id": produto.id,

        "nome": produto.nome,

        "preco": str(produto.preco),

        "permite_multiplos": produto.permite_multiplos_sabores,

        "maximo_sabores": produto.maximo_sabores

    })