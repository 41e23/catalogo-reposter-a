from django.shortcuts import render

PRODUCTOS = [
    {"nombre": "Harina 0000", "categoria": "Ingredientes", "precio": 1850, "disponible": True, "imagen": "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=600&q=80"},
    {"nombre": "Cacao amargo", "categoria": "Ingredientes", "precio": 3200, "disponible": True, "imagen": "https://images.unsplash.com/photo-1575377427642-087cf684f04d?auto=format&fit=crop&w=600&q=80"},
    {"nombre": "Chocolate cobertura", "categoria": "Ingredientes", "precio": 5800, "disponible": True, "imagen": "https://images.unsplash.com/photo-1575377427642-087cf684f04d?auto=format&fit=crop&w=600&q=80"},
    {"nombre": "Esencia de vainilla", "categoria": "Ingredientes", "precio": 2400, "disponible": False, "imagen": "https://images.unsplash.com/photo-1599785209707-a456fc1337bb?auto=format&fit=crop&w=600&q=80"},
    {"nombre": "Mix de grageas", "categoria": "Decoración", "precio": 2100, "disponible": True, "imagen": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=600&q=80"},
    {"nombre": "Batidor globo", "categoria": "Utensilios", "precio": 4600, "disponible": True, "imagen": "https://images.unsplash.com/photo-1556911220-bff31c812dba?auto=format&fit=crop&w=600&q=80"},
    {"nombre": "Espátula angular", "categoria": "Utensilios", "precio": 3900, "disponible": True, "imagen": "https://images.unsplash.com/photo-1598373182133-52452f7691ef?auto=format&fit=crop&w=600&q=80"},
    {"nombre": "Mangas descartables", "categoria": "Utensilios", "precio": 1750, "disponible": True, "imagen": "https://images.unsplash.com/photo-1623428187969-5da2dcea5b59?auto=format&fit=crop&w=600&q=80"},
    {"nombre": "Colorante coral", "categoria": "Decoración", "precio": 1950, "disponible": True, "imagen": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=600&q=80"},
    {"nombre": "Azúcar impalpable", "categoria": "Ingredientes", "precio": 1600, "disponible": True, "imagen": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?auto=format&fit=crop&w=600&q=80"},
    {"nombre": "Molde savarín", "categoria": "Utensilios", "precio": 7600, "disponible": True, "imagen": "https://images.unsplash.com/photo-1599785209707-a456fc1337bb?auto=format&fit=crop&w=600&q=80"},
    {"nombre": "Flores de azúcar", "categoria": "Decoración", "precio": 2800, "disponible": True, "imagen": "https://images.unsplash.com/photo-1535254973040-607b474cb50d?auto=format&fit=crop&w=600&q=80"},
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
