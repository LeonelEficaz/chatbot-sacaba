# -*- coding: utf-8 -*-
"""Genera CRONOGRAMA_PASANTIA.docx con tabla profesional."""
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Cm
from datetime import date, timedelta

AZUL = RGBColor(0x1F, 0x4E, 0x79)
GRIS = "D9E2F3"
VERDE = "E2EFDA"
AMARILLO = "FFF2CC"
NARANJA = "FCE4D6"
ROJO = "F8CBAD"
AZUL_CLARO = "D6E4F0"


def set_cell_bg(cell, color):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), color)
    cell._tc.get_or_add_tcPr().append(shd)


def add_table(doc, headers, rows, col_colors=None):
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
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i > 0 else WD_ALIGN_PARAGRAPH.LEFT
                    for r in p.runs:
                        r.font.size = Pt(9)
                if col_colors and ri < len(col_colors):
                    set_cell_bg(cells[i], col_colors[ri])
    return t


doc = Document()
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)

for s in doc.sections:
    s.top_margin = Cm(2.5)
    s.bottom_margin = Cm(2.5)
    s.left_margin = Cm(2.5)
    s.right_margin = Cm(2.5)

# =====================================================================
# TITULO
# =====================================================================
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("INSTITUTO TECNOLÓGICO SACABA")
r.bold = True
r.font.size = Pt(16)
r.font.color.rgb = AZUL

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Carrera de Sistemas Informáticos")
r.font.size = Pt(12)

doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("CRONOGRAMA DE PASANTÍA PROFESIONAL")
r.bold = True
r.font.size = Pt(14)
r.font.color.rgb = AZUL

doc.add_paragraph()

# Datos generales
p = doc.add_paragraph()
r = p.add_run("Estudiante: ")
r.bold = True
p.add_run("ALFREDO RAMÍREZ ESPINOZA")

p = doc.add_paragraph()
r = p.add_run("Tutor: ")
r.bold = True
p.add_run("Ing. FREDDY LEDEZMA HIGUERA")

p = doc.add_paragraph()
r = p.add_run("Proyecto: ")
r.bold = True
p.add_run("Chatbot Web Multiidioma (Castellano–Quechua) para Trámites y Multas Municipales – GAM Sacaba")

p = doc.add_paragraph()
r = p.add_run("Periodo: ")
r.bold = True
p.add_run("15 de mayo – 9 de agosto de 2026 (12 semanas)")

p = doc.add_paragraph()
r = p.add_run("Total horas: ")
r.bold = True
p.add_run("360 horas (30 hrs/semana · 6 hrs/día · lunes a viernes)")

doc.add_paragraph()

# =====================================================================
# CRONOGRAMA POR FASES
# =====================================================================
p = doc.add_paragraph()
r = p.add_run("CRONOGRAMA DETALLADO POR FASES")
r.bold = True
r.font.size = Pt(12)
r.font.color.rgb = AZUL

phases = [
    # (fase, actividades, inicio, fin, semanas, horas, color)
    ("FASE 1\nPlanificación y\nAnálisis",
     "• Levantamiento de información con el GAM\n• Análisis de requerimientos funcionales\n• Definición de alcance y objetivos\n• Revisión de trámites y multas vigentes\n• Elaboración del documento de requerimientos",
     "15 may", "7 jun", "3.5", 105, VERDE),
    ("FASE 2\nDiseño",
     "• Diseño de la base de conocimiento (25 trámites)\n• Diseño de la interfaz web (wireframes)\n• Diseño del flujo del chatbot\n• Diseño del módulo de traducción es/qu\n• Selección tecnológica (Flask, OpenAI, NLLB)",
     "8 jun", "21 jun", "2", 60, AMARILLO),
    ("FASE 3\nDesarrollo",
     "• Configuración del entorno (Flask, Python)\n• Desarrollo del motor de对话 (engine.py)\n• Desarrollo del frontend (HTML/CSS/JS)\n• Integración con ChatGPT API y Whisper\n• Implementación multiidioma (es↔qu)\n• Desarrollo del widget de chat embebido\n• Implementación de detección de idioma",
     "22 jun", "19 jul", "4", 120, NARANJA),
    ("FASE 4\nPruebas",
     "• Pruebas unitarias (62 tests)\n• Pruebas de caja negra (39 tests)\n• Pruebas de caja blanca (44 tests)\n• Pruebas de integración del chatbot\n• Corrección de errores y optimización\n• Cobertura de código ≥ 90%",
     "20 jul", "2 ago", "2", 60, ROJO),
    ("FASE 5\nDocumentación\ny Entrega",
     "• Redacción del informe final\n• Elaboración del cronograma y anexos\n• Preparación de la presentación\n• Entrega del sistema funcionando\n• Revisión final con el tutor",
     "3 ago", "9 ago", "1", 15, AZUL_CLARO),
]

