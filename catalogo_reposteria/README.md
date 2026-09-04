# Dulce Repostería — Catálogo Web

## Propósito
Catálogo web para un emprendimiento de repostería. Permite visualizar
de forma ordenada productos (ingredientes, utensilios, materiales de
decoración) con nombre, categoría, precio y disponibilidad, además de
información de proveedores.

## Proyección
En próximas evaluaciones se incorporarán modelos y base de datos
(productos reales con precio/stock), formularios, un CRUD para
administrar el catálogo y, más adelante, autenticación de usuarios.

## Integrantes
- [Nombre integrante 1] — App `inicio`
- [Nombre integrante 2] — App `materiales`
- [Nombre integrante 3] — App `proveedores`

## Instalación
```bash
git clone <url-del-repositorio>
cd catalogo_reposteria
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

## Ejecución
```bash
python manage.py runserver
```
Luego abrir http://127.0.0.1:8000/ en el navegador.

## Estructura
```
catalogo_reposteria/
├── manage.py
├── requirements.txt
├── .gitignore
├── config/          (settings.py, urls.py)
├── inicio/          (Inicio, Nosotros)
├── materiales/      (catálogo de productos)
├── proveedores/     (información de proveedores)
└── templates/base.html
```

## Rutas principales
| Nombre de ruta        | URL              | Descripción            |
|------------------------|------------------|-------------------------|
| inicio:inicio          | /                | Página de inicio        |
| inicio:nosotros        | /nosotros/       | Sobre el emprendimiento |
| materiales:lista       | /materiales/     | Catálogo de materiales  |
| proveedores:lista      | /proveedores/    | Listado de proveedores  |

## Distribución del trabajo
- **Persona 1 (Inicio/Estructura):** app `inicio`, base.html, menú,
  config/urls.py, INSTALLED_APPS.
- **Persona 2 (Materiales):** app `materiales` completa.
- **Persona 3 (Proveedores):** app `proveedores` completa.

## Dificultades y soluciones
_(completar por el grupo)_

## Aprendizajes / reflexión
_(completar por el grupo, incluyendo registro de uso de IA)_
