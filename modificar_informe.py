# -*- coding: utf-8 -*-
"""
Modifica Informe_Final_Feria_Sello_ITSa.docx:
Mantene las 2 portadas intactas y reemplaza TODO el contenido
restante por el proyecto del Chatbot Municipal Sacaba.
"""
import sys
import copy
sys.stdout.reconfigure(encoding='utf-8')

from docx import Document

doc = Document('Informe_Final_Feria_Sello_ITSa.docx')

# =====================================================================
# FUNCIONES AUXILIARES
# =====================================================================
def set_para_text(para, text):
    """Reemplaza el texto de un párrafo conservando formato del primer run."""
    if not para.runs:
        para.text = text
        return
    first_run = para.runs[0]
    # Guardar formato
    font_name = first_run.font.name
    font_size = first_run.font.size
    bold = first_run.bold
    italic = first_run.italic
    color = first_run.font.color.rgb if first_run.font.color and first_run.font.color.rgb else None
    # Limpiar todos los runs excepto el primero
    for run in para.runs[1:]:
        run.text = ""
    first_run.text = text
    if font_name:
        first_run.font.name = font_name
    if font_size:
        first_run.font.size = font_size
    if bold is not None:
        first_run.bold = bold
    if italic is not None:
        first_run.italic = italic
    if color:
        first_run.font.color.rgb = color


def set_cell_text(cell, text):
    """Reemplaza el texto de una celda de tabla conservando formato."""
    if not cell.paragraphs:
        cell.text = text
        return
    p = cell.paragraphs[0]
    if not p.runs:
        p.text = text
        return
    first_run = p.runs[0]
    font_name = first_run.font.name
    font_size = first_run.font.size
    bold = first_run.bold
    for run in p.runs[1:]:
        run.text = ""
    first_run.text = text
    if font_name:
        first_run.font.name = font_name
    if font_size:
        first_run.font.size = font_size
    if bold is not None:
        first_run.bold = bold


# =====================================================================
# MAPEO DE CONTENIDO: ÍNDICE DEL PÁRRAFO -> NUEVO TEXTO
# =====================================================================
# Solo modificamos desde párrafo 48 en adelante (después de las 2 portadas)

# -- RESUMEN (párrafo 48 en adelante) --
# El RESUMEN está en párrafos 48-57 aproximadamente
# Primero buscamos dónde empieza cada sección

# Función para reemplazar párrafos por índice
def replace_para(idx, text):
    if idx < len(doc.paragraphs):
        set_para_text(doc.paragraphs[idx], text)

# Reemplazar RESUMEN
replace_para(48, "RESUMEN")

# Párrafos del resumen (49-57)
replace_para(49, "Chatbot Municipal Sacaba es una aplicación web multiidioma desarrollada para orientar a los ciudadanos del municipio de Sacaba sobre trámites y multas municipales. La solución integra un asistente virtual con inteligencia artificial (ChatGPT de OpenAI) que responde consultas en castellano y quechua, apoyándose en una base de conocimiento local estructurada con información sobre 25 trámites municipales, multas, horarios y servicios públicos.")

replace_para(50, "El prototipo funciona con una arquitectura basada en Python y Flask en el backend, con una interfaz web construida en HTML, CSS y JavaScript. Utiliza la API de OpenAI para respuestas inteligentes (GPT-4o-mini) y Whisper para la transcripción de audio a texto. El sistema incluye detección automática de idioma (castellano/quechua), traducción del sitio web mediante IA y un widget de chat embebido disponible en dispositivos móviles y equipos de escritorio.")

# Saltamos párrafos vacíos y la tabla del resumen (se modifica por separado)
# Párrafos 51-58 son la tabla del resumen y espacios

