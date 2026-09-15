# -*- coding: utf-8 -*-
"""
Genera CAPITULO_III_INGENIERIA.docx - Versión final con 6 imágenes
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


def add_image_placeholder(doc, fig_num, description):
    t = doc.add_table(rows=1, cols=1)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = t.rows[0].cells[0]
    set_cell_bg(cell, GRIS_IMG)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for _ in range(2):
        p.add_run("\n")
    r = p.add_run(f"[ {fig_num} ]")
    r.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
    p.add_run("\n")
    r2 = p.add_run(description)
    r2.font.size = Pt(9)
    r2.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    r2.italic = True
    doc.add_paragraph()


def h1(t):
    doc.add_heading(t, level=1)

def h2(t):
    doc.add_heading(t, level=2)

def h3(t):
    doc.add_heading(t, level=3)

def h4(t):
    doc.add_heading(t, level=4)

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
for _ in range(6):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("CAPÍTULO III")
r.bold = True
r.font.size = Pt(24)
r.font.color.rgb = AZUL

doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("INGENIERÍA DEL PROYECTO")
r.bold = True
r.font.size = Pt(18)
r.font.color.rgb = AZUL

doc.add_page_break()

# =====================================================================
# 3.1 REQUERIMIENTOS
# =====================================================================
h1("3.1 REQUERIMIENTOS GENERALES DEL SISTEMA")

h2("3.1.1 Requerimientos Funcionales")

styled_table(doc,
    ["ID", "Requerimiento", "Descripción"],
    [
        ["RF-01", "Consulta de trámites", "Consultar 25 trámites con requisitos, costos y procedimientos"],
        ["RF-02", "Consulta de multas", "Información de multas de tránsito y municipales"],
        ["RF-03", "Chatbot interactivo", "Asistente virtual con respuestas predeterminadas"],
        ["RF-04", "Soporte bilingüe", "Interfaz en castellano y quechua"],
        ["RF-05", "Búsqueda de trámites", "Buscador por palabra clave y filtros"],
        ["RF-06", "Navegación por secciones", "Menú: Inicio, Trámites, Multas, Institución, Contacto"],
        ["RF-07", "Entrada de voz", "Mensajes de voz transcritos por IA"],
        ["RF-08", "Traducción con IA", "Traducción automática de la interfaz"],
        ["RF-09", "Info institucional", "Horarios, ubicación y contacto del GAM"],
        ["RF-10", "Accesos rápidos", "Accesos directos a trámites frecuentes"],
    ])

h2("3.1.2 Requerimientos No Funcionales")

styled_table(doc,
    ["ID", "Requerimiento", "Descripción"],
    [
        ["RNF-01", "Disponibilidad", "24 horas, 7 días a la semana"],
        ["RNF-02", "Tiempo de respuesta", "Menos de 3 segundos"],
        ["RNF-03", "Compatibilidad", "Chrome, Firefox, Safari, Edge"],
        ["RNF-04", "Responsivo", "320px a 1920px de ancho"],
        ["RNF-05", "Usabilidad", "Interfaz intuitiva sin instrucciones"],
        ["RNF-06", "Escalabilidad", "Agregar trámites sin modificar código"],
    ])

h2("3.1.3 Actores del Sistema")

styled_table(doc,
    ["Actor", "Tipo", "Descripción"],
    [
        ["Ciudadano", "Principal", "Consulta trámites, multas, usa chatbot"],
        ["Chatbot", "Sistema", "Responde consultas con IA"],
        ["Administrador", "Secundario", "Actualiza base de conocimientos"],
    ])

# IMAGEN 1: Diagrama de Casos de Uso
add_image_placeholder(doc,
    "Figura 1: Diagrama de Casos de Uso General",
    "Diagrama UML con el Ciudadano conectado a: Consultar Trámite, "
    "Buscar Trámite, Filtrar por Categoría, Consultar Multas, "
    "Usar Chatbot, Enviar Voz, Cambiar Idioma, Consultar Institución. "
    "El Administrador conectado a Actualizar KB. "
    "Archivo: diagramas_staruml/01_casos_de_uso.mdj")

h2("3.1.4 Diagrama de Clases")

styled_table(doc,
    ["Clase", "Atributos Principales", "Métodos Principales"],
    [
        ["Chatbot", "KB, UI, MULTAS, _client", "get_resp(), detect_intent(), detect_tramite()"],
        ["Tramite", "id, nombre, costo, tiempo", "get_info_es(), get_info_qu()"],
        ["Multa", "tipo, infracciones, montos", "get_info_transito(), get_info_municipal()"],
        ["App Flask", "app, routes", "index(), chat(), translate()"],
        ["Widget", "isOpen, messages, lang", "open(), close(), send()"],
        ["TranslatePage", "items, translations", "translate_with_ai()"],
    ])

# IMAGEN 2: Diagrama de Clases
add_image_placeholder(doc,
    "Figura 2: Diagrama de Clases General",
    "Diagrama UML con 6 clases: Chatbot, Tramite, Multa, App Flask, "
    "Widget Chatbot, TranslatePage. Se muestran atributos y métodos "
    "de cada clase. "
    "Archivo: diagramas_staruml/02_diagrama_clases.mdj")

h2("3.1.5 Arquitectura del Sistema")

styled_table(doc,
    ["Capa", "Tecnología", "Función"],
    [
        ["Presentación", "HTML5, CSS3, JavaScript", "Interfaz web y widget chatbot"],
        ["Lógica", "Python, Flask", "Rutas HTTP y procesamiento"],
        ["Datos", "KB en Python", "Base de conocimientos 25 trámites"],
        ["Servicios Externos", "OpenAI, NLLB-200, Whisper", "IA para respuestas y traducción"],
    ])

# IMAGEN 3: Arquitectura
add_image_placeholder(doc,
    "Figura 3: Arquitectura del Sistema",
    "Diagrama de componentes con 4 capas: Presentación (HTML/CSS/JS), "
    "Lógica (Flask + Engine.py), Datos (KB), Servicios Externos (IA). "
    "Archivo: diagramas_staruml/04_arquitectura.mdj")

# =====================================================================
# 3.2 SCRUM
# =====================================================================
h1("3.2 APLICACIÓN DE LA METODOLOGÍA ÁGIL SCRUM")

h2("3.2.1 Roles")

styled_table(doc,
    ["Rol", "Responsable", "Funciones"],
    [
        ["Product Owner", "Alfredo Ramírez", "Define prioridades y acepta incrementos"],
        ["Scrum Master", "Ing. Freddy Ledezma", "Facilita el proceso Scrum"],
        ["Equipo Desarrollo", "Alfredo Ramírez", "Diseña, programa, prueba y documenta"],
    ])

h2("3.2.2 Planificación de Sprints")

styled_table(doc,
    ["Sprint", "Nombre", "Duración", "Puntos"],
    [
        ["1", "Base Conocimiento + Motor Chatbot", "2 sem", "21"],
        ["2", "Interfaz Web + Navegación", "2 sem", "16"],
        ["3", "Soporte Multiidioma ES/QU", "2 sem", "13"],
        ["4", "Pruebas + Voz + Documentación", "2 sem", "14"],
    ])

h2("3.2.3 Implementación por Sprints")

# SPRINT 1
h3("Sprint 1: Base de Conocimiento y Motor del Chatbot")

styled_table(doc,
    ["Tarea", "Estado", "Horas"],
    [
        ["Estructura KB con 25 trámites (es/qu)", "OK", "8"],
        ["Funciones normalize, detect_tramite, detect_intent", "OK", "12"],
        ["Funciones build_card, build_tramite_list, build_multas", "OK", "8"],
        ["Función get_resp con lógica de intenciones", "OK", "10"],
        ["Mock de OpenAI (get_ai_resp)", "OK", "6"],
        ["Mock de Whisper (transcribe_audio)", "OK", "4"],
        ["62 pruebas unitarias", "OK", "10"],
    ])

# SPRINT 2
h3("Sprint 2: Interfaz Web y Navegación")

styled_table(doc,
    ["Tarea", "Estado", "Horas"],
    [
        ["HTML del portal (header, hero, secciones, footer)", "OK", "8"],
        ["CSS responsivo y colores institucionales", "OK", "10"],
        ["Grid de 25 tarjetas de trámites", "OK", "6"],
        ["Buscador en tiempo real", "OK", "4"],
        ["Filtros por categoría", "OK", "4"],
        ["Sección multas (3 tarjetas + pasos)", "OK", "6"],
        ["Widget del chatbot embebido", "OK", "10"],
        ["API Flask (/chat, /language, /audio-to-text)", "OK", "8"],
        ["39 pruebas caja negra", "OK", "8"],
    ])

# IMAGEN 4: Mockup Portal
add_image_placeholder(doc,
    "Figura 4: Mockup - Pantalla Principal",
    "Captura del sitio web mostrando: barra superior con teléfono 4701677 "
    "y horarios, header con logo GAM y menú (Inicio, Trámites, Multas, "
    "Institución, Contacto), banner hero con título y botones CTA.")

# SPRINT 3
h3("Sprint 3: Soporte Multiidioma (ES/QU)")

styled_table(doc,
    ["Tarea", "Estado", "Horas"],
    [
        ["Atributos data-qu en 99 elementos HTML", "OK", "8"],
        ["Función translatePage() en main.js", "OK", "6"],
        ["Endpoint /api/translate en Flask", "OK", "6"],
        ["Integración NLLB-200 para traducción", "OK", "8"],
        ["UI keys actualizadas (subalcaldías, guía telefónica)", "OK", "6"],
        ["Datos de contacto reales (4701677, horarios)", "OK", "4"],
    ])

# IMAGEN 5: Mockup Trámites
add_image_placeholder(doc,
    "Figura 5: Mockup - Sección de Trámites",
    "Captura mostrando: campo de búsqueda con 'carnet', botones de filtro "
    "(Todos, Identidad, Vivienda, Negocio, Servicios), grid de tarjetas "
    "con información de cada trámite.")

# SPRINT 4
h3("Sprint 4: Pruebas, Voz y Documentación")

styled_table(doc,
    ["Tarea", "Estado", "Horas"],
    [
        ["44 pruebas caja blanca (cobertura ramas)", "OK", "10"],
        ["Botón de micrófono en widget", "OK", "6"],
        ["Integración Whisper para voz", "OK", "6"],
        ["Optimización de tiempos", "OK", "4"],
        ["Corrección de 4 bugs", "OK", "4"],
        ["Documentación técnica", "OK", "6"],
    ])

styled_table(doc,
    ["Categoría", "Tests", "Resultado"],
    [
        ["Unitarias", "62", "PASSED"],
        ["Caja Negra", "39", "PASSED"],
        ["Caja Blanca", "44", "PASSED"],
        ["TOTAL", "145", "98% cobertura"],
    ])

# IMAGEN 6: Pruebas finales
add_image_placeholder(doc,
    "Figura 6: Resultado Final de Pruebas",
    "Captura de terminal mostrando: python -m pytest tests/ -v con "
    "145 tests en estado PASSED. Resumen: 145 passed in 34.77s.")

# =====================================================================
# 3.3 RESUMEN
# =====================================================================
h1("3.3 RESUMEN DE RESULTADOS")

styled_table(doc,
    ["Sprint", "Funcionalidad", "Tests", "Estado"],
    [
        ["1", "Base Conocimiento + Motor", "62 unitarias", "OK"],
        ["2", "Interfaz Web + API", "39 caja negra", "OK"],
        ["3", "Multiidioma ES/QU", "—", "OK"],
        ["4", "Pruebas + Voz", "44 caja blanca", "OK"],
        ["TOTAL", "Sistema completo", "145", "100%"],
    ])

# =====================================================================
# 3.4 CONCLUSIONES
# =====================================================================
h1("3.4 CONCLUSIONES")

bullet("10 requerimientos funcionales y 6 no funcionales guiaron el desarrollo.")
bullet("Arquitectura de 4 capas: Presentación, Lógica, Datos, Servicios Externos.")
bullet("4 sprints de 2 semanas cada uno (8 semanas totales).")
bullet("25 trámites con información bilingüe en la base de conocimientos.")
bullet("14 intenciones detectadas por el chatbot.")
bullet("145 pruebas con 98% de cobertura de código.")
bullet("99 elementos traducidos automáticamente entre ES y QU.")

# Save
doc.save(r"C:\Users\kanit\Desktop\chatbot-sacaba\CAPITULO_III_FINAL.docx")
print("CAPITULO_III_FINAL.docx generado con 6 imágenes.")
