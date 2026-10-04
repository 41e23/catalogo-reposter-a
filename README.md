# Alacena & Molde

Aplicación Django para un emprendimiento de repostería. Incluye un catálogo, información de proveedores y un CRUD de materiales persistido mediante el ORM.

## Aplicaciones

- `catalogo`: portada y página de información.
- `inicio`: páginas heredadas del proyecto original.
- `materiales`: inventario, validación y CRUD.
- `proveedores`: listado de proveedores.

El modelo `Material` guarda nombre, categoría, stock, precio y descripción. El CRUD está en `/materiales/`; Django Admin se encuentra en `/admin/`.

## Requisitos

- Python 3.10 o superior.
- Para la entrega con PostgreSQL: PostgreSQL 14 o superior, una base de datos y un usuario con permisos.

## Instalación en Windows

```powershell
git clone https://github.com/41e23/catalogo-reposter-a.git
cd catalogo-reposter-a
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edita `.env` con la configuración local. El archivo `.env` está excluido de Git y no se debe compartir. Para PostgreSQL, crea una base y un rol, por ejemplo desde `psql`:

```sql
CREATE ROLE alacena_user WITH LOGIN PASSWORD 'elige-una-clave-local';
CREATE DATABASE alacena_molde OWNER alacena_user;
```

En `.env`, cambia `DB_USER` a `alacena_user` y `DB_PASSWORD` por la misma clave local. No subas esa clave. Luego ejecuta:

```powershell
python manage.py check
python manage.py showmigrations
python manage.py migrate
python manage.py loaddata materiales_demo
python manage.py createsuperuser
python manage.py runserver
```

La fixture `materiales/fixtures/materiales_demo.json` carga tres materiales de ejemplo mediante Django. Abre `http://127.0.0.1:8000/`. Para completar la evidencia administrativa, inicia sesión en `http://127.0.0.1:8000/admin/`, modifica un material y elimina otro desde el panel.

Si `.env` no existe o `DB_ENGINE=sqlite`, el proyecto usa SQLite para desarrollo local. Para verificar el requisito PostgreSQL, configura PostgreSQL en `.env` y confirma que `migrate` y la aplicación se conecten antes de tomar las capturas de entrega.

## Variables de entorno

`.env.example` contiene valores de muestra. Copia el archivo a `.env` y reemplaza la clave y los datos de conexión localmente:

- `SECRET_KEY`: clave privada de Django.
- `DEBUG`: `False` en una instalación compartida o desplegada.
- `ALLOWED_HOSTS`: nombres de host permitidos.
- `DB_ENGINE`: `postgresql` para PostgreSQL o `sqlite` para desarrollo local.
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: conexión a PostgreSQL.

Nunca incluyas `.env`, contraseñas o claves en commits.

## Pruebas

```powershell
python manage.py test materiales
python manage.py check
```

La suite del CRUD cubre listado, creación válida, campos vacíos, datos inválidos, edición, cancelar y confirmar eliminación, 404 y protección CSRF.

## Rutas principales

- `/`: catálogo.
- `/inicio/`: inicio del proyecto original.
- `/nosotros/`: información del emprendimiento.
- `/materiales/`: inventario y acciones CRUD.
- `/proveedores/`: proveedores.
- `/admin/`: administración de Django.

## Equipo y uso de IA

Integrantes indicados en la primera etapa: Pablo Gutiérrez, Matías Gallardo y Álvaro García. Cada integrante debe registrar sus propios commits; la historia de Git debe reflejar las contribuciones reales.

La IA se usó para revisar el CRUD, investigar errores y preparar evidencia. El informe debe conservar las preguntas, propuestas, decisiones y resultados reales del equipo; completen la reflexión con sus propias palabras antes de entregar.

