from pathlib import Path
from datetime import date
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Image as ReportImage, Paragraph, Preformatted, SimpleDocTemplate, Spacer

BASE = Path(__file__).resolve().parent
OUTPUT = BASE / 'informe_materiales.pdf'


def read_file(rel_path: str) -> str:
    path = BASE / rel_path
    return path.read_text(encoding='utf-8')


def load_mono_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/CascadiaMono.ttf",
        "C:/Windows/Fonts/CascadiaCode.ttf",
        "C:/Program Files/Adobe/Acrobat DC/Acrobat/Resources/Font/Arial.ttf",
        "DejaVuSansMono.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def create_code_screenshot(rel_path: str, label: str) -> str:
    code = read_file(rel_path)
    lines = code.splitlines() or [""]
    width = 2200
    padding_x = 90
    padding_top = 110
    line_height = 30
    max_lines = 28
    height = max(500, padding_top + min(len(lines), max_lines) * line_height + 70)

    image = Image.new("RGB", (width, height), color=(24, 26, 32))
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle((20, 18, width - 20, height - 18), radius=18, fill=(33, 36, 43))
    draw.rounded_rectangle((20, 18, width - 20, 60), radius=18, fill=(46, 49, 58))
    for i, color in enumerate([(255, 92, 92), (255, 196, 87), (74, 222, 128)]):
        x = 36 + i * 18
        draw.ellipse((x, 30, x + 10, 40), fill=color)

    draw.text((40, 72), label, font=load_mono_font(28), fill=(212, 217, 232))

    font = load_mono_font(22)
    visible_lines = lines[:max_lines]
    for index, line in enumerate(visible_lines):
        safe_line = line if len(line) < 150 else line[:147] + "..."
        draw.text((padding_x, padding_top + index * line_height), safe_line, font=font, fill=(238, 240, 245))

    asset_dir = BASE / "_report_assets"
    asset_dir.mkdir(exist_ok=True)
    asset_name = str(Path(rel_path).with_suffix("")).replace("\\", "_").replace("/", "_")
    output_path = asset_dir / f"{asset_name}.png"
    image.save(output_path, format="PNG", optimize=True, quality=100)
    return str(output_path)


def create_output_screenshot(text: str, label: str) -> str:
    lines = text.splitlines() or [""]
    width = 2200
    padding_top = 110
    line_height = 30
    visible_lines = lines[:32]
    height = max(500, padding_top + len(visible_lines) * line_height + 70)

    image = Image.new("RGB", (width, height), color=(24, 26, 32))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((20, 18, width - 20, height - 18), radius=18, fill=(33, 36, 43))
    draw.rounded_rectangle((20, 18, width - 20, 60), radius=18, fill=(46, 49, 58))
    for index, color in enumerate([(255, 92, 92), (255, 196, 87), (74, 222, 128)]):
        x = 36 + index * 18
        draw.ellipse((x, 30, x + 10, 40), fill=color)

    draw.text((40, 72), label, font=load_mono_font(28), fill=(212, 217, 232))
    font = load_mono_font(22)
    for index, line in enumerate(visible_lines):
        safe_line = line if len(line) < 150 else line[:147] + "..."
        draw.text((90, padding_top + index * line_height), safe_line, font=font, fill=(238, 240, 245))

    output_path = BASE / "_report_assets" / "pruebas.png"
    image.save(output_path, format="PNG", optimize=True)
    return str(output_path)


