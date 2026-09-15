# -*- coding: utf-8 -*-
"""
Genera CRONOGRAMA_FINAL.docx - Gantt profesional estilo tabla de Excel
Fases | Actividades | Inicio | Fin | Columnas semanales coloreadas
"""
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Cm
from datetime import date

# Colores de fondo por fase
COLORS = {
    "fase1": "D5E8D4",  # Verde claro
    "fase2": "FFE6CC",  # Naranja claro
    "fase3": "FFF2CC",  # Amarillo claro
    "fase4": "F8CECC",  # Rojo/Rosa claro
    "fase5": "DAE8FC",  # Azul claro
}

AZUL_OSCURO = RGBColor(0x1F, 0x4E, 0x79)
BLANCO = RGBColor(0xFF, 0xFF, 0xFF)

def set_cell_bg(cell, color):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), color)
    cell._tc.get_or_add_tcPr().append(shd)

def styled_cell(cell, text, bold=False, size=8, font_color=None, bg=None, align=WD_ALIGN_PARAGRAPH.CENTER):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    r = p.add_run(str(text))
    r.bold = bold
    r.font.size = Pt(size)
    r.font.name = "Calibri"
    if font_color:
        r.font.color.rgb = font_color
    if bg:
        set_cell_bg(cell, bg)
    return cell

def is_week_active(week_start, week_end, act_start, act_end):
    """Verifica si la actividad cae dentro de la semana"""
    return act_start <= week_end and act_end >= week_start

# =====================================================================
# DEFINICIÓN DE SEMANAS (20 mayo - 11 agosto 2026)
# =====================================================================
# Semana 1: 20-22 mayo (miércoles a viernes) - 3 días
# Semana 2: 25-29 mayo (lunes a viernes) - 5 días
# Semana 3: 01-05 junio - 5 días
# Semana 4: 08-12 junio - 5 días
# Semana 5: 15-19 junio - 5 días
# Semana 6: 22-26 junio - 5 días
# Semana 7: 29 jun - 03 jul - 5 días
# Semana 8: 06-10 julio - 5 días
# Semana 9: 13-17 julio - 5 días
# Semana 10: 20-24 julio - 5 días
# Semana 11: 27-31 julio - 5 días
# Semana 12: 03-07 agosto - 5 días
# Semana 13: 10-11 agosto (lunes martes) - 2 días

weeks = [
    {"num": 1,  "month": "Mayo",    "label": "Sem 1",   "start": date(2026,5,20),  "end": date(2026,5,22),  "days": 3},
    {"num": 2,  "month": "Mayo",    "label": "Sem 2",   "start": date(2026,5,25),  "end": date(2026,5,29),  "days": 5},
    {"num": 3,  "month": "Junio",   "label": "Sem 1",   "start": date(2026,6,1),   "end": date(2026,6,5),   "days": 5},
    {"num": 4,  "month": "Junio",   "label": "Sem 2",   "start": date(2026,6,8),   "end": date(2026,6,12),  "days": 5},
    {"num": 5,  "month": "Junio",   "label": "Sem 3",   "start": date(2026,6,15),  "end": date(2026,6,19),  "days": 5},
    {"num": 6,  "month": "Junio",   "label": "Sem 4",   "start": date(2026,6,22),  "end": date(2026,6,26),  "days": 5},
    {"num": 7,  "month": "Julio",   "label": "Sem 1",   "start": date(2026,6,29),  "end": date(2026,7,3),   "days": 5},
    {"num": 8,  "month": "Julio",   "label": "Sem 2",   "start": date(2026,7,6),   "end": date(2026,7,10),  "days": 5},
    {"num": 9,  "month": "Julio",   "label": "Sem 3",   "start": date(2026,7,13),  "end": date(2026,7,17),  "days": 5},
    {"num": 10, "month": "Julio",   "label": "Sem 4",   "start": date(2026,7,20),  "end": date(2026,7,24),  "days": 5},
    {"num": 11, "month": "Agosto",  "label": "Sem 1",   "start": date(2026,7,27),  "end": date(2026,7,31),  "days": 5},
    {"num": 12, "month": "Agosto",  "label": "Sem 2",   "start": date(2026,8,3),   "end": date(2026,8,7),   "days": 5},
    {"num": 13, "month": "Agosto",  "label": "Sem 3",   "start": date(2026,8,10),  "end": date(2026,8,11),  "days": 2},
]

