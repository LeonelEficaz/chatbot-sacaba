# -*- coding: utf-8 -*-
"""
Exposición 1: "Beneficios y desafíos de la automatización" (30 pts, entrega 06/10/2026)
Genera un PPTX 16:9 con notas del orador. Todo el texto se mide con PIL usando
las fuentes reales de Windows y se ajusta de linea, de modo que no se produzcan
cuadros de texto desbordados. Al final ejecuta una auditoria del PPTX.
"""
import glob
import os
import sys

from PIL import ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

sys.stdout.reconfigure(encoding="utf-8")

BASE = [p for p in glob.glob(r"C:\Users\kanit\OneDrive\Escritorio\*\chatbot-sacaba") if os.path.isdir(p)][0]
OUT_DIR = os.path.join(BASE, "GESTION_2026_CUARTO_BIMESTRE", "02_exposicion_beneficios_desafios")
os.makedirs(OUT_DIR, exist_ok=True)

NAVY = RGBColor(0x0B, 0x12, 0x20)
NAVY2 = RGBColor(0x15, 0x22, 0x38)
TEAL = RGBColor(0x0F, 0x76, 0x6E)
TEAL_L = RGBColor(0x5E, 0xEA, 0xD4)
BLUE = RGBColor(0x1D, 0x4E, 0xD8)
AMBER = RGBColor(0xB4, 0x53, 0x09)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
INK = RGBColor(0x1E, 0x29, 0x3B)
GRAY = RGBColor(0x47, 0x55, 0x69)
LIGHT = RGBColor(0xF1, 0xF5, 0xF9)
BORDER = RGBColor(0xCB, 0xD5, 0xE1)
SLATE = RGBColor(0x94, 0xA3, 0xB8)
FONT = "Segoe UI"

ALUMNO = "Alfredo Ramirez Espinoza"
CURSO = "Sistemas Informaticos - ITSA - Gestion 2026"

_fonts = {}


def _pil(size_pt, bold=False):
    key = (round(size_pt, 1), bold)
    if key not in _fonts:
        path = r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf"
        _fonts[key] = ImageFont.truetype(path, max(6, int(round(size_pt * 96 / 72))))
    return _fonts[key]


def w_in(text, size_pt, bold=False):
    """Ancho del texto en pulgadas (medido con la fuente real)."""
    return _pil(size_pt, bold).getlength(text) / 96.0


def wrap(text, max_in, size_pt, bold=False):
    out = []
    for hard in text.split("\n"):
        words, cur = hard.split(), ""
        for word in words:
            cand = (cur + " " + word).strip()
            if not cur:
                if w_in(cand, size_pt, bold) > max_in:
                    raise SystemExit(f"TEXTO DEMASIADO ANCHO ({size_pt}pt): {cand!r}")
                cur = cand
            elif w_in(cand, size_pt, bold) <= max_in:
                cur = cand
            else:
                out.append(cur)
                cur = word
        out.append(cur)
    return out


AUDIT = []


def check(tag, text, box_in, size_pt, bold=False):
    for ln in text.split("\n"):
        w = w_in(ln, size_pt, bold)
        if w > box_in + 0.02:
            AUDIT.append(f"{tag}: linea de {w:.2f}in en caja de {box_in:.2f}in -> {ln[:60]!r}")


prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = 13.333, 7.5
BLANK = prs.slide_layouts[6]
_num = {"n": 0}


def rect(slide, x, y, w, h, fill=None, line=None, shape=MSO_SHAPE.RECTANGLE, adj=None):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(1.25)
    s.shadow.inherit = False
    if adj is not None:
        try:
            s.adjustments[0] = adj
        except Exception:
            pass
    return s


