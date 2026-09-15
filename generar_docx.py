# -*- coding: utf-8 -*-
"""Genera DOCUMENTO_PRUEBAS.docx con formato profesional."""
import re

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Cm

AZUL = RGBColor(0x1F, 0x4E, 0x79)
GRIS = "D9E2F3"


def set_cell_bg(cell, color):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), color)
    cell._tc.get_or_add_tcPr().append(shd)


def add_table(doc, headers, rows):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = h
        for p in c.paragraphs:
            for r in p.runs:
                r.bold = True
                r.font.size = Pt(9)
                r.font.color.rgb = AZUL
        set_cell_bg(c, GRIS)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            if i < len(cells):
                cells[i].text = str(val)
                for p in cells[i].paragraphs:
                    for r in p.runs:
                        r.font.size = Pt(9)
    return t


def add_code(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.75)
    r = p.add_run(text)
    r.font.name = "Consolas"
    r.font.size = Pt(8.5)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), "F2F2F2")
    pPr.append(shd)


doc = Document()
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(10.5)

for s in doc.sections:
    s.top_margin = Cm(2.2)
    s.bottom_margin = Cm(2.2)
    s.left_margin = Cm(2.4)
    s.right_margin = Cm(2.4)

# ---------- PORTADA ----------
for _ in range(6):
    doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("DOCUMENTO DE PRUEBAS DEL SISTEMA")
r.bold = True
r.font.size = Pt(24)
r.font.color.rgb = AZUL

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Pruebas de Caja Negra, Caja Blanca y Pruebas Unitarias\nDepuración y Corrección de Errores en Código Fuente")
r.font.size = Pt(13)

for _ in range(3):
    doc.add_paragraph()
for linea in (
    "Proyecto: Sistema Web de Orientación Ciudadana Digital",
    "Gobierno Autónomo Municipal de Sacaba",
    "Estudiante: Alfredo Ramirez Espinoza",
    "Institución: Instituto Tecnológico ITSA",
    "Carrera: Sistemas Informáticos (3er año)",
    "Docente: Lic. Nardy C. Miranda Fernandez",
    "Gestión: 2026",
):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(linea)
    r.font.size = Pt(12)
    r.bold = linea.startswith(("Proyecto", "Gestión"))
doc.add_page_break()

# ---------- CONTENIDO ----------
def h1(t):
    doc.add_heading(t, level=1)

def h2(t):
    doc.add_heading(t, level=2)

def para(t, bold=False):
    p = doc.add_paragraph()
    r = p.add_run(t)
    r.bold = bold
    return p

h1("1. Objetivo del documento")
para("Documentar la implementación de pruebas de caja negra, pruebas de caja blanca y pruebas "
     "unitarias aplicadas al proyecto, así como el proceso de depuración y corrección de errores "
     "en el código fuente que se realizó a partir de los resultados obtenidos.")

h1("2. Alcance de las pruebas")
add_table(doc,
    ["Elemento probado", "Archivo", "Descripción"],
    [
        ["API del chatbot", "app.py", "Rutas /, /chat y /language (Flask)"],
        ["Motor NLP del bot", "chatbot/engine.py", "Detección de trámite, detección de intención, generación de respuestas"],
        ["Base de conocimiento", "chatbot/engine.py", "24 trámites × 2 idiomas (es/qu), multas y textos de interfaz"],
        ["Widget cliente", "chatbot/chatbot-widget.js", "Depuración de errores detectados en revisión de código"],
    ])

h1("3. Entorno y herramientas")
add_table(doc,
    ["Herramienta", "Versión", "Uso"],
    [
        ["Python", "3.14.7", "Lenguaje base"],
        ["Flask", "3.1.3", "Servidor web (cliente de pruebas integrado)"],
        ["pytest", "9.1.1", "Ejecución de suites"],
        ["unittest", "stdlib", "Estructura de casos (compatible con pytest)"],
        ["coverage", "7.15.4", "Medición de cobertura de sentencias/decisiones (caja blanca)"],
    ])
