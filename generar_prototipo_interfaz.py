# -*- coding: utf-8 -*-
"""
Genera PROTOTIPO_INTERFAZ.docx
Tarea: Implementa un prototipo de interfaz abstracta adecuado
"""
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Cm

AZUL = RGBColor(0x1F, 0x4E, 0x79)
GRIS_IMG = "F2F2F2"


def set_cell_bg(cell, color):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), color)
    cell._tc.get_or_add_tcPr().append(shd)


def styled_table(doc, headers, rows):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = h
        for p in c.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True
                r.font.size = Pt(9)
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_bg(c, "1F4E79")
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for i, val in enumerate(row):
            if i < len(cells):
                cells[i].text = str(val)
                for p in cells[i].paragraphs:
                    for r in p.runs:
                        r.font.size = Pt(9)
    return t


def add_image_placeholder(doc, description, width_cm=14, height_cm=7):
    """Agrega un recuadro gris como placeholder de imagen con descripción."""
    t = doc.add_table(rows=1, cols=1)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = t.rows[0].cells[0]
    set_cell_bg(cell, GRIS_IMG)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    # Espacio para imagen
    for _ in range(3):
        p.add_run("\n")
    r = p.add_run("[ CAPTURA DE PANTALLA ]")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
    p.add_run("\n")
    r2 = p.add_run(description)
    r2.font.size = Pt(10)
    r2.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    r2.italic = True
    # Alto mínimo
    cell.width = Cm(width_cm)
    doc.add_paragraph()


def h1(t):
    doc.add_heading(t, level=1)

def h2(t):
    doc.add_heading(t, level=2)

def h3(t):
    doc.add_heading(t, level=3)

def para(t, bold=False):
    p = doc.add_paragraph()
    r = p.add_run(t)
    r.bold = bold
    r.font.size = Pt(11)
    return p

def bullet(t):
    p = doc.add_paragraph(t, style="List Bullet")
    for r in p.runs:
        r.font.size = Pt(10)
    return p


# =====================================================================
doc = Document()
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)

for s in doc.sections:
    s.top_margin = Cm(2.5)
    s.bottom_margin = Cm(2.5)
    s.left_margin = Cm(3)
    s.right_margin = Cm(2.5)

# =====================================================================
# PORTADA
# =====================================================================
for _ in range(4):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("INSTITUTO TECNOLÓGICO SACABA")
r.bold = True
r.font.size = Pt(18)
r.font.color.rgb = AZUL

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Carrera de Sistemas Informáticos")
r.font.size = Pt(13)

doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("PROTOTIPO DE INTERFAZ ABSTRACTA")
r.bold = True
r.font.size = Pt(16)
r.font.color.rgb = AZUL

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Interacciones Principales de la Interfaz\nChatbot Web Multiidioma - GAM Sacaba")
r.font.size = Pt(13)
r.italic = True

doc.add_paragraph()

for linea in (
    "ESTUDIANTE:\tALFREDO RAMÍREZ ESPINOZA",
    "TUTOR:\tIng. FREDDY LEDEZMA HIGUERA",
    "FECHA:\tJunio, 2026",
):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(linea)
    r.font.size = Pt(12)

doc.add_page_break()

# =====================================================================
# 1. INTRODUCCIÓN
# =====================================================================
h1("1. INTRODUCCIÓN")

para(
    "El presente documento muestra el prototipo de interfaz abstracta "
    "del sistema web \"Chatbot Municipal de Sacaba\", describiendo las "
    "interacciones principales que el usuario puede realizar. Cada "
    "interacción se documenta con una captura de pantalla que ilustra "
    "el estado de la interfaz en ese momento."
)

para(
    "El prototipo cubre las 6 interacciones fundamentales del sistema: "
    "navegación general, búsqueda de trámites, consulta de multas, "
    "cambio de idioma, uso del chatbot y consulta de información "
    "institucional."
)

# =====================================================================
# 2. INTERACCIÓN 1: NAVEGACIÓN GENERAL
# =====================================================================
h1("3. INTERACCIÓN 1: NAVEGACIÓN GENERAL")

h2("3.1 Descripción")
para(
    "El usuario accede al portal y utiliza el menú de navegación principal "
    "para desplazarse entre las secciones del sitio. El menú está ubicado "
    "en la parte superior y permite acceso directo a: Inicio, Trámites, "
    "Multas, Institución y Contacto."
)