def tbox(slide, tag, x, y, w, h, text, size=18, bold=False, color=INK, align=PP_ALIGN.LEFT,
         spacing=1.05):
    text = text.replace("\n", "\n")
    if "\n" not in text:
        text = "\n".join(wrap(text, w, size, bold))
    check(tag, text, w, size, bold)
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, ln in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        r = p.add_run()
        r.text = ln
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
        r.font.name = FONT
    need = len(text.split("\n")) * size * 1.42 / 72.0
    if need > h + 0.06:
        AUDIT.append(f"{tag}: alto insuficiente (necesita {need:.2f}in, caja {h:.2f}in)")
    return tb


def slide_base(kicker, title, notes):
    _num["n"] += 1
    s = prs.slides.add_slide(BLANK)
    rect(s, 0, 0, SW, SH, fill=WHITE)
    rect(s, 0, 0, SW, 1.02, fill=NAVY)
    rect(s, 0, 1.02, SW, 0.055, fill=TEAL)
    tbox(s, f"s{_num['n']}.kicker", 0.55, 0.13, 11.5, 0.28, kicker.upper(), size=12, bold=True, color=TEAL_L)
    tbox(s, f"s{_num['n']}.title", 0.55, 0.4, 12.3, 0.55, title, size=26, bold=True, color=WHITE)
    tbox(s, f"s{_num['n']}.foot", 0.55, 7.02, 8.5, 0.28, f"{ALUMNO}  |  {CURSO}", size=10.5, color=GRAY)
    tbox(s, f"s{_num['n']}.num", 11.9, 7.02, 0.9, 0.28, str(_num["n"]), size=10.5, color=GRAY,
         align=PP_ALIGN.RIGHT)
    s.notes_slide.notes_text_frame.text = notes
    return s


def bullets(slide, tag, items, x, y, w, size=16.5, step=0.44):
    cy = y
    for lvl, txt in items:
        if lvl == 0:
            rect(slide, x, cy + 0.09, 0.13, 0.13, fill=TEAL, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.3)
            tbox(slide, tag, x + 0.3, cy, w - 0.3, 0.38, txt, size=size, bold=True, color=INK)
        else:
            rect(slide, x + 0.32, cy + 0.17, 0.07, 0.07, fill=SLATE, shape=MSO_SHAPE.OVAL)
            tbox(slide, tag, x + 0.58, cy + 0.02, w - 0.58, 0.36, txt, size=size - 2, color=GRAY)
        cy += step
    return cy


def card(slide, tag, x, y, w, h, title, text, accent, badge):
    rect(slide, x, y, w, h, fill=LIGHT, line=BORDER, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.06)
    rect(slide, x, y, 0.075, h, fill=accent)
    rect(slide, x + 0.28, y + 0.26, 0.5, 0.5, fill=accent, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.25)
    tbox(slide, tag, x + 0.28, y + 0.36, 0.5, 0.3, badge, size=15, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER)
    tbox(slide, tag, x + 0.9, y + 0.32, w - 1.2, 0.4, title, size=15.5, bold=True, color=INK)
    lines = wrap(text, w - 0.6, 12.5)
    tbox(slide, tag, x + 0.28, y + 0.95, w - 0.6, h - 1.15, "\n".join(lines), size=12.5, color=GRAY,
         spacing=1.1)


# ---------------------------------------------------------------- 1. portada
_num["n"] += 1
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, SW, SH, fill=NAVY)
rect(s, 0, 0, 0.42, SH, fill=TEAL)
rect(s, 6.9, 0, 6.44, SH, fill=NAVY2)
tbox(s, "p.kick", 1.1, 1.3, 5.6, 0.3, "CUARTO BIMESTRE 2026  |  30 PUNTOS", size=13, bold=True, color=TEAL_L)
tbox(s, "p.title", 1.1, 1.6, 5.6, 3.05,
     "Beneficios y\ndesafios de la\nautomatizacion\nde pruebas", size=36, bold=True, color=WHITE,
     spacing=1.05)
rect(s, 1.1, 4.8, 1.5, 0.05, fill=TEAL)
tbox(s, "p.sub", 1.1, 5.1, 5.5, 0.95,
     "Actividad 1: exposicion sobre la automatizacion y su impacto en el ciclo de pruebas "
     "de una aplicacion web real.", size=13, color=SLATE, spacing=1.2)