# Modificar la tabla del resumen (Tabla 1)
t0 = doc.tables[0]  # Portada 1 - NO tocar
t1 = doc.tables[1]  # Tabla del resumen
set_cell_text(t1.rows[1].cells[0], "Nombre del proyecto")
set_cell_text(t1.rows[1].cells[1], "Chatbot Municipal Sacaba")
set_cell_text(t1.rows[2].cells[1], "Proyecto de Grado")
set_cell_text(t1.rows[3].cells[0], "Área")
set_cell_text(t1.rows[3].cells[1], "Desarrollo de Aplicaciones Web / Atención Ciudadana")
set_cell_text(t1.rows[4].cells[1], "Prototipo funcional en desarrollo")
set_cell_text(t1.rows[5].cells[0], "Tecnologías")
set_cell_text(t1.rows[5].cells[1], "Python, Flask, HTML, CSS, JavaScript, OpenAI API")
set_cell_text(t1.rows[6].cells[0], "Método")
set_cell_text(t1.rows[6].cells[1], "Base de conocimiento local + ChatGPT (GPT-4o-mini)")
set_cell_text(t1.rows[7].cells[0], "Alcance")
set_cell_text(t1.rows[7].cells[1], "Trámites y multas del G.A.M. Sacaba")
# Agregar fila de idiomas
row_idiomas = t1.add_row()
set_cell_text(row_idiomas.cells[0], "Idiomas soportados")
set_cell_text(row_idiomas.cells[1], "Castellano y Quechua (runasimi boliviano)")

# =====================================================================
# CAPÍTULO I - PLANTEAMIENTO DEL PROBLEMA (párrafos ~59-82)
# =====================================================================
replace_para(59, "CAPÍTULO I. PLANTEAMIENTO DEL PROBLEMA")

# 1.1
replace_para(60, "1.1 Diagnóstico y justificación")
replace_para(61, "El Gobierno Autónomo Municipal de Sacaba gestiona diversos trámites y servicios públicos que los ciudadanos requieren de manera frecuente: emisión de cédulas de identidad, constancias de residencia, licencias de funcionamiento, permisos de construcción, inscripción de vehículos, entre otros. Sin embargo, la información sobre estos trámites se encuentra dispersa en dependencias municipales, y los ciudadanos frecuentemente deben acudir presencialmente para obtener orientación básica sobre requisitos, costos, horarios y procedimientos.")
replace_para(62, "Esta situación genera tiempos de espera prolongados, múltiples desplazamientos innecesarios y saturación de los canales de atención. El problema se agrava para la población quechua-hablante del municipio, ya que la mayoría de los servicios de información municipal se encuentran únicamente en castellano, generando barreras lingüísticas que limitan el acceso equitativo a la información pública. Implementar un chatbot bilingüe constituye una oportunidad concreta de modernización y inclusión social.")

# 1.2
replace_para(63, "1.2 Planteamiento y formulación")
replace_para(64, "Problema central:")
replace_para(65, "Limitado acceso a información oportuna y bilingüe sobre trámites y multas municipales en el Gobierno Autónomo Municipal de Sacaba.")
replace_para(67, "Formulación: ¿De qué manera se puede contribuir a mejorar la orientación sobre trámites y multas municipales, reducir los tiempos de respuesta y fortalecer la inclusión lingüística de los ciudadanos del municipio de Sacaba?")

# Tabla de causas-efectos (Tabla 2)
t2 = doc.tables[2]
set_cell_text(t2.rows[1].cells[0], "Atención presencial como canal principal")
set_cell_text(t2.rows[1].cells[1], "Tiempos de espera prolongados y múltiples desplazamientos")
set_cell_text(t2.rows[2].cells[0], "Información municipal dispersa y no digitalizada")
set_cell_text(t2.rows[2].cells[1], "Dificultad para acceder a requisitos y costos actualizados")
set_cell_text(t2.rows[3].cells[0], "Ausencia de soporte en idioma quechua")
set_cell_text(t2.rows[3].cells[1], "Barreras lingüísticas para la población quechua-hablante")
set_cell_text(t2.rows[4].cells[0], "Horarios limitados de atención presencial")
set_cell_text(t2.rows[4].cells[1], "Inaccesibilidad fuera del horario laboral")

# 1.3
replace_para(69, "1.3 Objetivos")
replace_para(70, "1.3.1 Objetivo general")
replace_para(71, "Desarrollar un chatbot web multiidioma (Castellano–Quechua) que permita orientar a los ciudadanos del municipio de Sacaba sobre trámites y multas municipales mediante una plataforma digital accesible, disponible las 24 horas del día.")