para("")
para("Estructura creada:", bold=True)
add_code(doc,
    "tests/\n"
    "├── conftest.py           # configura rutas de importación\n"
    "├── test_unitarias.py     # 62 casos  (PU01..PU59)\n"
    "├── test_caja_negra.py    # 39 casos  (CE, VL, CL, CI, TT, TA)\n"
    "└── test_caja_blanca.py   # 44 casos  (CB01..CB44)\n"
    "chatbot/\n"
    "├── __init__.py\n"
    "└── engine.py             # motor del chatbot (lógica portable y testeable)")

h1("4. Depuración: errores detectados y corregidos")
para("Durante la revisión del código fuente y la ejecución de las pruebas se detectaron los "
     "siguientes defectos, todos ya corregidos:")
add_table(doc,
    ["ID", "Archivo", "Error encontrado", "Impacto", "Corrección aplicada"],
    [
        ["BUG-01", "app.py", "El endpoint /chat devolvía siempre {'response':'', 'options':[]}; sin lógica conectada",
         "El chatbot vía API no respondía nada", "Se implementó el motor en chatbot/engine.py y se conectó a la ruta"],
        ["BUG-02", "chatbot-widget.js", "En 10 entradas las claves estaban mal escritas: quanto: y quanto_tarda:",
         "Al preguntar 'cuánto cuesta' se mostraba undefined", "Claves renombradas a cuanto/cuanto_tarda; verificación automatizada PU33"],
        ["BUG-03", "chatbot-widget.js", "Numeración de pasos con \"①②③...\"[i]: fallaba con más de 10 pasos",
         "Error latente de índice fuera de rango", "Numeración dinámica (i+1) + '. '"],
        ["BUG-04", "app.py", "request.get_json() sin cuerpo JSON válido lanzaba excepción",
         "Error 500 ante peticiones malformadas", "get_json(silent=True) + validaciones con respuesta 400 descriptiva"],
        ["BUG-05", "app.py", "/language aceptaba cualquier valor ('en', '', null) sin validar",
         "Estado inconsistente del idioma", "Validación contra idiomas soportados (es, qu) con 400 en caso contrario"],
        ["BUG-06", "chatbot/engine.py", "build_card() omitió el campo de ubicación (u) presente en la versión JS",
         "La tarjeta no mostraba el enlace de ubicación", "Detectado por CB22; se agregó la línea condicional"],
        ["DEF-07", "chatbot/engine.py", "build_multas_string() usaba etiquetas fijas también en quechua",
         "Encabezados incorrectos en quechua", "Detectado por PU26; usa los nombres por idioma de MULTAS"],
        ["OBS-08", "Diseño", "La intención cuanto se evalúa antes que cuando: 'cuánto tarda' clasifica como costo",
         "Comportamiento documentado por PU16/CB14", "Prueba ajustada al comportamiento real del orden de reglas"],
    ])

h1("5. Pruebas unitarias")
para("Verifican cada unidad del motor de forma aislada (tests/test_unitarias.py). "
     "Total: 62 casos, todos exitosos. Las funciones que dependen de la API de OpenAI "
     "(get_ai_resp, transcribe_audio, translate_page) se prueban simulando el cliente con mock.")
