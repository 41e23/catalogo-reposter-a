from django.shortcuts import render


def imagen_por_categoria(categoria):
    mapa = {
        "Ingredientes": "/static/images/ingredientes.svg",
        "Utensilios": "/static/images/utensilios.svg",
        "Decoración": "/static/images/decoracion.svg",
    }
    return mapa.get(categoria, "/static/images/varios.svg")


PRODUCTOS = [
    {"nombre": "Harina 0000", "categoria": "Ingredientes", "precio": 1850, "disponible": True, "imagen": imagen_por_categoria("Ingredientes")},
    {"nombre": "Cacao amargo", "categoria": "Ingredientes", "precio": 3200, "disponible": True, "imagen": imagen_por_categoria("Ingredientes")},
    {"nombre": "Chocolate cobertura", "categoria": "Ingredientes", "precio": 5800, "disponible": True, "imagen": imagen_por_categoria("Ingredientes")},
    {"nombre": "Esencia de vainilla", "categoria": "Ingredientes", "precio": 2400, "disponible": False, "imagen": imagen_por_categoria("Ingredientes")},
    {"nombre": "Mix de grageas", "categoria": "Decoración", "precio": 2100, "disponible": True, "imagen": imagen_por_categoria("Decoración")},
    {"nombre": "Batidor globo", "categoria": "Utensilios", "precio": 4600, "disponible": True, "imagen": imagen_por_categoria("Utensilios")},
    {"nombre": "Espátula angular", "categoria": "Utensilios", "precio": 3900, "disponible": True, "imagen": imagen_por_categoria("Utensilios")},
    {"nombre": "Mangas descartables", "categoria": "Utensilios", "precio": 1750, "disponible": True, "imagen": imagen_por_categoria("Utensilios")},
    {"nombre": "Colorante coral", "categoria": "Decoración", "precio": 1950, "disponible": True, "imagen": imagen_por_categoria("Decoración")},
    {"nombre": "Azúcar impalpable", "categoria": "Ingredientes", "precio": 1600, "disponible": True, "imagen": imagen_por_categoria("Ingredientes")},
    {"nombre": "Molde savarín", "categoria": "Utensilios", "precio": 7600, "disponible": True, "imagen": imagen_por_categoria("Utensilios")},
    {"nombre": "Flores de azúcar", "categoria": "Decoración", "precio": 2800, "disponible": True, "imagen": imagen_por_categoria("Decoración")},
]

PROVEEDORES = [
    {"nombre": "La Espiga", "detalle": "Harinas y granos · Córdoba", "tipo": "MATERIAS PRIMAS"},
    {"nombre": "Casa Cobre", "detalle": "Herramientas de cocina · Buenos Aires", "tipo": "UTENSILIOS"},
    {"nombre": "Colorín", "detalle": "Colorantes y detalles · Rosario", "tipo": "DECORACIÓN"},
    {"nombre": "Origen Cacao", "detalle": "Chocolate de origen · Misiones", "tipo": "MATERIAS PRIMAS"},
]


def inicio(request):
    categoria = request.GET.get("categoria", "Todos")
    busqueda = request.GET.get("buscar", "").strip()
    productos = PRODUCTOS
    if categoria != "Todos":
        productos = [producto for producto in productos if producto["categoria"] == categoria]
    if busqueda:
        productos = [producto for producto in productos if busqueda.lower() in producto["nombre"].lower()]

    contexto = {
        "productos": productos,
        "proveedores": PROVEEDORES,
        "categoria_actual": categoria,
        "busqueda": busqueda,
        "categorias": ["Todos", "Ingredientes", "Utensilios", "Decoración"],
    }
    return render(request, "catalogo/inicio.html", contexto)


def nosotros(request):
    return render(request, "catalogo/nosotros.html")
