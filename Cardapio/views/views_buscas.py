from django.http import JsonResponse
from django.db.models import Q
from Cardapio.models import Categoria, Produto

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
                'url': c.get_absolute_url() if hasattr(c, 'get_absolute_url') else f'/categoria/{c.slug}/',
            })

        for p in produtos:
            resultados.append({
                'tipo': 'produto',
                'nome': p.nome,
                'categoria': p.categoria.nome,
                'preco': str(p.preco),
                'imagem': p.imagem.url if p.imagem else '',
                'url': f'/produto/{p.nome}/',
            })

    return JsonResponse({'resultados': resultados})