replace_para(72, "1.3.2 Objetivos específicos")
replace_para(73, "Identificar los trámites y multas municipales de mayor demanda ciudadana mediante la recopilación y análisis de información proporcionada por las dependencias del Gobierno Autónomo Municipal de Sacaba.")
replace_para(74, "Elaborar una base de conocimiento bilingüe en castellano y quechua con información estructurada sobre requisitos, procedimientos, costos y sanciones municipales.")
replace_para(75, "Diseñar la arquitectura funcional del sistema y los flujos de conversación del chatbot, definiendo categorías de consulta y mecanismos de interacción.")
replace_para(76, "Implementar una aplicación web de orientación ciudadana con un chatbot con inteligencia artificial integrada, con soporte bilingüe castellano–quechua.")
replace_para(77, "Implementar una interfaz accesible e intuitiva que permita consultar información municipal desde dispositivos móviles y equipos de escritorio.")
replace_para(78, "Realizar pruebas funcionales, unitarias y de caja blanca para verificar el correcto funcionamiento del sistema y la precisión de las respuestas.")

# 1.4
replace_para(79, "1.4 Enfoque metodológico")
replace_para(80, "La investigación adopta un enfoque mixto, combinando técnicas cuantitativas y cualitativas para analizar la problemática del acceso a información municipal. El componente cuantitativo trabaja con datos medibles como porcentajes de cobertura, tiempos de respuesta y resultados de pruebas. El componente cualitativo conoce las opiniones y necesidades de los usuarios mediante entrevistas y observación en dependencias municipales.")
replace_para(81, "El desarrollo sigue un enfoque iterativo e incremental, construyendo y validando funcionalidades de manera progresiva: análisis de requerimientos, diseño, implementación, pruebas y retroalimentación.")
replace_para(82, "")

# =====================================================================
# CAPÍTULO II - MARCO TEÓRICO (párrafos 83-109)
# =====================================================================
replace_para(83, "CAPÍTULO II. MARCO TEÓRICO CONCEPTUAL")

replace_para(84, "2.1 Chatbots y asistentes virtuales")
replace_para(85, "Un chatbot es un programa de software diseñado para simular conversaciones con usuarios a través de interfaces de texto o voz. Los chatbots se clasifican en basados en reglas (respuestas predeterminadas) e impulsados por inteligencia artificial (comprensión y generación de lenguaje natural). En servicios públicos, los chatbots permiten automatizar consultas frecuentes, reducir tiempos de atención y ofrecer servicio disponible las 24 horas.")
replace_para(86, "Los modelos de lenguaje grandes (LLM) como GPT-4 de OpenAI representan el estado del arte en generación de texto. Para un chatbot municipal, la integración de un LLM permite ofrecer respuestas flexibles y naturales, superando las limitaciones de chatbots basados exclusivamente en respuestas predeterminadas.")

replace_para(87, "2.2 Inteligencia artificial y procesamiento de lenguaje natural")
replace_para(88, "El procesamiento de lenguaje natural (NLP) es una rama de la inteligencia artificial que permite a las máquinas comprender, interpretar y generar texto o voz humana. Incluye tokenización, lematización, análisis de sentimientos, detección de intención y generación de respuestas. Los modelos como GPT-4o-mini permiten generar respuestas coherentes y contextuales.")

replace_para(89, "2.3 Detección de idioma y bilingüismo")
replace_para(90, "La detección automática de idioma permite al chatbot identificar si el usuario escribe en castellano o quechua y responder en el mismo idioma. Para el quechua boliviano (runasimi), se utilizan tokens característicos como \"imaynallan\", \"allillanmi\", \"kachkani\" que permiten distinguirlo del castellano. Esta funcionalidad es esencial para promover la inclusión lingüística.")

replace_para(91, "2.4 Transcripción de voz a texto")
replace_para(92, "La transcripción de audio a texto permite a los usuarios realizar consultas mediante voz. Modelos como Whisper de OpenAI ofrecen transcripción precisa en múltiples idiomas. Esta capacidad es especialmente relevante para poblaciones con limitaciones de lectoescritura o que prefieren la interacción vocal.")

replace_para(93, "2.5 Flask y arquitectura web")
replace_para(94, "Flask es un framework de desarrollo web en Python diseñado para aplicaciones de pequeña y mediana escala. Su arquitectura ligera y modular permite crear APIs RESTful, gestionar rutas y manejar sesiones. Adopta el enfoque MVC que mejora la mantenibilidad, escalabilidad y testeo del sistema.")