headers = ["FASE", "ACTIVIDADES", "INICIO", "FIN", "SEMANAS", "HORAS"]
rows = []
colors = []
for fase, acts, ini, fin, sem, hrs, col in phases:
    rows.append([fase, acts, ini, fin, sem, str(hrs)])
    colors.append(col)

add_table(doc, headers, rows, colors)

doc.add_paragraph()

# =====================================================================
# RESUMEN SEMANAL
# =====================================================================
p = doc.add_paragraph()
r = p.add_run("RESUMEN SEMANAL DE HORAS")
r.bold = True
r.font.size = Pt(12)
r.font.color.rgb = AZUL

# Calculate week-by-week breakdown
start = date(2026, 5, 15)
weeks_data = []
current_week_start = start
week_num = 1
total_hrs = 0

while current_week_start <= date(2026, 8, 9):
    # Find end of week (Friday) or end of period
    days_to_friday = (4 - current_week_start.weekday()) % 7
    if days_to_friday == 0 and current_week_start.weekday() != 4:
        days_to_friday = 7
    week_end = current_week_start + timedelta(days=days_to_friday)
    if week_end > date(2026, 8, 9):
        week_end = date(2026, 8, 9)

    # Count weekdays in this week
    wd = 0
    d = current_week_start
    while d <= week_end:
        if d.weekday() < 5:
            wd += 1
        d += timedelta(days=1)

    # Determine phase
    if current_week_start <= date(2026, 6, 7):
        phase = "Fase 1 - Planificación"
    elif current_week_start <= date(2026, 6, 21):
        phase = "Fase 2 - Diseño"
    elif current_week_start <= date(2026, 7, 19):
        phase = "Fase 3 - Desarrollo"
    elif current_week_start <= date(2026, 8, 2):
        phase = "Fase 4 - Pruebas"
    else:
        phase = "Fase 5 - Documentación"
    
    # Use 6 hrs/day but cap total at 360
    hrs = wd * 6
    if total_hrs + hrs > 360:
        hrs = 360 - total_hrs
    total_hrs += hrs

    weeks_data.append((week_num, f"{current_week_start.strftime('%d/%m')} - {week_end.strftime('%d/%m')}", phase, f"{wd} días", f"{hrs} hrs"))
    week_num += 1
    current_week_start = week_end + timedelta(days=1)
    if current_week_start.weekday() >= 5:  # Skip weekends
        current_week_start += timedelta(days=(7 - current_week_start.weekday()))

# Create weekly summary table
headers2 = ["SEMANA", "FECHAS", "FASE", "DÍAS", "HORAS"]
rows2 = []
total_hrs_table = 0
for wnum, fec, pha, dias, hrs in weeks_data:
    rows2.append([f"Sem {wnum}", fec, pha, dias, hrs])
    total_hrs_table += int(hrs.replace(' hrs', ''))

# Add total row
rows2.append(["", "TOTAL", "", "61 días", f"{total_hrs_table} hrs"])

t2 = doc.add_table(rows=1, cols=5)
t2.style = "Table Grid"
t2.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(headers2):
    c = t2.rows[0].cells[i]
    c.text = h
    for p in c.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_bg(c, "1F4E79")

for ri, row in enumerate(rows2):
    cells = t2.add_row().cells
    for i, val in enumerate(row):
        cells[i].text = str(val)
        for p in cells[i].paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.size = Pt(9)
                if ri == len(rows2) - 1:  # Total row
                    r.bold = True
    if ri == len(rows2) - 1:
        for i in range(5):
            set_cell_bg(cells[i], GRIS)

doc.add_paragraph()

# =====================================================================
# OBSERVACIONES
# =====================================================================
p = doc.add_paragraph()
r = p.add_run("OBSERVACIONES")
r.bold = True
r.font.size = Pt(12)
r.font.color.rgb = AZUL

obs = [
    "Se trabajan 6 horas diarias, de lunes a viernes (sin sábados ni domingos).",
    "El total de 360 horas se distribuye en 12 semanas completas.",
    "Las fases pueden solaparse según avance del proyecto.",
    "Las horas incluyen: análisis, diseño, desarrollo, pruebas y documentación.",
    "El informe final se entrega en la última semana de la pasantía.",
]
for o in obs:
    p = doc.add_paragraph(o, style="List Bullet")
    for r in p.runs:
        r.font.size = Pt(10)

# Save
doc.save(r"C:\Users\kanit\Desktop\chatbot-sacaba\CRONOGRAMA_PASANTIA.docx")
print("CRONOGRAMA_PASANTIA.docx generado correctamente.")
print(f"Total: {total_hrs} horas en {week_num - 1} semanas")
