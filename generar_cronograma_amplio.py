# -*- coding: utf-8 -*-
"""
Genera CRONOGRAMA_AMPLIO.docx - Gantt completo Mayo 20 - Agosto 11 2026
"""
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Cm, Inches
from datetime import date, timedelta

AZUL = RGBColor(0x1F, 0x4E, 0x79)
VERDE = RGBColor(0x27, 0xAE, 0x60)
NARANJA = RGBColor(0xE6, 0x7E, 0x22)
ROJO = RGBColor(0xE7, 0x4C, 0x3C)
GRIS = RGBColor(0x7F, 0x8C, 0x8D)

# Colores de fondo para Gantt
COLORS_BG = {
    "prep": "D5E8D4",      # verde claro
    "kb": "DAE8FC",        # azul claro
    "ui": "FFE6CC",        # naranja claro
    "multi": "E1D5E7",     # morado claro
    "test": "FFF2CC",      # amarillo claro
    "doc": "F8CECC",       # rojo claro
    "final": "BDD7EE",     # azul fuerte
    "entrega": "C9DAF8",   # azul muy claro
}

def set_cell_bg(cell, color):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), color)
    cell._tc.get_or_add_tcPr().append(shd)

def set_cell_border(cell, top=None, bottom=None, left=None, right=None):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        if val:
            el = OxmlElement(f'w:{edge}')
            el.set(qn('w:val'), 'single')
            el.set(qn('w:sz'), '4')
            el.set(qn('w:color'), 'FFFFFF')
            el.set(qn('w:space'), '0')
            tcBorders.append(el)
    tcPr.append(tcBorders)

def styled_cell(cell, text, bold=False, size=8, color=None, bg=None, align=WD_ALIGN_PARAGRAPH.CENTER):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    r = p.add_run(str(text))
    r.bold = bold
    r.font.size = Pt(size)
    r.font.name = "Calibri"
    if color:
        r.font.color.rgb = color
    if bg:
        set_cell_bg(cell, bg)
    return cell

def get_weeks():
    """Genera semanas del 20 mayo al 11 agosto 2026"""
    weeks = []
    start = date(2026, 5, 20)  # Miércoles 20 mayo
    end = date(2026, 8, 11)    # Martes 11 agosto

    # Ajustar al lunes más cercano
    while start.weekday() != 0:  # 0 = lunes
        start += timedelta(days=1)

    current = start
    week_num = 1
    while current <= end:
        week_end = current + timedelta(days=4)  # Viernes
        weeks.append({
            "num": week_num,
            "start": current,
            "end": week_end,
            "label": f"Sem {week_num}"
        })
        current += timedelta(days=7)
        week_num += 1
    return weeks


def create_gantt_table(doc, weeks, activities):
    """Crea tabla Gantt"""
    num_weeks = len(weeks)

    # Table: Activity | Weeks...
    table = doc.add_table(rows=1, cols=num_weeks + 1)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Header row - Activity
    hdr = table.rows[0].cells[0]
    styled_cell(hdr, "ACTIVIDAD", bold=True, size=7, color=RGBColor(0xFF, 0xFF, 0xFF), bg="1F4E79")

    # Header row - Week numbers
    for i, w in enumerate(weeks):
        cell = table.rows[0].cells[i + 1]
        styled_cell(cell, f"S{w['num']}\n{w['start'].strftime('%d/%m')}", bold=True, size=6, color=RGBColor(0xFF, 0xFF, 0xFF), bg="1F4E79")

    # Activity rows
    for act_name, act_weeks, color in activities:
        row = table.add_row()
        styled_cell(row.cells[0], act_name, bold=True, size=7, align=WD_ALIGN_PARAGRAPH.LEFT)
        for i in range(num_weeks):
            cell = row.cells[i + 1]
            week_num = i + 1
            if week_num in act_weeks:
                styled_cell(cell, "■", size=7, color=RGBColor(0xFF, 0xFF, 0xFF), bg=color)
            else:
                styled_cell(cell, "", size=7)

    return table


doc = Document()
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(10)

for section in doc.sections:
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(1.5)
    section.right_margin = Cm(1.5)
    section.orientation = 1  # Landscape
    section.page_width = Cm(33)
    section.page_height = Cm(21)

# =====================================================================
# PORTADA
# =====================================================================
for _ in range(4):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("CRONOGRAMA DE PASANTÍA")
r.bold = True
r.font.size = Pt(28)
r.font.color.rgb = AZUL

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Instituto Técnico Superior (ITSa)")
r.font.size = Pt(16)
r.font.color.rgb = AZUL

doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Desarrollo de un Chatbot Web Multiidioma\n(Castellano–Quechua) para la Orientación sobre\nTrámites y Multas Municipales del GAM de Sacaba")
r.font.size = Pt(14)
r.font.color.rgb = GRIS

doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Estudiante: ALFREDO RAMÍREZ ESPINOZA")
r.font.size = Pt(12)
r.bold = True

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Tutor: Ing. FREDDY LEDEZMA HIGUERA")
r.font.size = Pt(12)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Periodo: 20 de Mayo – 11 de Agosto 2026")
r.font.size = Pt(12)
r.font.color.rgb = AZUL
r.bold = True

doc.add_page_break()

# =====================================================================
# DATOS GENERALES
# =====================================================================
doc.add_heading("1. DATOS GENERALES", level=1)

data_table = doc.add_table(rows=7, cols=2)
data_table.style = "Table Grid"
data_table.alignment = WD_TABLE_ALIGNMENT.CENTER

datos = [
    ("Institución", "Instituto Técnico Superior (ITSa)"),
    ("Programa", "Sistemas Informáticos"),
    ("Estudiante", "ALFREDO RAMÍREZ ESPINOZA"),
    ("Tutor Académico", "Ing. FREDDY LEDEZMA HIGUERA"),
    ("Empresa/Organización", "Gobierno Autónomo Municipal de Sacaba"),
    ("Periodo de Pasantía", "20 de Mayo – 11 de Agosto 2026 (12 semanas)"),
    ("Horas Totales", "360 horas (6 horas/día, Lun-Vie)")
]

for i, (label, value) in enumerate(datos):
    styled_cell(data_table.rows[i].cells[0], label, bold=True, size=10, bg="1F4E79", color=RGBColor(0xFF, 0xFF, 0xFF))
    styled_cell(data_table.rows[i].cells[1], value, size=10, align=WD_ALIGN_PARAGRAPH.LEFT)

# =====================================================================
# CRONOGRAMA GANTT
# =====================================================================
doc.add_heading("2. CRONOGRAMA GENERAL DE ACTIVIDADES", level=1)

p = doc.add_paragraph()
r = p.add_run("Periodo: 20 de mayo – 11 de agosto 2026 | 12 semanas | 360 horas")
r.font.size = Pt(10)
r.bold = True
r.font.color.rgb = AZUL

weeks = get_weeks()

# Activities: (name, [week_numbers], color)
activities = [
    ("1. Selección y delimitación del tema", [1], COLORS_BG["prep"]),
    ("2. Investigación y revisión bibliográfica", [1, 2], COLORS_BG["prep"]),
    ("3. Análisis de requerimientos del sistema", [2, 3], COLORS_BG["kb"]),
    ("4. Diseño de la base de conocimientos", [3, 4], COLORS_BG["kb"]),
    ("5. Diseño de la interfaz web (mockups)", [4, 5], COLORS_BG["ui"]),
    ("6. Desarrollo del motor del chatbot (engine.py)", [5, 6, 7], COLORS_BG["kb"]),
    ("7. Desarrollo de la interfaz web (HTML/CSS/JS)", [6, 7, 8], COLORS_BG["ui"]),
    ("8. Implementación multiidioma ES/QU", [7, 8, 9], COLORS_BG["multi"]),
    ("9. Integración de servicios IA (OpenAI/NLLB)", [8, 9], COLORS_BG["multi"]),
    ("10. Pruebas unitarias y de caja negra", [9, 10], COLORS_BG["test"]),
    ("11. Pruebas de caja blanca y cobertura", [10, 11], COLORS_BG["test"]),
    ("12. Corrección de errores y optimización", [10, 11], COLORS_BG["doc"]),
    ("13. Documentación técnica y manual", [11, 12], COLORS_BG["doc"]),
    ("14. Elaboración del informe final", [11, 12], COLORS_BG["doc"]),
    ("15. Preparación de presentación (Feria)", [12], COLORS_BG["final"]),
    ("16. Entrega y sustentación", [12], COLORS_BG["entrega"]),
]

create_gantt_table(doc, weeks, activities)

doc.add_paragraph()

# =====================================================================
# DETALLE POR SEMANA
# =====================================================================
doc.add_heading("3. DETALLE DE ACTIVIDADES POR SEMANA", level=1)