tbox(s, "p.who", 1.1, 6.3, 5.5, 0.8, ALUMNO + "\n" + CURSO, size=12.5, bold=True, color=TEAL_L,
     spacing=1.25)
for i, (big, small) in enumerate([("145", "pruebas automatizadas"), ("98 %", "de cobertura"),
                                  ("35 s", "de ejecucion total")]):
    y = 1.85 + i * 1.42
    rect(s, 7.75, y, 4.6, 1.12, fill=RGBColor(0x1E, 0x29, 0x3B), shape=MSO_SHAPE.ROUNDED_RECTANGLE,
         adj=0.1)
    rect(s, 7.75, y, 0.06, 1.12, fill=TEAL_L)
    tbox(s, f"p.stat{i}", 8.1, y + 0.14, 2.2, 0.55, big, size=28, bold=True, color=TEAL_L)
    tbox(s, f"p.statl{i}", 8.1, y + 0.7, 4.1, 0.3, small, size=12, color=RGBColor(0xCB, 0xD5, 0xE1))
tbox(s, "p.sys", 7.75, 6.25, 4.6, 0.35, "Sistema evaluado: chatbot municipal G.A.M. Sacaba", size=11.5,
     color=RGBColor(0x64, 0x74, 0x8B))
s.notes_slide.notes_text_frame.text = (
    "Buenos dias. Mi exposicion trata sobre los beneficios y los desafios de la automatizacion de pruebas. "
    "Para no quedarme en lo teorico, todos los datos que presento salen de mi proyecto real: el chatbot "
    "municipal del Gobierno Autonomo Municipal de Sacaba. A la derecha esta el resultado final: 145 "
    "pruebas que se ejecutan en 35 segundos y que alcanzan un 98 por ciento de cobertura de codigo."
)

# ------------------------------------------------------------- 2. contenido
s = slide_base("Contenido", "Recorrido de la exposicion",
               "Voy a seguir seis bloques: primero que es la automatizacion y por que se necesita; luego "
               "el problema de las pruebas manuales; despues los beneficios; luego los desafios; luego "
               "el caso real medido en mi proyecto; y por ultimo las conclusiones.")
for i, (n, t, sub) in enumerate([
    ("1", "Que es la automatizacion de pruebas", "Definicion y alcance"),
    ("2", "El problema de las pruebas manuales", "Costo, tiempo y riesgo humano"),
    ("3", "Beneficios de la automatizacion", "Velocidad, cobertura, consistencia"),
    ("4", "Desafios de la automatizacion", "Costo, mantenimiento y limites"),
    ("5", "Caso real: chatbot de Sacaba", "145 pruebas y 98 % de cobertura"),
    ("6", "Conclusiones", "Cuando conviene automatizar"),
]):
    col, row = i % 2, i // 2
    x, y = 0.75 + col * 6.2, 1.62 + row * 1.66
    rect(s, x, y, 5.65, 1.3, fill=LIGHT, line=BORDER, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.09)
    rect(s, x + 0.28, y + 0.34, 0.6, 0.6, fill=TEAL, shape=MSO_SHAPE.OVAL)
    tbox(s, f"c{n}.n", x + 0.28, y + 0.47, 0.6, 0.32, n, size=18, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER)
    tbox(s, f"c{n}.t", x + 1.05, y + 0.32, 4.4, 0.34, t, size=15, bold=True, color=INK)
    tbox(s, f"c{n}.s", x + 1.05, y + 0.72, 4.4, 0.3, sub, size=12, color=GRAY)

# ------------------------------------------------- 3. que es la automatizacion
s = slide_base("Fundamentos", "Que es la automatizacion de pruebas",
               "La automatizacion es escribir la prueba en un lenguaje de programacion para que la "
               "ejecute una maquina en lugar de una persona. Ojo con una confusion frecuente: automatizar "
               "no es usar una inteligencia artificial cualquiera, es crear un script reproducible que "
               "siempre hace lo mismo y siempre muestra el mismo resultado.")
