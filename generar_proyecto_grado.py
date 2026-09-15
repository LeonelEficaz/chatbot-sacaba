# -*- coding: utf-8 -*-
"""Genera PROYECTO_GRADO_CHATBOT.docx con formato profesional."""
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
style.font.size = Pt(11)

for s in doc.sections:
    s.top_margin = Cm(2.5)
    s.bottom_margin = Cm(2.5)
    s.left_margin = Cm(3)
    s.right_margin = Cm(2.5)


# =====================================================================
# FUNCIONES AUXILIARES
# =====================================================================
def h1(t):
    doc.add_heading(t, level=1)

def h2(t):
    doc.add_heading(t, level=2)

def h3(t):
    doc.add_heading(t, level=3)

def para(t, bold=False, italic=False, align=None):
    p = doc.add_paragraph()
    r = p.add_run(t)
    r.bold = bold
    r.italic = italic
    if align:
        p.alignment = align
    return p

def bullet(t):
    return doc.add_paragraph(t, style="List Bullet")

def add_page_break():
    doc.add_page_break()


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
r = p.add_run("R.M. 995/2015\nFundado el 19 de Marzo del año 2007\nSacaba – Cochabamba – Bolivia")
r.font.size = Pt(12)

doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("CARRERA DE SISTEMAS INFORMÁTICOS")
r.bold = True
r.font.size = Pt(14)

for _ in range(3):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('"DESARROLLO DE UN CHATBOT WEB MULTIIDIOMA\n(CASTELLANO–QUECHUA) PARA LA ORIENTACIÓN\nSOBRE TRÁMITES Y MULTAS MUNICIPALES\nDEL GOBIERNO AUTÓNOMO MUNICIPAL DE SACABA"')
r.bold = True
r.font.size = Pt(16)
r.font.color.rgb = AZUL

doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Proyecto de Grado")
r.font.size = Pt(13)
r.bold = True

for _ in range(3):
    doc.add_paragraph()

for linea in (
    "ESTUDIANTE:\tALFREDO RAMÍREZ ESPINOZA",
    "DOCENTE TUTOR:\tIng. FREDDY LEDEZMA HIGUERA",
):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(linea)
    r.font.size = Pt(12)

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Junio, 2026\nSacaba - Cochabamba – Bolivia")
r.font.size = Pt(12)

add_page_break()

# =====================================================================
# RESUMEN
# =====================================================================
h1("RESUMEN")

para(
    "Chatbot Municipal Sacaba es una aplicación web multiidioma desarrollada para orientar a los "
    "ciudadanos del municipio de Sacaba sobre trámites y multas municipales. La solución integra un "
    "asistente virtual con inteligencia artificial (ChatGPT de OpenAI) que responde consultas en "
    "castellano y quechua, apoyándose en una base de conocimiento local estructurada con información "
    "sobre 25 trámites municipales, multas, horarios y servicios públicos."
)

para(
    "El prototipo funciona con una arquitectura basada en Python y Flask en el backend, con una "
    "interfaz web construida en HTML, CSS y JavaScript. Utiliza la API de OpenAI para respuestas "
    "inteligentes y Whisper para la transcripción de audio. El sistema incluye detección automática "
    "de idioma, traducción del sitio web a quechua mediante IA y un widget de chat embebido "
    "disponible en dispositivos móviles y equipos de escritorio."
)

para(
    "El propósito del sistema no es reemplazar la atención presencial, sino proporcionar un canal "
    "digital complementario que reduzca tiempos de espera, mejore el acceso a la información y "
    "promueva la inclusión lingüística de la población quechua-hablante del municipio."
)

doc.add_paragraph()

add_table(doc,
    ["Dato", "Descripción"],
    [
        ["Nombre del proyecto", "Chatbot Municipal Sacaba"],
        ["Modalidad", "Proyecto de Grado"],
        ["Área", "Desarrollo de Aplicaciones Web / Atención Ciudadana"],
        ["Estado", "Prototipo funcional en desarrollo"],
        ["Tecnologías", "Python, Flask, HTML, CSS, JavaScript, OpenAI API"],
        ["Método de respuesta", "Base de conocimiento local + ChatGPT (GPT-4o-mini)"],
        ["Alcance", "Trámites y multas del G.A.M. Sacaba"],
        ["Idiomas soportados", "Castellano y Quechua (runasimi boliviano)"],
    ])

add_page_break()

# =====================================================================
# CAPÍTULO I. PLANTEAMIENTO DEL PROBLEMA
# =====================================================================
h1("CAPÍTULO I. PLANTEAMIENTO DEL PROBLEMA")

h2("1.1 Diagnóstico y justificación")