weekly_detail = [
    ("Semana 1\n(20-24 May)", "Selección del tema\nInvestigación inicial", "Investigar temas de chatbots municipales\nRevisar proyectos similares\nDelimitar alcance del proyecto", "20 h"),
    ("Semana 2\n(27-31 May)", "Revisión bibliográfica\nAnálisis preliminar", "Recolectar 10 fuentes académicas\nAnalizar GAM Sacaba (25 trámites)\nDefinir arquitectura del sistema", "30 h"),
    ("Semana 3\n(03-07 Jun)", "Análisis de requerimientos", "Requerimientos funcionales (10)\nRequerimientos no funcionales (6)\nDiagrama de casos de uso", "30 h"),
    ("Semana 4\n(10-14 Jun)", "Diseño de la KB", "Estructura de 25 trámites\nCampos: nombre, costo, tiempo, requisitos\nDiseño de la interfaz (mockups)", "30 h"),
    ("Semana 5\n(17-21 Jun)", "Diseño UI + Inicio desarrollo", "Mockups del portal web\nInicio del motor del chatbot\nFunciones: normalize, detect_intent", "30 h"),
    ("Semana 6\n(24-28 Jun)", "Motor del chatbot", "Funciones: get_resp, detect_tramite\nConstrucción de tarjetas\nBase de conocimientos completa", "30 h"),
    ("Semana 7\n(01-05 Jul)", "Interfaz web", "HTML5 del portal\nCSS3 responsivo\nWidget del chatbot embebido", "30 h"),
    ("Semana 8\n(08-12 Jul)", "Multiidioma", "Atributos data-qu (99 elementos)\nTraducción automática con NLLB-200\nCambio de idioma en tiempo real", "30 h"),
    ("Semana 9\n(15-19 Jul)", "IA + Voz", "Integración OpenAI\nTranscripción de audio (Whisper)\nTraducción con IA", "30 h"),
    ("Semana 10\n(22-26 Jul)", "Pruebas", "62 pruebas unitarias\n39 pruebas caja negra\nDetección y corrección de bugs", "30 h"),
    ("Semana 11\n(29 Jul-02 Ago)", "Pruebas + Documentación", "44 pruebas caja blanca\nCobertura de código: 98%\nInforme técnico", "30 h"),
    ("Semana 12\n(05-11 Ago)", "Informe + Entrega", "Informe final completo\nPreparación presentación\nSustentación y entrega", "30 h"),
]

# Table for weekly detail
t = doc.add_table(rows=1, cols=4)
t.style = "Table Grid"
t.alignment = WD_TABLE_ALIGNMENT.CENTER

headers = ["SEMANA", "ACTIVIDADES PRINCIPALES", "DETALLE", "HORAS"]
for i, h in enumerate(headers):
    styled_cell(t.rows[0].cells[i], h, bold=True, size=8, color=RGBColor(0xFF, 0xFF, 0xFF), bg="1F4E79")

for week_label, activities_text, detail, hours in weekly_detail:
    row = t.add_row()
    styled_cell(row.cells[0], week_label, bold=True, size=8)
    styled_cell(row.cells[1], activities_text, size=8, align=WD_ALIGN_PARAGRAPH.LEFT)
    styled_cell(row.cells[2], detail, size=7, align=WD_ALIGN_PARAGRAPH.LEFT)
    styled_cell(row.cells[3], hours, bold=True, size=9)

# =====================================================================
# RESUMEN DE HORAS
# =====================================================================
doc.add_heading("4. RESUMEN DE HORAS POR FASE", level=1)

hours_table = doc.add_table(rows=8, cols=3)
hours_table.style = "Table Grid"
hours_table.alignment = WD_TABLE_ALIGNMENT.CENTER

styled_cell(hours_table.rows[0].cells[0], "FASE", bold=True, size=9, color=RGBColor(0xFF, 0xFF, 0xFF), bg="1F4E79")
styled_cell(hours_table.rows[0].cells[1], "SEMANAS", bold=True, size=9, color=RGBColor(0xFF, 0xFF, 0xFF), bg="1F4E79")
styled_cell(hours_table.rows[0].cells[2], "HORAS", bold=True, size=9, color=RGBColor(0xFF, 0xFF, 0xFF), bg="1F4E79")

phases = [
    ("Planificación e Investigación", "1-2", "50"),
    ("Análisis y Diseño", "3-4", "60"),
    ("Desarrollo Backend", "5-7", "90"),
    ("Desarrollo Frontend + Multiidioma", "6-9", "120"),
    ("Integración IA", "8-9", "30"),
    ("Pruebas y Control de Calidad", "10-11", "60"),
    ("Documentación y Entrega", "11-12", "30"),
]