bullets(s, "f3", [
    (0, "Es escribir la prueba en codigo para que la ejecute la maquina"),
    (1, "La persona define el caso una vez y el script lo repite ilimitadamente"),
    (0, "Responde a tres preguntas en cada entrega"),
    (1, "¿Dice el sistema lo que debe decir? (correccion)"),
    (1, "¿Lo dice siempre igual? (consistencia)"),
    (1, "¿Lo dice rapido? (rendimiento)"),
    (0, "No sustituye al criterio humano: el tester sigue decidiendo que probar"),
], 0.8, 1.55, 11.7)
rect(s, 0.8, 5.8, 11.7, 0.95, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.12)
rect(s, 0.8, 5.8, 0.09, 0.95, fill=TEAL_L)
tbox(s, "f3.key", 1.2, 6.02, 11.0, 0.5,
     "Idea clave: la automatizacion no hace la prueba mas inteligente, la hace mas repetible.", size=16,
     bold=True, color=WHITE)

# ----------------------------------------------- 4. problema pruebas manuales
s = slide_base("El problema", "El costo de las pruebas manuales",
               "Este es el punto de partida. En mi proyecto verificar el chatbot a mano exigia unos 145 "
               "casos. A un ritmo de dos minutos por caso son casi cinco horas por entrega. Con scripts se "
               "reduce a 35 segundos. Esa diferencia es la que justifica automatizar.")
rect(s, 0.8, 1.5, 5.7, 2.2, fill=LIGHT, line=BORDER, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.06)
tbox(s, "m4.a", 1.1, 1.72, 5.1, 0.35, "Pruebas manuales", size=17, bold=True, color=AMBER)
tbox(s, "m4.b", 1.1, 2.2, 5.1, 1.3,
     "145 casos x 2 minutos\n= 4 h 50 min por entrega\n\nEl tester se cansa y deja de\nrevisar los ultimos casos.",
     size=13.5, color=GRAY, spacing=1.2)
rect(s, 6.85, 1.5, 5.7, 2.2, fill=LIGHT, line=BORDER, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.06)
tbox(s, "m4.c", 7.15, 1.72, 5.1, 0.35, "Pruebas automatizadas", size=17, bold=True, color=TEAL)
tbox(s, "m4.d", 7.15, 2.2, 5.1, 1.3,
     "145 casos ejecutados por codigo\n= 35 segundos\n\nEl resultado es siempre identico y el\nequipo analiza, no transcribe.",
     size=13.5, color=GRAY, spacing=1.2)
bullets(s, "m4", [
    (0, "Errores humanos: un olvido en la ultima fila de la tabla de verificacion"),
    (0, "Tiempo que no se invierte en disenar nuevas pruebas"),
    (0, "Resultados que dependen de quien ejecuto, no del sistema"),
], 0.8, 4.05, 11.7)

# ------------------------------------------------------------ 5. beneficios I
s = slide_base("Beneficios", "Beneficios (1 de 2): velocidad, cobertura y consistencia",
               "Estos tres beneficios se notan en el dia a dia. La velocidad se ve en el cronograma, la "
               "cobertura permite revisar casos que a mano se escaparian, y la consistencia elimina el "
               "factor humano de los resultados.")
card(s, "b5.1", 0.8, 1.5, 3.7, 2.4, "Velocidad", "La suite corre en segundos y se puede lanzar en cada "
     "cambio de codigo. En mi proyecto: 145 pruebas en 35 segundos.", TEAL, "1")
card(s, "b5.2", 4.82, 1.5, 3.7, 2.4, "Cobertura", "Permite revisar cientos de casos y combinaciones de datos "
     "que nadie comprobaria a mano por falta de tiempo.", BLUE, "2")
card(s, "b5.3", 8.84, 1.5, 3.7, 2.4, "Consistencia", "El mismo caso da siempre el mismo resultado, sin "
     "depender del estado de animo ni del cansancio del tester.", AMBER, "3")