replace_para(95, "2.6 Base de conocimiento estructurada")
replace_para(96, "Una base de conocimiento es una estructura de datos que almacena información organizada para su consulta y procesamiento. Para este proyecto, se estructura como un diccionario anidado en Python, con entradas para cada trámite en castellano y quechua, permitiendo al motor del chatbot generar respuestas contextuales e idiomáticas.")

replace_para(97, "2.7 Tecnologías utilizadas")
replace_para(98, "")
replace_para(99, "")
replace_para(100, "")
replace_para(101, "")
replace_para(102, "")
replace_para(103, "")
replace_para(104, "2.8 Seguridad y protección de la información")
replace_para(105, "La aplicación protege credenciales mediante variables de entorno (.env) que almacenan las claves de API fuera del código fuente. Flask proporciona protección CSRF, validación de entradas y gestión segura de sesiones. Los documentos de audio se procesan de forma temporal y no se almacenan permanentemente.")

# Tabla de tecnologías (Tabla 4)
t4 = doc.tables[4]
set_cell_text(t4.rows[1].cells[0], "Python 3.14")
set_cell_text(t4.rows[1].cells[1], "Lenguaje de programación principal del backend")
set_cell_text(t4.rows[2].cells[0], "Flask 3.1.3")
set_cell_text(t4.rows[2].cells[1], "Framework web para API REST y servidor")
set_cell_text(t4.rows[3].cells[0], "OpenAI API (GPT-4o-mini)")
set_cell_text(t4.rows[3].cells[1], "Generación de respuestas inteligentes con IA")
set_cell_text(t4.rows[4].cells[0], "HTML5 / CSS3 / JavaScript")
set_cell_text(t4.rows[4].cells[1], "Interfaz de usuario y widget de chat")
set_cell_text(t4.rows[5].cells[0], "OpenAI Whisper")
set_cell_text(t4.rows[5].cells[1], "Transcripción de audio a texto")
set_cell_text(t4.rows[6].cells[0], "python-dotenv")
set_cell_text(t4.rows[6].cells[1], "Gestión de variables de entorno")
set_cell_text(t4.rows[7].cells[0], "pytest / coverage")
set_cell_text(t4.rows[7].cells[1], "Pruebas y medición de cobertura de código")

# =====================================================================
# CAPÍTULO III - PROPUESTA DE INNOVACIÓN (párrafos 110-168)
# =====================================================================
replace_para(110, "CAPÍTULO III. PROPUESTA DE INNOVACIÓN")

replace_para(111, "3.1 Descripción de la solución")
replace_para(112, "Chatbot Municipal Sacaba es una aplicación web que centraliza la información municipal y ofrece un canal de atención automatizada mediante un asistente virtual bilingüe. El flujo comienza con la interacción del usuario a través del widget de chat: el sistema detecta el idioma, procesa la consulta mediante el motor NLP local o la API de ChatGPT, y retorna una respuesta estructurada con información relevante sobre el trámite consultado. El sistema también incluye transcripción de audio y traducción del sitio web a quechua.")

replace_para(113, "3.2 Usuarios y responsabilidades")

# Tabla de usuarios (Tabla 5)
t5 = doc.tables[5]
set_cell_text(t5.rows[1].cells[0], "Ciudadano")
set_cell_text(t5.rows[1].cells[1], "Realizar consultas sobre trámites, multas, horarios y servicios municipales mediante chat de texto o voz.")
set_cell_text(t5.rows[2].cells[0], "Administrador")
set_cell_text(t5.rows[2].cells[1], "Gestionar la base de conocimiento, actualizar información, monitorear el uso y configurar la API de IA.")
set_cell_text(t5.rows[3].cells[0], "Desarrollador")
set_cell_text(t5.rows[3].cells[1], "Mantener el código fuente, implementar mejoras, realizar pruebas y gestionar actualizaciones.")

replace_para(115, "3.3 Módulos del sistema")
replace_para(116, "Módulo de Chat: Interfaz de conversación con el usuario, envío y recepción de mensajes.")
replace_para(117, "Motor NLP: Detección de idioma, intención y trámite. Generación de respuestas basadas en reglas.")
replace_para(118, "Integración con IA: Conexión con la API de OpenAI (ChatGPT) para respuestas inteligentes.")
replace_para(119, "Transcripción de Audio: Conversión de voz a texto mediante Whisper de OpenAI.")
replace_para(120, "Base de Conocimiento: Estructura de datos con 25 trámites bilingües, multas, horarios y contacto.")
replace_para(121, "Widget de Chat: Componente JavaScript embebido en el sitio web, adaptable a dispositivos móviles.")

