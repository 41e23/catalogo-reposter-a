# Dulce Repostería — Catálogo Web

## Propósito

Aplicación Django con API RESTful JWT para organizar materiales de repostería y consultar
información de proveedores. Los materiales se almacenan en PostgreSQL y se
pueden crear, consultar, editar y eliminar desde el sitio. La portada presenta
hasta tres materiales disponibles consultados mediante el ORM.

## Integrantes

- Pablo Gutiérrez
- Matías Gallardo
- Álvaro García

## Aplicaciones

- `inicio`: portada e información general.
- `materiales`: modelo `Material`, migraciones, ModelForm, Django Admin, CRUD HTML y API REST.
- `proveedores`: módulo de proveedores.

## Requisitos

- Python compatible con Django 6.1
- PostgreSQL
- Git

## Instalación y ejecución (Windows)

```powershell
git clone https://github.com/41e23/catalogo-reposter-a.git
cd catalogo-reposter-a
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edita `.env` localmente con la configuración de tu PostgreSQL. Genera una clave
secreta local con:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Crea la base de datos configurada en `DB_NAME` y ejecuta:

```powershell
python manage.py check
python manage.py showmigrations
python manage.py migrate
python manage.py test materiales inicio
python manage.py runserver
```

Abre http://127.0.0.1:8000/ en el navegador.

## Variables de entorno y seguridad

`config/settings.py` carga `.env` localmente mediante `python-dotenv`. Configura
`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` y las credenciales PostgreSQL mediante
variables de entorno, nunca en el código. Completa `DB_NAME`, `DB_USER`,
`DB_PASSWORD`, `DB_HOST` y `DB_PORT` para tu instancia.

`.gitignore` excluye `.env` y permite versionar `.env.example`, que solo
contiene valores de muestra. Si falta `SECRET_KEY` o `DB_PASSWORD`, Django
detiene el arranque con un mensaje explícito.

Las dependencias para PostgreSQL y el archivo de entorno son
`psycopg[binary]` y `python-dotenv`.

## Rutas

- `/` — Inicio con materiales disponibles.
- `/nosotros/` — Información del emprendimiento.
- `/materiales/` — CRUD de materiales.
- `/proveedores/` — Proveedores.
- `/admin/` — Django Admin.

## Trabajo colaborativo

Este proyecto se desarrolla en un repositorio compartido en GitHub por Pablo
Gutiérrez, Matías Gallardo y Álvaro García. Las aplicaciones mantienen sus
propias rutas mediante `urls.py` e `include()`.

## Dificultades y soluciones

1. Organizar las rutas de las aplicaciones: usar un `urls.py` por aplicación
   e incluirlos desde `config/urls.py`.
2. Evitar repetir estructura HTML: utilizar plantillas con `extends` y bloques.
3. Conectar el catálogo a datos persistentes: consultar `Material` mediante el
   ORM en el CRUD y en la portada.
4. Proteger configuración sensible: cargar secretos desde `.env`, ignorarlo
   en Git y compartir únicamente `.env.example`.

## Registro de uso de IA

La IA apoyó la configuración de PostgreSQL, la protección de credenciales y la
integración de la portada. Problema: la configuración inicial usaba SQLite y
tenía una clave escrita en `settings.py`. Prompt: “¿Cómo puedo configurar
Django con PostgreSQL usando un archivo .env para no guardar SECRET_KEY,
usuario ni contraseña directamente en settings.py?”. Decisión: utilizar
`python-dotenv`, excluir `.env` de Git, conservar las tres aplicaciones e
integrar la portada con el ORM.

Registra los resultados de `check`, `migrate`, las pruebas y la revisión en
navegador después de ejecutarlos en el entorno PostgreSQL local. No marques
como verificada una comprobación que no se haya ejecutado.


## Evaluación 3 — API RESTful y JWT

La API añade acceso JSON al **mismo modelo `Material` y la misma base PostgreSQL**;
no elimina el CRUD HTML ni las aplicaciones `inicio`, `materiales` y `proveedores`.
Instalar las dependencias actualizadas con `python -m pip install -r requirements.txt`.

| Método | URL | Resultado | Acceso |
| --- | --- | --- | --- |
| GET | `/api/materiales/` | Lista JSON (200) | Público |
| GET | `/api/materiales/<id>/` | Detalle JSON (200/404) | Público |
| POST | `/api/materiales/` | Crear (201/400) | JWT |
| PUT/PATCH | `/api/materiales/<id>/` | Actualizar (200/400/404) | JWT |
| DELETE | `/api/materiales/<id>/` | Borrar (204/404) | JWT |
| POST | `/api/token/` | Obtener `access` y `refresh` | Usuario válido |
| POST | `/api/token/refresh/` | Renovar `access` | Refresh válido |

### Usuario de pruebas y obtención del token

Crear un usuario propio con `python manage.py createsuperuser` (no publicar su contraseña).
En Postman/Thunder Client enviar `POST http://127.0.0.1:8000/api/token/`, JSON:

```json
{"username":"TU_USUARIO","password":"TU_CONTRASEÑA_LOCAL"}
```

Copiar el `access` y añadir a las solicitudes protegidas la cabecera
`Authorization: Bearer TU_ACCESS_TOKEN`. No almacenar tokens ni contraseñas en Git.
Ejemplo de creación `POST /api/materiales/`:

```json
{"nombre":"Chocolate amargo","categoria":"chocolates","precio":"250.00","disponible":true,"descripcion":"70% cacao"}
```

La API valida el mismo mínimo de precio ($100 CLP), nombre de al menos tres
caracteres y nombre que no sea solo numérico, además de categorías y tipos.
Las lecturas son públicas; las escrituras exigen token JWT. Los tokens access
expiran a los 15 minutos y los refresh al día. El CRUD HTML conserva sus
protecciones CSRF de la evaluación anterior.

### Comprobación

1. Configurar `.env` local y crear la base PostgreSQL de `DB_NAME`.
2. `python manage.py check` y `python manage.py migrate`.
3. `python manage.py test materiales inicio proveedores`.
4. `python manage.py runserver` y verificar las ocho pruebas de la pauta
   en Postman/Thunder Client: tokens, GET sin token, GET autorizado, POST,
   PUT/PATCH, DELETE, POST inválido y POST sin token.
5. Comprobar datos en `/admin/` y PostgreSQL, capturar evidencia para el PDF.

Los tests `materiales/test_api.py` automatizan estas operaciones, además de
validar 404 y tokens inválidos. **La ejecución real y las capturas deben hacerse
con PostgreSQL local configurado; no se considera una prueba aprobada solo por
existir el test.**

### Desarrollo colaborativo e IA

Se incorporaron `serializers.py`, `api_views.py`, `api_urls.py`, `test_api.py`,
configuración DRF/JWT en `settings.py`, rutas en `config/urls.py` y dependencias.
El equipo debe documentar los problemas, prompts, cambios aceptados y resultados
reales de las pruebas; no inventar iteraciones ni capturas. Realizar commits
individuales descriptivos sobre una rama de trabajo y revisar antes del merge.