# =====================================================================
# DEFINICIÓN DE FASES Y ACTIVIDADES
# =====================================================================
# (nombre_actividad, inicio, fin, es_fase, color)
activities = [
    # FASE 1: Planificación y Análisis (15 mayo - 07 jun)
    ("FASE 1: Planificación y Análisis", date(2026,5,15), date(2026,6,7), True, COLORS["fase1"]),
    ("Levantamiento de información con el GAM", date(2026,5,15), date(2026,5,29), False, COLORS["fase1"]),
    ("Análisis de requerimientos funcionales", date(2026,5,25), date(2026,6,5), False, COLORS["fase1"]),
    ("Definición de alcance y objetivos", date(2026,5,15), date(2026,5,29), False, COLORS["fase1"]),
    ("Revisión de trámites y multas vigentes", date(2026,5,25), date(2026,6,5), False, COLORS["fase1"]),
    ("Elaboración del documento de requerimientos", date(2026,6,1), date(2026,6,7), False, COLORS["fase1"]),

    # FASE 2: Diseño (08 jun - 21 jun)
    ("FASE 2: Diseño", date(2026,6,8), date(2026,6,21), True, COLORS["fase2"]),
    ("Diseño de la base de conocimiento (25 trámites)", date(2026,6,8), date(2026,6,19), False, COLORS["fase2"]),
    ("Diseño de la interfaz web (wireframes)", date(2026,6,8), date(2026,6,19), False, COLORS["fase2"]),
    ("Diseño del flujo del chatbot", date(2026,6,8), date(2026,6,19), False, COLORS["fase2"]),
    ("Diseño del módulo de traducción es/qu", date(2026,6,15), date(2026,6,21), False, COLORS["fase2"]),

    # FASE 3: Desarrollo (22 jun - 19 jul)
    ("FASE 3: Desarrollo", date(2026,6,22), date(2026,7,19), True, COLORS["fase3"]),
    ("Selección tecnológica (Flask, OpenAI, NLLB)", date(2026,6,22), date(2026,6,26), False, COLORS["fase3"]),
    ("Configuración del entorno (Flask, Python)", date(2026,6,22), date(2026,6,26), False, COLORS["fase3"]),
    ("Desarrollo del motor de IA (engine.py)", date(2026,6,22), date(2026,7,10), False, COLORS["fase3"]),
    ("Desarrollo del frontend (HTML/CSS/JS)", date(2026,6,29), date(2026,7,17), False, COLORS["fase3"]),
    ("Integración con ChatGPT API y Whisper", date(2026,7,6), date(2026,7,17), False, COLORS["fase3"]),
    ("Implementación multiidioma (es ↔ qu)", date(2026,7,6), date(2026,7,19), False, COLORS["fase3"]),
    ("Desarrollo del widget de chat embebido", date(2026,6,29), date(2026,7,10), False, COLORS["fase3"]),
    ("Implementación de detección de idioma", date(2026,7,13), date(2026,7,19), False, COLORS["fase3"]),

    # FASE 4: Pruebas (20 jul - 02 ago)
    ("FASE 4: Pruebas", date(2026,7,20), date(2026,8,2), True, COLORS["fase4"]),
    ("Pruebas unitarias (62 tests)", date(2026,7,20), date(2026,7,24), False, COLORS["fase4"]),
    ("Pruebas de caja negra (39 tests)", date(2026,7,20), date(2026,7,31), False, COLORS["fase4"]),
    ("Pruebas de caja blanca (44 tests)", date(2026,7,27), date(2026,8,2), False, COLORS["fase4"]),
    ("Pruebas de integración del chatbot", date(2026,7,27), date(2026,8,2), False, COLORS["fase4"]),
    ("Corrección de errores y optimización", date(2026,7,27), date(2026,8,2), False, COLORS["fase4"]),
    ("Cobertura de código >= 90%", date(2026,7,27), date(2026,8,2), False, COLORS["fase4"]),

    # FASE 5: Documentación y Entrega (03 ago - 11 ago)
    ("FASE 5: Documentación y Entrega", date(2026,8,3), date(2026,8,11), True, COLORS["fase5"]),
    ("Redacción del informe final", date(2026,8,3), date(2026,8,7), False, COLORS["fase5"]),
    ("Elaboración del cronograma y anexos", date(2026,8,3), date(2026,8,7), False, COLORS["fase5"]),
    ("Preparación de la presentación", date(2026,8,3), date(2026,8,11), False, COLORS["fase5"]),
    ("Entrega del sistema funcionando", date(2026,8,10), date(2026,8,11), False, COLORS["fase5"]),
    ("Revisión final con el tutor", date(2026,8,10), date(2026,8,11), False, COLORS["fase5"]),
]