replace_para(123, "3.4 Arquitectura funcional")

# Tabla de arquitectura (Tabla 6)
t6 = doc.tables[6]
set_cell_text(t6.rows[1].cells[0], "Presentación")
set_cell_text(t6.rows[1].cells[1], "Widget de chat (JS/CSS), sitio web (HTML/CSS/JS)")
set_cell_text(t6.rows[1].cells[2], "Interacción visual con el usuario, envío de mensajes")
set_cell_text(t6.rows[2].cells[0], "Aplicación")
set_cell_text(t6.rows[2].cells[1], "Rutas Flask (app.py), lógica de negocio")
set_cell_text(t6.rows[2].cells[2], "Recibir peticiones, validar datos, coordinar respuestas")
set_cell_text(t6.rows[3].cells[0], "Motor NLP")
set_cell_text(t6.rows[3].cells[1], "chatbot/engine.py")
set_cell_text(t6.rows[3].cells[2], "Detección de idioma, intención, trámite; respuestas por reglas")
set_cell_text(t6.rows[4].cells[0], "IA")
set_cell_text(t6.rows[4].cells[1], "API de OpenAI (ChatGPT, Whisper)")
set_cell_text(t6.rows[4].cells[2], "Respuestas inteligentes, transcripción, traducción")

replace_para(125, "3.5 Modelo de datos - Base de conocimiento")

# Tabla de modelo de datos (Tabla 7)
t7 = doc.tables[7]
# Eliminar filas existentes y crear nuevas
# Primero limpiar filas existentes (rows 1-6)
new_data = [
    ("carnet", "Carnet de Identidad (SEGIP) - Bs. 17, inmediato"),
    ("residencia", "Constancia de Residencia - Bs. 15, 2-3 días"),
    ("funcionamiento", "Licencia de Funcionamiento - Bs. 60 nuevo / Bs. 40 renovación"),
    ("construccion", "Permiso de Construcción - Planos de vivienda"),
    ("propiedad", "Registro de Propiedad - Derechos Reales"),
    ("solteria", "Constancia de Soltería - Bs. 10, inmediato"),
    ("prediales", "Impuestos Prediales - 0.5% - 1% del valor catastral"),
    ("agua", "Servicio de Agua Potable - Bs. 50-200"),
    ("vehiculos", "Registro de Vehículos - Bs. 30-150"),
    ("MULTAS", "Tránsito (Bs. 50-1000) y Municipales (Bs. 50-2000)"),
]
for i, (ent, info) in enumerate(new_data):
    if i + 1 < len(t7.rows):
        set_cell_text(t7.rows[i + 1].cells[0], ent)
        set_cell_text(t7.rows[i + 1].cells[1], info)
    else:
        row = t7.add_row()
        set_cell_text(row.cells[0], ent)
        set_cell_text(row.cells[1], info)

replace_para(127, "La base de conocimiento contiene 25 trámites municipales organizados por categorías, cada uno con información en castellano y quechua incluyendo: nombre, descripción, ubicación, costo, requisitos, procedimiento, tiempo estimado, horario y consejo práctico.")

replace_para(129, "3.6 Funcionamiento del motor de chat")

# Tabla de algoritmo (Tabla 8)
t8 = doc.tables[8]
set_cell_text(t8.rows[1].cells[0], "1. Recepción")
set_cell_text(t8.rows[1].cells[1], "El usuario envía un mensaje de texto o audio a través del widget de chat.")
set_cell_text(t8.rows[2].cells[0], "2. Detección de idioma")
set_cell_text(t8.rows[2].cells[1], "Se analizan tokens de quechua para determinar el idioma de respuesta.")
set_cell_text(t8.rows[3].cells[0], "3. Detección de trámite")
set_cell_text(t8.rows[3].cells[1], "Se buscan palabras clave para identificar el trámite (25 patrones).")
set_cell_text(t8.rows[4].cells[0], "4. Detección de intención")
set_cell_text(t8.rows[4].cells[1], "Se clasifica: saludo, costo, ubicación, requisitos, procedimiento, multas, etc.")
set_cell_text(t8.rows[5].cells[0], "5. Generación de respuesta")
set_cell_text(t8.rows[5].cells[1], "Si la IA está disponible, se usa ChatGPT con contexto. Si no, respuesta local.")
set_cell_text(t8.rows[6].cells[0], "6. Respuesta")
set_cell_text(t8.rows[6].cells[1], "El sistema retorna la respuesta formateada en el idioma detectado.")
set_cell_text(t8.rows[7].cells[0], "7. Traducción del sitio")
set_cell_text(t8.rows[7].cells[1], "Opcionalmente traduce elementos HTML del sitio web a quechua.")