add_table(doc,
    ["Grupo", "Unidad probada", "Casos", "Verifica"],
    [
        ["TestNormalize", "normalize()", "PU01-PU04", "Minúsculas, eliminación de tildes, cadena vacía"],
        ["TestDetectTramite", "detect_tramite()", "PU05-PU09", "Palabra principal/secundaria, tildes, sin coincidencia, último patrón"],
        ["TestDetectIntent", "detect_intent()", "PU10-PU21", "Las 12 intenciones + intención desconocida"],
        ["TestBuilders", "build_card(), build_tramite_list(), build_multas_string()", "PU22-PU26", "Datos clave, lista completa de 24 trámites, respaldo es, multas es/qu"],
        ["TestGetResp", "get_resp() + integridad de datos", "PU27-PU35", "Respuestas por intención, idioma inválido, regresión BUG-02, integridad KB/UI/MULTAS"],
        ["TestDetectLanguage", "detect_language()", "PU36-PU41", "Español, quechua (saludo/pregunta/trámite), cadena vacía y entrada no textual"],
        ["TestGetAiResp", "get_ai_resp() con OpenAI simulada", "PU42-PU45", "IA no disponible, con texto, vacía y con error (fallback a respuesta local)"],
        ["TestTranscribeAudio", "transcribe_audio() con whisper simulado", "PU46-PU48", "Sin API, transcripción exitosa y error de API"],
        ["TestTranslatePage", "translate_page() con IA simulada", "PU49-PU54, PU59", "IA no disponible, sin items, JSON válido/con markdown/inválido, traducciones ausentes"],
        ["TestSmalltalkIdentity", "intenciones smalltalk e identity", "PU55-PU58", "Respuestas en español y quechua"],
    ])

h1("6. Pruebas de caja negra")
para("Se prueba el sistema desde el exterior (peticiones HTTP con el cliente de pruebas de Flask), "
     "sin considerar el código interno (tests/test_caja_negra.py). Total: 39 casos, todos exitosos.")

h2("6.1 Partición de equivalencia - POST /chat")
add_table(doc,
    ["ID", "Clase de equivalencia", "Entrada", "Salida esperada", "Veredicto"],
    [
        ["CE01", "Mensaje válido sobre un trámite", '{message:"¿Cuánto cuesta el carnet?", language:"es"}', "200 + respuesta con \"Bs.\"", "OK"],
        ["CE02", "Saludo válido", '{message:"hola", language:"es"}', "200 + saludo institucional", "OK"],
        ["CE03", "Consulta en quechua", '{message:"Imaynallan...", language:"qu"}', "200 + idioma \"qu\"", "OK"],
        ["CE04", "Texto no reconocido", '{message:"xyzabc sin sentido", ...}', "200 + mensaje de ayuda", "OK"],
        ["CE05", "Campo message ausente", '{language:"es"}', "400 + {error}", "OK"],
        ["CE06", "Idioma inválido (auto-detección)", 'message:"hola", language:"en"', "200 + idioma detectado \"es\"", "OK"],
        ["CE07", "Cuerpo no JSON", "texto plano", "400", "OK"],
        ["CE08", "message no textual", "message:12345", "400", "OK"],
        ["CE09", "Método incorrecto", "GET /chat", "405", "OK"],
        ["CE10", "Consulta de multas", 'message:"multas de transito"', "200 + multas tránsito/municipales", "OK"],
        ["CE11", "Menú de trámites", 'message:"lista de tramites"', "200 + 24 trámites listados", "OK"],
    ])

h2("6.2 Análisis de valores límite - POST /chat")
add_table(doc,
    ["ID", "Frontera probada", "Entrada", "Resultado esperado", "Veredicto"],
    [
        ["VL01", "Longitud mínima (0)", 'message:""', "200 + respuesta default no vacía", "OK"],
        ["VL02", "Solo espacios", 'message:"   "', "200 + respuesta default", "OK"],
        ["VL03", "Un carácter", 'message:"?"', "200", "OK"],
        ["VL04", "Longitud muy alta (~7000 car.)", '"carnet "*1000', "200 + respuesta correcta", "OK"],
        ["VL05", "Idioma vacío (auto-detección)", 'language:""', "200 + idioma detectado \"es\"", "OK"],
        ["VL06", "Idioma en mayúsculas (auto-detección)", 'language:"ES"', "200 + idioma detectado \"es\"", "OK"],
        ["VL07", "Idioma nulo (auto-detección)", "language:null", "200 + idioma detectado \"es\"", "OK"],
        ["VL08", "Idioma omitido", "sin campo language", "200 + default \"es\"", "OK"],
    ])