para(
    "El Gobierno Autónomo Municipal de Sacaba gestiona diversos trámites y servicios públicos "
    "que los ciudadanos requieren de manera frecuente: emisión de cédulas de identidad, constancias "
    "de residencia, licencias de funcionamiento, permisos de construcción, inscripción de vehículos, "
    "entre otros. Sin embargo, la información sobre estos trámites se encuentra dispersa en "
    "dependencias municipales, y los ciudadanos frecuentemente deben acudir presencialmente para "
    "obtener orientación básica sobre requisitos, costos, horarios y procedimientos."
)

para(
    "Esta situación genera tiempos de espera prolongados, múltiples desplazamientos innecesarios "
    "y saturación de los canales de atención. El problema se agrava para la población quechua-hablante, "
    "ya que la mayoría de los servicios de información municipal se encuentran únicamente en castellano, "
    "generando barreras lingüísticas que limitan el acceso equitativo a la información pública."
)

para(
    "Asimismo, el crecimiento poblacional del municipio de Sacaba y el aumento en el uso de "
    "dispositivos móviles han incrementado la demanda de canales digitales de atención. Los chatbots "
    "o asistentes virtuales se han consolidado a nivel internacional como una herramienta eficiente "
    "para brindar orientación automatizada, reducir costos operativos y mejorar la satisfacción "
    "ciudadana. Implementar un chatbot bilingüe para el municipio de Sacaba representa una oportunidad "
    "concreta de modernización y inclusión social."
)

h2("1.2 Planteamiento y formulación")

para("Problema central:", bold=True)
para(
    "Limitado acceso a información oportuna y bilingüe sobre trámites y multas municipales "
    "en el Gobierno Autónomo Municipal de Sacaba."
)

doc.add_paragraph()

add_table(doc,
    ["Causas", "Efectos"],
    [
        ["Atención presencial como canal principal", "Tiempos de espera prolongados y múltiples desplazamientos"],
        ["Información municipal dispersa y no digitalizada", "Dificultad para acceder a requisitos y costos actualizados"],
        ["Ausencia de soporte en idioma quechua", "Barreras lingüísticas para una parte significativa de la población"],
        ["Horarios limitados de atención", "Inaccesibilidad fuera del horario laboral"],
        ["Falta de herramientas digitales de orientación", "Insatisfacción ciudadana y baja eficiencia en la atención"],
    ])

doc.add_paragraph()

para("Formulación:", bold=True)
para(
    "¿De qué manera se puede contribuir a mejorar la orientación sobre trámites y multas "
    "municipales, reducir los tiempos de respuesta y fortalecer la inclusión lingüística de "
    "los ciudadanos del municipio de Sacaba?"
)

h2("1.3 Objetivos")

h3("1.3.1 Objetivo general")
para(
    "Desarrollar un chatbot web multiidioma (Castellano–Quechua) que permita orientar a los "
    "ciudadanos del municipio de Sacaba sobre trámites y multas municipales mediante una "
    "plataforma digital accesible, disponible las 24 horas del día."
)

h3("1.3.2 Objetivos específicos")
bullet("Identificar los trámites y multas municipales de mayor demanda ciudadana mediante la recopilación y análisis de información proporcionada por las dependencias del Gobierno Autónomo Municipal de Sacaba.")
bullet("Elaborar una base de conocimiento bilingüe en castellano y quechua que contenga información estructurada sobre requisitos, procedimientos, costos y sanciones municipales.")
bullet("Diseñar la arquitectura funcional del sistema y los flujos de conversación del chatbot, definiendo la estructura de navegación, categorías de consulta y mecanismos de interacción con el usuario.")
bullet("Implementar una aplicación web de orientación ciudadana mediante tecnologías web y un chatbot con inteligencia artificial integrada, con soporte bilingüe castellano–quechua.")
bullet("Implementar una interfaz accesible e intuitiva que permita a los usuarios consultar información municipal desde dispositivos móviles y equipos de escritorio.")
bullet("Integrar la API de OpenAI (ChatGPT y Whisper) para respuestas inteligentes y transcripción de voz a texto.")
bullet("Realizar pruebas funcionales, unitarias y de caja blanca para verificar el correcto funcionamiento del sistema y la precisión de las respuestas.")
bullet("Elaborar la documentación técnica y el manual de usuario para facilitar la administración, mantenimiento y utilización del sistema.")

h2("1.4 Enfoque metodológico")

para(
    "La investigación adopta un enfoque mixto, combinando técnicas cuantitativas y cualitativas "
    "para analizar de manera integral la problemática relacionada con el acceso a información "
    "municipal en el municipio de Sacaba."
)

para(
    "El componente cuantitativo permite trabajar con datos medibles, como los porcentajes de "
    "cobertura de la base de conocimiento, los tiempos de respuesta del chatbot y los resultados "
    "obtenidos durante las pruebas de funcionamiento. El componente cualitativo permite conocer "
    "las opiniones, necesidades y experiencias de los usuarios mediante entrevistas, observación "
    "directa en dependencias municipales y recopilación de información sobre los procedimientos "
    "actuales de atención."
)

