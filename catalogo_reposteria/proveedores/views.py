from django.shortcuts import render


def lista(request):
    """Vista placeholder: la persona a cargo de 'proveedores' debe
    completar esta vista con el listado real de proveedores."""
    contexto = {
        'titulo_pagina': 'Proveedores',
    }
    return render(request, 'proveedores/lista.html', contexto)
