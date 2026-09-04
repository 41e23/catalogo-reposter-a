from django.shortcuts import render

# Datos de ejemplo para mostrar contenido dinamico en la portada.
# Mas adelante estos datos podrian venir de un modelo (base de datos).
destacados = [
    {'nombre': 'Harina sin polvos de hornear', 'categoria': 'Ingredientes'},
    {'nombre': 'Manga pastelera reutilizable', 'categoria': 'Utensilios'},
    {'nombre': 'Colorante en gel rojo', 'categoria': 'Decoracion'},
]


def inicio(request):
    """Pagina principal del catalogo: presenta el emprendimiento y
    muestra algunos productos destacados usando contexto y un for."""
    contexto = {
        'titulo_pagina': 'Bienvenido/a',
        'nombre_emprendimiento': 'Dulce Reposteria',
        'hay_destacados': len(destacados) > 0,
        'destacados': destacados,
    }
    return render(request, 'inicio/inicio.html', contexto)


def nosotros(request):
    """Pagina con la historia y proposito del emprendimiento."""
    contexto = {
        'titulo_pagina': 'Nosotros',
        'anio_inicio': 2023,
        'integrantes_equipo': ['Maria', 'Pedro', 'Javiera'],
    }
    return render(request, 'inicio/nosotros.html', contexto)