para("Metodología de desarrollo:", bold=True)
para(
    "El desarrollo del sistema sigue un enfoque iterativo e incremental, permitiendo construir "
    "y validar funcionalidades de manera progresiva. Cada iteración incluye análisis de "
    "requerimientos, diseño, implementación, pruebas y retroalimentación del usuario."
)

add_page_break()

# =====================================================================
# CAPÍTULO II. MARCO TEÓRICO CONCEPTUAL
# =====================================================================
h1("CAPÍTULO II. MARCO TEÓRICO CONCEPTUAL")

h2("2.1 Chatbots y asistentes virtuales")
para(
    "Un chatbot es un programa de software diseñado para simular conversaciones con usuarios "
    "a través de interfaces de texto o voz. Los chatbots pueden clasificarse en dos categorías "
    "principales: basados en reglas (respuestas predeterminadas) e impulsados por inteligencia "
    "artificial (capaces de comprender y generar lenguaje natural). Los asistentes virtuales "
    "modernos integran ambas aproximaciones para ofrecer respuestas precisas y contextuales."
)

para(
    "En el ámbito de los servicios públicos, los chatbots permiten automatizar consultas "
    "frecuentes, reducir tiempos de atención y ofrecer servicio disponible las 24 horas. "
    "Su implementación en gobiernos municipales ha demostrado mejoras significativas en la "
    "satisfacción ciudadana y en la eficiencia operativa de las dependencias públicas."
)

h2("2.2 Inteligencia artificial y procesamiento de lenguaje natural")
para(
    "El procesamiento de lenguaje natural (NLP) es una rama de la inteligencia artificial que "
    "permite a las máquinas comprender, interpretar y generar texto o voz humana. Las técnicas "
    "de NLP incluyen la tokenización, lematización, análisis de sentimientos, detección de "
    "intención y generación de respuestas."
)

para(
    "Los modelos de lenguaje grandes (LLM) como GPT-4 de OpenAI representan el estado del "
    "arte en generación de texto. Estos modelos entrenan con grandes volúmenes de datos "
    "textuales y son capaces de generar respuestas coherentes, contextuales y gramaticalmente "
    "correctas. Para un chatbot municipal, la integración de un LLM permite ofrecer respuestas "
    "flexibles y naturales, superando las limitaciones de los chatbots basados exclusivamente "
    "en respuestas predeterminadas."
)

h2("2.3 Procesamiento de voz: transcripción de audio")
para(
    "La transcripción de audio a texto es una funcionalidad que permite a los usuarios "
    "realizar consultas mediante voz en lugar de texto. Modelos como Whisper de OpenAI "
    "ofrecen transcripción precisa en múltiples idiomas, incluyendo español y quechua. "
    "Esta capacidad es especialmente relevante para poblaciones con limitaciones de lectoescritura "
    "o que prefieren la interacción vocal."
)

h2("2.4 Bilingüismo y quechua en Bolivia")
para(
    "Según el Instituto Nacional de Estadística (INE), una proporción significativa de la "
    "población del departamento de Cochabamba utiliza el idioma quechua como lengua materna "
    "o de uso habitual. La Constitución Política del Estado reconoce el quechua como idioma "
    "oficial junto al castellano. Sin embargo, la mayoría de los servicios digitales públicos "
    "se ofrecen únicamente en castellano, generando una brecha de acceso para la población "
    "quechua-hablante."
)

para(
    "La incorporación de soporte bilingüe en herramientas digitales municipales contribuye "
    "a cerrar esta brecha, promoviendo la inclusión lingüística y el acceso equitativo a la "
    "información pública. Un chatbot capaz de detectar y responder en quechua representa un "
    "avance significativo en la modernización inclusiva de los servicios municipales."
)

h2("2.5 Flask y arquitectura web")
para(
    "Flask es un framework de desarrollo web en Python diseñado para aplicaciones de pequeña "
    "y mediana escala. Su arquitectura ligera y modular permite crear APIs RESTful, gestionar "
    "rutas, manejar sesiones y integrar servicios externos de forma sencilla. Flask adopta un "
    "enfoque minimalista que permite al desarrollador estructurar el proyecto según sus necesidades, "
    "lo que lo hace ideal para prototipos y proyectos académicos."
)

para(
    "La arquitectura MVC (Modelo-Vista-Controlador) organiza el código en capas separadas: "
    "el modelo gestiona los datos, la vista presenta la información al usuario y el controlador "
    "coordina la lógica de la aplicación. Esta separación mejora la mantenibilidad, escalabilidad "
    "y testeo del sistema."
)

h2("2.6 Base de conocimiento estructurada")
para(
    "Una base de conocimiento es una estructura de datos que almacena información organizada "
    "y accesible para su consulta y procesamiento. En el contexto de un chatbot, la base de "
    "conocimiento contiene la información sobre trámites, requisitos, costos, procedimientos "
    "y demás datos necesarios para generar respuestas precisas."
)