bullets(s, "b5", [
    (0, "Ademas el resultado queda registrado y es comparable entre versiones"),
    (0, "Una regresion se detecta en minutos y no en la semana siguiente"),
], 0.8, 4.3, 11.7)

# ----------------------------------------------------------- 6. beneficios II
s = slide_base("Beneficios", "Beneficios (2 de 2): deteccion temprana, evidencia y metricas",
               "Aqui respondo a la segunda parte de la pregunta del docente. Los beneficios no son solo "
               "de tiempo: tambien generan informacion que antes no existia, como la cobertura o el tiempo "
               "de ejecucion por modulo.")
card(s, "b6.1", 0.8, 1.5, 3.7, 2.4, "Deteccion temprana", "Un fallo encontrado el mismo dia cuesta "
     "mucho menos que un fallo encontrado en la entrega final.", TEAL, "4")
card(s, "b6.2", 4.82, 1.5, 3.7, 2.4, "Evidencia automatica", "Cada ejecucion produce un reporte con "
     "estado, duracion y linea de codigo afectada.", BLUE, "5")
card(s, "b6.3", 8.84, 1.5, 3.7, 2.4, "Metricas de calidad", "Permite medir cobertura, estabilidad y "
     "tiempo de respuesta, y comparar el estado entre entregas.", AMBER, "6")
rect(s, 0.8, 4.25, 11.7, 0.9, fill=LIGHT, line=BORDER, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.12)
tbox(s, "b6.k", 1.2, 4.45, 11.0, 0.62,
     "Dato propio del proyecto: la cobertura con coverage.py fue de 98 %, por encima del 90 % que "
     "plantea el objetivo de calidad del curso.", size=14, bold=True, color=INK)

# --------------------------------------------------------- 7. desafios I
s = slide_base("Desafios", "Desafios (1 de 2): costo, mantenimiento y aprendizaje",
               "Ahora la parte incomoda. Automatizar no es gratis. El primer costo es construir el "
               "framework y el segundo, mas importante, es mantenerlo: cada vez que el sitio web cambia "
               "un boton, el script puede romperse.")
bullets(s, "d7", [
    (0, "Costo inicial de inversion"),
    (1, "Escribir el framework y preparar los datos de prueba"),
    (1, "En un proyecto pequeno puede no amortizarse nunca"),
    (0, "Mantenimiento de los scripts"),
    (1, "Los localizadores se rompen cuando el HTML cambia"),
    (1, "Una suite abandonada da falsa confianza y hay que mantenerla viva"),
    (0, "Curva de aprendizaje"),
    (1, "Exige saber programar ademas de la disciplina de pruebas"),
    (1, "En equipos pequenos el costo de aprender supera el beneficio inmediato"),
], 0.8, 1.5, 11.7, step=0.5)

# -------------------------------------------------------- 8. desafios II
s = slide_base("Desafios", "Desafios (2 de 2): los limites de la automatizacion",
               "El error mas comun es creer que con todo automatizado esta todo resuelto. La "
               "automatizacion no evalua la usabilidad, no juzga si el mensaje del chatbot es claro para "
               "un vecino y no detecta por si sola un requisito mal entendido. Por eso la cobertura de "
               "codigo es una metrica, no una garantia de calidad.")
card(s, "d8.1", 0.8, 1.5, 3.7, 2.55, "Falsa seguridad", "Una cobertura del 98 % del codigo no "
     "garantiza que el producto sea util: puede haber mucho codigo probado que no sirve.", AMBER, "!")
card(s, "d8.2", 4.82, 1.5, 3.7, 2.55, "No se automatiza todo", "La usabilidad, la comprension del "
     "mensaje y las decisiones de diseno siguen dependiendo de la persona.", BLUE, "!")
card(s, "d8.3", 8.84, 1.5, 3.7, 2.55, "Entorno y datos", "Los scripts dependen del navegador, de la "
     "red y de los datos de prueba: tres fuentes de fallos externos al sistema.", TEAL, "!")