def build_report():
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=22,
        leading=28, textColor=colors.HexColor('#1d1d1d'), spaceAfter=18
    )
    subtitle_style = ParagraphStyle(
        'SubtitleStyle', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=14,
        leading=18, textColor=colors.HexColor('#1b1b1b'), spaceBefore=18, spaceAfter=8
    )
    body = ParagraphStyle(
        'Body', parent=styles['BodyText'], fontName='Helvetica', fontSize=11,
        leading=15, spaceAfter=8
    )
    code = ParagraphStyle(
        'Code', parent=styles['Code'], fontName='Courier', fontSize=8.8,
        leading=11, backColor=colors.HexColor('#1e1f24'), textColor=colors.HexColor('#f4f7fb'),
        borderPadding=10, borderWidth=1, borderColor=colors.HexColor('#2f3138'),
        spaceBefore=8, spaceAfter=12, leftIndent=8, rightIndent=8
    )
    file_tag = ParagraphStyle(
        'FileTag', parent=styles['Heading3'], fontName='Helvetica-Bold', fontSize=10,
        leading=12, textColor=colors.HexColor('#2d2d2d'), spaceBefore=12, spaceAfter=4
    )
    section_title = ParagraphStyle(
        'SectionTitle', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=15,
        leading=18, textColor=colors.HexColor('#1a1a1a'), spaceBefore=12, spaceAfter=8
    )

    def add_code_block(label: str, rel_path: str):
        story.append(Paragraph(label, file_tag))
        screenshot = create_code_screenshot(rel_path, label)
        story.append(ReportImage(screenshot, width=170 * mm, height=220 * mm, kind='proportional'))

    def add_evidence(label: str, rel_path: str):
        story.append(Paragraph(label, file_tag))
        story.append(ReportImage(str(BASE / rel_path), width=170 * mm, height=230 * mm, kind='proportional'))
        story.append(Spacer(1, 3 * mm))

    story = []
    story.append(Paragraph('Informe de proyecto: Sistema web de materiales', title_style))
    story.append(Paragraph('Alacena & Molde', ParagraphStyle('Brand', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=colors.HexColor('#2c2c2c'))))
    story.append(Paragraph(f'Fecha de elaboración: {date.today().strftime("%d/%m/%Y")}', body))
    story.append(Paragraph('Integrantes registrados: Pablo Gutiérrez, Matías Gallardo y Álvaro García.', body))
    story.append(Paragraph('Repositorio: github.com/41e23/catalogo-reposter-a | Rama de entrega: entrega-materiales.', body))
    story.append(Spacer(1, 6 * mm))

    story.append(Paragraph('Problemática, continuidad y entidad', subtitle_style))
    story.append(Paragraph(
        'El proyecto continúa el catálogo de un emprendimiento de repostería. La entidad Material permite registrar insumos y controlar nombre, '
        'categoría, stock, precio y descripción. El CRUD se implementa en la aplicación materiales y se relaciona con el catálogo y la consulta de proveedores.', body
    ))
    story.append(Paragraph(
        'La estructura contiene cuatro aplicaciones Django: catalogo, inicio, materiales y proveedores. Los usuarios responsables del inventario '
        'pueden consultar y modificar materiales desde la interfaz web; el personal autorizado puede administrarlos desde Django Admin.', body
    ))

    story.append(Paragraph('Base de datos, entorno y estado de verificación', subtitle_style))
    story.append(Paragraph(
        'El proyecto admite PostgreSQL mediante DB_ENGINE y las variables DB_NAME, DB_USER, DB_PASSWORD, DB_HOST y DB_PORT cargadas desde .env. '
        'El archivo .env.example contiene solo valores de muestra y .env está excluido por .gitignore. psycopg está declarado en requirements.txt.', body
    ))
    story.append(Paragraph(
        '<b>Estado:</b> en el entorno usado para esta revisión no se detectó un servidor PostgreSQL local. Las pruebas ejecutadas aquí usaron SQLite '
        'como respaldo; por tanto, la conexión real a PostgreSQL, la verificación en pgAdmin y sus capturas siguen pendientes de realizar en un equipo con PostgreSQL configurado.', body
    ))

    story.append(Paragraph('Modelo, migraciones, datos de ejemplo y Admin', subtitle_style))
    story.append(Paragraph(
        'Material está definido en materiales/models.py y su migración inicial está en materiales/migrations/0001_initial.py. El modelo está '
        'registrado en Django Admin con columnas, filtro por categoría y búsqueda. Una prueba automatizada inicia sesión como superusuario de prueba '
        'y verifica que el listado administrativo muestre materiales.', body
    ))
    story.append(Paragraph(
        'La fixture materiales_demo carga tres registros de ejemplo mediante Django. Para completar la demostración, el equipo debe crear un superusuario '
        'local con createsuperuser, iniciar sesión en /admin/, modificar un registro y eliminar otro; no se guardan credenciales en este repositorio.', body
    ))
    add_code_block('materiales/admin.py', 'materiales/admin.py')
    add_code_block('config/urls.py', 'config/urls.py')
    add_code_block('materiales/migrations/0001_initial.py', 'materiales/migrations/0001_initial.py')

    story.append(Paragraph('Captura de código y estructura del proyecto', section_title))
    story.append(Paragraph(
        'A continuación se muestran bloques de código reales del proyecto, presentados con un estilo visual tipo captura de editor de texto, '
        'para facilitar la explicación técnica del CRUD de materiales y la estructura del sistema.', body
    ))
    story.append(Paragraph('1. Introducción', subtitle_style))
    story.append(Paragraph(
        'Este proyecto tuvo como objetivo desarrollar una aplicación web con Django para gestionar materiales de una repostería. '
        'Se implementó un CRUD funcional que permite visualizar, registrar, actualizar y eliminar materiales, manteniendo una estructura organizada '
        'y con validaciones necesarias para evitar errores en la entrada de datos.', body
    ))

    story.append(Paragraph('2. Objetivos', subtitle_style))
    story.append(Paragraph(
        '- Listar materiales mediante consultas ORM de Django.\n'
        '- Crear nuevos registros desde un formulario web.\n'
        '- Editar materiales ya existentes.\n'
        '- Eliminar materiales con confirmación.\n'
        '- Mantener validación de campos, control de errores 404 y protección CSRF.', body
    ))

    story.append(Paragraph('3. Requisitos funcionales', subtitle_style))
    story.append(Paragraph(
        'La aplicación debía incorporar CRUD completo, uso de get_object_or_404(), manejo adecuado de formularios, rutas específicas para cada operación '
        'y una vista de listado con acceso directo a cada acción. Además, se contempló validación para campos vacíos y valores inválidos.', body
    ))
    story.append(Paragraph('3.1 Lista específica del CRUD solicitado', subtitle_style))
    story.append(Paragraph(
        'En materiales/views.py se reemplazaron los datos escritos manualmente por consultas ORM y se implementaron las funciones para listar, crear, editar y eliminar materiales. '
        'Las funciones de edición y eliminación usan get_object_or_404() para registros inexistentes. materiales/urls.py define las rutas de listado, creación, edición y eliminación. '
        'La plantilla lista.html muestra los materiales y sus acciones; formulario.html sirve para crear y editar; eliminar.html confirma la acción y permite cancelarla. '
        'Los formularios incluyen {% csrf_token %} y la eliminación solo modifica datos mediante POST. '
        'Las pruebas comprueban listado, creación válida, campos vacíos, dato inválido, edición, cancelación, confirmación, 404 y CSRF. '
        'Las capturas de cada flujo aparecen en la sección 7.', body
    ))

    story.append(Paragraph('4. Desarrollo del sistema', subtitle_style))
    story.append(Paragraph(
        'El módulo de materiales se estructura con una app Django llamada materiales. Este módulo incluye un modelo que almacena los datos, un formulario '
        'de validación, las vistas de lógica y una serie de templates para mostrar la interfaz. El patrón seguido fue el típico de Django MVC, '
        'aprovechando el ORM para gestionar todas las operaciones contra la base de datos.', body
    ))

    story.append(Paragraph('4.1 Modelo de datos', subtitle_style))
    add_code_block('materiales/models.py', 'materiales/models.py')

    story.append(Paragraph('4.2 Formularios y validación', subtitle_style))
    add_code_block('materiales/forms.py', 'materiales/forms.py')

    story.append(Paragraph('4.3 Vistas del CRUD', subtitle_style))
    add_code_block('materiales/views.py', 'materiales/views.py')

    story.append(Paragraph('4.4 Rutas del sistema', subtitle_style))
    add_code_block('materiales/urls.py', 'materiales/urls.py')

    story.append(Paragraph('4.5 Templates', subtitle_style))
    story.append(Paragraph('Se crearon las plantillas para listar, crear, editar y confirmar eliminación.', body))
    add_code_block('materiales/templates/materiales/lista.html', 'materiales/templates/materiales/lista.html')
    add_code_block('materiales/templates/materiales/formulario.html', 'materiales/templates/materiales/formulario.html')
    add_code_block('materiales/templates/materiales/eliminar.html', 'materiales/templates/materiales/eliminar.html')

    story.append(Paragraph('5. Pruebas realizadas', subtitle_style))
    story.append(Paragraph(
        'Se ejecutaron pruebas para comprobar el correcto funcionamiento del sistema. Se validaron los casos de listado, creación, edición, '
        'cancelación de eliminación, confirmación, manejo de 404, validación de errores y seguridad CSRF.', body
    ))
    add_code_block('materiales/tests.py', 'materiales/tests.py')

    story.append(Paragraph('6. Resultados verificados', subtitle_style))
    test_result = subprocess.run(
        [sys.executable, 'manage.py', 'test', 'materiales', '--verbosity=2'],
        cwd=BASE,
        capture_output=True,
        text=True,
    )
    check_result = subprocess.run(
        [sys.executable, 'manage.py', 'check'],
        cwd=BASE,
        capture_output=True,
        text=True,
    )
    test_output = test_result.stdout + test_result.stderr
    test_lines = [
        line for line in test_output.splitlines()
        if line.startswith(('Found ', 'test_', 'Ran ', 'FAILED'))
        or line in {'OK'}
        or 'System check identified' in line
    ]
    check_output = check_result.stdout + check_result.stderr
    check_lines = [line for line in check_output.splitlines() if line.strip()]
    verification = (
        '$ python manage.py test materiales --verbosity=2\n'
        + '\n'.join(test_lines)
        + '\n\n$ python manage.py check\n'
        + '\n'.join(check_lines)
        + f'\n\nExit codes: tests={test_result.returncode}, check={check_result.returncode}'
    )
    screenshot = create_output_screenshot(verification, 'Resultados reales de pruebas')
    story.append(Paragraph('Verificación', file_tag))
    story.append(ReportImage(screenshot, width=170 * mm, height=115 * mm, kind='proportional'))

    story.append(Paragraph('7. Capturas de pruebas web', subtitle_style))
    story.append(Paragraph(
        'Las siguientes capturas se tomaron del sitio local durante las pruebas. El registro creado para las capturas fue temporal y se eliminó al terminar.', body
    ))
    evidence = [
        ('Listado con materiales de ejemplo', '_report_assets/listado_web.png'),
        ('Formulario para crear', '_report_assets/crear_web.png'),
        ('Validación de campos vacíos', '_report_assets/validacion_vacia_web.png'),
        ('Rechazo de stock y precio inválidos', '_report_assets/dato_invalido_web.png'),
        ('Registro creado', '_report_assets/creacion_web.png'),
        ('Formulario de edición precargado', '_report_assets/edicion_precargada_web.png'),
        ('Edición guardada', '_report_assets/edicion_guardada_web.png'),
        ('Confirmación de eliminación', '_report_assets/confirmar_eliminacion_web.png'),
        ('Cancelación: el registro permanece', '_report_assets/cancelar_eliminacion_web.png'),
        ('Eliminación confirmada: el registro ya no aparece', '_report_assets/eliminacion_confirmada_web.png'),
        ('Error 404 para identificador inexistente', '_report_assets/error_404_web.png'),
        ('403 al enviar el formulario sin token CSRF', '_report_assets/csrf_403_web.png'),
        ('Acceso de inicio de sesión a Django Admin', '_report_assets/admin_login_web.png'),
    ]
    for label, rel_path in evidence:
        add_evidence(label, rel_path)

    story.append(Paragraph('8. GitHub, uso de IA y reflexión', subtitle_style))
    story.append(Paragraph(
        'La rama publicada es entrega-materiales. El historial de Git debe revisarse para identificar las contribuciones reales de cada integrante; '
        'no se atribuyen commits individuales en este informe.', body
    ))
    story.append(Paragraph(
        '<b>Prompt del equipo:</b> “Trabajar principalmente en el CRUD web de materiales; reemplazar los materiales escritos manualmente por consultas ORM; '
        'crear funciones para listar, crear, editar y eliminar; usar get_object_or_404(); crear las rutas y plantillas; incorporar CSRF; ejecutar el borrado solo por POST; '
        'mantener la cancelación; probar listado, creación válida, campos vacíos, dato inválido, edición, cancelación, confirmación, 404 y CSRF; sacar capturas de las pruebas”. '
        '<b>Propuesta aplicada:</b> ModelForm, operaciones ORM, rutas con nombres, validación, confirmación POST y pruebas automatizadas. '
        '<b>Decisión:</b> aceptar los cambios después de revisar archivos y ejecutar pruebas; mantener PostgreSQL como requisito pendiente cuando no hay servidor local disponible. '
        '<b>Verificación:</b> diez pruebas automatizadas y manage.py check sin errores en SQLite; captura real de 403, 404 y flujos CRUD.', body
    ))
    story.append(Paragraph(
        '<b>Reflexión del equipo (completar con sus propias respuestas):</b><br/>'
        '¿Qué parte del CRUD fue más difícil y por qué? ______________________________________________<br/>'
        '¿Qué error permitió aprender algo importante? ______________________________________________<br/>'
        '¿Qué sugerencia de IA aceptaron, modificaron o rechazaron y por qué? __________________________<br/>'
        '¿Qué funcionalidad implementarán en la siguiente evaluación? _________________________________', body
    ))
    story.append(Paragraph(
        '<b>Pendiente antes de entregar:</b> configurar y demostrar PostgreSQL; ejecutar migrate y mostrar pgAdmin; crear superusuario y realizar '
        'las operaciones requeridas desde Admin; incorporar capturas de esas acciones; completar la reflexión y confirmar la distribución real de commits.', body
    ))

    story.append(Paragraph('9. Conclusión', subtitle_style))
    story.append(Paragraph(
        'El CRUD web y sus validaciones están implementados y verificados localmente. La configuración admite PostgreSQL y Django Admin; '
        'la evaluación completa depende de comprobar la conexión PostgreSQL y adjuntar la evidencia administrativa pendiente indicada arriba.', body
    ))

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
    )
    doc.build(story)
    print(f'PDF generado: {OUTPUT}')


if __name__ == '__main__':
    build_report()