para(
    "Para este proyecto, la base de conocimiento se estructura como un diccionario anidado en "
    "Python, con entries para cada trámite que incluyen información en castellano y quechua. "
    "Esta estructura permite al motor del chatbot acceder rápidamente a la información y generar "
    "respuestas contextuales e idiomáticas."
)

h2("2.7 Tecnologías utilizadas")

add_table(doc,
    ["Tecnología", "Función"],
    [
        ["Python 3.14", "Lenguaje de programación principal del backend"],
        ["Flask 3.1.3", "Framework web para API REST y servidor"],
        ["OpenAI API (GPT-4o-mini)", "Generación de respuestas inteligentes con IA"],
        ["OpenAI Whisper", "Transcripción de audio a texto"],
        ["HTML5 / CSS3 / JavaScript", "Interfaz de usuario y widget de chat"],
        ["python-dotenv", "Gestión de variables de entorno"],
        ["pytest / coverage", "Pruebas unitarias, caja negra, caja blanca y medición de cobertura"],
        ["Visual Studio Code", "Edición y mantenimiento del código"],
        ["Git / GitHub", "Control de versiones y respaldo del código"],
    ])

h2("2.8 Seguridad y protección de la información")
para(
    "La aplicación protege credenciales y datos sensibles mediante variables de entorno (.env) "
    "que almacenan las claves de API fuera del código fuente. Flask proporciona protección CSRF, "
    "validación de entradas y gestión segura de sesiones. Los documentos de audio se procesan "
    "de forma temporal y no se almacenan permanentemente en el servidor."
)

add_page_break()

# =====================================================================
# CAPÍTULO III. PROPUESTA DE INNOVACIÓN
# =====================================================================
h1("CAPÍTULO III. PROPUESTA DE INNOVACIÓN")

h2("3.1 Descripción de la solución")
para(
    "Chatbot Municipal Sacaba es una aplicación web que centraliza la información municipal "
    "y ofrece un canal de atención automatizada mediante un asistente virtual bilingüe. "
    "El flujo comienza con la interacción del usuario a través del widget de chat: el sistema "
    "detecta el idioma (castellano o quechua), procesa la consulta mediante el motor NLP local "
    "o la API de ChatGPT, y retorna una respuesta estructurada con información relevante sobre "
    "el trámite o servicio consultado."
)

para(
    "El sistema también incluye funcionalidades de transcripción de audio (voz a texto) y "
    "traducción del sitio web completo a quechua, permitiendo una experiencia accesible y "
    "包容 para todos los ciudadanos del municipio."
)

h2("3.2 Usuarios y responsabilidades")

add_table(doc,
    ["Rol", "Responsabilidades principales"],
    [
        ["Ciudadano", "Realizar consultas sobre trámites, multas, horarios y servicios municipales mediante el chat de texto o voz."],
        ["Administrador del chatbot", "Gestionar la base de conocimiento, actualizar información de trámites, monitorear el uso del sistema y configurar la API de IA."],
        ["Desarrollador", "Mantener el código fuente, implementar mejoras, realizar pruebas y gestionar actualizaciones del sistema."],
    ])

h2("3.3 Módulos del sistema")
bullet("Módulo de Chat: Interfaz de conversación con el usuario, envío y recepción de mensajes.")
bullet("Motor NLP: Detección de idioma, intención y trámite. Generación de respuestas basadas en reglas.")
bullet("Integración con IA: Conexión con la API de OpenAI (ChatGPT) para respuestas inteligentes.")
bullet("Transcripción de Audio: Módulo de conversión de voz a texto mediante Whisper.")
bullet("Traducción del Sitio: API para traducir elementos HTML del sitio web a quechua usando IA.")
bullet("Base de Conocimiento: Estructura de datos con 25 trámites bilingües, multas, horarios y contacto.")
bullet("Widget de Chat: Componente JavaScript embebido en el sitio web, adaptable a dispositivos móviles.")
bullet("API REST: Endpoints para chat, audio, idioma, estado de IA y traducción.")

h2("3.4 Arquitectura funcional")

add_table(doc,
    ["Capa", "Elementos", "Responsabilidad"],
    [
        ["Presentación", "Widget de chat (JS/CSS), sitio web principal (HTML/CSS/JS)", "Interacción visual con el usuario, envío de mensajes, visualización de respuestas"],
        ["Aplicación", "Rutas Flask (app.py), lógica de negocio", "Recibir peticiones, validar datos, coordinar respuestas"],
        ["Motor NLP", "chatbot/engine.py", "Detección de idioma, intención, trámite; generación de respuestas por reglas"],
        ["IA", "API de OpenAI (ChatGPT, Whisper)", "Respuestas inteligentes, transcripción de audio, traducción de texto"],
        ["Datos", "Base de conocimiento (KB) en Python", "Almacenamiento de información de 25 trámites, multas, UI texts"],
    ])