replace_para(130, "3.7 Flujo de navegación")
replace_para(131, "Ingreso al sitio web → Visualización del widget de chat → Envío de consulta (texto o voz) → Detección automática de idioma → Procesamiento de la consulta → Visualización de la respuesta → Posibilidad de realizar nuevas consultas. El usuario también puede cambiar el idioma del sitio completo mediante un botón en la barra de navegación.")
replace_para(132, "")

replace_para(134, "3.8 Estado de implementación")

# Tabla de estado (Tabla 9)
t9 = doc.tables[9]
set_cell_text(t9.rows[1].cells[0], "Base de conocimiento")
set_cell_text(t9.rows[1].cells[1], "25 trámites × 2 idiomas, multas y textos de interfaz")
set_cell_text(t9.rows[2].cells[0], "Motor NLP")
set_cell_text(t9.rows[2].cells[1], "Funcional: detección de idioma, intención y trámite")
set_cell_text(t9.rows[3].cells[0], "Integración con OpenAI")
set_cell_text(t9.rows[3].cells[1], "Funcional: ChatGPT para respuestas, Whisper para audio")
set_cell_text(t9.rows[4].cells[0], "Widget de chat")
set_cell_text(t9.rows[4].cells[1], "Implementado con diseño responsive y soporte de voz")
set_cell_text(t9.rows[5].cells[0], "Traducción del sitio")
set_cell_text(t9.rows[5].cells[1], "Funcional: traduce elementos HTML a quechua mediante IA")
set_cell_text(t9.rows[6].cells[0], "API REST")
set_cell_text(t9.rows[6].cells[1], "Todos los endpoints funcionales y validados")
set_cell_text(t9.rows[7].cells[0], "Pruebas automatizadas")
set_cell_text(t9.rows[7].cells[1], "145 pruebas exitosas (unitarias, caja negra, caja blanca)")
# Agregar fila
row_cov = t9.add_row()
set_cell_text(row_cov.cells[0], "Cobertura de código")
set_cell_text(row_cov.cells[1], "98% de cobertura de sentencias y decisiones")

replace_para(136, "El sistema se presenta como prototipo funcional. Durante la feria se demuestra el chatbot respondiendo consultas en castellano y quechua, la transcripción de audio, la traducción del sitio y los resultados de las 145 pruebas automatizadas con 98% de cobertura.")

replace_para(137, "3.9 Innovación y aporte")
replace_para(138, "El aporte distintivo es la combinación de inteligencia artificial con una base de conocimiento local específica para Sacaba. A diferencia de chatbots basados solo en respuestas predeterminadas, este sistema integra ChatGPT para respuestas flexibles y naturales. El soporte bilingüe castellano–quechua promueve la inclusión lingüística, y la detección automática de idioma con respuesta en quechua cotidiano (runasimi boliviano) es un avance significativo respecto a soluciones existentes.")

replace_para(140, "3.10 Pruebas realizadas")
replace_para(141, "3.11 Resultados preliminares")

# Tabla de pruebas (Tabla 10)
t10 = doc.tables[10]
set_cell_text(t10.rows[1].cells[0], "CP-01")
set_cell_text(t10.rows[1].cells[2], "Envío de mensaje válido sobre trámite.")
set_cell_text(t10.rows[1].cells[3], "200 + respuesta con información del trámite.")
set_cell_text(t10.rows[2].cells[0], "CP-02")
set_cell_text(t10.rows[2].cells[2], "Consulta en quechua.")
set_cell_text(t10.rows[2].cells[3], "200 + respuesta en quechua.")
set_cell_text(t10.rows[3].cells[0], "CP-03")
set_cell_text(t10.rows[3].cells[2], "Transcripción de audio válido.")
set_cell_text(t10.rows[3].cells[3], "200 + texto transcrito.")
set_cell_text(t10.rows[4].cells[0], "CP-04")
set_cell_text(t10.rows[4].cells[2], "Traducción de textos del sitio.")
set_cell_text(t10.rows[4].cells[3], "200 + traducciones en quechua.")
set_cell_text(t10.rows[5].cells[0], "CP-05")
set_cell_text(t10.rows[5].cells[2], "Estado de la API de IA.")
set_cell_text(t10.rows[5].cells[3], "200 + {ai: true/false}.")