for i, (phase, sems, hrs) in enumerate(phases):
    row = hours_table.rows[i + 1]
    styled_cell(row.cells[0], phase, size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
    styled_cell(row.cells[1], sems, size=9)
    styled_cell(row.cells[2], hrs, bold=True, size=9)

# Total row
row = hours_table.add_row()
styled_cell(row.cells[0], "TOTAL", bold=True, size=9, bg="1F4E79", color=RGBColor(0xFF, 0xFF, 0xFF))
styled_cell(row.cells[1], "12 semanas", bold=True, size=9, bg="1F4E79", color=RGBColor(0xFF, 0xFF, 0xFF))
styled_cell(row.cells[2], "360 h", bold=True, size=9, bg="1F4E79", color=RGBColor(0xFF, 0xFF, 0xFF))

# =====================================================================
# ENTREGABLES
# =====================================================================
doc.add_heading("5. ENTREGABLES POR SEMANA", level=1)

deliv = doc.add_table(rows=13, cols=3)
deliv.style = "Table Grid"
deliv.alignment = WD_TABLE_ALIGNMENT.CENTER

styled_cell(deliv.rows[0].cells[0], "SEMANA", bold=True, size=8, color=RGBColor(0xFF, 0xFF, 0xFF), bg="1F4E79")
styled_cell(deliv.rows[0].cells[1], "ENTREGABLE", bold=True, size=8, color=RGBColor(0xFF, 0xFF, 0xFF), bg="1F4E79")
styled_cell(deliv.rows[0].cells[2], "ESTADO", bold=True, size=8, color=RGBColor(0xFF, 0xFF, 0xFF), bg="1F4E79")

deliverables = [
    ("S1", "Propuesta del tema y delimitación", "Pendiente"),
    ("S2", "Revisión bibliográfica (10 fuentes)", "Pendiente"),
    ("S3", "Documento de requerimientos", "Pendiente"),
    ("S4", "Diseño de la base de conocimientos", "Pendiente"),
    ("S5", "Mockups de la interfaz web", "Pendiente"),
    ("S6", "Motor del chatbot funcional", "Pendiente"),
    ("S7", "Portal web con widget chatbot", "Pendiente"),
    ("S8", "Sistema multiidioma ES/QU activo", "Pendiente"),
    ("S9", "Integración IA completa", "Pendiente"),
    ("S10", "Suite de pruebas (101 tests)", "Pendiente"),
    ("S11", "Informe técnico + 145 tests", "Pendiente"),
    ("S12", "Informe final + sustentación", "Pendiente"),
]

for i, (sem, deliverable, status) in enumerate(deliverables):
    row = deliv.rows[i + 1]
    styled_cell(row.cells[0], sem, bold=True, size=8)
    styled_cell(row.cells[1], deliverable, size=8, align=WD_ALIGN_PARAGRAPH.LEFT)
    color = VERDE if status == "Completado" else NARANJA
    styled_cell(row.cells[2], status, size=8, color=color)

# =====================================================================
# HITOS
# =====================================================================
doc.add_heading("6. HITOS IMPORTANTES", level=1)

milestones = doc.add_table(rows=7, cols=3)
milestones.style = "Table Grid"
milestones.alignment = WD_TABLE_ALIGNMENT.CENTER

styled_cell(milestones.rows[0].cells[0], "FECHA", bold=True, size=9, color=RGBColor(0xFF, 0xFF, 0xFF), bg="1F4E79")
styled_cell(milestones.rows[0].cells[1], "HITO", bold=True, size=9, color=RGBColor(0xFF, 0xFF, 0xFF), bg="1F4E79")
styled_cell(milestones.rows[0].cells[2], "DESCRIPCIÓN", bold=True, size=9, color=RGBColor(0xFF, 0xFF, 0xFF), bg="1F4E79")

milestone_data = [
    ("20 May 2026", "Inicio de Pasantía", "Presentación del plan de trabajo"),
    ("07 Jun 2026", "Diseño Aprobado", "KB y mockups validados"),
    ("28 Jun 2026", "Motor Funcional", "Chatbot con 25 trámites operativo"),
    ("12 Jul 2026", "Multiidioma", "Sistema ES/QU completo"),
    ("26 Jul 2026", "Pruebas", "145 tests con 98% cobertura"),
    ("11 Ago 2026", "Entrega Final", "Sustentación y entrega del proyecto"),
]

for i, (date_str, milestone, desc) in enumerate(milestone_data):
    row = milestones.rows[i + 1]
    styled_cell(row.cells[0], date_str, bold=True, size=9)
    styled_cell(row.cells[1], milestone, bold=True, size=9, color=AZUL)
    styled_cell(row.cells[2], desc, size=9, align=WD_ALIGN_PARAGRAPH.LEFT)

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

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Fecha: _____________                    Fecha: _____________")
r.font.size = Pt(9)

# Save
doc.save(r"C:\Users\kanit\Desktop\chatbot-sacaba\CRONOGRAMA_AMPLIO.docx")
print("CRONOGRAMA_AMPLIO.docx generado correctamente")
print(f"Semanas: {len(weeks)} (20 Mayo - 11 Agosto 2026)")
print("Total: 360 horas | 12 semanas | 6 hrs/día")