h2("3.5 Modelo de datos - Base de conocimiento")

add_table(doc,
    ["Entidad", "Información principal", "Idiomas"],
    [
        ["carnet", "Carnet de Identidad - SEGIP, Bs. 17, inmediato", "es / qu"],
        ["residencia", "Constancia de Residencia - Bs. 15, 2-3 días", "es / qu"],
        ["funcionamiento", "Licencia de Funcionamiento - Bs. 60 nuevo / Bs. 40 renovación", "es / qu"],
        ["construccion", "Permiso de Construcción - Planos de vivienda", "es / qu"],
        ["propiedad", "Registro de Propiedad - Derechos Reales", "es / qu"],
        ["solteria", "Constancia de Soltería - Bs. 10, inmediato", "es / qu"],
        ["prediales", "Impuestos Prediales - 0.5% - 1% del valor catastral", "es / qu"],
        ["agua", "Servicio de Agua Potable - Bs. 50-200", "es / qu"],
        ["eventos", "Permiso para Eventos - Bs. 30-300", "es / qu"],
        ["vehiculos", "Registro de Vehículos - Bs. 30-150", "es / qu"],
        ["nodeuda", "Constancia de No Deuda - Bs. 10", "es / qu"],
        ["catastro_*", "Empadronamiento, Certificado y Avalúo Catastral", "es / qu"],
        ["urbanismo_*", "Planos, Ampliación, Uso de Suelo, Verjas", "es / qu"],
        ["vehiculo_*", "Inscripción, Transferencia, Radicatoria, Baja, Reemplaque", "es / qu"],
        ["MULTAS", "Tránsito (Bs. 50-1000) y Municipales (Bs. 50-2000)", "es / qu"],
    ])

h2("3.6 Funcionamiento del motor de chat")

add_table(doc,
    ["Etapa", "Descripción"],
    [
        ["1. Recepción", "El usuario envía un mensaje de texto o audio a través del widget de chat."],
        ["2. Detección de idioma", "El sistema analiza tokens de quechua para determinar si responde en castellano o quechua."],
        ["3. Detección de trámite", "Se buscan palabras clave en el mensaje para identificar el trámite consultado (25 patrones)."],
        ["4. Detección de intención", "Se clasifica la consulta: saludo, costo, ubicación, requisitos, procedimiento, multas, etc."],
        ["5. Generación de respuesta", "Si la IA está disponible, se envía a ChatGPT con contexto de la base de conocimiento. Si no, se genera una respuesta local basada en reglas."],
        ["6. Respuesta", "El sistema retorna la respuesta formateada en el idioma detectado, con tarjetas, listas o textos informativos."],
    ])

h2("3.7 Flujo de navegación")
para(
    "El flujo principal del usuario es el siguiente: Ingreso al sitio web → Visualización del "
    "widget de chat → Envío de consulta (texto o voz) → Detección automática de idioma → "
    "Procesamiento de la consulta → Visualización de la respuesta → Posibilidad de realizar "
    "nuevas consultas. El usuario también puede cambiar el idioma del sitio web completo "
    "(castellano/quechua) mediante un botón en la barra de navegación."
)

h2("3.8 Endpoints de la API")

add_table(doc,
    ["Ruta", "Método", "Descripción"],
    [
        ["/", "GET", "Página principal del sitio web"],
        ["/chat", "POST", "Endpoint principal del chatbot. Recibe {message, language} y retorna {response, options, language}"],
        ["/audio-to-text", "POST", "Transcripción de audio. Recibe {audio (base64), language} y retorna {text}"],
        ["/language", "POST", "Cambio de idioma del chat. Recibe {language} y retorna {language}"],
        ["/api/ai-status", "GET", "Verifica si la API de OpenAI está configurada. Retorna {ai: bool}"],
        ["/api/translate", "POST", "Traduce textos del sitio a quechua. Recibe {items: [{id, text}]} y retorna {translations}"],
    ])

h2("3.9 Estado de implementación")

add_table(doc,
    ["Componente", "Estado verificado"],
    [
        ["Base de conocimiento", "Implementada con 25 trámites × 2 idiomas, multas y textos de interfaz"],
        ["Motor NLP", "Funcional: detección de idioma, intención y trámite"],
        ["Integración con OpenAI", "Funcional: ChatGPT para respuestas, Whisper para audio"],
        ["Widget de chat", "Implementado con diseño responsive y soporte de voz"],
        ["Traducción del sitio", "Funcional: traduce elementos HTML a quechua mediante IA"],
        ["API REST", "Todos los endpoints funcionales y validados"],
        ["Pruebas automatizadas", "145 pruebas exitosas (unitarias, caja negra, caja blanca)"],
        ["Cobertura de código", "98% de cobertura de sentencias y decisiones"],
        ["Documentación técnica", "En desarrollo"],
        ["Manual de usuario", "Pendiente"],
    ])

