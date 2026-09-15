# -*- coding: utf-8 -*-
"""
Genera CAPITULO_III_INGENIERIA.docx
Capítulo III: Ingeniería del Proyecto - Chatbot Municipal Sacaba
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
# PORTADA CAPÍTULO III
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

doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Chatbot Web Multiidioma (Castellano–Quechua)\npara Trámites y Multas Municipales\nGobierno Autónomo Municipal de Sacaba")
r.font.size = Pt(13)
r.italic = True

doc.add_page_break()

# =====================================================================
# 3.1 REQUERIMIENTOS GENERALES DEL SISTEMA
# =====================================================================
h1("3.1 REQUERIMIENTOS GENERALES DEL SISTEMA")

h2("3.1.1 Requerimientos Funcionales Generales")

styled_table(doc,
    ["ID", "Requerimiento", "Descripción"],
    [
        ["RF-01", "Consulta de trámites", "El sistema permitirá consultar información sobre 25 trámites municipales incluyendo requisitos, costos, procedimientos y ubicaciones."],
        ["RF-02", "Consulta de multas", "El sistema brindará información sobre multas de tránsito y municipales, incluyendo montos, infracciones y procedimientos de pago."],
        ["RF-03", "Chatbot interactivo", "El sistema incluirá un asistente virtual que responda consultas en lenguaje natural mediante respuestas predeterminadas."],
        ["RF-04", "Soporte bilingüe", "El sistema deberá presentar la interfaz y los contenidos en castellano y quechua, permitiendo cambio de idioma."],
        ["RF-05", "Búsqueda de trámites", "El usuario podrá buscar trámites por palabra clave y filtrar por categorías (Identidad, Vivienda, Negocio, Servicios)."],
        ["RF-06", "Navegación por secciones", "El sitio contará con menú de navegación para acceder a: Inicio, Trámites, Multas, Institución y Contacto."],
        ["RF-07", "Entrada de voz", "El chatbot permitirá enviar mensajes de voz que serán transcritos a texto mediante IA."],
        ["RF-08", "Traducción con IA", "El sistema utilizará inteligencia artificial para traducir elementos de la interfaz a quechua."],
        ["RF-09", "Información institucional", "El sistema mostrará horarios, ubicación, teléfono y correo del GAM Sacaba."],
        ["RF-10", "Accesos rápidos", "El sitio incluirá accesos directos a los trámites más consultados (carnet, residencia, licencia, catastro, vehículos, multas)."],
    ])

h2("3.1.2 Requerimientos No Funcionales Generales")

styled_table(doc,
    ["ID", "Requerimiento", "Descripción"],
    [
        ["RNF-01", "Disponibilidad", "El sistema estará disponible las 24 horas del día, los 7 días de la semana."],
        ["RNF-02", "Tiempo de respuesta", "El chatbot responderá en menos de 3 segundos para consultas predefinidas."],
        ["RNF-03", "Compatibilidad", "El sitio será compatible con Chrome, Firefox, Safari y Edge en desktop y móvil."],
        ["RNF-04", "Diseño responsivo", "La interfaz se adaptará a dispositivos de 320px a 1920px de ancho."],
        ["RNF-05", "Usabilidad", "La interfaz será intuitiva y no requerirá instrucciones de uso."],
        ["RNF-06", "Escalabilidad", "La arquitectura permitirá agregar nuevos trámites sin modificar el código fuente."],
        ["RNF-07", "Seguridad", "El sistema no almacenará datos personales de los usuarios."],
        ["RNF-08", "Mantenibilidad", "El código será modular y documentado para facilitar actualizaciones."],
    ])

h2("3.1.3 Identificación y Descripción de los Actores del Sistema")

styled_table(doc,
    ["Actor", "Tipo", "Descripción", "Interacciones"],
    [
        ["Ciudadano", "Principal", "Usuario que consulta información sobre trámites y multas municipales", "Consulta trámites, usa el chatbot, cambia de idioma, consulta multas"],
        ["Asistente Virtual (Chatbot)", "Sistema", "Bot que responde consultas mediante respuestas predefinidas e IA", "Recibe mensajes, detecta intención, retorna información"],
        ["Administrador", "Secundario", "Personal del GAM que actualiza la base de conocimientos", "Actualiza trámites, modifica horarios, gestiona información"],
    ])

add_image_placeholder(doc,
    "Figura 7: Actores del Sistema",
    "Diagrama de actores mostrando al Ciudadano (usuario principal), "
    "el Chatbot (sistema) y el Administrador (gestor de contenido). "
    "El ciudadano interactúa con el chatbot y la interfaz web. "
    "El administrador gestiona la base de conocimientos.")

h2("3.1.4 Diagrama de Casos de Usos General")

styled_table(doc,
    ["ID", "Caso de Uso", "Actor", "Descripción"],
    [
        ["CU-01", "Consultar trámite", "Ciudadano", "El ciudadano busca y consulta información de un trámite específico"],
        ["CU-02", "Buscar trámite", "Ciudadano", "El ciudadano utiliza el buscador para encontrar trámites por palabra clave"],
        ["CU-03", "Filtrar por categoría", "Ciudadano", "El ciudadano filtra trámites por categoría (Identidad, Vivienda, etc.)"],
        ["CU-04", "Consultar multas", "Ciudadano", "El ciudadano consulta información sobre multas y formas de pago"],
        ["CU-05", "Usar chatbot", "Ciudadano", "El ciudadano interactúa con el asistente virtual para obtener orientación"],
        ["CU-06", "Enviar mensaje de voz", "Ciudadano", "El ciudadano envía un mensaje de voz que se transcribe a texto"],
        ["CU-07", "Cambiar idioma", "Ciudadano", "El ciudadano cambia la interfaz entre castellano y quechua"],
        ["CU-08", "Consultar información institucional", "Ciudadano", "El ciudadano consulta horarios, ubicación y contacto del GAM"],
        ["CU-09", "Actualizar base de conocimientos", "Administrador", "El administrador agrega o modifica información de trámites"],
    ])

add_image_placeholder(doc,
    "Figura 8: Caso de Usos General",
    "Diagrama UML de casos de uso mostrando al Ciudadano interactuando con: "
    "Consultar Trámite, Buscar Trámite, Filtrar por Categoría, Consultar Multas, "
    "Usar Chatbot, Enviar Voz, Cambiar Idioma, Consultar Institución. "
    "El Administrador interactúa con Actualizar Base de Conocimientos. "
    "El Chatbot se muestra como sistema que recibe las consultas.")

h2("3.1.5 Diagrama de Clases General")

styled_table(doc,
    ["Clase", "Atributos", "Métodos", "Descripción"],
    [
        ["Chatbot", "KB, UI, MULTAS, _client, _ai_available", "get_resp(), detect_intent(), detect_tramite(), normalize()", "Motor principal del chatbot"],
        ["Tramite", "id, nombre, descripcion, costo, tiempo, requisitos, pasos, ubicacion", "get_info_es(), get_info_qu()", "Representa un trámite municipal"],
        ["Multa", "tipo, infracciones, montos, procedimiento_pago", "get_info_transito(), get_info_municipal()", "Información de multas"],
        ["App Flask", "routes, templates, static", "index(), chat(), translate(), language()", "Servidor web y endpoints"],
        ["Widget Chatbot", "isOpen, messages, currentLang", "open(), close(), send(), receive()", "Interfaz del chatbot en el navegador"],
        ["TranslatePage", "items, translations", "translate_with_ai(), apply_translations()", "Módulo de traducción con IA"],
    ])

add_image_placeholder(doc,
    "Figura 9: Diagrama de Clases General",
    "Diagrama UML de clases mostrando: Chatbot (con KB, UI, MULTAS), "
    "Tramite (con atributos de información), Multa (con montos e infracciones), "
    "App Flask (con rutas HTTP), Widget Chatbot (interfaz de usuario), "
    "y TranslatePage (traducción con IA). Se muestran las relaciones "
    "de composición y dependencia entre clases.")

h2("3.1.6 Arquitectura del Sistema")

para(
    "El sistema utiliza una arquitectura web de tres capas separadas por "
    "responsabilidades, complementada con servicios externos de inteligencia artificial."
)

h3("3.1.6.1 Capa de Presentación (Vista)")
para(
    "Construida con HTML5, CSS3 y JavaScript. Incluye la página principal "
    "del portal municipal, las secciones de trámites y multas, el widget "
    "del chatbot embebido y el sistema de traducción de la interfaz."
)

h3("3.1.6.2 Capa de Lógica del Sistema (Controlador)")
para(
    "Implementada en Python con Flask. Gestiona las rutas HTTP (/chat, "
    "/language, /api/translate, /audio-to-text), procesa las consultas "
    "del chatbot y coordina las respuestas."

)

h3("3.1.6.3 Capa de Datos (Motor del Chatbot)")
para(
    "El motor del chatbot (engine.py) contiene la base de conocimientos "
    "estructurada en Python con 25 trámites, multas, horarios y contacto. "
    "Utiliza expresiones regulares para detectar intenciones y trámites."
)

h3("3.1.6.4 Capa de Servicios Externos")
para(
    "Integra servicios de IA: OpenAI ChatGPT para respuestas inteligentes "
    "y traducción de página, OpenAI Whisper para transcripción de audio, "
    "y NLLB-200 (Hugging Face) para traducción castellano-quechua."
)

add_image_placeholder(doc,
    "Figura 10: Arquitectura del Sistema",
    "Diagrama de arquitectura en capas mostrando: (1) Capa de Presentación "
    "con HTML/CSS/JS y Widget Chatbot, (2) Capa de Lógica con Flask y "
    "Engine.py, (3) Capa de Datos con Base de Conocimientos KB, "
    "(4) Servicios Externos con OpenAI API y NLLB-200. "
    "Se muestran las flechas de comunicación entre capas.")

# =====================================================================
# 3.2 APLICACIÓN DE LA METODOLOGÍA ÁGIL SCRUM
# =====================================================================
h1("3.2 APLICACIÓN DE LA METODOLOGÍA ÁGIL SCRUM")

h2("3.2.1 Roles en Scrum")

styled_table(doc,
    ["Rol", "Responsable", "Funciones"],
    [
        ["Product Owner", "Alfredo Ramírez Espinoza", "Define prioridades del backlog, representa las necesidades de los ciudadanos, acepta los incrementos"],
        ["Scrum Master", "Ing. Freddy Ledezma Higuera", "Facilita el proceso Scrum, remueve obstáculos, asegura la aplicación de prácticas ágiles"],
        ["Equipo de Desarrollo", "Alfredo Ramírez Espinoza", "Diseña, programa, prueba y documenta el sistema"],
    ])

h2("3.2.2 Planificación y Gestión de Sprints")

h3("3.2.2.1 Product Backlog")

styled_table(doc,
    ["ID", "Historia de Usuario", "Prioridad", "Estimación"],
    [
        ["HU-01", "Como ciudadano quiero consultar trámites para obtener información de requisitos y costos", "Alta", "8 pts"],
        ["HU-02", "Como ciudadano quiero usar el chatbot para preguntar sobre trámites de forma natural", "Alta", "13 pts"],
        ["HU-03", "Como ciudadano quiero cambiar el idioma a quechua para entender mejor la información", "Alta", "8 pts"],
        ["HU-04", "Como ciudadano quiero consultar multas para saber montos y procedimientos de pago", "Media", "5 pts"],
        ["HU-05", "Como ciudadano quiero buscar trámites por palabra clave para encontrarlos rápido", "Media", "5 pts"],
        ["HU-06", "Como ciudadano quiero filtrar trámites por categoría para navegar organizadamente", "Media", "3 pts"],
        ["HU-07", "Como ciudadano quiero enviar mensajes de voz para consultar sin escribir", "Baja", "8 pts"],
        ["HU-08", "Como ciudadano quiero ver información del GAM para conocer horarios y contacto", "Baja", "3 pts"],
        ["HU-09", "Como administrador quiero actualizar la base de conocimientos para mantener la información vigente", "Media", "5 pts"],
    ])

h3("3.2.2.2 Planificación de Sprints")

styled_table(doc,
    ["Sprint", "Nombre", "Duración", "Historias", "Puntos"],
    [
        ["Sprint 1", "Base de Conocimiento y Motor del Chatbot", "2 semanas", "HU-01, HU-02", "21"],
        ["Sprint 2", "Interfaz Web y Navegación", "2 semanas", "HU-04, HU-05, HU-06, HU-08", "16"],
        ["Sprint 3", "Soporte Multiidioma (ES/QU)", "2 semanas", "HU-03, HU-09", "13"],
        ["Sprint 4", "Pruebas, Voz y Documentación", "2 semanas", "HU-07 + Pruebas", "14"],
    ])

add_image_placeholder(doc,
    "Figura 11: Metodología Scrum",
    "Diagrama del proceso Scrum mostrando los 4 sprints con sus "
    "correspondientes historias de usuario, puntos estimados y "
    "la duración de cada sprint (2 semanas). Se muestra el "
    "Product Backlog inicial y los incrementos resultantes.")

# =====================================================================
# 3.2.3 IMPLEMENTACIÓN POR SPRINTS
# =====================================================================
h2("3.2.3 Implementación por Sprints")

# ---------- SPRINT 1 ----------
h3("3.2.3.1 Sprint 1: Base de Conocimiento y Motor del Chatbot")

h4("3.2.3.1.1 Objetivo del Sprint")
para(
    "Desarrollar la base de conocimientos bilingüe con 25 trámites municipales "
    "y el motor de procesamiento del chatbot capaz de detectar intenciones, "
    "trámites y responder consultas en castellano y quechua."
)

h4("3.2.3.1.2 Sprint Backlog")

styled_table(doc,
    ["Tarea", "Estado", "Horas"],
    [
        ["Definir estructura de KB con 25 trámites (es/qu)", "Completada", "8"],
        ["Implementar funciones: normalize(), detect_tramite(), detect_intent()", "Completada", "12"],
        ["Implementar build_card(), build_tramite_list(), build_multas_string()", "Completada", "8"],
        ["Implementar get_resp() con lógica de intenciones", "Completada", "10"],
        ["Implementar get_ai_resp() con mock de OpenAI", "Completada", "6"],
        ["Implementar transcribe_audio() con mock de Whisper", "Completada", "4"],
        ["Crear 62 pruebas unitarias", "Completada", "10"],
        ["Configurar pytest y coverage", "Completada", "2"],
    ])

h4("3.2.3.1.3 Diseño y Arquitectura")

para("El motor del chatbot (engine.py) utiliza las siguientes estructuras de datos:")

bullet("KB: Diccionario con 25 trámites, cada uno con información en es y qu")
bullet("MULTAS: Información de multas de tránsito y municipales")
bullet("UI: Textos de interfaz en ambos idiomas (title, sub, ph, greeting, etc.)")
bullet("INTENT_PATTERNS: Lista de patrones regex para detectar intenciones")

add_image_placeholder(doc,
    "Figura 12: Diagrama de Clases del Motor del Chatbot",
    "Diagrama UML de la clase Chatbot mostrando atributos (KB, MULTAS, UI, "
    "_client, _ai_available) y métodos (normalize, detect_tramite, detect_intent, "
    "get_resp, get_ai_resp, transcribe_audio, build_card, build_tramite_list, "
    "build_multas_string). Se muestran las relaciones con Tramite y Multa.")

h4("3.2.3.1.4 Pruebas de Testing")

styled_table(doc,
    ["Tipo de Prueba", "Cantidad", "Herramienta", "Cobertura"],
    [
        ["Pruebas Unitarias", "62", "pytest + unittest.mock", "100% funciones"],
        ["Pruebas de Caja Negra", "11", "Flask test client", "Endpoints HTTP"],
        ["Pruebas de Caja Blanca", "16", "pytest", "Decisiones if/for"],
    ])

add_image_placeholder(doc,
    "Figura 13: Resultado de Pruebas Unitarias - Sprint 1",
    "Captura de pantalla de la terminal mostrando la ejecución de "
    "python -m pytest tests/test_unitarias.py -v con los 62 tests "
    "en estado PASSED. Se muestra el resumen: 62 passed en ~15s.")

# ---------- SPRINT 2 ----------
h3("3.2.3.2 Sprint 2: Interfaz Web y Navegación")

h4("3.2.3.2.1 Objetivo del Sprint")
para(
    "Desarrollar la interfaz web del portal municipal con las secciones de "
    "trámites, multas e información institucional, incluyendo el buscador, "
    "filtros por categoría y accesos rápidos."
)

h4("3.2.3.2.2 Sprint Backlog")

styled_table(doc,
    ["Tarea", "Estado", "Horas"],
    [
        ["Crear estructura HTML del portal (header, hero, secciones, footer)", "Completada", "8"],
        ["Diseñar CSS con diseño responsivo y colores institucionales", "Completada", "10"],
        ["Implementar grid de trámites con 25 tarjetas", "Completada", "6"],
        ["Implementar buscador en tiempo real", "Completada", "4"],
        ["Implementar filtros por categoría", "Completada", "4"],
        ["Implementar sección de multas (3 tarjetas + pasos)", "Completada", "6"],
        ["Implementar sección institucional (horarios, ubicación, contacto)", "Completada", "4"],
        ["Crear widget del chatbot embebido", "Completada", "10"],
        ["Implementar API Flask (/chat, /language, /audio-to-text)", "Completada", "8"],
        ["Crear 39 pruebas de caja negra", "Completada", "8"],
    ])

h4("3.2.3.2.3 Diseño y Arquitectura")

para("La interfaz web consta de las siguientes secciones:")

styled_table(doc,
    ["Sección", "ID", "Contenido"],
    [
        ["Barra Superior", "top-bar", "Teléfono, email, horarios, redes sociales"],
        ["Header", "main-header", "Logo, menú de navegación (5 enlaces), botón idioma"],
        ["Hero Banner", "inicio", "Título, descripción, botones CTA, badges informativos"],
        ["Accesos Rápidos", "quick-access", "6 tarjetas de trámites frecuentes"],
        ["Trámites", "tramites", "Buscador, filtros, grid de 25 tarjetas"],
        ["Multas", "multas", "3 tarjetas (tránsito, municipal, pagos) + pasos"],
        ["Institución", "institucion", "Horarios, ubicación con mapa, contacto"],
        ["Footer", "main-footer", "Logo, enlaces, contacto, copyright"],
    ])

add_image_placeholder(doc,
    "Figura 14: Diagrama de Casos de Uso - Interfaz Web",
    "Diagrama UML de casos de uso de la interfaz web mostrando al Ciudadano "
    "interactuando con: Navegar por secciones, Buscar Trámites, Filtrar por "
    "Categoría, Consultar Multas, Ver Información Institucional, "
    "y Abrir Chatbot.")

h4("3.2.3.2.4 Diseño e Implementación de Interfaces")

add_image_placeholder(doc,
    "Figura 15: Mockup - Pantalla Principal del Portal",
    "Mockup de la página principal mostrando: barra superior con teléfono "
    "y horarios, header con logo y menú (Inicio, Trámites, Multas, Institución, "
    "Contacto), banner hero con título 'Sistema de Orientación Ciudadana Digital' "
    "y botones 'Ver Trámites' y 'Pagos y Multas'.")

add_image_placeholder(doc,
    "Figura 16: Mockup - Sección de Trámites",
    "Mockup de la sección Trámites mostrando: campo de búsqueda con placeholder "
    "'Buscar trámite: carnet, catastro, vehículo, licencia...', botones de "
    "filtro (Todos, Identidad, Vivienda, Negocio, Servicios), y grid de "
    "tarjetas con información de cada trámite.")

add_image_placeholder(doc,
    "Figura 17: Mockup - Sección de Multas",
    "Mockup de la sección Multas mostrando: tarjeta 'Multas de Tránsito' con "
    "5 infracciones, tarjeta 'Multas Municipales' con 5 infracciones, "
    "tarjeta 'Pago de Multas' con 4 opciones de pago, y sección de "
    "pasos de pago con código QR.")

h4("3.2.3.2.5 Pruebas de Testing")

add_image_placeholder(doc,
    "Figura 18: Resultado de Pruebas de Caja Negra - Sprint 2",
    "Captura de pantalla mostrando la ejecución de "
    "python -m pytest tests/test_caja_negra.py -v con los 39 tests "
    "en estado PASSED. Se muestra el resumen: 39 passed en ~8s.")

# ---------- SPRINT 3 ----------
h3("3.2.3.3 Sprint 3: Soporte Multiidioma (ES/QU)")

h4("3.2.3.3.1 Objetivo del Sprint")
para(
    "Implementar el sistema de traducción automática de la interfaz web "
    "entre castellano y quechua, incluyendo atributos data-qu en todos "
    "los elementos HTML y el endpoint /api/translate con IA."
)

h4("3.2.3.3.2 Sprint Backlog")

styled_table(doc,
    ["Tarea", "Estado", "Horas"],
    [
        ["Agregar atributos data-qu a 99 elementos HTML", "Completada", "8"],
        ["Implementar función translatePage() en main.js", "Completada", "6"],
        ["Implementar endpoint /api/translate en Flask", "Completada", "6"],
        ["Integrar NLLB-200 para traducción es/qu", "Completada", "8"],
        ["Actualizar engine.py con UI keys (subalcaldías, guía telefónica)", "Completada", "6"],
        ["Agregar intents subalcaldías y guía telefónica", "Completada", "4"],
        ["Actualizar datos de contacto reales (teléfono, horarios)", "Completada", "4"],
        ["Crear pruebas para nuevos endpoints", "Completada", "4"],
    ])

h4("3.2.3.3.3 Diseño y Arquitectura")

para("El sistema de traducción funciona en tres niveles:")

styled_table(doc,
    ["Nivel", "Método", "Alcance", "Tecnología"],
    [
        ["Estático", "Atributos data-qu", "Elementos HTML predefinidos", "JavaScript puro"],
        ["Dinámico", "NLLB-200", "Contenido del chatbot", "Hugging Face API"],
        ["IA", "OpenAI GPT", "Textos largos del sitio", "OpenAI API"],
    ])

add_image_placeholder(doc,
    "Figura 19: Diagrama de Secuencia - Traducción",
    "Diagrama de secuencia mostrando: (1) Usuario hace clic en botón QU, "
    "(2) JavaScript llama a translatePage('qu'), (3) Se leen atributos data-qu "
    "de 99 elementos, (4) Se llama a /api/translate con los items, "
    "(5) Flask procesa con NLLB-200, (6) Se retornan traducciones, "
    "(7) Se aplican al DOM.")

h4("3.2.3.3.4 Pruebas de Testing")

add_image_placeholder(doc,
    "Figura 20: Resultado de Pruebas - Sprint 3",
    "Captura de pantalla mostrando la ejecución completa de "
    "python -m pytest tests/ -v con 145 tests en estado PASSED. "
    "Se muestra el resumen: 145 passed en ~35s, 98% cobertura.")

# ---------- SPRINT 4 ----------
h3("3.2.3.4 Sprint 4: Pruebas, Voz y Documentación")

h4("3.2.3.4.1 Objetivo del Sprint")
para(
    "Completar las pruebas de caja blanca, implementar la funcionalidad "
    "de entrada de voz, optimizar el rendimiento y elaborar la documentación "
    "técnica y de usuario."
)

h4("3.2.3.4.2 Sprint Backlog")

styled_table(doc,
    ["Tarea", "Estado", "Horas"],
    [
        ["Crear 44 pruebas de caja blanca (cobertura de ramas)", "Completada", "10"],
        ["Implementar botón de micrófono en el widget", "Completada", "6"],
        ["Integrar Whisper para transcripción de audio", "Completada", "6"],
        ["Optimizar tiempos de respuesta del chatbot", "Completada", "4"],
        ["Corregir bugs detectados en pruebas (4 bugs)", "Completada", "4"],
        ["Elaborar documentación técnica del sistema", "Completada", "6"],
        ["Crear manual de usuario", "Completada", "4"],
        ["Generar cronograma de pasantía (360 horas)", "Completada", "2"],
    ])

h4("3.2.3.4.3 Diseño y Arquitectura")

add_image_placeholder(doc,
    "Figura 21: Diagrama de Actividades - Flujo del Chatbot",
    "Diagrama de actividades mostrando el flujo completo: (1) Usuario abre "
    "chatbot, (2) Escribe o envía voz, (3) Sistema detecta idioma, "
    "(4) Sistema detecta intención y trámite, (5) Busca en KB, "
    "(6) Genera respuesta, (7) Muestra tarjeta formateada, "
    "(8) Usuario puede continuar o cerrar.")

h4("3.2.3.4.4 Pruebas de Testing")

styled_table(doc,
    ["Categoría", "Tests", "Herramienta", "Resultado"],
    [
        ["Pruebas Unitarias", "62", "pytest", "145/145 PASSED"],
        ["Pruebas Caja Negra", "39", "Flask test client", "145/145 PASSED"],
        ["Pruebas Caja Blanca", "44", "pytest + coverage", "145/145 PASSED"],
        ["Cobertura Total", "—", "coverage", "98%"],
    ])

add_image_placeholder(doc,
    "Figura 22: Resultado Final de Pruebas - Todos los Tests",
    "Captura de pantalla mostrando la ejecución completa de "
    "python -m pytest tests/ -v con los 145 tests (62+39+44) "
    "en estado PASSED. Se muestra: 145 passed in 34.77s, "
    "100% éxito, cobertura 98%.")

# =====================================================================
# 3.3 RESUMEN DE RESULTADOS
# =====================================================================
h1("3.3 RESUMEN DE RESULTADOS POR SPRINT")

styled_table(doc,
    ["Sprint", "Funcionalidad", "Tests", "Estado"],
    [
        ["Sprint 1", "Base de conocimiento + Motor chatbot", "62 unitarias", "Completado"],
        ["Sprint 2", "Interfaz web + Navegación + API", "39 caja negra", "Completado"],
        ["Sprint 3", "Multiidioma ES/QU + Datos reales", "—", "Completado"],
        ["Sprint 4", "Pruebas + Voz + Documentación", "44 caja blanca", "Completado"],
        ["TOTAL", "Sistema completo funcional", "145 tests", "100% éxito"],
    ])

# =====================================================================
# 3.4 CONCLUSIONES DEL CAPÍTULO
# =====================================================================
h1("3.4 CONCLUSIONES DEL CAPÍTULO")

bullet("Se identificaron 10 requerimientos funcionales y 8 no funcionales que guiaron el desarrollo del sistema.")
bullet("La arquitectura de 3 capas (Presentación, Lógica, Datos) facilitó el desarrollo modular y mantenible.")
bullet("La aplicación de Scrum con 4 sprints permitió entregar funcionalidades de forma incremental.")
bullet("Se implementaron 25 trámites municipales con información bilingüe (es/qu) en la base de conocimientos.")
bullet("El chatbot detecta 14 intenciones y responde con información precisa de la base de conocimientos.")
bullet("Se alcanzó una cobertura de pruebas del 98% con 145 casos de prueba (62+39+44).")
bullet("El sistema de traducción automática cubre 99 elementos de la interfaz entre castellano y quechua.")
bullet("La integración con IA (OpenAI, Whisper, NLLB-200) potencia las capacidades del chatbot.")

# Save
doc.save(r"C:\Users\kanit\Desktop\chatbot-sacaba\CAPITULO_III_INGENIERIA.docx")
print("CAPITULO_III_INGENIERIA.docx generado correctamente.")
print("Se generaron 12 espacios para imágenes/diagramas.")