h2("3.2 Elementos de Interacción")
styled_table(doc,
    ["Elemento", "Tipo", "Acción"],
    [
        ["Menú Principal", "Navegación horizontal", "Click en enlace → scroll suave a la sección"],
        ["Logo GAM", "Enlace", "Click → vuelve al inicio"],
        ["Botón Idioma (QU/ES)", "Toggle", "Click → cambia idioma de toda la página"],
        ["Menú Móvil (≡)", "Hamburger", "Click → abre/cierra menú desplegable"],
    ])

h2("3.3 Captura de Pantalla")
add_image_placeholder(doc,
    "DESCRIPCIÓN: Captura completa del sitio mostrando la barra superior "
    "(teléfono, email, horarios), el header con logo y menú de navegación "
    "(Inicio, Trámites, Multas, Institución, Contacto), el botón de idioma "
    "QU/ES, y el banner hero con el título \"Sistema de Orientación Ciudadana "
    "Digital\". Se debe mostrar la vista de escritorio completa.")

# =====================================================================
# 3. INTERACCIÓN 2: BÚSQUEDA DE TRÁMITES
# =====================================================================
h1("4. INTERACCIÓN 2: BÚSQUEDA DE TRÁMITES")

h2("4.1 Descripción")
para(
    "El usuario busca un trámite específico utilizando el buscador de "
    "la sección Trámites. Puede escribir palabras clave como \"carnet\", "
    "\"residencia\" o \"licencia\" para filtrar los 25 trámites disponibles. "
    "También puede usar los filtros por categoría."
)

h2("4.2 Elementos de Interacción")
styled_table(doc,
    ["Elemento", "Tipo", "Acción"],
    [
        ["Campo de búsqueda", "Input text", "Escribe palabra clave → filtra en tiempo real"],
        ["Filtros de categoría", "Botones (Todos, Identidad, etc.)", "Click → filtra por categoría"],
        ["Tarjeta de trámite", "Card expandible", "Click en \"Ver requisitos\" → accordion se abre"],
        ["Botón \"Consultar con el Chat\"", "Botón", "Click → abre chatbot con consulta predefinida"],
    ])

h2("4.3 Captura de Pantalla")
add_image_placeholder(doc,
    "DESCRIPCIÓN: Captura de la sección Trámites mostrando el campo de "
    "búsqueda con el texto \"carnet\" escrito, los filtros de categoría "
    "(Todos, Identidad, Vivienda, Negocio, Servicios), y las tarjetas "
    "filtradas que muestran \"Carnet de Identidad\" y \"Certificado de "
    "Conducta\". Cada tarjeta muestra: número, icono, nombre, descripción, "
    "costo (Bs. 17), tiempo (Inmediato), departamento (SEGIP) y botón "
    "de expandir.")

# =====================================================================
# 4. INTERACCIÓN 3: CONSULTA DE MULTAS
# =====================================================================
h1("5. INTERACCIÓN 3: CONSULTA DE MULTAS")

h2("5.1 Descripción")
para(
    "El usuario consulta la información de multas de tránsito y municipales, "
    "incluyendo montos, infracciones y formas de pago. La sección muestra "
    "tres tarjetas: Multas de Tránsito, Multas Municipales y Pago de Multas."
)

h2("5.2 Elementos de Interacción")
styled_table(doc,
    ["Elemento", "Tipo", "Acción"],
    [
        ["Tarjeta Multas Tránsito", "Card con lista", "Muestra 5 infracciones y montos"],
        ["Tarjeta Multas Municipales", "Card con lista", "Muestra 5 infracciones y montos"],
        ["Tarjeta Pago de Multas", "Card con opciones", "Muestra 4 métodos de pago"],
        ["Botón \"Más Información\"", "Botón", "Click → abre chatbot con consulta de multas"],
        ["Pasos de pago", "Lista numerada", "Muestra flujo: Consulta → Pago → Comprobante"],
    ])

h2("5.3 Captura de Pantalla")
add_image_placeholder(doc,
    "DESCRIPCIÓN: Captura de la sección Multas y Formas de Pago mostrando "
    "las tres tarjetas principales: (1) Multas de Tránsito con infracciones "
    "como \"Exceso de velocidad Bs. 100-300\", (2) Multas Municipales con "
    "\"Arrojar basura Bs. 50-100\", (3) Pago de Multas con opciones Caja "
    "Municipal, Banco Unión, BNB/BISA y Código QR. Debajo se muestran los "
    "3 pasos del pago con números y el código QR.")