h2("3.10 Innovación y aporte")
para(
    "El aporte distintivo de Chatbot Municipal Sacaba frente a soluciones existentes es la "
    "combinación de inteligencia artificial con una base de conocimiento local específica, "
    "adaptada al contexto municipal de Sacaba. A diferencia de chatbots basados exclusivamente "
    "en respuestas predeterminadas, este sistema integra ChatGPT para ofrecer respuestas "
    "flexibles y naturales, manteniendo la precisión de la información institucional."
)

para(
    "Además, el soporte bilingüe castellano–quechua constituye un elemento innovador que "
    "promueve la inclusión lingüística en los servicios digitales municipales. La detección "
    "automática del idioma y la capacidad de responder en quechua cotidiano (runasimi "
    "boliviano) representan un avance significativo respecto a las soluciones existentes "
    "que operan únicamente en castellano."
)

h2("3.11 Pruebas realizadas")

add_table(doc,
    ["ID", "Tipo", "Caso", "Resultado esperado"],
    [
        ["CP-01", "Caja negra", "Envío de mensaje válido sobre trámite", "200 + respuesta con información del trámite"],
        ["CP-02", "Caja negra", "Consulta en quechua", "200 + respuesta en quechua"],
        ["CP-03", "Caja negra", "Transcripción de audio válido", "200 + texto transcrito"],
        ["CP-04", "Caja negra", "Traducción de textos del sitio", "200 + traducciones en quechua"],
        ["CP-05", "Caja negra", "Estado de la API de IA", "200 + {ai: true/false}"],
        ["CP-06", "Unitaria", "Detección de idioma (es/qu)", "Correcta identificación de idioma"],
        ["CP-07", "Unitaria", "Detección de trámite por palabra clave", "Correcta identificación del trámite"],
        ["CP-08", "Unitaria", "Detección de intención (12 tipos)", "Clasificación correcta de intención"],
        ["CP-09", "Caja blanca", "Cobertura de decisiones en engine.py", "≥95% de cobertura"],
        ["CP-10", "Caja blanca", "Cobertura total del sistema", "≥95% de cobertura"],
    ])

h2("3.12 Resultados preliminares")
para(
    "Las 145 pruebas ejecutadas demuestran el correcto funcionamiento del motor del chatbot, "
    "la API REST y la integración con los servicios de IA. La base de conocimiento contiene "
    "25 trámites con información bilingüe completa, y el widget de chat funciona correctamente "
    "en dispositivos móviles y equipos de escritorio. La cobertura del 98% da confianza "
    "sobre la solidez del código implementado."
)

h2("3.13 Viabilidad y sostenibilidad")

h3("3.13.1 Viabilidad técnica")
para(
    "La solución utiliza tecnologías de código abierto disponibles en el entorno de desarrollo. "
    "Python y Flask permiten crear una API eficiente con un framework probado. La API de OpenAI "
    "ofrece capacidades de IA de vanguardia sin necesidad de infraestructura propia de "
    "entrenamiento de modelos. El sistema puede ejecutarse en un servidor local o en plataformas "
    "cloud con planes gratuitos o de bajo costo."
)

h3("3.13.2 Viabilidad económica")
para(
    "Python, Flask y las tecnologías de frontend son gratuitas. La API de OpenAI tiene costos "
    "bajos por consulta (aproximadamente $0.15 por millón de tokens de entrada con GPT-4o-mini). "
    "El mantenimiento puede ser realizado por personal técnico de la institución sin necesidad "
    "de licencias comerciales."
)

h3("3.13.3 Sostenibilidad institucional")
para(
    "Para sostener la aplicación será necesario: asignar responsables de mantenimiento, "
    "establecer una política de actualización de la base de conocimiento, realizar copias "
    "de respaldo periódicas y mantener actualizado el entorno técnico. La documentación "
    "del código y el manual de usuario facilitarán futuras mejoras."
)

add_table(doc,
    ["Recurso", "Disponibilidad", "Acción para sostenerlo"],
    [
        ["Software", "Tecnologías libres (Python, Flask)", "Actualizar dependencias y conservar versiones estables"],
        ["Base de conocimiento", "Información municipal de Sacaba", "Definir procedimiento de actualización trimestral"],
        ["API de OpenAI", "Servicio externo de pago", "Monitorear uso y costos, optimizar consultas"],
        ["Personal técnico", "Docentes y responsables TIC del ITSa", "Capacitar usuarios y asignar administración"],
        ["Infraestructura", "Servidor o equipo local", "Programar respaldos y mantenimiento preventivo"],
    ])

add_page_break()

# =====================================================================
# CAPÍTULO IV. CONCLUSIONES Y RECOMENDACIONES
# =====================================================================
h1("CAPÍTULO IV. CONCLUSIONES Y RECOMENDACIONES")

