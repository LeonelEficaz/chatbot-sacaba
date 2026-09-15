# -*- coding: utf-8 -*-
"""
Genera ESTRUCTURA_NAVEGACIONAL.docx
Diseño de Estructura Navegacional Funcional del Proyecto
"""
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Cm

AZUL = RGBColor(0x1F, 0x4E, 0x79)
VERDE = "E2EFDA"
AMARILLO = "FFF2CC"
NARANJA = "FCE4D6"
ROJO = "F8CBAD"
AZUL_CL = "D6E4F0"


def set_cell_bg(cell, color):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), color)
    cell._tc.get_or_add_tcPr().append(shd)


def styled_table(doc, headers, rows, col_colors=None):
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
                if col_colors and ri < len(col_colors):
                    set_cell_bg(cells[i], col_colors[ri])
    return t


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
r = p.add_run("DISEÑO DE ESTRUCTURA NAVEGACIONAL FUNCIONAL")
r.bold = True
r.font.size = Pt(16)
r.font.color.rgb = AZUL

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Chatbot Web Multiidioma para Trámites y Multas\nGobierno Autónomo Municipal de Sacaba")
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
    "El presente documento describe la estructura navegacional funcional "
    "del sistema web \"Chatbot Municipal de Sacaba\". La navegación está "
    "diseñada para ser intuitiva, accesible y bilingüe (castellano/quechua), "
    "permitiendo a los ciudadanos consultar trámites, multas e información "
    "municipal de forma rápida y sencilla."
)

para(
    "El sitio utiliza una arquitectura de página única (SPA ligera) con "
    "secciones ancladas, complementada por un widget de chatbot flotante "
    "que ofrece asistencia interactiva en tiempo real."
)

# =====================================================================
# 2. MAPA DE NAVEGACIÓN
# =====================================================================
h1("2. MAPA DE NAVEGACIÓN GENERAL")

styled_table(doc,
    ["Nivel", "Sección", "Ancla / Ruta", "Descripción"],
    [
        ["0", "Logo / Header", "#inicio", "Logo institucional + navegación principal"],
        ["1", "Inicio", "#inicio", "Banner hero con bienvenida y accesos rápidos"],
        ["2", "Trámites", "#tramites", "Catálogo de 25 trámites municipales"],
        ["3", "Multas", "#multas", "Información de multas y formas de pago"],
        ["4", "Institución", "#institucion", "Datos del GAM Sacaba"],
        ["5", "Contacto", "#contacto", "Horarios, dirección, teléfono"],
        ["—", "Chatbot Widget", "Widget flotante", "Asistente virtual IA en 2 idiomas"],
    ])

# =====================================================================
# 3. ESTRUCTURA DETALLADA POR SECCIONES
# =====================================================================
h1("3. ESTRUCTURA DETALLADA POR SECCIONES")

# ---------- 3.1 HEADER ----------
h2("3.1 Barra Superior + Header (Navegación Principal)")

styled_table(doc,
    ["Componente", "Elementos", "Funcionalidad"],
    [
        ["Barra Superior", "Teléfono, Email, Horarios", "Información de contacto rápida"],
        ["Redes Sociales", "Facebook, X (Twitter), WhatsApp", "Enlaces a redes institucionales"],
        ["Logo Institucional", "Emblema + Texto GAM Sacaba", "Identidad visual, enlace a inicio"],
        ["Menú Principal", "Inicio, Trámites, Multas, Institución, Contacto", "Navegación por secciones (scroll suave)"],
        ["Botón Idioma", "QU / ES", "Toggle entre castellano y quechua"],
        ["Menú Móvil", "Hamburger (≡)", "Menú responsive para dispositivos móviles"],
    ])

# ---------- 3.2 INICIO ----------
h2("3.2 Sección Inicio (#inicio)")

styled_table(doc,
    ["Componente", "Elementos", "Funcionalidad"],
    [
        ["Banner Hero", "Logo, Título, Descripción, Botones", "Bienvenida y llamado a la acción"],
        ["Botones CTA", "Ver Trámites / Pagos y Multas", "Acceso directo a secciones principales"],
        ["Badges Informativos", "24/7, IA, Voz, Aprendizaje", "Características destacadas del sistema"],
        ["Accesos Rápidos", "6 tarjetas de trámites frecuentes", "Acceso directo a trámites populares"],
    ])