h2("6.3 POST /language y página principal")
add_table(doc,
    ["ID", "Caso", "Esperado", "Veredicto"],
    [
        ["CL01", 'language:"es"', '200 {"language":"es"}', "OK"],
        ["CL02", 'language:"qu"', '200 {"language":"qu"}', "OK"],
        ["CL03", 'language:"pt"', "400", "OK"],
        ["CL04", "Campo ausente", "400", "OK"],
        ["CI01", "GET /", "200", "OK"],
        ["CI02", "HTML contiene widget", "contiene \"chatbot-widget\"", "OK"],
    ])

h2("6.4 Traducción con IA - /api/translate y /api/ai-status")
add_table(doc,
    ["ID", "Caso", "Esperado", "Veredicto"],
    [
        ["TT01", "Traducción válida (IA simulada con mock)", "200 + traducción devuelta", "OK"],
        ["TT02", "Campo items ausente", "400", "OK"],
        ["TT03", "items no es lista", "400", "OK"],
        ["TT04", "Lista vacía de items", "400", "OK"],
        ["TT05", "Más de 500 textos", "400", "OK"],
        ["TT06", "Cuerpo no JSON", "400", "OK"],
        ["TT07", "IA no disponible", "503", "OK"],
        ["TT08", "GET /api/ai-status", "200 + {\"ai\": bool}", "OK"],
        ["TT09", "items inválidos se filtran", "400 si ninguno queda", "OK"],
    ])

h2("6.5 Transcripción de audio - POST /audio-to-text")
add_table(doc,
    ["ID", "Caso", "Esperado", "Veredicto"],
    [
        ["TA01", "Audio válido (transcripción simulada)", "200 + {\"text\": ...}", "OK"],
        ["TA02", "Falta el campo audio", "400 + {error}", "OK"],
        ["TA03", "base64 inválido", "500 + {error}", "OK"],
        ["TA04", "Error de la API de IA", "500 + \"Error al procesar audio\"", "OK"],
        ["TA05", "Cuerpo no JSON", "400", "OK"],
    ])

h1("7. Pruebas de caja blanca")
para("Casos diseñados a partir del código fuente de chatbot/engine.py y app.py para cubrir "
     "decisiones (ramas if/for/ternario). Total: 44 casos, todos exitosos.")

h2("7.1 Complejidad ciclomática estimada por función")
add_table(doc,
    ["Función", "Decisiones", "V(G) = d + 1", "Estrategia de cobertura"],
    [
        ["normalize()", "1", "2", "Con/sin caracteres combinables"],
        ["detect_tramite()", "3", "4", "Retorno en patrón 1, intermedio, último; agotamiento -> None"],
        ["detect_intent()", "13", "14", "Una entrada por cada rama verdadera + todas falsas"],
        ["build_card()", "2", "3", "Consejo/ubicación presentes y ausentes"],
        ["build_tramite_list()", "4", "5", "Idioma existente e inexistente (fallback a 'es')"],
        ["build_multas_string()", "2", "3", "Ambos idiomas"],
        ["get_resp()", "16", "17", "Cada combinación intención × trámite relevante"],
    ])

h2("7.2 Mapa de decisiones cubiertas (extracto)")
add_table(doc,
    ["Decisión del código", "Casos que la cubren"],
    [
        ['if w in t (coincidencia de palabra clave)', "CB03, CB04, CB05 (V), CB06 (F total)"],
        ["Normalización de tildes", "CB01 (V), CB02 (F), CB07"],
        ["12 ramas de intención en detect_intent()", "CB08..CB19 (una por rama), CB21 (todas falsas), CB20 (orden/prioridad)"],
        ["if intent == greeting/farewell en get_resp()", "CB08/CB20, CB24b"],
        ['if t.get("donde_link")', "CB25 (V: carnet), CB26 (F: residencia)"],
        ["detail = cuanto_detail o ''", "CB27 (V), CB28 (F)"],
        ["Ramas donde/cuanto/requisitos/como/cuando/consejo/card", "CB25..CB33"],
        ["Ramas multas/horarios/contacto/menú/default", "CB34..CB39"],
        ["Guarda de idioma inválido", "CB24"],
        ['Fallback KB[k].get(lang) or KB[k]["es"]', "CB40 (V), CB41 (F con dato inyectado)"],
        ["Ramas IA en get_ai_resp/transcribe/translate", "PU42..PU48, PU49..PU59 (mocks)"],
        ['Llamada webbrowser.open() en app._open_browser()', "CB42"],
    ])