h2("4.1 Conclusiones")
bullet(
    "El chatbot municipal responde a una necesidad real del municipio de Sacaba al ofrecer "
    "un canal digital de orientación ciudadana disponible las 24 horas del día."
)
bullet(
    "La integración de inteligencia artificial (ChatGPT) con una base de conocimiento local "
    "estructurada permite ofrecer respuestas precisas y flexibles, superando las limitaciones "
    "de los chatbots basados exclusivamente en respuestas predeterminadas."
)
bullet(
    "El soporte bilingüe castellano–quechua constituye un avance significativo en inclusión "
    "lingüística, permitiendo que la población quechua-hablante acceda a información municipal "
    "en su idioma."
)
bullet(
    "La arquitectura Flask–Python con API REST permite una implementación eficiente, modular "
    "y escalable que facilita futuras ampliaciones."
)
bullet(
    "Las 145 pruebas automatizadas con 98% de cobertura demuestran la solidez del código "
    "implementado y proporcionan confianza ante futuras modificaciones."
)
bullet(
    "El valor del sistema está en apoyar la revisión e información ciudadana; el chatbot no "
    "reemplaza la atención presencial sino que la complementa."
)

h2("4.2 Recomendaciones")
bullet(
    "Ampliar la base de conocimiento con nuevos trámites y servicios a medida que el municipio "
    "los implemente, siguiendo un procedimiento documentado de actualización."
)
bullet(
    "Implementar un sistema de registro y monitoreo de consultas para identificar los trámites "
    "más consultados y detectar posibles vacíos de información."
)
bullet(
    "Realizar validaciones periódicas de las traducciones al quechua con hablantes nativos "
    "para garantizar la precisión y naturalidad de los contenidos."
)
bullet(
    "Considerar la implementación de OCR (reconocimiento óptico de caracteres) para permitir "
    "la comparación de documentos escaneados en futuras versiones."
)
bullet(
    "Establecer respaldos periódicos de la base de conocimiento y controles de acceso antes "
    "del uso institucional definitivo."
)
bullet(
    "Definir institucionalmente los criterios de uso y las responsabilidades asociadas al "
    "mantenimiento del chatbot como herramienta pública."
)

add_page_break()

# =====================================================================
# BIBLIOGRAFÍA
# =====================================================================
h1("BIBLIOGRAFÍA")

referencias = [
    "Bird, S., Klein, E., & Loper, E. (2009). Natural Language Processing with Python. O'Reilly Media.",
    "González, J. (2022). Transformación digital en gobiernos locales. McGraw-Hill.",
    "Instituto Nacional de Estadística. (2024). Censo de Población y Vivienda 2024. INE Bolivia.",
    "Jurafsky, D., & Martin, J. H. (2023). Speech and Language Processing (3.ª ed.). Pearson.",
    "Laravel. (2026). Documentación oficial del framework Laravel.",
    "Manning, C. D., Raghavan, P. y Schütze, H. (2008). Introduction to Information Retrieval. Cambridge University Press.",
    "Mozilla Foundation. (2024). MDN Web Docs. https://developer.mozilla.org/",
    "OpenAI. (2026). Documentation: Chat Completions API and Whisper.",
    "Oracle. (2026). MySQL Reference Manual.",
    "Pallets Projects. (2024). Flask Documentation. https://flask.palletsprojects.com/",
    "Pressman, R. S. y Maxim, B. R. (2014). Software Engineering: A Practitioner's Approach. McGraw-Hill.",
    "Sommerville, I. (2011). Software Engineering. Pearson.",
    "Agencia para el Desarrollo de la Sociedad de la Información en Bolivia (ADSIB). (2025). Ciudadanía Digital y Gobierno Electrónico en Bolivia. Gobierno del Estado Plurinacional de Bolivia.",
    "Hernández-Sampieri, R., Fernández-Collado, C. y Baptista, P. (2018). Metodología de la investigación. McGraw-Hill.",
]

for ref in referencias:
    p = doc.add_paragraph(ref)
    p.paragraph_format.space_after = Pt(4)

add_page_break()

# =====================================================================
# ANEXO A. Estructura del proyecto
# =====================================================================
h1("ANEXO A. Estructura del proyecto")

add_code(doc,
    "chatbot-sacaba/\n"
    "├── app.py                    # Servidor Flask y rutas API\n"
    "├── chatbot/\n"
    "│   ├── __init__.py\n"
    "│   ├── engine.py             # Motor: KB, detección de idioma/intención, respuestas IA\n"
    "│   ├── chatbot-widget.css    # Estilos del widget de chat\n"
    "│   └── chatbot-widget.js     # Lógica del widget de chat\n"
    "├── templates/\n"
    "│   └── index.html            # Página principal del sitio web\n"
    "├── static/\n"
    "│   ├── css/                  # Estilos del sitio\n"
    "│   ├── js/                   # Scripts del sitio\n"
    "│   └── img/                  # Imágenes y logo\n"
    "├── tests/\n"
    "│   ├── conftest.py           # Configuración de pruebas\n"
    "│   ├── test_unitarias.py     # 62 pruebas unitarias\n"
    "│   ├── test_caja_negra.py    # 39 pruebas de caja negra\n"
    "│   └── test_caja_blanca.py   # 44 pruebas de caja blanca\n"
    "├── requirements.txt          # Dependencias del proyecto\n"
    "├── .env                      # Variables de entorno (API key)\n"
    "├── generar_docx.py           # Generador de documento de pruebas\n"
    "└── generar_proyecto_grado.py # Generador de este documento"
)