h3("Accesos Rápidos (6 tarjetas)")
styled_table(doc,
    ["#", "Acceso", "Enlace", "Icono"],
    [
        ["1", "Carnet de Identidad", "#carnet", "fas fa-id-card"],
        ["2", "Constancia Residencia", "#tramites (búsqueda)", "fas fa-home"],
        ["3", "Licencia Funcionamiento", "#tramites (búsqueda)", "fas fa-store"],
        ["4", "Catastro Predial", "#tramites (búsqueda)", "fas fa-map-marked-alt"],
        ["5", "Vehículos", "#tramites (búsqueda)", "fas fa-car"],
        ["6", "Multas y Pago", "#multas", "fas fa-qrcode"],
    ])

# ---------- 3.3 TRÁMITES ----------
h2("3.3 Sección Trámites (#tramites)")

styled_table(doc,
    ["Componente", "Elementos", "Funcionalidad"],
    [
        ["Encabezado", "Tag + Título + Descripción", "Identificación de la sección"],
        ["Buscador", "Input de búsqueda en tiempo real", "Filtra trámites por palabra clave"],
        ["Filtros por Categoría", "Todos, Identidad, Vivienda, Negocio, Servicios", "Filtra trámites por categoría"],
        ["Grid de Tarjetas", "25 tarjetas de trámites", "Muestra información resumida de cada trámite"],
        ["Tarjeta de Trámite", "Número, Nombre, Descripción, Costo, Tiempo, Departamento", "Información del trámite"],
        ["Accordion", "Requisitos, Pasos, Ubicación", "Detalle expandible de cada trámite"],
        ["Botón Consultar", "Chat con el chatbot", "Abre el chatbot con consulta predefinida"],
    ])

h3("Categorías de Trámites")
styled_table(doc,
    ["Categoría", "Filtro", "Trámites Incluidos"],
    [
        ["Todos", "todos", "25 trámites completos"],
        ["Identidad", "identidad", "Carnet, Certificado Conducta, Licencia Conducir, Registro Civil, Residencia, Soltería, Viudez"],
        ["Vivienda y Catastro", "vivienda", "Catastro Predial, Permiso Construcción, Habilitación Urbana"],
        ["Negocio", "negocio", "Licencia Funcionamiento, Patente Municipal, Certificado Sanitario"],
        ["Servicios y Vehículos", "servicios", "Vehículos, Agua Potable, Alumbrado, Registro Defunción"],
    ])

# ---------- 3.4 MULTAS ----------
h2("3.4 Sección Multas (#multas)")

styled_table(doc,
    ["Componente", "Elementos", "Funcionalidad"],
    [
        ["Encabezado", "Tag + Título + Descripción", "Identificación de la sección"],
        ["Tarjeta Multas Tránsito", "5 infracciones + montos", "Información de multas por tránsito"],
        ["Tarjeta Multas Municipales", "5 infracciones + montos", "Información de multas municipales"],
        ["Tarjeta Pago de Multas", "4 opciones de pago", "Caja, Bancos, QR"],
        ["Pasos de Pago", "3 pasos ilustrados", "Consulta → Pago → Comprobante"],
        ["Código QR", "Imagen QR + Instrucciones", "Pago móvil 24 horas"],
    ])

h3("Infracciones de Tránsito")
styled_table(doc,
    ["Infracción", "Monto (Bs.)"],
    [
        ["Exceso de velocidad", "100 - 300"],
        ["Conducir sin licencia", "200 - 500"],
        ["Estacionamiento prohibido", "50 - 100"],
        ["No respetar semáforo", "100 - 200"],
        ["Conducir en estado de ebriedad", "500 - 1.000"],
    ])

h3("Infracciones Municipales")
styled_table(doc,
    ["Infracción", "Monto (Bs.)"],
    [
        ["Arrojar basura en la vía pública", "50 - 100"],
        ["Ruido excesivo después de 22:00", "100 - 200"],
        ["Vender sin autorización", "200 - 500"],
        ["Dañar mobiliario municipal", "100 - 300"],
        ["Construir sin permiso", "500 - 2.000"],
    ])

