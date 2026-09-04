from django.shortcuts import render


def lista(request):
    """Vista placeholder: la persona a cargo de 'materiales' debe
    completar esta vista con el listado real de productos."""
    contexto = {
        'titulo_pagina': 'Materiales',
    }
    return render(request, 'materiales/lista.html', contexto)