replace_para(142, "Las 145 pruebas ejecutadas demuestran el correcto funcionamiento del motor del chatbot, la API REST y la integración con los servicios de IA. La base de conocimiento contiene 25 trámites bilingües, y el widget de chat funciona en dispositivos móviles y escritorio. La cobertura del 98% da confianza sobre la solidez del código.")

replace_para(144, "3.12 Viabilidad y sostenibilidad")

# 3.12.1
replace_para(145, "3.12.1 Viabilidad técnica")
replace_para(146, "La solución utiliza tecnologías de código abierto. Python y Flask permiten crear una API eficiente. La API de OpenAI ofrece capacidades de IA sin infraestructura propia de entrenamiento. El sistema puede ejecutarse en un servidor local o en plataformas cloud con planes gratuitos o de bajo costo.")

# 3.12.2
replace_para(147, "3.12.2 Viabilidad económica")
replace_para(148, "Python, Flask y las tecnologías de frontend son gratuitas. La API de OpenAI tiene costos bajos por consulta. El mantenimiento puede ser realizado por personal técnico de la institución sin licencias comerciales.")

# 3.12.3
replace_para(149, "3.12.3 Sostenibilidad institucional")
replace_para(150, "Para sostener la aplicación será necesario: asignar responsables de mantenimiento, establecer una política de actualización de la base de conocimiento, realizar copias de respaldo periódicas y mantener actualizado el entorno técnico.")

# Tabla de sostenibilidad (Tabla 11)
t11 = doc.tables[11]
set_cell_text(t11.rows[1].cells[0], "Software")
set_cell_text(t11.rows[1].cells[1], "Tecnologías libres (Python, Flask)")
set_cell_text(t11.rows[1].cells[2], "Actualizar dependencias y conservar versiones estables")
set_cell_text(t11.rows[2].cells[0], "Base de conocimiento")
set_cell_text(t11.rows[2].cells[1], "Información municipal de Sacaba")
set_cell_text(t11.rows[2].cells[2], "Definir procedimiento de actualización trimestral")
set_cell_text(t11.rows[3].cells[0], "API de OpenAI")
set_cell_text(t11.rows[3].cells[1], "Servicio externo de pago")
set_cell_text(t11.rows[3].cells[2], "Monitorear uso y costos, optimizar consultas")
set_cell_text(t11.rows[4].cells[0], "Personal técnico")
set_cell_text(t11.rows[4].cells[1], "Docentes y responsables TIC del ITSa")
set_cell_text(t11.rows[4].cells[2], "Capacitar usuarios y asignar administración")
# Agregar fila de infraestructura
row_infra = t11.add_row()
set_cell_text(row_infra.cells[0], "Infraestructura")
set_cell_text(row_infra.cells[1], "Servidor o equipo local")
set_cell_text(row_infra.cells[2], "Programar respaldos y mantenimiento preventivo")

replace_para(153, "3.13 Plan de finalización del prototipo")
replace_para(154, "Debido a que el sistema se encuentra en fase de prototipo funcional, la finalización se organiza por prioridades:")