# =====================================================================
# CREAR DOCUMENTO
# =====================================================================
doc = Document()
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(8)

for section in doc.sections:
    section.orientation = 1  # Landscape
    section.page_width = Cm(38)
    section.page_height = Cm(24)
    section.top_margin = Cm(1.5)
    section.bottom_margin = Cm(1.5)
    section.left_margin = Cm(1.5)
    section.right_margin = Cm(1.5)

# =====================================================================
# PORTADA
# =====================================================================
for _ in range(3):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("CRONOGRAMA DE PASANTÍA")
r.bold = True
r.font.size = Pt(26)
r.font.color.rgb = AZUL_OSCURO

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Instituto Técnico Superior (ITSa)")
r.font.size = Pt(14)
r.font.color.rgb = AZUL_OSCURO

doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Chatbot Web Multiidioma (Castellano–Quechua)\npara Trámites y Multas Municipales del GAM de Sacaba")
r.font.size = Pt(12)
r.font.color.rgb = RGBColor(0x7F, 0x8C, 0x8D)

doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Estudiante: ALFREDO RAMÍREZ ESPINOZA")
r.font.size = Pt(11)
r.bold = True

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Tutor: Ing. FREDDY LEDEZMA HIGUERA")
r.font.size = Pt(11)

doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Periodo: 15 de Mayo – 11 de Agosto 2026")
r.font.size = Pt(12)
r.font.color.rgb = AZUL_OSCURO
r.bold = True

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Total: 360 horas | 6 horas/día | Lunes a Viernes")
r.font.size = Pt(11)

doc.add_page_break()

# =====================================================================
# CRONOGRAMA GANTT
# =====================================================================
doc.add_heading("CRONOGRAMA GENERAL DE ACTIVIDADES", level=1)

p = doc.add_paragraph()
r = p.add_run("Periodo: 15 de Mayo – 11 de Agosto 2026 | 13 semanas | 360 horas totales")
r.font.size = Pt(9)
r.bold = True
r.font.color.rgb = AZUL_OSCURO

# Crear tabla: Fase/Actividad | Inicio | Fin | 13 columnas semanales
num_cols = 3 + len(weeks)  # 3 + 13 = 16
table = doc.add_table(rows=1, cols=num_cols)
table.style = "Table Grid"
table.alignment = WD_TABLE_ALIGNMENT.CENTER

# ---- HEADER ROW ----
header_cells = table.rows[0].cells
styled_cell(header_cells[0], "Fase / Actividad", bold=True, size=7, font_color=BLANCO, bg="2C3E50")
styled_cell(header_cells[1], "Inicio", bold=True, size=7, font_color=BLANCO, bg="2C3E50")
styled_cell(header_cells[2], "Fin", bold=True, size=7, font_color=BLANCO, bg="2C3E50")

# Headers de semanas
prev_month = ""
for i, w in enumerate(weeks):
    cell = header_cells[i + 3]
    if w["month"] != prev_month:
        label = f"{w['month']}\n{w['label']}"
        prev_month = w["month"]
    else:
        label = w["label"]
    styled_cell(cell, label, bold=True, size=6, font_color=BLANCO, bg="2C3E50")

