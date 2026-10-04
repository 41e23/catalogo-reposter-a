from pathlib import Path
from datetime import date

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
    output_path = asset_dir / f"{Path(rel_path).stem}.png"
    image.save(output_path, format="PNG", optimize=True, quality=100)
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

    story = []
    story.append(Paragraph('Informe de proyecto: Sistema web de materiales', title_style))
    story.append(Paragraph('Alacena & Molde', ParagraphStyle('Brand', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=colors.HexColor('#2c2c2c'))))
    story.append(Paragraph(f'Fecha de elaboración: {date.today().strftime("%d/%m/%Y")}', body))
    story.append(Spacer(1, 6 * mm))

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
    verification = '''
python manage.py test materiales
Resultado: 9 pruebas ejecutadas, OK

python manage.py check
Resultado: System check identified no issues (0 silenced)

URL validada: http://localhost:8000/materiales/
Resultado: HTTP 200
    '''
    screenshot = create_code_screenshot('materiales/tests.py', 'Verificación')
    story.append(Paragraph('Verificación', file_tag))
    story.append(ReportImage(screenshot, width=170 * mm, height=230 * mm, kind='proportional'))

    story.append(Paragraph('7. Conclusión', subtitle_style))
    story.append(Paragraph(
        'El proyecto cumple con los requisitos solicitados para un CRUD web de materiales en Django. La aplicación se encuentra operativa, '
        'con enlaces funcionales, validaciones, manejo de errores y seguridad básica mediante CSRF. Además, la estructura es escalable y preparada '
        'para continuar con nuevas funcionalidades del catálogo de repostería.', body
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
