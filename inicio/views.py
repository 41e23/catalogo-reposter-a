from django.shortcuts import render

from materiales.models import Material


def inicio(request):
    """Presenta el emprendimiento y materiales disponibles de la base de datos."""
    destacados = Material.objects.filter(disponible=True).order_by('nombre')[:3]
    contexto = {
        'titulo_pagina': 'Bienvenido/a',
        'nombre_emprendimiento': 'Dulce Repostería',
        'hay_destacados': destacados.exists(),
        'destacados': destacados,
    }
    return render(request, 'inicio/inicio.html', contexto)


def nosotros(request):
    """Pagina con la historia y proposito del emprendimiento."""
    contexto = {
        'titulo_pagina': 'Nosotros',
        'anio_inicio': 2023,
        'integrantes_equipo': [
            'Pablo Gutiérrez',
            'Matías Gallardo',
            'Álvaro García',
        ],
    }
    return render(request, 'inicio/nosotros.html', contexto)