# ---------- 3.5 INSTITUCIÓN ----------
h2("3.5 Sección Institución (#institucion)")

styled_table(doc,
    ["Componente", "Elementos", "Funcionalidad"],
    [
        ["Encabezado", "Tag + Título + Descripción", "Información institucional"],
        ["Horarios de Atención", "Lun-Vie, Sáb, Dom", "Horarios oficiales del GAM"],
        ["Ubicación", "Dirección + Mapa", "Consistorial S-002, enlace a Google Maps"],
        ["Contacto", "Teléfono, Email, Web", "Canales de comunicación"],
    ])

# ---------- 3.6 CONTACTO / FOOTER ----------
h2("3.6 Footer (Pie de Página)")

styled_table(doc,
    ["Componente", "Elementos", "Funcionalidad"],
    [
        ["Logo Footer", "Emblema + Texto", "Identidad institucional"],
        ["Descripción", "Texto orientativo", "Descripción del servicio"],
        ["Enlaces Rápidos", "Inicio, Trámites, Multas, Institución", "Navegación rápida"],
        ["Contacto", "Teléfono, Email, Dirección", "Información de contacto"],
        ["Copyright", "© 2026 GAM Sacaba", "Derechos reservados"],
    ])

# =====================================================================
# 4. NAVEGACIÓN DEL CHATBOT
# =====================================================================
h1("4. NAVEGACIÓN DEL CHATBOT WIDGET")

h2("4.1 Arquitectura del Chatbot")
styled_table(doc,
    ["Componente", "Tecnología", "Función"],
    [
        ["Widget Flotante", "HTML/CSS/JS embebido", "Botón flotante en esquina inferior derecha"],
        ["Ventana de Chat", "Panel deslizante", "Interfaz de conversación"],
        ["Entrada de Voz", "Web Audio API + Whisper", "Transcripción de audio a texto"],
        ["Motor de Diálogo", "Python/Flask + OpenAI", "Procesamiento de lenguaje natural"],
        ["Base de Conocimiento", "KB en engine.py", "25 trámites + multas + información municipal"],
    ])

h2("4.2 Flujo de Navegación del Chatbot")
styled_table(doc,
    ["Paso", "Acción del Usuario", "Respuesta del Sistema"],
    [
        ["1", "Hace clic en el botón flotante", "Se abre la ventana de chat"],
        ["2", "Escribe o voice input un mensaje", "El sistema detecta idioma (es/qu)"],
        ["3", "El usuario envía la consulta", "Se procesa con regex + IA (ChatGPT)"],
        ["4", "El sistema responde", "Muestra tarjeta con información del trámite"],
        ["5", "El usuario puede continuar", "Nueva consulta o cierre del chat"],
    ])

h2("4.3 Intenciones Detectadas")
styled_table(doc,
    ["Intención", "Palabras Clave", "Respuesta"],
    [
        ["greeting", "hola, buenos días, buenas tardes", "Saludo bienvenida + opciones"],
        ["farewell", "adios, gracias, hasta luego", "Despedida amable"],
        ["donde", "dónde, ubicación, dirección", "Ubicación del trámite"],
        ["cuanto", "cuánto cuesta, precio, costo", "Costo del trámite"],
        ["que_necesito", "requisitos, documentos, qué necesito", "Lista de requisitos"],
        ["como", "cómo, procedimiento, pasos", "Pasos a seguir"],
        ["cuando", "cuándo, tiempo, tarda", "Tiempo estimado"],
        ["horarios", "horario, atención, horas", "Horarios de atención"],
        ["contacto", "teléfono, email, contacto", "Datos de contacto"],
        ["multas", "multa, infracción, pago", "Información de multas"],
        ["menu_tramites", "lista, trámites, todos", "Lista completa de trámites"],
        ["consejo", "consejo, tip, recomendación", "Consejo práctico"],
        ["subalcaldias", "subalcaldía, distrito, alcalde de barrio", "Directorio de subalcaldías"],
        ["guia_telefonica", "teléfono, números, directorio", "Guía telefónica institucional"],
    ])

