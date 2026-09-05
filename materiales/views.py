from django.shortcuts import render


def lista(request):
    """Lista de materiales (datos en memoria). Permite filtrar por categoría
    mediante `?categoria=` en la query string."""
    materiales = [
        {
            'nombre': 'Harina 0000',
            'categoria': 'Ingredientes',
            'precio': 1850,
            'disponible': True,
            'descripcion': 'Harina refinada ideal para bizcochos y masas ligeras.',
        },
        {
            'nombre': 'Cacao amargo',
            'categoria': 'Ingredientes',
            'precio': 3200,
            'disponible': True,
            'descripcion': 'Cacao en polvo para rellenos y coberturas intensas.',
        },
        {
            'nombre': 'Batidor globo',
            'categoria': 'Utensilios',
            'precio': 4600,
            'disponible': True,
            'descripcion': 'Batidor de acero inoxidable, resistente y ergonómico.',
        },
        {
            'nombre': 'Espátula angular',
            'categoria': 'Utensilios',
            'precio': 3900,
            'disponible': True,
            'descripcion': 'Espátula perfecta para alisar y desmoldar.',
        },
        {
            'nombre': 'Mix de grageas',
            'categoria': 'Decoración',
            'precio': 2100,
            'disponible': True,
            'descripcion': 'Surtido de grageas de colores para decorar tortas y cupcakes.',
        },
        {
            'nombre': 'Flores de azúcar',
            'categoria': 'Decoración',
            'precio': 2800,
            'disponible': False,
            'descripcion': 'Juego de flores comestibles para acabados elegantes.',
        },
    ]

    categorias = ['Todos', 'Ingredientes', 'Utensilios', 'Decoración']
    categoria_actual = request.GET.get('categoria', 'Todos')

    if categoria_actual and categoria_actual != 'Todos':
        materiales = [m for m in materiales if m['categoria'] == categoria_actual]

    contexto = {
        'titulo_pagina': 'Materiales',
        'materiales': materiales,
        'categorias': categorias,
        'categoria_actual': categoria_actual,
    }
    return render(request, 'materiales/lista.html', contexto)