add_page_break()

# =====================================================================
# ANEXO B. Evidencias del sistema
# =====================================================================
h1("ANEXO B. Evidencias del sistema")

para("B.1 Página principal del sitio web", bold=True)
para("El sitio web presenta la información del municipio con navegación por secciones: Inicio, Trámites, Multas, Institución y Contacto. El widget de chat se encuentra embebido en la esquina inferior derecha.")

doc.add_paragraph()

para("B.2 Widget de chat - Interacción en castellano", bold=True)
para("El usuario puede escribir consultas en castellano sobre trámites municipales. El chatbot responde con información estructurada incluyendo ubicación, costo, tiempo y consejos.")

doc.add_paragraph()

para("B.3 Widget de chat - Interacción en quechua", bold=True)
para("El sistema detecta automáticamente cuando el usuario escribe en quechua y responde en el mismo idioma, utilizando vocabulario cotidiano (runasimi boliviano) con préstamos del castellano para mayor claridad.")

doc.add_paragraph()

para("B.4 Transcripción de audio", bold=True)
para("El usuario puede enviar mensajes de voz que son transcritos a texto mediante la API de Whisper, permitiendo la interacción vocal con el chatbot.")

doc.add_paragraph()

para("B.5 Respuesta con tarjeta de trámite", bold=True)
para("El chatbot genera tarjetas formateadas con icono, nombre del trámite, descripción, ubicación (con enlace a Google Maps), costo, tiempo estimado y consejo práctico.")

doc.add_paragraph()

para("B.6 Respuesta de multas", bold=True)
para("El sistema muestra la información de multas de tránsito y municipales con sus rangos de costo y el procedimiento de pago.")

add_page_break()

# =====================================================================
# ANEXO C. Pruebas automatizadas
# =====================================================================
h1("ANEXO C. Resumen de pruebas automatizadas")

para("Total de pruebas: 145 — Todas exitosas", bold=True)

doc.add_paragraph()

add_table(doc,
    ["Suite", "Archivo", "Casos", "Estado"],
    [
        ["Unitarias", "tests/test_unitarias.py", "62", "62 passed ✓"],
        ["Caja negra", "tests/test_caja_negra.py", "39", "39 passed ✓"],
        ["Caja blanca", "tests/test_caja_blanca.py", "44", "44 passed ✓"],
        ["Total", "", "145", "145 passed ✓"],
    ])

doc.add_paragraph()

para("Cobertura de código: 98%", bold=True)

add_table(doc,
    ["Módulo", "Sentencias", "Sin cubrir", "Cobertura"],
    [
        ["app.py", "83", "3", "96%"],
        ["chatbot/engine.py", "230", "3", "99%"],
        ["TOTAL", "313", "6", "98%"],
    ])

doc.add_paragraph()

para(
    "Las 6 líneas sin cubrir corresponden a la configuración de arranque (run_app), el modo "
    "empaquetado PyInstaller (_load_env_file) y la rama de importación sin API key: código de "
    "entorno que no forma parte de la lógica de negocio del chatbot."
)

add_page_break()

# =====================================================================
# ANEXO D. Comandos para ejecutar pruebas
# =====================================================================
h1("ANEXO D. Cómo ejecutar las pruebas")

add_code(doc,
    "pip install -r requirements.txt\n"
    "\n"
    "# Ejecutar todas las suites\n"
    "python -m pytest tests -v\n"
    "\n"
    "# Solo unitarias\n"
    "python -m pytest tests/test_unitarias.py -v\n"
    "\n"
    "# Solo caja negra\n"
    "python -m pytest tests/test_caja_negra.py -v\n"
    "\n"
    "# Solo caja blanca\n"
    "python -m pytest tests/test_caja_blanca.py -v\n"
    "\n"
    "# Alternativa sin pytest\n"
    "python -m unittest discover -s tests -v\n"
    "\n"
    "# Informe de cobertura\n"
    "coverage run -m pytest tests && coverage report\n"
    "coverage html  # Reporte navegable en htmlcov/"
)

# =====================================================================
# GUARDAR
# =====================================================================
doc.save("PROYECTO_GRADO_CHATBOT.docx")
print("PROYECTO_GRADO_CHATBOT.docx generado correctamente")