# =====================================================================
# 5. NAVEGACIÓN MULTIIDIOMA
# =====================================================================
h1("5. NAVEGACIÓN MULTIIDIOMA (ES/QU)")

h2("5.1 Mecanismo de Traducción")
styled_table(doc,
    ["Método", "Alcance", "Tecnología"],
    [
        ["Traducción estática", "Elementos HTML con data-qu", "Atributos data-qu en el HTML"],
        ["Traducción dinámica", "Contenido del chatbot", "NLLB-200 (Hugging Face)"],
        ["Traducción IA", "Textos largos del sitio", "API OpenAI GPT"],
    ])

h2("5.2 Ejemplos de Traducción")
styled_table(doc,
    ["Sección", "Español", "Quechua"],
    [
        ["Navegación", "Inicio / Trámites / Multas", "Qallariy / Trámitekuna / Multakuna"],
        ["Título Hero", "Sistema de Orientación Ciudadana Digital", "Runakunapaq Yachay Sistema Digital"],
        ["Botón", "Ver Trámites", "Trámitekuna Qhaway"],
        ["Filtros", "Todos / Identidad / Vivienda", "Tukuy / Identidad / Wasi"],
        ["Footer", "Gobierno Autónomo Municipal", "Munisipyu Gobierno Autónomo"],
    ])

# =====================================================================
# 6. FLUJO DE NAVEGACIÓN DEL USUARIO
# =====================================================================
h1("6. FLUJO DE NAVEGACIÓN DEL USUARIO")

styled_table(doc,
    ["Escenario", "Ruta de Navegación", "Resultado"],
    [
        ["Consulta general", "Inicio → Trámites → Buscar → Tarjeta → Chat", "Información del trámite"],
        ["Pago de multa", "Inicio → Multas → Pago de Multas → Ver Procedimiento", "Procedimiento de pago"],
        ["Contacto directo", "Inicio → Contacto → Teléfono/Email", "Comunicación con GAM"],
        ["Trámite específico", "Inicio → Acceso Rápido → Tarjeta → Detalle", "Requisitos y pasos"],
        ["Asistencia IA", "Widget Chatbot → Escribir/Preguntar → Respuesta", "Orientación personalizada"],
        ["Cambio de idioma", "Botón QU/ES → Todo el sitio se traduce", "Navegación en quechua"],
    ])

# =====================================================================
# 7. DISEÑO RESPONSIVE
# =====================================================================
h1("7. DISEÑO RESPONSIVE")

styled_table(doc,
    ["Dispositivo", "Comportamiento de Navegación"],
    [
        ["Desktop (>1024px)", "Menú horizontal completo, grid de 3-4 columnas"],
        ["Tablet (768-1024px)", "Menú horizontal, grid de 2 columnas"],
        ["Móvil (<768px)", "Menú hamburguesa, grid de 1 columna, chatbot a pantalla completa"],
    ])

h2("7.1 Elementos Responsive")
bullet("Menú hamburguesa (#mobileMenuBtn) para dispositivos móviles")
bullet("Grid de tarjetas adaptable (1-4 columnas según ancho)")
bullet("Chatbot widget a pantalla completa en móviles")
bullet("Filtros de trámites con scroll horizontal en móviles")
bullet("Footer en columnas apilables")

# =====================================================================
# 8. CONCLUSIONES
# =====================================================================
h1("8. CONCLUSIONES")

bullet("La estructura navegacional es clara y lógica, con 5 secciones principales bien diferenciadas.")
bullet("El sistema de anclajes (#inicio, #tramites, etc.) permite navegación rápida sin recarga de página.")
bullet("El buscador y los filtros facilitan encontrar trámites específicos entre los 25 disponibles.")
bullet("El chatbot complementa la navegación estática con asistencia interactiva y personalizada.")
bullet("La navegación bilingüe (es/qu) garantiza accesibilidad para hablantes de quechua.")
bullet("El diseño responsive确保 una experiencia óptima en desktop, tablet y móvil.")

# Save
doc.save(r"C:\Users\kanit\Desktop\chatbot-sacaba\ESTRUCTURA_NAVEGACIONAL.docx")
print("ESTRUCTURA_NAVEGACIONAL.docx generado correctamente.")