# ---- ACTIVITY ROWS ----
for act_name, act_start, act_end, es_fase, color in activities:
    row = table.add_row()

    # Columna 1: Nombre
    styled_cell(row.cells[0], act_name, bold=es_fase, size=7 if es_fase else 6,
                align=WD_ALIGN_PARAGRAPH.LEFT if es_fase else WD_ALIGN_PARAGRAPH.LEFT)

    # Columna 2: Inicio
    styled_cell(row.cells[1], act_start.strftime("%d-%b"), bold=es_fase, size=6)

    # Columna 3: Fin
    styled_cell(row.cells[2], act_end.strftime("%d-%b"), bold=es_fase, size=6)

    # Columnas 4-16: Semanas
    for i, w in enumerate(weeks):
        cell = row.cells[i + 3]
        if is_week_active(w["start"], w["end"], act_start, act_end):
            styled_cell(cell, "■", size=6, font_color=RGBColor(0x66, 0x66, 0x66), bg=color)
        else:
            styled_cell(cell, "", size=6)

# =====================================================================
# RESUMEN DE HORAS POR FASE
# =====================================================================
doc.add_paragraph()
doc.add_heading("RESUMEN DE HORAS POR FASE", level=1)

hours_table = doc.add_table(rows=7, cols=4)
hours_table.style = "Table Grid"
hours_table.alignment = WD_TABLE_ALIGNMENT.CENTER

styled_cell(hours_table.rows[0].cells[0], "FASE", bold=True, size=8, font_color=BLANCO, bg="2C3E50")
styled_cell(hours_table.rows[0].cells[1], "FECHAS", bold=True, size=8, font_color=BLANCO, bg="2C3E50")
styled_cell(hours_table.rows[0].cells[2], "SEMANAS", bold=True, size=8, font_color=BLANCO, bg="2C3E50")
styled_cell(hours_table.rows[0].cells[3], "HORAS", bold=True, size=8, font_color=BLANCO, bg="2C3E50")

phases = [
    ("FASE 1: Planificación y Análisis", "15 May - 07 Jun", "1-3", "60", COLORS["fase1"]),
    ("FASE 2: Diseño", "08 Jun - 21 Jun", "4-5", "60", COLORS["fase2"]),
    ("FASE 3: Desarrollo", "22 Jun - 19 Jul", "6-9", "144", COLORS["fase3"]),
    ("FASE 4: Pruebas", "20 Jul - 02 Ago", "10-11", "60", COLORS["fase4"]),
    ("FASE 5: Documentación y Entrega", "03 Ago - 11 Ago", "12-13", "36", COLORS["fase5"]),
]

for i, (phase, dates, sems, hrs, color) in enumerate(phases):
    row = hours_table.rows[i + 1]
    styled_cell(row.cells[0], phase, bold=True, size=8, align=WD_ALIGN_PARAGRAPH.LEFT, bg=color)
    styled_cell(row.cells[1], dates, size=8)
    styled_cell(row.cells[2], sems, size=8)
    styled_cell(row.cells[3], hrs, bold=True, size=9)

# Total
row = hours_table.rows[6]
styled_cell(row.cells[0], "TOTAL", bold=True, size=9, font_color=BLANCO, bg="2C3E50")
styled_cell(row.cells[1], "15 May - 11 Ago", bold=True, size=8, font_color=BLANCO, bg="2C3E50")
styled_cell(row.cells[2], "13 sem", bold=True, size=8, font_color=BLANCO, bg="2C3E50")
styled_cell(row.cells[3], "360 h", bold=True, size=9, font_color=BLANCO, bg="2C3E50")

# =====================================================================
# DETALLE DE ACTIVIDADES POR SEMANA
# =====================================================================
doc.add_page_break()
doc.add_heading("DETALLE DE ACTIVIDADES POR SEMANA", level=1)

detail_table = doc.add_table(rows=1, cols=5)
detail_table.style = "Table Grid"
detail_table.alignment = WD_TABLE_ALIGNMENT.CENTER

for i, h in enumerate(["SEMANA", "FECHAS", "ACTIVIDADES", "HORAS", "ENTREGABLE"]):
    styled_cell(detail_table.rows[0].cells[i], h, bold=True, size=8, font_color=BLANCO, bg="2C3E50")