bullets(s, "d8", [
    (0, "Conclusion parcial: la automatizacion cubre lo repetitivo y verificable"),
    (0, "El criterio humano sigue siendo obligatorio para lo que no se puede medir"),
], 0.8, 4.45, 11.7)

# ------------------------------------------------------- 9. tabla benef/desaf
s = slide_base("Sintesis", "Beneficios frente a desafios en una sola mirada",
               "Esta tabla es el resumen que dejo, para que se vea el equilibrio. Ningun beneficio es "
               "gratis: cada uno tiene un desafio asociado. La estrategia correcta es aceptar el costo de "
               "mantener la suite a cambio de la velocidad y la consistencia.")
RH = 0.62
rect(s, 0.8, 1.45, 5.7, 0.5, fill=TEAL)
tbox(s, "t9.a", 1.0, 1.57, 5.3, 0.28, "BENEFICIO", size=13, bold=True, color=WHITE)
rect(s, 6.85, 1.45, 5.7, 0.5, fill=AMBER)
tbox(s, "t9.b", 7.05, 1.57, 5.3, 0.28, "DESAFIO ASOCIADO", size=13, bold=True, color=WHITE)
for i, (a, b, c) in enumerate([
    ("Velocidad de ejecucion", "35 segundos frente a casi 5 horas", "Alta inversion inicial"),
    ("Consistencia de resultados", "Mismo resultado siempre", "Scripts que hay que mantener"),
    ("Cobertura de casos", "145 casos y 98 % del codigo", "No mide usabilidad"),
    ("Evidencia de calidad", "Reporte automatico por caso", "Falta criterio humano"),
    ("Deteccion temprana", "Fallos el mismo dia", "Requiere equipo capacitado"),
    ("Metricas de calidad", "Cobertura y tiempos comparables", "Datos y entorno inestable"),
]):
    y = 2.04 + i * (RH + 0.07)
    rect(s, 0.8, y, 5.7, RH, fill=LIGHT if i % 2 == 0 else WHITE, line=BORDER)
    rect(s, 6.85, y, 5.7, RH, fill=RGBColor(0xFF, 0xF7, 0xED) if i % 2 == 0 else WHITE, line=BORDER)
    tbox(s, f"t9.c{i}", 1.0, y + 0.08, 2.35, 0.45, a, size=12, bold=True, color=INK)
    tbox(s, f"t9.d{i}", 3.35, y + 0.1, 3.05, 0.45, b, size=11, color=GRAY)
    tbox(s, f"t9.e{i}", 7.05, y + 0.17, 5.3, 0.35, c, size=12, bold=True, color=AMBER)

# ----------------------------------------------------------- 10. caso real
s = slide_base("Caso real", "Que ocurrio al aplicarlo al chatbot de Sacaba",
               "Este es el trabajo practico que respalda toda la exposicion. Dividi las pruebas en tres "
               "niveles: unitarias para el motor del chatbot, caja negra para la API vista desde fuera y "
               "caja blanca para forzar cada rama del codigo. El resultado es una base de 145 pruebas que "
               "equivale a casi cinco horas de trabajo manual.")
card(s, "r10.1", 0.8, 1.5, 3.7, 2.55, "Pruebas unitarias", "62 casos sobre el motor: deteccion de "
     "tramites, intencion y detector de idioma (espanol y quechua).", TEAL, "62")
card(s, "r10.2", 4.82, 1.5, 3.7, 2.55, "Pruebas de caja negra", "39 casos sobre la API real: "
     "particion de equivalencia y valores limite en /chat y /language.", BLUE, "39")
card(s, "r10.3", 8.84, 1.5, 3.7, 2.55, "Pruebas de caja blanca", "44 casos que recorren cada decision "
     "(if, for, ternario) del codigo con datos simulados.", AMBER, "44")
