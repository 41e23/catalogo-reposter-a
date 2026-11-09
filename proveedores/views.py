from django.shortcuts import render


def lista(request):
    """Listado sencillo de proveedores en memoria con filtro por tipo.
    No se usan modelos ni base de datos según las restricciones del ejercicio."""
    proveedores = [
        {
            'nombre': 'La Espiga',
            'tipo': 'Materias primas',
            'productos': ['Harina', 'Azúcar', 'Levadura'],
            'ciudad': 'Córdoba',
            'contacto': 'contacto@laespiga.example',
        },
        {
            'nombre': 'Casa Cobre',
            'tipo': 'Utensilios',
            'productos': ['Batidores', 'Moldes', 'Espátulas'],
            'ciudad': 'Buenos Aires',
            'contacto': 'ventas@casacobre.example',
        },
        {
            'nombre': 'Colorín',
            'tipo': 'Decoración',
            'productos': ['Colorantes', 'Grageas', 'Sprinkles'],
            'ciudad': 'Rosario',
            'contacto': 'hola@colorin.example',
        },
        {
            'nombre': 'Origen Cacao',
            'tipo': 'Materias primas',
            'productos': ['Chocolate en barra', 'Cacao en polvo'],
            'ciudad': 'Misiones',
            'contacto': 'info@origencacao.example',
        },
    ]

    tipos = ['Todos', 'Materias primas', 'Utensilios', 'Decoración']
    tipo_actual = request.GET.get('tipo', 'Todos')

    if tipo_actual and tipo_actual != 'Todos':
        proveedores = [p for p in proveedores if p['tipo'] == tipo_actual]

    contexto = {
        'titulo_pagina': 'Proveedores',
        'proveedores': proveedores,
        'tipos': tipos,
        'tipo_actual': tipo_actual,
    }
    return render(request, 'proveedores/lista.html', contexto)