weekly = [
    ("S1", "20-22 May", "Levantamiento de información GAM\nDefinición de alcance y objetivos", "18", "Acta de inicio"),
    ("S2", "25-29 May", "Análisis de requerimientos\nRevisión de trámites y multas", "30", "Documento de requerimientos"),
    ("S3", "01-05 Jun", "Elaboración de requerimientos\nRevisión bibliográfica", "30", "Revisión bibliográfica"),
    ("S4", "08-12 Jun", "Diseño de la KB (25 trámites)\nDiseño de wireframes", "30", "Diseño de KB"),
    ("S5", "15-19 Jun", "Diseño del flujo del chatbot\nDiseño módulo traducción", "30", "Wireframes aprobados"),
    ("S6", "22-26 Jun", "Selección tecnológica\nConfiguración del entorno", "30", "Entorno funcional"),
    ("S7", "29 Jun-03 Jul", "Desarrollo motor IA (engine.py)\nDesarrollo widget chat", "30", "Motor del chatbot"),
    ("S8", "06-10 Jul", "Desarrollo frontend HTML/CSS/JS\nIntegración ChatGPT API", "30", "Portal web funcional"),
    ("S9", "13-17 Jul", "Multiidioma es↔qu\nDetección de idioma", "30", "Sistema multiidioma"),
    ("S10", "20-24 Jul", "Pruebas unitarias (62)\nPruebas caja negra (39)", "30", "Suite de pruebas"),
    ("S11", "27-31 Jul", "Pruebas caja blanca (44)\nCorrección de errores", "30", "145 tests pasando"),
    ("S12", "03-07 Ago", "Redacción informe final\nElaboración cronograma", "30", "Informe final"),
    ("S13", "10-11 Ago", "Preparación presentación\nEntrega y sustentación", "12", "Entrega del proyecto"),
]

for sem, dates, acts, hrs, deliv in weekly:
    row = detail_table.add_row()
    styled_cell(row.cells[0], sem, bold=True, size=8)
    styled_cell(row.cells[1], dates, size=7)
    styled_cell(row.cells[2], acts, size=7, align=WD_ALIGN_PARAGRAPH.LEFT)
    styled_cell(row.cells[3], hrs, bold=True, size=8)
    styled_cell(row.cells[4], deliv, size=7, align=WD_ALIGN_PARAGRAPH.LEFT)

# =====================================================================
# LEYENDA DE COLORES
# =====================================================================
doc.add_paragraph()
doc.add_heading("LEYENDA DE COLORES", level=1)

legend = doc.add_table(rows=1, cols=5)
legend.style = "Table Grid"
legend.alignment = WD_TABLE_ALIGNMENT.CENTER

legend_data = [
    (COLORS["fase1"], "FASE 1:\nPlanificación y Análisis"),
    (COLORS["fase2"], "FASE 2:\nDiseño"),
    (COLORS["fase3"], "FASE 3:\nDesarrollo"),
    (COLORS["fase4"], "FASE 4:\nPruebas"),
    (COLORS["fase5"], "FASE 5:\nDocumentación"),
]

for i, (color, label) in enumerate(legend_data):
    cell = legend.rows[0].cells[i]
    styled_cell(cell, label, bold=True, size=7, bg=color)

# =====================================================================
# FIRMA
# =====================================================================
doc.add_paragraph()
doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("_" * 30 + "          " + "_" * 30)
r.font.size = Pt(10)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Ing. Freddy Ledezma Higuera          ALFREDO RAMÍREZ ESPINOZA")
r.font.size = Pt(9)
r.bold = True

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Tutor Académico ITSa                    Estudiante")
r.font.size = Pt(9)

# =====================================================================
# SAVE
# =====================================================================
doc.save(r"C:\Users\kanit\Desktop\chatbot-sacaba\CRONOGRAMA_FINAL.docx")
print("CRONOGRAMA_FINAL.docx generado correctamente")
print("13 semanas | 15 mayo - 11 agosto 2026 | 360 horas")
print("5 fases | 32 actividades | Gantt con colores")
