# Dulce Repostería — Catálogo Web

## Propósito
Aplicación web desarrollada con Django para presentar y organizar
materiales utilizados en un emprendimiento de repostería y consultar
información de proveedores.

## Proyección
En futuras evaluaciones se podrá ampliar con base de datos, gestión de
stock, formularios y otras funcionalidades; estas mejoras no se
implementan en la entrega actual.

## Integrantes
- Pablo Gutiérrez
- Matías Gallardo
- Álvaro García

## Repositorio
https://github.com/41e23/catalogo-reposter-a

## Instalación y ejecución
```bash
git clone https://github.com/41e23/catalogo-reposter-a.git
cd catalogo-reposter-a
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abrir en el navegador:

http://127.0.0.1:8000/

## Estructura principal
```
config/
inicio/
materiales/
proveedores/
templates/
static/
manage.py
requirements.txt
.gitignore
README.md
```

## Rutas
/                  Inicio
/nosotros/         Nosotros
/materiales/       Materiales
/proveedores/      Proveedores

Materiales y Proveedores permiten filtrar contenido mediante parámetros
GET en la URL (por ejemplo `?categoria=` o `?tipo=`).

## Trabajo colaborativo
Este proyecto se desarrolla en un repositorio compartido en GitHub por:

- Pablo Gutiérrez
- Matías Gallardo
- Álvaro García

Los integrantes trabajan sobre el mismo repositorio usando Git y GitHub
para subir cambios, crear commits e integrar el trabajo.

## Dificultades y soluciones
1. Organización de rutas de las distintas aplicaciones.
   Solución: uso de `urls.py` por aplicación e `include()` en
   `config/urls.py`.
2. Evitar repetir estructura HTML.
   Solución: uso de `base.html`, `extends` y `block`.
3. Envío de información hacia los templates.
   Solución: uso de contexto desde las vistas mediante `render()`.
4. Filtrado de materiales y proveedores.
   Solución: utilización de `request.GET` y listas Python en las vistas.

## Aprendizajes
- Diferencia entre proyecto y aplicación en Django.
- Organización de rutas y uso de `include()`.
- Vistas basadas en funciones y `render()`.
- Plantillas: `extends`, `block`, `if` y `for`.
- Uso de `{% url %}` para navegación interna.
- Trabajo colaborativo con GitHub.

## Registro de uso de IA
La IA se utilizó como apoyo para revisar y proponer cambios menores en
la estructura y documentación del proyecto. Ejemplos breves:

- Conexión de rutas mediante `include()`:
  - Necesidad: organizar urls por aplicación.
  - Consulta: cómo incluir rutas de apps en `config/urls.py`.
  - Solución propuesta: usar `path('app/', include('app.urls'))`.
  - Cambio aplicado: ver `config/urls.py`.
  - Aprendizaje: facilita separación de responsabilidad.

- Herencia de plantillas con `base.html`:
  - Necesidad: evitar duplicación de HTML.
  - Consulta: cómo estructurar `base.html` y usar `extends`.
  - Solución propuesta: crear bloques `titulo` y `contenido`.
  - Cambio aplicado: las plantillas usan `{% extends 'base.html' %}`.
  - Aprendizaje: simplifica mantenimiento de layout.

- Envío de contexto desde vistas:
  - Necesidad: mostrar listas y variables en templates.
  - Consulta: cómo pasar contexto con `render()`.
  - Solución propuesta: pasar un diccionario `contexto`.
  - Cambio aplicado: vistas envían listas de materiales/proveedores.
  - Aprendizaje: permite templates dinámicos sin modelos.

- Implementación de filtros mediante `request.GET`:
  - Necesidad: filtrar listados sin formularios ni DB.
  - Consulta: cómo leer parámetros GET en vistas.
  - Solución propuesta: `request.GET.get('categoria')` y filtrar la lista.
  - Cambio aplicado: filtros en `materiales` y `proveedores`.
  - Aprendizaje: útil para demostraciones y prototipos.