# Tabla de plan (Tabla 12)
t12 = doc.tables[12]
set_cell_text(t12.rows[1].cells[0], "Crítica")
set_cell_text(t12.rows[1].cells[1], "Probar chat, audio, traducción y respuestas en ambos idiomas.")
set_cell_text(t12.rows[1].cells[2], "El flujo se completa sin errores con datos de prueba.")
set_cell_text(t12.rows[2].cells[0], "Alta")
set_cell_text(t12.rows[2].cells[1], "Validar permisos, mensajes de error y edge cases.")
set_cell_text(t12.rows[2].cells[2], "Entradas inválidas se rechazan de forma clara.")
set_cell_text(t12.rows[3].cells[0], "Alta")
set_cell_text(t12.rows[3].cells[1], "Preparar base de demostración y respaldo.")
set_cell_text(t12.rows[3].cells[2], "Existe una copia restaurable y verificada.")
set_cell_text(t12.rows[4].cells[0], "Media")
set_cell_text(t12.rows[4].cells[1], "Completar manual de usuario.")
set_cell_text(t12.rows[4].cells[2], "Cada módulo incluye pasos y capturas reales.")
set_cell_text(t12.rows[5].cells[0], "Media")
set_cell_text(t12.rows[5].cells[1], "Registrar resultados de pruebas.")
set_cell_text(t12.rows[5].cells[2], "Cada caso tiene evidencia y estado.")
set_cell_text(t12.rows[6].cells[0], "Futura")
set_cell_text(t12.rows[6].cells[1], "OCR, análisis semántico avanzado.")
set_cell_text(t12.rows[6].cells[2], "Queda documentado como mejora, no como función actual.")

# =====================================================================
# CAPÍTULO IV - CONCLUSIONES (párrafos 157-168)
# =====================================================================
replace_para(157, "CAPÍTULO IV. CONCLUSIONES Y RECOMENDACIONES")
replace_para(158, "4.1 Conclusiones")
replace_para(159, "El chatbot municipal responde a una necesidad real del municipio de Sacaba al ofrecer un canal digital de orientación ciudadana disponible las 24 horas del día.")
replace_para(160, "La integración de inteligencia artificial (ChatGPT) con una base de conocimiento local permite ofrecer respuestas precisas y flexibles, superando las limitaciones de chatbots basados solo en respuestas predeterminadas.")
replace_para(161, "El soporte bilingüe castellano–quechua constituye un avance significativo en inclusión lingüística, permitiendo que la población quechua-hablante acceda a información municipal en su idioma.")
replace_para(162, "La arquitectura Flask–Python con API REST permite una implementación eficiente, modular y escalable que facilita futuras ampliaciones.")
replace_para(163, "Las 145 pruebas automatizadas con 98% de cobertura demuestran la solidez del código implementado y proporcionan confianza ante futuras modificaciones.")

replace_para(164, "4.2 Recomendaciones")
replace_para(165, "Ampliar la base de conocimiento con nuevos trámites y servicios a medida que el municipio los implemente.")
replace_para(166, "Realizar validaciones periódicas de las traducciones al quechua con hablantes nativos para garantizar la precisión de los contenidos.")
replace_para(167, "Establecer respaldos periódicos de la base de conocimiento y controles de acceso antes del uso institucional definitivo.")
replace_para(168, "Definir institucionalmente los criterios de uso y las responsabilidades asociadas al mantenimiento del chatbot como herramienta pública.")

# =====================================================================
# BIBLIOGRAFÍA (párrafos 179-185)
# =====================================================================
replace_para(179, "BIBLIOGRAFÍA")
replace_para(180, "Bird, S., Klein, E., & Loper, E. (2009). Natural Language Processing with Python. O'Reilly Media.")
replace_para(181, "González, J. (2022). Transformación digital en gobiernos locales. McGraw-Hill.")
replace_para(182, "Instituto Nacional de Estadística. (2024). Censo de Población y Vivienda 2024. INE Bolivia.")
replace_para(183, "Jurafsky, D., & Martin, J. H. (2023). Speech and Language Processing (3.ª ed.). Pearson.")
replace_para(184, "Pallets Projects. (2024). Flask Documentation. https://flask.palletsprojects.com/")
replace_para(185, "Pressman, R. S. y Maxim, B. R. (2020). Ingeniería del software: Un enfoque práctico (9.ª ed.). McGraw-Hill.")

# =====================================================================
# ANEXOS (párrafos 187-201)
# =====================================================================
replace_para(187, "ANEXO B. Evidencias del sistema")
replace_para(188, "B.1 Página principal del widget de chat")
replace_para(197, "B.2 Interacción en castellano - Consulta de trámites")
replace_para(199, "B.3 Interacción en quechua - Respuesta bilingüe")
replace_para(201, "B.4 Transcripción de audio y traducción del sitio")

# =====================================================================
# GUARDAR
# =====================================================================
doc.save('Informe_Final_Feria_Chatbot.docx')
print("Informe_Final_Feria_Chatbot.docx generado correctamente")
print("Las 2 portadas se mantienen intactas.")