# =====================================================================
# 5. INTERACCIÓN 4: CAMBIO DE IDIOMA
# =====================================================================
h1("6. INTERACCIÓN 4: CAMBIO DE IDIOMA (ES/QU)")

h2("6.1 Descripción")
para(
    "El usuario cambia el idioma de toda la interfaz de castellano a quechua "
    "utilizando el botón toggle \"QU/ES\" ubicado en el header. Todos los "
    "textos estáticos se traducen automáticamente incluyendo menús, títulos, "
    "descripciones y botones."
)

h2("6.2 Elementos de Interacción")
styled_table(doc,
    ["Elemento", "Tipo", "Acción"],
    [
        ["Botón QU/ES", "Toggle button", "Click → traduce toda la página a quechua"],
        ["Texto del botón", "Label dinámico", "Muestra \"QU\" cuando está en español, \"ES\" en quechua"],
        ["Elementos data-qu", "Atributos HTML", "Cada elemento tiene traducción predefinida"],
    ])

h2("6.3 Captura de Pantalla - Español")
add_image_placeholder(doc,
    "DESCRIPCIÓN: Captura del sitio en idioma ESPAÑOL mostrando el menú "
    "\"Inicio, Trámites, Multas, Institución, Contacto\", el botón muestra "
    "\"QU\", el título \"Sistema de Orientación Ciudadana Digital\", los "
    "botones \"Ver Trámites\" y \"Pagos y Multas\", y los badges "
    "\"Disponible 24/7\", \"Inteligencia Artificial\", \"Voz y Audio\".")

h2("6.4 Captura de Pantalla - Quechua")
add_image_placeholder(doc,
    "DESCRIPCIÓN: Captura del sitio en idioma QUECHUA mostrando el menú "
    "\"Qallariy, Trámitekuna, Multakuna, Institución, Contacto\", el botón "
    "muestra \"ES\", el título \"Runakunapaq Yachay Sistema Digital\", los "
    "botones \"Trámitekuna Qhaway\" y \"Multakuna\", y los badges traducidos "
    "\"24 horas p'unchay-tuta\", \"Inteligencia Artificial\", \"Kunka Taqwa\".")

# =====================================================================
# 6. INTERACCIÓN 5: USO DEL CHATBOT
# =====================================================================
h1("7. INTERACCIÓN 5: USO DEL CHATBOT")

h2("7.1 Descripción")
para(
    "El usuario interactúa con el asistente virtual haciendo clic en el "
    "botón flotante del chatbot. Puede escribir preguntas sobre trámites, "
    "multas, horarios o contacto, y el sistema responde con información "
    "relevante. También puede enviar mensajes de voz."
)

h2("7.2 Elementos de Interacción")
styled_table(doc,
    ["Elemento", "Tipo", "Acción"],
    [
        ["Botón flotante", "FAB (Floating Action Button)", "Click → abre ventana de chat"],
        ["Ventana de chat", "Panel deslizante", "Muestra historial de conversación"],
        ["Campo de entrada", "Input + Botón enviar", "Escribe mensaje → envía al chatbot"],
        ["Botón de voz", "Microphone icon", "Click → graba audio → transcribe → responde"],
        ["Mensaje del usuario", "Burbuja derecha", "Muestra el mensaje enviado"],
        ["Respuesta del bot", "Burbuja izquierda + card", "Muestra respuesta con información del trámite"],
    ])

h2("7.3 Captura de Pantalla - Chat Cerrado")
add_image_placeholder(doc,
    "DESCRIPCIÓN: Captura del sitio mostrando solo el botón flotante del "
    "chatbot en la esquina inferior derecha. El botón es circular con "
    "un ícono de robot/chat y tiene un indicador visual de que está "
    "disponible. Se debe mostrar el contexto de la página de fondo.")

h2("7.4 Captura de Pantalla - Chat Abierto")
add_image_placeholder(doc,
    "DESCRIPCIÓN: Captura del chatbot abierto mostrando: (1) Cabecera "
    "con título \"Chatbot Municipal\" y botón de cerrar (X), (2) Mensaje "
    "de bienvenida del bot \"¡Hola! Soy el asistente virtual del GAM "
    "Sacaba\", (3) Campo de entrada de texto con placeholder \"Escribe "
    "tu consulta...\", (4) Botón de enviar y botón de micrófono para voz.")