bullets(s, "r10", [
    (0, "Resultado: 145 pruebas, 98 % de cobertura y 4 bugs reales detectados antes de la entrega"),
    (0, "El mismo criterio se aplica ahora con Selenium sobre la interfaz real del portal"),
], 0.8, 4.4, 11.7)

# ----------------------------------------------------------- 11. conclusiones
s = slide_base("Cierre", "Conclusiones",
               "Cierro con la idea que quiero que se lleven. Automatizar no es un fin, es un medio. Cuando "
               "la respuesta es si, la ganancia es enorme; cuando se usa por obligacion en un proyecto "
               "pequeno, es una carga que nadie mantiene.")
bullets(s, "k11", [
    (0, "Automatizar es invertir hoy para ahorrar tiempo y riesgo cada dia"),
    (0, "Los beneficios mas notorios: velocidad, consistencia y deteccion temprana"),
    (0, "Los mayores desafios: mantenimiento, costo inicial y limites de alcance"),
    (0, "Debe aplicarse donde el caso es repetitivo y verificable de forma objetiva"),
    (0, "No reemplaza la revision humana: la combina y la potencia"),
], 0.8, 1.5, 11.7)
rect(s, 0.8, 4.5, 11.7, 1.7, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.08)
rect(s, 0.8, 4.5, 0.09, 1.7, fill=TEAL_L)
tbox(s, "k11.t", 1.2, 4.72, 11.0, 0.32, "Reflexion final", size=15, bold=True, color=TEAL_L)
tbox(s, "k11.b", 1.2, 5.15, 11.0, 0.9,
     "En el chatbot de Sacaba, 145 pruebas que antes ocupaban casi cinco horas se resuelven en 35 "
     "segundos: esa es la medida concreta de lo que aporta la automatizacion.", size=14, color=WHITE,
     spacing=1.2)

# -------------------------------------------------------------- 12. referencias
s = slide_base("Anexo", "Referencias consultadas",
               "Estas son las fuentes que me sirvieron para construir el contenido teorico y las practicas "
               "de esta exposicion.")
cy = 1.5
for i, r in enumerate([
    "Documentacion oficial de Selenium WebDriver (selenium.dev) - manual de pruebas.",
    "Documentacion oficial de Playwright (playwright.dev) -arquitectura y depuracion.",
    "Documentacion oficial de Cypress (docs.cypress.io) -ciclo de pruebas.",
    "Documentacion de Chrome DevTools (developer.chrome.com) -paneles Network y Elements.",
    "Python Software Foundation - modulo unittest, base estandar de pruebas.",
    "pytest.org - fixtures, parametrizacion y reporte JUnit XML.",
    "coverage.py - medicion de cobertura de sentencias y ramas.",
    "Documentacion oficial de Flask - rutas HTTP y cliente de prueba.",
    "Grockit, A. y Williams, C. - Real World Software Testing (3a edicion).",
    "ISTQB Syllabus v4.0 - fundamentos de pruebas y nivel de automatizacion.",
]):
    n = i + 1
    rect(s, 0.8, cy + 0.02, 0.32, 0.32, fill=LIGHT, line=BORDER, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
         adj=0.3)
    tbox(s, f"r{n}.n", 0.8, cy + 0.09, 0.32, 0.24, str(n), size=10, bold=True, color=TEAL,
         align=PP_ALIGN.CENTER)
    tbox(s, f"r{n}.t", 1.28, cy + 0.06, 11.2, 0.32, r, size=13, color=INK)
    cy += 0.52

PPTX = os.path.join(OUT_DIR, "Exposicion_1_Beneficios_y_Desafios_de_la_Automatizacion.pptx")
prs.save(PPTX)
print("PPTX:", os.path.getsize(PPTX), "bytes |", len(prs.slides._sldIdLst), "diapositivas")
if AUDIT:
    print("\nAUDITORIA (%d avisos):" % len(AUDIT))
    for a in AUDIT:
        print("  -", a)
else:
    print("AUDITORIA: sin desbordes de texto.")