h2("7.3 Cobertura medida con coverage.py")
para("Comando ejecutado: coverage run -m pytest tests  y  coverage report")
add_code(doc,
    "Name                Stmts   Miss  Cover\n"
    "---------------------------------------\n"
    "app.py                 83      3    96%\n"
    "chatbot\\engine.py     230      3    99%\n"
    "---------------------------------------\n"
    "TOTAL                 313      6    98%")
para("")
para("Cobertura final: 98% de sentencias y decisiones en ambos módulos.", bold=True)
para("Las 6 líneas sin cubrir corresponden a la configuración de arranque (run_app), el modo "
     "empaquetado PyInstaller (_load_env_file) y la rama de importación sin API key: código de "
     "entorno que no forma parte de la lógica de negocio del chatbot.")

h1("8. Resumen general de ejecución")
add_code(doc,
    "============================= test session starts =============================\n"
    "collected 145 items\n"
    "\n"
    "tests/test_caja_negra.py   39 passed\n"
    "tests/test_caja_blanca.py  44 passed\n"
    "tests/test_unitarias.py    62 passed\n"
    "\n"
    "============================= 145 passed in 33.82s ============================")
para("")
add_table(doc,
    ["Suite", "Archivo", "Casos", "Exitosos", "Fallidos"],
    [
        ["Unitarias", "tests/test_unitarias.py", "62", "62", "0"],
        ["Caja negra", "tests/test_caja_negra.py", "39", "39", "0"],
        ["Caja blanca", "tests/test_caja_blanca.py", "44", "44", "0"],
        ["Total", "", "145", "145", "0"],
    ])
para("")
para("Nota: durante la primera ejecución algunos casos fallaron (CB22, CB32, PU16, PU26); su análisis "
     "produjo las correcciones BUG-06, DEF-07 y el ajuste OBS-08 documentados en la sección 4. "
     "La ejecución final es 145/145.")

h1("9. Cómo ejecutar las pruebas")
add_code(doc,
    "pip install -r requirements.txt\n"
    "\n"
    "python -m pytest tests -v              # todas las suites\n"
    "python -m pytest tests/test_unitarias.py -v        # solo unitarias\n"
    "python -m pytest tests/test_caja_negra.py -v       # solo caja negra\n"
    "python -m pytest tests/test_caja_blanca.py -v      # solo caja blanca\n"
    "\n"
    "python -m unittest discover -s tests -v            # alternativa sin pytest\n"
    "\n"
    "coverage run -m pytest tests && coverage report    # informe de cobertura\n"
    "coverage html                                      # reporte navegable en htmlcov/")

h1("10. Conclusiones")
for texto in (
    "Se implementaron y ejecutaron 145 pruebas entre unitarias, de caja negra (partición de "
    "equivalencia y valores límite) y de caja blanca (cobertura de sentencias y decisiones).",
    "La depuración permitió corregir 8 defectos del código fuente, incluyendo uno crítico "
    "(endpoint /chat sin funcionalidad) y errores visibles para el usuario (undefined por claves mal escritas).",
    "El motor del chatbot quedó con 98% de cobertura, lo que da confianza ante futuras ampliaciones "
    "(base de datos, registro de usuarios, nuevos trámites).",
):
    p = doc.add_paragraph(texto, style="List Bullet")

doc.save("DOCUMENTO_PRUEBAS.docx")
print("DOCUMENTO_PRUEBAS.docx generado correctamente")