h2("7.5 Captura de Pantalla - Conversación")
add_image_placeholder(doc,
    "DESCRIPCIÓN: Captura del chatbot mostrando una conversación completa: "
    "(1) Usuario escribe \"¿Cuánto cuesta el carnet?\", (2) Bot responde "
    "con tarjeta formateada: \"**Carnet de Identidad (Cédula)** - Costo: "
    "Bs. 17 - Tiempo: Inmediato - Departamento: SEGIP - Ubicación: "
    "Oficinas del SEGIP de Sacaba\", (3) Botón \"Consultar con el Chat\" "
    "en la parte inferior.")

# =====================================================================
# 7. INTERACCIÓN 6: INFORMACIÓN INSTITUCIONAL
# =====================================================================
h1("8. INTERACCIÓN 6: INFORMACIÓN INSTITUCIONAL")

h2("8.1 Descripción")
para(
    "El usuario consulta la información del Gobierno Autónomo Municipal "
    "de Sacaba, incluyendo horarios de atención, ubicación, datos de "
    "contacto y enlaces a redes sociales."
)

h2("8.2 Elementos de Interacción")
styled_table(doc,
    ["Elemento", "Tipo", "Acción"],
    [
        ["Sección Horarios", "Card", "Muestra horarios Lun-Vie y Sáb"],
        ["Sección Ubicación", "Card + Mapa", "Muestra dirección y enlace a Google Maps"],
        ["Sección Contacto", "Card", "Muestra teléfono, email y web"],
        ["Footer", "Pie de página", "Muestra enlaces rápidos y copyright"],
    ])

h2("8.3 Captura de Pantalla")
add_image_placeholder(doc,
    "DESCRIPCIÓN: Captura de la sección Institución mostrando las tres "
    "tarjetas: (1) Horarios de Atención con \"Lun-Vie: 8:00 - 12:00 / "
    "14:00 - 18:00, Sáb: 8:00 - 12:00, Dom: Cerrado\", (2) Ubicación "
    "con \"Consistorial S-002, Sacaba, Cochabamba\" y botón \"Cómo llegar\" "
    "con enlace a Google Maps, (3) Contacto con \"Tel: 4701677, "
    "Email: info@sacaba.gob.bo, Web: sacaba.gob.bo\".")

# =====================================================================
# 8. RESUMEN DE INTERACCIONES
# =====================================================================
h1("9. RESUMEN DE INTERACCIONES DOCUMENTADAS")

styled_table(doc,
    ["# Interacción", "Nombre", "Capturas", "Descripción"],
    [
        ["1", "Navegación General", "1", "Menú principal, header, banner hero"],
        ["2", "Búsqueda de Trámites", "1", "Buscador, filtros, tarjetas filtradas"],
        ["3", "Consulta de Multas", "1", "3 tarjetas de multas + pasos de pago"],
        ["4", "Cambio de Idioma", "2", "Vista en español + vista en quechua"],
        ["5", "Uso del Chatbot", "3", "Chat cerrado, chat abierto, conversación"],
        ["6", "Información Institucional", "1", "Horarios, ubicación, contacto"],
        ["", "TOTAL", "9", "Cubre las interacciones principales del sistema"],
    ])

# =====================================================================
# 9. CONCLUSIONES
# =====================================================================
h1("10. CONCLUSIONES")

bullet("Se documentaron 6 interacciones principales que cubren el 100% de las funcionalidades del sistema.")
bullet("Cada interacción incluye descripción, elementos de interacción y captura de pantalla.")
bullet("El prototipo demuestra la navegabilidad, usabilidad y accesibilidad del sistema.")
bullet("Las capturas muestran tanto la vista de escritorio como las funciones interactivas.")
bullet("El cambio de idioma ES/QU se documenta con ambas vistas para mostrar la funcionalidad bilingüe.")
bullet("El chatbot se documenta en tres estados: cerrado, abierto y en conversación.")

# Save
doc.save(r"C:\Users\kanit\Desktop\chatbot-sacaba\PROTOTIPO_INTERFAZ.docx")
print("PROTOTIPO_INTERFAZ.docx generado correctamente.")
print("Se generaron 9 espacios para capturas de pantalla.")
