"""
Motor del chatbot municipal de Sacaba.
Integra ChatGPT (API de OpenAI) para respuestas inteligentes en espanol y quechua
+ base de conocimiento local.
"""

# Importaciones necesarias
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

from dotenv import load_dotenv
import openai
import requests

# Idiomas soportados: español (es) y quechua (qu)
LANGUAGES = ("es", "qu")

# =====================================================================
# APIs EXTERNAS GRATUITAS
# =====================================================================

# API de mapas - OpenStreetMap (100% gratuita)
NOMINATIM_URL = "https://nominatim.openstreetmap.org"
OSM_TILES_URL = "https://tile.openstreetmap.org"

# API de diccionario español-quechua - Glosbe (gratuita)
GLOSBLE_API_KEY = os.getenv('GLOSBLE_API_KEY', '')
GLOSBLE_API_URL = "https://glosbe.com/gapi"

# API de IA gratuita - Google Gemini (como ChatGPT pero gratis)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
GEMINI_AVAILABLE = bool(GEMINI_API_KEY and GEMINI_API_KEY != 'TU_API_KEY_AQUI')


def _load_env_file():
    candidates = []
    bundle = getattr(sys, "_MEIPASS", None)
    if bundle:
        candidates.append(Path(bundle) / ".env")
    candidates.append(Path(".env"))
    candidates.append(Path(__file__).resolve().parent / ".env")
    candidates.append(Path(sys.argv[0]).resolve().parent / ".env")
    for p in candidates:
        if p.exists():
            load_dotenv(p)
            return


_load_env_file()

CHAT_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
AUDIO_MODEL = os.getenv('OPENAI_AUDIO_MODEL', 'whisper-1')

_api_key = os.getenv('OPENAI_API_KEY', '')
if _api_key and _api_key != 'TU_API_KEY_AQUI':
    _client = openai.OpenAI(api_key=_api_key)
    _ai_available = True
else:
    _client = None
    _ai_available = False

# --- Traductor IA gratuito de quechua (Hugging Face - NLLB-200) ----
# Actua como "especialista en quechua" junto a ChatGPT:
#   * Si el ciudadano escribe en quechua, NLLB traduce su mensaje a espanol
#     para que ChatGPT lo entienda, y luego NLLB devuelve la respuesta a quechua.
#   * Tambien se usa para traducir la pagina web (es -> quechua boliviano).
# Codigos NLLB: espanol = spa_Latn, quechua sur boliviano = quz_Latn (Cochabamba/Cuzco).
# Se apaga solo y de forma transparente si la API de HF no esta disponible.
HF_NLLB_MODEL = os.getenv('HF_NLLB_MODEL', 'facebook/nllb-200-distilled-600M')
HF_API_TOKEN = os.getenv('HF_API_TOKEN', '')
HF_INFERENCE_URL = 'https://api-inference.huggingface.co/models/' + HF_NLLB_MODEL
NLLB_ES = 'spa_Latn'
NLLB_QU = 'quz_Latn'

_HF_AVAILABLE = None  # cache: True/False tras el primer intento

def _hf_nllb_translate(text, src=NLLB_ES, tgt=NLLB_QU, timeout=60):
    """Traduce `text` de `src` a `tgt` usando el modelo NLLB-200 de Hugging Face.
    Devuelve un string, o None si la API de HF falla (no disponible, sin red, error)."""
    global _HF_AVAILABLE
    if _HF_AVAILABLE is False:
        return None
    if not text or not text.strip():
        return ""
    headers = {'Content-Type': 'application/json'}
    if HF_API_TOKEN:
        headers['Authorization'] = 'Bearer ' + HF_API_TOKEN
    payload = {
        'inputs': text,
        'parameters': {'src_lang': src, 'tgt_lang': tgt},
        'options': {'wait_for_model': True, 'use_cache': False},
    }
    try:
        r = requests.post(HF_INFERENCE_URL, json=payload, headers=headers, timeout=timeout)
        if r.status_code != 200:
            _HF_AVAILABLE = False
            return None
        data = r.json()
        if isinstance(data, list) and data:
            out = data[0].get('translation_text')
            if isinstance(out, str) and out.strip():
                return out.strip()
        _HF_AVAILABLE = False
        return None
    except Exception:
        _HF_AVAILABLE = False
        return None

def hf_nllb_available():
    """Ejecuta una mini-prueba (traduce una palabra) para saber si el traductor HF funciona."""
    if _HF_AVAILABLE is False:
        return False
    res = _hf_nllb_translate('hola', NLLB_ES, NLLB_QU)
    return res is not None

KB = {
    "carnet": {
        "es": {
            "n": "Carnet de Identidad (Cedula)",
            "icon": "\U0001FAAA",
            "d": "Documento de identificacion personal obligatorio para todos los ciudadanos bolivianos.",
            "donde": "Las oficinas del SEGIP se encuentran en Sacaba.",
            "donde_link": "https://maps.app.goo.gl/f27gLh5Accp2UmKW9",
            "cuanto": "Bs. 17 (diecisiete bolivianos).",
            "cuanto_detail": "Se puede pagar en Banco Union u otras entidades financieras autorizadas.",
            "que_necesito": ["Comprobante de pago de Bs. 17", "Cedula anterior (si es renovacion)", "Denuncia policial (en caso de perdida)"],
            "como": ["Realiza el pago de Bs. 17 en Banco Union", "Acude a las oficinas del SEGIP", "Presenta tu comprobante y cedula anterior", "Registraran tus huellas dactilares", "Te tomaran una foto digital", "Listo! Retiras tu carnet"],
            "cuanto_tarda": "Inmediato, lo haces el mismo dia.",
            "horario": "Lunes a viernes en horario habil de oficina.",
            "consejo": "Ve temprano para evitar filas. Lleva todos tus documentos.",
            "c": "Bs. 17", "t": "Inmediato", "dep": "SEGIP",
            "u": "https://maps.app.goo.gl/f27gLh5Accp2UmKW9",
        },
        "qu": {
            "n": "Carnet de Identidad (Cedula)",
            "icon": "\U0001FAAA",
            "d": "Identidad documento, obligatorio tukuy runapaq. SEGIP oficinaspi qillchachikuy (mushuqta utaq renovacion).",
            "donde": "SEGIP oficinas Sacabapi tiyanku.",
            "donde_link": "https://maps.app.goo.gl/f27gLh5Accp2UmKW9",
            "cuanto": "Bs. 17 (chunka qanchisniyuq bolivianos).",
            "cuanto_detail": "Banco Unionpi utaq huk bankokunapi pagay tiyan.",
            "que_necesito": ["Bs. 17 pagasqayki comprobante (Banco Union)", "Nawpaq cedula (renovacion kaspa)", "Denuncia policial (chinkachiptiykiqa)"],
            "como": ["Bs. 17ta pagay Banco Unionpi", "SEGIP oficinasman riy", "Comprobante nitaq cedulata rikuchiy", "Maki huellakunata registray", "Fotota horqoy", "Listo! Carnetta chaskikuy"],
            "cuanto_tarda": "Chay p'unchaylla rurasqa kan.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Tempranuta riy, filakuna ama kananpaq. Tukuy documentoykita apamuy.",
            "c": "Bs. 17", "t": "Chaylla", "dep": "SEGIP",
            "u": "https://maps.app.goo.gl/f27gLh5Accp2UmKW9",
        },
    },
    "carnet_conducta": {
        "es": {
            "n": "Certificado de Conducta (Antecedentes)",
            "icon": "\u2705",
            "d": "Documento que certifica que no tienes antecedentes penales ni policiales en Bolivia.",
            "donde": "Oficinas de la Policía (FELCC) o en línea a traves del portal policial.",
            "cuanto": "Bs. 20 (valor de ley del certificado).",
            "que_necesito": ["Cedula de identidad vigente", "Formulario de solicitud", "Pago de la tasa correspondiente"],
            "como": ["Reune tu cedula de identidad", "Llena el formulario de solicitud", "Cancela el valor del certificado", "Te lo entregan impreso y firmado"],
            "cuanto_tarda": "Inmediato o hasta 1 dia habil segun el sistema.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "Se pide para empleo, estudios y tramites en el exterior.",
            "c": "Bs. 20", "t": "1 dia", "dep": "Policia (FELCC)",
            "u": "",
        },
        "qu": {
            "n": "Conducta Certificado (Antecedente)",
            "icon": "\u2705",
            "d": "Boliviapi mana penaltapas ni policial yachaycachay kasqaykita riqsichiq documento.",
            "donde": "Policia (FELCC) oficinaspi.",
            "cuanto": "Bs. 20 (certificadoq chanin).",
            "que_necesito": ["Cedula vigente", "Solicitud formulario", "Chantinta pagay"],
            "como": ["Cedulaykita apamuy", "Formulariota qillqay", "Certificadoq chantinta pagay", "Firmado nitaq impreso chaskikuy"],
            "cuanto_tarda": "Chay p'unchay utaq 1 p'unchay llamkaq.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Llamkay, yachay nitaq huk paisespi tramitospaq mañakun.",
            "c": "Bs. 20", "t": "1 p'unchay", "dep": "Policia (FELCC)",
            "u": "",
        },
    },
    "licencia_conducir": {
        "es": {
            "n": "Licencia de Conducir",
            "icon": "\U0001F697",
            "d": "Obtencion o renovacion de la licencia de conducir vehiculos livianos, pesados o motocicletas (SEGIP).",
            "donde": "Centro de Licencias SEGIP en Sacaba o Cochabamba.",
            "cuanto": "Varía segun la categoria (liviana, pesada, moto) y el curso.",
            "que_necesito": ["Cedula de identidad vigente", "Certificado de conducta (antecedentes)", "Certificado medico de salud", "Comprobante de pago", "Fotografias (para el expediente)"],
            "como": ["Reune tus documentos (CI, antecedentes, certificado medico)", "Cancela el valor de la categoria", "Aprueba el examen (teorico y practico)", "Entregan tu licencia"],
            "cuanto_tarda": "De 1 a 2 semanas segun la agenda del SEGIP.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "Renueva tu licencia antes del vencimiento para evitar sanciones.",
            "c": "Segun categoria", "t": "1-2 semanas", "dep": "SEGIP - Transito",
            "u": "",
        },
        "qu": {
            "n": "Manejo Licencia",
            "icon": "\U0001F697",
            "d": "Liviano, pesado utaq moto vehiculokunata manenaypaq licencia hurqoy utaq renovay (SEGIP).",
            "donde": "SEGIP Centro de Licencias Sacabapi utaq Cochabambapi.",
            "cuanto": "Categoriaqmanhina (liviana, pesada, moto) utaq cursomanhina.",
            "que_necesito": ["Cedula vigente", "Conducta certificado", "Salud medico certificado", "Pago comprobante", "Fotokuna (expedientepaq)"],
            "como": ["Documentosta apamuy (CI, antecedente, medico)", "Categoriaq chantinta pagay", "Examen aprobay (teorico y practico)", "Licenciaykita qun"],
            "cuanto_tarda": "1-2 semana SEGIP agendaqmanhina.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Licenciaykita vencenantataq renovay, sancion ama kananpaq.",
            "c": "Segun categoria", "t": "1-2 semana", "dep": "SEGIP - Transito",
            "u": "",
        },
    },
    "registro_civil": {
        "es": {
            "n": "Registro Civil (Certificado de Nacimiento)",
            "icon": "\U0001F582\uFE0F",
            "d": "Certificado de nacimiento, matrimonio o defuncion expedido por el Registro Civil de Sacaba.",
            "donde": "Oficina del Registro Civil - Municipalidad de Sacaba.",
            "cuanto": "Bs. 10 por certificado (el valor puede variar).",
            "que_necesito": ["Cedula de identidad del solicitante", "Datos del inscrito (nombres, fecha y lugar)", "En caso de aclaracion, partida original"],
            "como": ["Acude al Registro Civil de Sacaba", "Solicita el certificado con los datos", "Cancela el valor", "Retira tu certificado"],
            "cuanto_tarda": "Inmediato si los datos existen en el registro.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "Lleva los datos exactos del inscrito para una busqueda rapida.",
            "c": "Bs. 10", "t": "Inmediato", "dep": "Registro Civil",
            "u": "",
        },
        "qu": {
            "n": "Registro Civil (Nacimiento Certificado)",
            "icon": "\U0001F582\uFE0F",
            "d": "Nacimiento, matrimonio utaq defuncion certificado, Sacaba Registro Civil qusqa.",
            "donde": "Registro Civil Oficina - Municipalidad de Sacaba.",
            "cuanto": "Bs. 10 certificado (chaninmi tiyan).",
            "que_necesito": ["Solicitanteq cedula", "Inscritop datos (suti, p'unchay, lugar)", "Aclaracion kaspaqa, partida original"],
            "como": ["Sacaba Registro Civilman riy", "Datoswan certificadota mañay", "Chaninta pagay", "Certificadoykita chaskiy"],
            "cuanto_tarda": "Datos registropi kaptinqa, chay p'unchaylla.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Inscritop exacto datosta apamuy, usqay maskanaykipaq.",
            "c": "Bs. 10", "t": "Chaylla", "dep": "Registro Civil",
            "u": "",
        },
    },
    "residencia": {
        "es": {
            "n": "Constancia de Residencia",
            "icon": "\U0001F3E0",
            "d": "Documento que certifica tu residencia en el municipio de Sacaba.",
            "donde": "Direccion de Registro Social, en la municipalidad.",
            "cuanto": "Bs. 15.",
            "que_necesito": ["Fotocopia de cedula de identidad", "Fotocopia de libreta de servicio militar", "Recibo de pago de servicios basicos", "Declaracion jurada de residencia", "Dos fotos tamano carnet"],
            "como": ["Recoge el formulario en Ventanilla Unica", "Llena el formulario con tus datos", "Presenta los requisitos", "Realiza el pago en caja", "Retira la constancia en 2-3 dias"],
            "cuanto_tarda": "2 a 3 dias habiles.",
            "horario": "Lunes a viernes, 8:00 a 12:00 / 14:30 a 18:30.",
            "consejo": "Lleva todos los requisitos para un solo viaje.",
            "c": "Bs. 15", "t": "2-3 dias", "dep": "Registro Social",
            "u": "",
        },
        "qu": {
            "n": "Tiyay Constancia (Residencia)",
            "icon": "\U0001F3E0",
            "d": "Huk runaq Sakaba munisipyupi tiyasqanta riqsichiq documento.",
            "donde": "Registro Social oficinaqpi, municipalidadpi.",
            "cuanto": "Bs. 15.",
            "que_necesito": ["Cedula fotocopia", "Libreta militar fotocopia", "Servicios recibo (yaku, lliphi, telefono)", "Declaracion jurada", "Iskay carnet fotokuna"],
            "como": ["Formulariota apakamuy (Ventanilla Unica)", "Formulariota qillqay qan datosniykita", "Requisitokunata rikuchiy", "Cajapi pagay", "Constanciata chaskikuy (2-3 p'unchay)"],
            "cuanto_tarda": "2-3 p'unchay llamkaq.",
            "horario": "Lun-Vie, 8:00-12:00 / 14:30-18:30.",
            "consejo": "Tukuy requisitokunata apakuy, huk kutilla kananpaq.",
            "c": "Bs. 15", "t": "2-3 p'unchay", "dep": "Registro Social",
            "u": "",
        },
    },
    "funcionamiento": {
        "es": {
            "n": "Licencia de Funcionamiento",
            "icon": "\U0001F3E2",
            "d": "Permiso municipal (patente) para operar un negocio o actividad economica en Sacaba. Se tramita en la Direccion de Ingresos y Servicios Municipales.",
            "donde": "Direccion de Ingresos y Servicios Municipales - Municipalidad de Sacaba (caja central o subalcaldias).",
            "cuanto": "Bs. 60 (licencia nueva), Bs. 40 (renovacion) - valores municipales.",
            "cuanto_detail": "Los valores se compran en Caja Central o subalcaldias. Segun el rubro puede pedirse licencia ambiental o contrato GERES.",
            "que_necesito": ["Formulario de solicitud con caracter de Declaracion Jurada (DJ)", "Fotocopia de carnet de identidad del propietario", "Fotocopia de contrato de alquiler y/o anticretico (si corresponde)", "Licencia ambiental o certificacion (si el rubro lo exige)", "Contrato o certificacion de GERES (segun rubro)", "Valores municipales: Bs. 60 nuevo o Bs. 40 renovacion"],
            "como": ["Acude a la caja central o subalcaldia y compra los valores municipales (Bs. 60 o Bs. 40)", "Llena el formulario de solicitud (Declaracion Jurada)", "Adjunta fotocopia de CI y contrato de alquiler del local", "Presenta licencia ambiental y contrato GERES si tu rubro lo exige", "Cancela en caja y recoge tu licencia"],
            "cuanto_tarda": "Con los requisitos completos se gestiona en la municipalidad.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "Verifica los requisitos de tu rubro antes de ir. Los rubros van desde industrias, comercio y restaurantes, hasta talleres, servicios de salud y educacion.",
            "c": "Bs. 60 (nuevo) / Bs. 40 (renov.)", "t": "Gestion directa", "dep": "Ingresos y Servicios",
            "u": "",
        },
        "qu": {
            "n": "Licencia Funcionamiento",
            "icon": "\U0001F3E2",
            "d": "Munisipyuq suyúnpi negociota ruwanaykipaq permiso.",
            "donde": "Ingresos y Servicios oficinaqpi, Sacaba Municipalidad.",
            "cuanto": "Bs. 60 (mushuq licencia), Bs. 40 (renovacion) - valores municipales.",
            "cuanto_detail": "Valores Caja Centralpi utaq subalcaldiaspi rantikun. Rubro mañaptinqa licencia ambiental utaq contrato GERES mañakun.",
            "que_necesito": ["Mañakuy qillqa (Declaracion Jurada)", "Propietarioq cedula fotocopia", "Contrato de alquiler utaq anticretico fotocopia", "Licencia ambiental utaq certificacion (rubro mañaptin)", "GERES contrato utaq certificacion (rurun jina)", "Valores: Bs. 60 nuevo utaq Bs. 40 renovacion"],
            "como": ["Caja centralman utaq subalcaldiaman riy, valores rantikuy (Bs. 60 utaq Bs. 40)", "Mañakuy qillqata qillqay (Declaracion Jurada)", "Cedula nitaq localq contrato fotocopiata churay", "Licencia ambiental nitaq GERES contrato rikuchiy (rubro mañaptin)", "Cajapi pagay, licenciata chaskikuy"],
            "cuanto_tarda": "Requisitos tukukuptiykiqa municipalidadpi rurasqa kan.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Rillasqayki, rubroykiq requisitunkunata qhaway. Industrias, comercio, restaurantes, talleres, salud utaq educacion — tukuy ruwaykuna.",
            "c": "Bs. 60 (nuevo) / Bs. 40 (renov.)", "t": "Gestion directa", "dep": "Ingresos y Servicios",
            "u": "",
        },
    },
    "construccion": {
        "es": {
            "n": "Permiso de Construccion (Plano de Vivienda)",
            "icon": "\U0001F3D7\uFE0F",
            "d": "Aprobacion de plano para construir o legalizar una vivienda u obra nueva en Sacaba (tramite de Urbanismo).",
            "donde": "Direccion de Urbanismo - Municipalidad de Sacaba (Gestion Urbana y Territorial).",
            "cuanto": "Costo por valores municipales (folder administrativo y timbres).",
            "que_necesito": ["Memorial dirigido al Alcalde o Subalcalde", "Titulo de propiedad y folio real (no mayor a 1 anio)", "Comprobante de pago de impuestos IPBI de la ultima gestion", "Planos del proyecto elaborados por arquitecto (3 ejemplares + digital)", "Certificado catastral actualizado", "Fotocopia de CI vigente", "Compra de valores municipales"],
            "como": ["Prepara los planos con un arquitecto colegiado", "Reune titulo, folio real y pago de IPBI", "Presenta memorial y requisitos en Urbanismo", "Adjunta certificado catastral y plano de lote", "Cancela valores municipales y espera la aprobacion"],
            "cuanto_tarda": "Se revisa por la Direccion de Urbanismo; el plazo depende del proyecto.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "Para legalizar una obra ya construida se necesita ademas declaracion jurada, carta notariada y fotografias de la fachada e interiores.",
            "c": "Valores municipales", "t": "Segun proyecto", "dep": "Urbanismo",
            "u": "",
        },
        "qu": {
            "n": "Construccion Permiso",
            "icon": "\U0001F3D7\uFE0F",
            "d": "Wasi ruwana utaq allchasqanapaq permiso, Urbanismoqpi rurasqa.",
            "donde": "Urbanismo Oficina - Sacaba Municipalidad (Gestion Urbana y Territorial).",
            "cuanto": "Valores municipales (folder administrativo utaq timbres).",
            "que_necesito": ["Memorial (Alcalde utaq Subalcalde llamkan)", "Titulo de propiedad nitaq folio real (mana huk watamanta aswan)", "IPBI impuesto pagasqayki comprobante (qhipa gestion)", "Arquitectop planos (3 ejemplares + digital)", "Certificado catastral musuq", "Cedula fotocopia", "Valores municipales rantikuy"],
            "como": ["Arquitectowan planosta pukllachiy", "Titulo, folio real nitaq IPBI paguytantachiy", "Urbanismoqpi memorial nitaq requisitosta rikuchiy", "Certificado catastral nitaq lotep plano churay", "Valores municipales pagay, aprobacion suyay"],
            "cuanto_tarda": "Urbanismoq qhawariyninman jina; proyectoq plazunman.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Rurasqa wasita legalizayta munaqtinqa: declaracion jurada, carta notariada nitaq fachada fotokuna apamuy.",
            "c": "Valores municipales", "t": "Segun proyecto", "dep": "Urbanismo",
            "u": "",
        },
    },
    "propiedad": {
        "es": {
            "n": "Registro de Propiedad",
            "icon": "\U0001F4DC",
            "d": "Inscripcion de bienes inmuebles para legalizar tu propiedad.",
            "donde": "Direccion de Derechos Reales.",
            "cuanto": "Bs. 50 - 200 (segun valor catastral).",
            "que_necesito": ["Titulo de propiedad original", "Plano de ubicacion", "Cedula de identidad", "Pago de tasa"],
            "como": ["Reune los documentos", "Presenta en Derechos Reales", "Realiza el pago", "Espera la inscripcion", "Retira tu certificado"],
            "cuanto_tarda": "15 a 30 dias habiles.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "Verifica que no haya deudas pendientes.",
            "c": "Bs. 50-200", "t": "15-30 dias", "dep": "Derechos Reales",
            "u": "",
        },
        "qu": {
            "n": "Propiedad Registro",
            "icon": "\U0001F4DC",
            "d": "Propiedadyki munisipyuq registronpi qillchachikuy.",
            "donde": "Derechos Reales Oficinaqpi.",
            "cuanto": "Bs. 50 - 200 (valor catastralman jina).",
            "que_necesito": ["Titulo de propiedad original", "Ubicacion plano", "Cedula", "Tasa pagay"],
            "como": ["Documentosta tantachiy", "Derechos Realesqpi rikuchiy", "Pagay", "Inscripcion suyay", "Certificadota chaskikuy"],
            "cuanto_tarda": "15-30 p'unchay llamkaq.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Manaraq mana deudas kashasqanta qhaway.",
            "c": "Bs. 50-200", "t": "15-30 p'unchay", "dep": "Derechos Reales",
            "u": "",
        },
    },
    "solteria": {
        "es": {
            "n": "Constancia de Solteria",
            "icon": "\U0001F48D",
            "d": "Certificado que acredita tu estado civil soltero.",
            "donde": "Direccion de Registro Civil.",
            "cuanto": "Bs. 10.",
            "que_necesito": ["Cedula de identidad", "Dos testigos con cedula", "Pago de tasa"],
            "como": ["Acude a Registro Civil con tus testigos", "Presenta la cedula", "Firma la declaracion", "Paga la tasa", "Recibe tu constancia"],
            "cuanto_tarda": "Inmediato.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "Lleva testigos que te conozcan personalmente.",
            "c": "Bs. 10", "t": "Inmediato", "dep": "Registro Civil",
            "u": "",
        },
        "qu": {
            "n": "Solteria Constancia",
            "icon": "\U0001F48D",
            "d": "Mana casarakusqa kasqaykita riqsichiq documento.",
            "donde": "Registro Civil Oficinaqpi.",
            "cuanto": "Bs. 10.",
            "que_necesito": ["Cedula", "Iskay willaqkuna cedulawan", "Tasa pagay"],
            "como": ["Registro Civilman riy willaqkunawan", "Cedulata rikuchiy", "Declaracionta firmay", "Tasata pagay", "Constanciata chaskikuy"],
            "cuanto_tarda": "Chay p'unchaylla.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Kikiykita riqsikuq willaqkunata apamuy.",
            "c": "Bs. 10", "t": "Chaylla", "dep": "Registro Civil",
            "u": "",
        },
    },
    "prediales": {
        "es": {
            "n": "Impuestos Prediales",
            "icon": "\U0001F4B0",
            "d": "Impuesto anual que grava la propiedad de bienes inmuebles.",
            "donde": "Direccion de Rentas Internas de la municipalidad.",
            "cuanto": "0.5% - 1% del valor catastral del inmueble.",
            "que_necesito": ["Cedula de identidad", "Titulo de propiedad", "Certificado catastral actualizado"],
            "como": ["Consulta el monto en Rentas Internas", "Realiza el pago en caja municipal", "Guarda tu comprobante", "Presenta el comprobante si es necesario"],
            "cuanto_tarda": "Inmediato al pagar.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "Paga antes de la fecha de vencimiento para evitar recargos.",
            "c": "0.5-1%", "t": "Inmediato", "dep": "Rentas Internas",
            "u": "",
        },
        "qu": {
            "n": "Predial Impuestokuna",
            "icon": "\U0001F4B0",
            "d": "Sapa wata propiedadyuq impuestota pagay.",
            "donde": "Rentas Internas Oficinaqpi, municipalidadpi.",
            "cuanto": "0.5% - 1% valor catastralmanta.",
            "que_necesito": ["Cedula", "Titulo de propiedad", "Certificado catastral musuq"],
            "como": ["Rentas Internaspi monto qhaway", "Caja municipalpi pagay", "Comprobanteta waqaychay", "Comprobante rikuchiy (mañaptinqa)"],
            "cuanto_tarda": "Pagayta ruwaspa chay p'unchaylla.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Vencimiento fecha riman, mana recargo kananpaq.",
            "c": "0.5-1%", "t": "Chaylla", "dep": "Rentas Internas",
            "u": "",
        },
    },
    "agua": {
        "es": {
            "n": "Servicio de Agua Potable",
            "icon": "\U0001F4A7",
            "d": "Tramite para conectar o regularizar el servicio de agua potable.",
            "donde": "Empresa de Agua Potable de Sacaba.",
            "cuanto": "Bs. 50 - 200 (segun tipo de conexion).",
            "que_necesito": ["Solicitud formal", "Cedula de identidad", "Constancia de propiedad o recibo de alquiler", "Pago de conexion"],
            "como": ["Presenta tu solicitud", "Paga la conexion", "Espera la inspeccion", "Recibe tu servicio"],
            "cuanto_tarda": "5 a 10 dias habiles.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "Verifica tu deuda antes de solicitar.",
            "c": "Bs. 50-200", "t": "5-10 dias", "dep": "Empresa de Agua",
            "u": "",
        },
        "qu": {
            "n": "Yaku (Agua Potable)",
            "icon": "\U0001F4A7",
            "d": "Munisipyuq yakunmanta servicio.",
            "donde": "Empresa de Agua Potable Sacabaqpi.",
            "cuanto": "Bs. 50 - 200 (conexionjina).",
            "que_necesito": ["Mañakuy qillqa formal", "Cedula", "Tiyay constancia utaq alquiler recibo", "Conexion pagay"],
            "como": ["Mañakuy qillqata rikuchiy", "Conexion pagay", "Inspeccion suyay", "Serviciota chaskikuy"],
            "cuanto_tarda": "5-10 p'unchay llamkaq.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Mañakuy rawayki, deudaykita qhaway.",
            "c": "Bs. 50-200", "t": "5-10 p'unchay", "dep": "Empresa de Agua",
            "u": "",
        },
    },
    "eventos": {
        "es": {
            "n": "Permiso para Eventos",
            "icon": "\U0001F389",
            "d": "Autorizacion para realizar eventos publicos o privados.",
            "donde": "Direccion de Seguridad Ciudadana.",
            "cuanto": "Bs. 30 - 300 (segun tipo de evento).",
            "que_necesito": ["Solicitud con detalles del evento", "Cedula del organizador", "Poliza de responsabilidad civil", "Pago de tasa"],
            "como": ["Presenta la solicitud", "Adjunta los documentos", "Paga la tasa", "Obten el permiso", "Cumple las condiciones"],
            "cuanto_tarda": "3 a 5 dias habiles.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "Solicita con anticipacion para evitar problemas.",
            "c": "Bs. 30-300", "t": "3-5 dias", "dep": "Seguridad Ciudadana",
            "u": "",
        },
        "qu": {
            "n": "Eventopaq Permiso",
            "icon": "\U0001F389",
            "d": "Eventokunata ruwanaykipaq munisipyuq permiso.",
            "donde": "Seguridad Ciudadana Oficinaqpi.",
            "cuanto": "Bs. 30 - 300 (eventojina).",
            "que_necesito": ["Mañakuy qillqa (eventop detallenkuna)", "Organizadorq cedula", "Poliza responsabilidad civil", "Tasa pagay"],
            "como": ["Mañakuy qillqata rikuchiy", "Documentosta apuy", "Tasata pagay", "Permisota chaskikuy", "Kamachikunata huntay"],
            "cuanto_tarda": "3-5 p'unchay llamkaq.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Unayta mañakuy, problemas kananpaq.",
            "c": "Bs. 30-300", "t": "3-5 p'unchay", "dep": "Seguridad Ciudadana",
            "u": "",
        },
    },
    "vehiculos": {
        "es": {
            "n": "Registro de Vehiculos",
            "icon": "\U0001F697",
            "d": "Inscripcion de vehiculos motorizados.",
            "donde": "Direccion de Transito y Transporte.",
            "cuanto": "Bs. 30 - 150.",
            "que_necesito": ["Cedula", "Libreta de transito", "Revision vehicular", "SOAT"],
            "como": ["Solicita en Transito", "Presenta documentos", "Revision tecnica", "Paga", "Obten placa y libreta"],
            "cuanto_tarda": "2 a 5 dias habiles.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "Ten todos los documentos al dia.",
            "c": "Bs. 30-150", "t": "2-5 dias", "dep": "Transito",
            "u": "",
        },
        "qu": {
            "n": "Vehiculo Registro",
            "icon": "\U0001F697",
            "d": "Vehiculokunata munisipyuqpi registray.",
            "donde": "Transito y Transporte Oficinaqpi.",
            "cuanto": "Bs. 30 - 150.",
            "que_necesito": ["Cedula", "Transito libreta", "Revision vehicular", "SOAT"],
            "como": ["Transitoqpi mañakuy", "Documentosta rikuchiy", "Revision tecnica", "Pagay", "Placa nitaq libreta chaskikuy"],
            "cuanto_tarda": "2-5 p'unchay llamkaq.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Tukuy documentosta p'unchaysapa allinchay.",
            "c": "Bs. 30-150", "t": "2-5 p'unchay", "dep": "Transito",
            "u": "",
        },
    },
    "nodeuda": {
        "es": {
            "n": "Constancia de No Deuda",
            "icon": "\u2705",
            "d": "Certifica que no tienes deudas con el municipio.",
            "donde": "Direccion de Rentas Internas.",
            "cuanto": "Bs. 10.",
            "que_necesito": ["Cedula de identidad", "Certificado de propiedad"],
            "como": ["Acude a Rentas Internas", "Presenta los documentos", "Verifican tus deudas", "Paga si tienes deudas", "Emite la constancia"],
            "cuanto_tarda": "1 a 2 dias habiles.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "Verifica tus deudas antes de solicitar.",
            "c": "Bs. 10", "t": "1-2 dias", "dep": "Rentas",
            "u": "",
        },
        "qu": {
            "n": "Mana Deuda Constancia",
            "icon": "\u2705",
            "d": "Munisipyuwan mana deudayuq kasqaykita riqsichiq.",
            "donde": "Rentas Internas Oficinaqpi.",
            "cuanto": "Bs. 10.",
            "que_necesito": ["Cedula", "Certificado de propiedad"],
            "como": ["Rentas Internasman riy", "Documentosta rikuchiy", "Deudaykita qhaway", "Deudayuq kaspaqqa pagay", "Constanciata qillqay"],
            "cuanto_tarda": "1-2 p'unchay llamkaq.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Mañakuy rawayki, deudaykita qhaway.",
            "c": "Bs. 10", "t": "1-2 p'unchay", "dep": "Rentas",
            "u": "",
        },
    },
    "catastro_empadronamiento": {
        "es": {
            "n": "Empadronamiento Predial",
            "icon": "\U0001F3E0",
            "d": "Registro de tu predio (terreno/lote) en el sistema catastral de Sacaba, con titulo de propiedad o en calidad de poseedor.",
            "donde": "Unidad de Catastro - Municipalidad de Sacaba.",
            "cuanto": "Valores municipales (folder administrativo y timbres de Bs. 10).",
            "que_necesito": ["Memorial dirigido al Alcalde o Subalcalde firmado por el propietario", "Titulo de propiedad registrado en Derechos Reales y folio real (no mayor a 1 anio), fotocopia con timbre de Bs. 10", "Plano de lote georeferenciado por profesional colegiado (impreso y shapefile en CD)", "Formulario de Declaracion Jurada EMP-CAT-01", "Fotocopia de identidad o cedula de extranjeria", "Compra de valores (folder y timbres Bs. 10)"],
            "como": ["Prepara memorial, titulo, folio real y plano georeferenciado", "Llena el formulario EMP-CAT-01 con tu profesional", "Presenta todo en la Unidad de Catastro", "Cancela los valores municipales", "Se registra tu predio y queda listo"],
            "cuanto_tarda": "Se gestiona en la Unidad de Catastro (Decreto Municipal 014/2024).",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "Si eres poseedor (sin titulo), tambien puedes empadronar: lleva minuta de compra-venta, boletas de servicios y declaracion voluntaria notariada.",
            "c": "Valores municipales", "t": "Gestion directa", "dep": "Catastro",
            "u": "",
        },
        "qu": {
            "n": "Empadronamiento Predial",
            "icon": "\U0001F3E0",
            "d": "Predioykta munisipyuq katastroqpi qillqachiy (terreno/lote), titulo yuqpa utaq rikchariy uwanpi.",
            "donde": "Catastro Oficinaqpi, Municipalidad de Sacaba.",
            "cuanto": "Valores municipales (folder y timbres Bs. 10).",
            "que_necesito": ["Memorial Alcaldepaq alcaldewan firmasqa", "Titulo de propiedad y folio real (1 anio imanmana)", "Plano georeferenciado profesionalwan (impreso y CD)", "Formulario EMP-CAT-01", "Identidad fotocopia", "Valores municipales compra"],
            "como": ["Memorial nitaq planos preparay", "Formulariota qillqay", "Catastro oficinapi presentay", "Valores municipales pagay", "Predioykta qillqachinkuy"],
            "cuanto_tarda": "Catastro oficinapi gestionay.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Rikchariy uwanpis taqyaykupas empadronayta atinkiy: minuta, servicios recibokuna nitaq declaracion notariada.",
            "c": "Valores municipales", "t": "Gestion directa", "dep": "Catastro",
            "u": "",
        },
    },
    "catastro_certificado": {
        "es": {
            "n": "Certificado Catastral",
            "icon": "\U0001F4C4",
            "d": "Documento que certifica los datos del predio (ubicacion, superficie, codigo catastral) ante la municipalidad.",
            "donde": "Unidad de Catastro - Municipalidad de Sacaba.",
            "cuanto": "Valores municipales (folder administrativo y timbres).",
            "que_necesito": ["Memorial dirigido al Alcalde o Subalcalde", "Titulo de propiedad y folio real actualizado (no mayor a 1 anio)", "Reporte sin deudas con timbre de Bs. 5", "Fotocopia del plano de lote aprobado y RTA", "Fotocopia de identidad del propietario", "Compra de valores municipales"],
            "como": ["Reune titulo, folio real y reporte sin deudas", "Adjunta plano aprobado y resolucion tecnica", "Presenta el memorial en Catastro", "Cancela valores municipales", "Retira tu certificado catastral"],
            "cuanto_tarda": "Se gestiona en la Unidad de Catastro.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "Tambien puedes pedir reimpresion o actualizacion del certificado catastral.",
            "c": "Valores municipales", "t": "Gestion directa", "dep": "Catastro",
            "u": "",
        },
        "qu": {
            "n": "Certificado Catastral",
            "icon": "\U0001F4C4",
            "d": "Predioykta munisipyuqpi riqsichiq documento (maypi, superficie, codigo catastral).",
            "donde": "Catastro Oficinaqpi, Municipalidad de Sacaba.",
            "cuanto": "Valores municipales (folder y timbres).",
            "que_necesito": ["Memorial Alcaldepaq", "Titulo y folio real actualizado (1 anio imanmana)", "Reporte mana deuda yuq timbre Bs. 5", "Plano de lote aprobado y RTA fotocopia", "Identidad propietariop fotocopia", "Valores municipales compra"],
            "como": ["Titulo, folio real nitaq reporte apamuy", "Plano aprobado nitaq resolucion adjuntay", "Catastro oficinapi memorial presentay", "Valores municipales pagay", "Certificado catastralta chaskikuy"],
            "cuanto_tarda": "Catastro oficinapi gestionay.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Certificado catastraltapacha qawqkupas impersion utaq actualizacionqa chaynallan.",
            "c": "Valores municipales", "t": "Gestion directa", "dep": "Catastro",
            "u": "",
        },
    },
    "catastro_avaluo": {
        "es": {
            "n": "Avaluo Catastral",
            "icon": "\U0001F4B0",
            "d": "Calculo del valor oficial de tu inmueble para impuestos, transferencias o regularizaciones.",
            "donde": "Unidad de Catastro - Municipalidad de Sacaba.",
            "cuanto": "Valores municipales (folder administrativo).",
            "que_necesito": ["Memorial dirigido al Alcalde solicitando el avaluo", "Titulo de propiedad y folio real actualizado", "Fotocopia del ultimo impuesto o IPBI", "Plano de lote aprobado o georeferenciado", "Fotocopia de identidad", "Compra de valores municipales"],
            "como": ["Presenta el memorial y documentos en Catastro", "Adjunta titulo, folio real y ultimo impuesto", "Entrega el plano del lote", "Cancela los valores", "Recibe el informe de avaluo"],
            "cuanto_tarda": "Se gestiona en la Unidad de Catastro.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "El avaluo es la base para calcular impuestos prediales y tasas.",
            "c": "Valores municipales", "t": "Gestion directa", "dep": "Catastro",
            "u": "",
        },
        "qu": {
            "n": "Avaluo Catastral",
            "icon": "\U0001F4B0",
            "d": "Wasikunap qullqi cachay (impuesto, transferencia utaq regularizacionpaq).",
            "donde": "Catastro Oficinaqpi, Municipalidad de Sacaba.",
            "cuanto": "Valores municipales (folder administrativo).",
            "que_necesito": ["Memorial Alcaldepaq avaluo mañay", "Titulo y folio real actualizado", "Ultimo impuesto o IPBI fotocopia", "Plano georeferenciado aprobado", "Identidad fotocopia", "Valores municipales compra"],
            "como": ["Memorial nitaq documentosta Catastroqpi presentay", "Titulo, folio real nitaq impuesto adjuntay", "Plano del terreno qawqay", "Valores pagay", "Avaluo informe chaskiy"],
            "cuanto_tarda": "Catastro oficinapi gestionay.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Avaluoqa impuesto predial y tasas cachayna pachaqta.",
            "c": "Valores municipales", "t": "Gestion directa", "dep": "Catastro",
            "u": "",
        },
    },
    "urbanismo_plano": {
        "es": {
            "n": "Aprobacion de Plano (Terreno/Lote)",
            "icon": "\U0001F3D7\uFE0F",
            "d": "Aprobacion, anexion, division o subdivision de plano de terreno o lote (regularizacion predial).",
            "donde": "Direccion de Urbanismo - Municipalidad de Sacaba.",
            "cuanto": "Valores municipales (folder administrativo y timbres).",
            "que_necesito": ["Memorial dirigido al Alcalde o Subalcalde", "Titulo de propiedad y folio real (no mayor a 1 anio)", "Comprobante de pago de impuestos IPBI de la ultima gestion", "Planos elaborados por arquitecto/ingeniero (5 ejemplares + shapefile)", "Fotocopia de identidad vigente", "Compra de valores municipales"],
            "como": ["Contrata un profesional para los planos (5 ejemplares)", "Reune titulo, folio real y recibo de IPBI", "Presenta memorial y expediente en Urbanismo", "Cancela los valores municipales", "Espera la revision y aprobacion"],
            "cuanto_tarda": "Revisado por la Direccion de Urbanismo.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "Incluye aqui: aprobacion de plano, anexion de terrenos, division y subdivision de lotes.",
            "c": "Valores municipales", "t": "Segun revision", "dep": "Urbanismo",
            "u": "",
        },
        "qu": {
            "n": "Plano Aprobacion (Terreno/Lote)",
            "icon": "\U0001F3D7\uFE0F",
            "d": "Terreno/lote planota aprobay, huñuy, rakiy utaq subdividiy (regularizacion predial).",
            "donde": "Urbanismo Direccionpi, Municipalidad de Sacaba.",
            "cuanto": "Valores municipales (folder y timbres).",
            "que_necesito": ["Memorial Alcaldepaq", "Titulo y folio real (1 anio imanmana)", "IPBI ultimo gestion pagasqa recibo", "Arquitecto/ingeniero planos (5 kopia + shapefile)", "Identidad vigente fotocopia", "Valores municipales compra"],
            "como": ["Profesionalta contratay planospaq (5 kopia)", "Titulo, folio real nitaq IPBI apamuy", "Memorial nitaq expediente Urbanismoqpi presentay", "Valores municipales pagay", "Revision nitaq aprobacion suyay"],
            "cuanto_tarda": "Urbanismo Direccionpi qhawarikun.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Kaypiga: plano aprobacion, terreno huñuy, division nitaq subdivision.",
            "c": "Valores municipales", "t": "Segun revision", "dep": "Urbanismo",
            "u": "",
        },
    },
    "urbanismo_ampliacion": {
        "es": {
            "n": "Ampliacion o Remodelacion de Construccion",
            "icon": "\U0001F3D8\uFE0F",
            "d": "Aprobacion municipal para ampliar o remodelar una construccion, casa o edificio.",
            "donde": "Direccion de Urbanismo - Municipalidad de Sacaba.",
            "cuanto": "Valores municipales (folder administrativo y timbres).",
            "que_necesito": ["Memorial dirigido al Alcalde o Subalcalde", "Titulo de propiedad y folio real actualizado", "Comprobante de IPBI de la ultima gestion", "Proyecto de ampliacion o remodelacion por arquitecto (3 ejemplares + CAD)", "Certificado catastral actualizado", "Plano de terreno aprobado", "Fotocopia de identidad", "Compra de valores"],
            "como": ["Prepara el proyecto con un arquitecto", "Reune titulo, IPBI y certificado catastral", "Presenta memorial y planos en Urbanismo", "Cancela valores municipales", "Se aprueba el plano de ampliacion/remodelacion"],
            "cuanto_tarda": "Revisado por Urbanismo (edificios de 4+ niveles piden mas requisitos).",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "Para edificios de 4 niveles o mas se suman memorias de calculo sanitario, electrico y estructural.",
            "c": "Valores municipales", "t": "Segun proyecto", "dep": "Urbanismo",
            "u": "",
        },
        "qu": {
            "n": "Construccion Ampliacion/Remodelacion",
            "icon": "\U0001F3D8\uFE0F",
            "d": "Wasita, casata utaq edificiota ampliyanapaq utaq remodekuyanapaq munisipyuq aprobacion.",
            "donde": "Urbanismo Direccionpi, Municipalidad de Sacaba.",
            "cuanto": "Valores municipales (folder y timbres).",
            "que_necesito": ["Memorial Alcaldepaq", "Titulo y folio real actualizado", "IPBI ultimo gestion recibo", "Arquitecto proyecto (3 kopia + CAD)", "Certificado catastral actualizado", "Terreno plano aprobado", "Identidad fotocopia", "Valores compra"],
            "como": ["Arquitecto huqwan proyecto preparay", "Titulo, IPBI nitaq certificado apamuy", "Memorial nitaq planos Urbanismoqpi presentay", "Valores municipales pagay", "Ampliacion/remodelacion planota apruebay"],
            "cuanto_tarda": "Urbanismoqpi qhawarikun (4+ pisokuna mas requisitokuna).",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "4+ pisokuna edificiopaqqa sanitaria, electrica nitaq estructural memoria sumakun.",
            "c": "Valores municipales", "t": "Segun proyecto", "dep": "Urbanismo",
            "u": "",
        },
    },
    "urbanismo_horizontal": {
        "es": {
            "n": "Propiedad Horizontal o Condominio",
            "icon": "\U0001F3E8",
            "d": "Adecuacion de un inmueble a propiedad horizontal o condominio (departamentos, parqueos, bauleras).",
            "donde": "Direccion de Urbanismo - Municipalidad de Sacaba.",
            "cuanto": "Valores municipales (folder administrativo y timbres).",
            "que_necesito": ["Memorial dirigido al Alcalde o Subalcalde", "Titulo de propiedad y folio real actualizado", "Comprobante de IPBI de la ultima gestion", "Plano de adecuacion a propiedad horizontal por arquitecto (3 ejemplares + CAD/Excel)", "Certificado catastral actualizado", "Plano de terreno aprobado", "Fotocopia de identidad", "Compra de valores"],
            "como": ["Contrata un arquitecto para el plano de adecuacion", "Reune titulo, IPBI y certificado catastral", "Presenta el expediente en Urbanismo", "Cancela valores municipales", "Recibe la resolucion de propiedad horizontal"],
            "cuanto_tarda": "Revisado por la Direccion de Urbanismo.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "Sirve para regularizar departamentos, locales, parqueos y bauleras de un edificio.",
            "c": "Valores municipales", "t": "Segun revision", "dep": "Urbanismo",
            "u": "",
        },
        "qu": {
            "n": "Propiedad Horizontal/Condominio",
            "icon": "\U0001F3E8",
            "d": "Wasikunata propiedad horizontal utaq condominio nisqaman adecuay (departamentos, parqueos, bauleras).",
            "donde": "Urbanismo Direccionpi, Municipalidad de Sacaba.",
            "cuanto": "Valores municipales (folder y timbres).",
            "que_necesito": ["Memorial Alcaldepaq", "Titulo y folio real actualizado", "IPBI ultimo gestion recibo", "Arquitecto adecuacion plano (3 kopia + CAD)", "Certificado catastral actualizado", "Terreno plano aprobado", "Identidad fotocopia", "Valores compra"],
            "como": ["Arquitectota contratay adecuacion planopaq", "Titulo, IPBI nitaq certificado apamuy", "Expediente Urbanismoqpi presentay", "Valores municipales pagay", "Propiedad horizontal resolucion chaskiy"],
            "cuanto_tarda": "Urbanismo Direccionpi qhawarikun.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Departamentos, locales, parqueos nitaq bauleras regularizanapaq.",
            "c": "Valores municipales", "t": "Segun revision", "dep": "Urbanismo",
            "u": "",
        },
    },
    "urbanismo_uso_suelo": {
        "es": {
            "n": "Certificacion de Uso de Suelo",
            "icon": "\U0001F3DB\uFE0F",
            "d": "Certificaciones de urbanismo: uso de suelo, fijacion de rasante, linea nivel, zona y distrito, verificacion de medidas.",
            "donde": "Direccion de Urbanismo - Municipalidad de Sacaba.",
            "cuanto": "Valores municipales (folder administrativo y timbres).",
            "que_necesito": ["Memorial o carta dirigida al Alcalde", "Titulo de propiedad y folio real actualizado", "Comprobante de IPBI (cuando corresponda)", "Plano de lote georeferenciado o plano aprobado", "Fotocopia de identidad", "Compra de valores"],
            "como": ["Indica el motivo de la solicitud en el memorial", "Adjunta titulo, folio real e IPBI", "Incluye el plano correspondiente", "Cancela valores municipales", "Recibe la certificacion solicitada"],
            "cuanto_tarda": "Gestion en la Direccion de Urbanismo.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "Tambien se emiten certificaciones por orden judicial y de limites de areas protegidas.",
            "c": "Valores municipales", "t": "Gestion directa", "dep": "Urbanismo",
            "u": "",
        },
        "qu": {
            "n": "Uso de Suelo Certificacion",
            "icon": "\U0001F3DB\uFE0F",
            "d": "Urbanismo certificaciones: uso de suelo, rasante, linea nivel, zona nitaq distrito, medidas verificacion.",
            "donde": "Urbanismo Direccionpi, Municipalidad de Sacaba.",
            "cuanto": "Valores municipales (folder y timbres).",
            "que_necesito": ["Memorial o carta Alcaldepaq", "Titulo y folio real actualizado", "IPBI recibo (kaptinqa)", "Plano georeferenciado o aprobado", "Identidad fotocopia", "Valores compra"],
            "como": ["Memorialpi imaraykuta qillqay", "Titulo, folio real nitaq IPBI adjuntay", "Plano chaymantapas chaskiy", "Valores municipales pagay", "Certificacion mañakusqaykita chaskiy"],
            "cuanto_tarda": "Urbanismo Direccionpi gestionay.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Orden judicial nitaq areas protegidas limitespi certificaciontapas qun.",
            "c": "Valores municipales", "t": "Gestion directa", "dep": "Urbanismo",
            "u": "",
        },
    },
    "urbanismo_verja": {
        "es": {
            "n": "Permiso de Trabajos Menores (Verja)",
            "icon": "\U0001F3F7\uFE0F",
            "d": "Permiso para construccion de verja, cerco o muro (trabajos menores de construccion).",
            "donde": "Direccion de Urbanismo - Municipalidad de Sacaba.",
            "cuanto": "Valores municipales (folder administrativo y timbres).",
            "que_necesito": ["Memorial dirigido al Alcalde o Subalcalde firmado por el propietario", "Titulo de propiedad y folio real actualizado", "Comprobante de IPBI", "Planos de verja por arquitecto (3 ejemplares)", "Plano de lote aprobado", "Fotocopia de identidad", "Compra de valores"],
            "como": ["Prepara los planos de la verja con un arquitecto", "Reune titulo, IPBI y plano de lote", "Presenta el memorial en Urbanismo", "Cancela valores municipales", "Aprueban el permiso de trabajos menores"],
            "cuanto_tarda": "Gestion en la Direccion de Urbanismo.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "Aplica para verjas, cercos y muros; es un tramite mas simple que el plano de vivienda.",
            "c": "Valores municipales", "t": "Gestion directa", "dep": "Urbanismo",
            "u": "",
        },
        "qu": {
            "n": "Trabajos Menores Permiso (Verja)",
            "icon": "\U0001F3F7\uFE0F",
            "d": "Verja, cerco utaq muro ruwanapaq permiso (huchuy construccion ruwakuna).",
            "donde": "Urbanismo Direccionpi, Municipalidad de Sacaba.",
            "cuanto": "Valores municipales (folder y timbres).",
            "que_necesito": ["Memorial Alcaldepaq firmasqa", "Titulo y folio real actualizado", "IPBI recibo", "Arquitecto verja planos (3 kopia)", "Terreno plano aprobado", "Identidad fotocopia", "Valores compra"],
            "como": ["Arquitecto huqwan verja planos preparay", "Titulo, IPBI nitaq plano apamuy", "Urbanismoqpi memorial presentay", "Valores municipales pagay", "Trabajos menores permiso apruebay"],
            "cuanto_tarda": "Urbanismo Direccionpi gestionay.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Verjas, cercos nitaq murospaq; vivienda planomanta mas simple.",
            "c": "Valores municipales", "t": "Gestion directa", "dep": "Urbanismo",
            "u": "",
        },
    },
    "vehiculo_inscripcion": {
        "es": {
            "n": "Inscripcion de Vehiculo",
            "icon": "\U0001F697",
            "d": "Registro RUAT de un vehiculo automotor nuevo (importacion directa o casa comercial) en Sacaba.",
            "donde": "Unidad de Vehiculos - Municipalidad de Sacaba.",
            "cuanto": "Folder administrativo y valores segun el tramite (Decreto Municipal 015/2024).",
            "que_necesito": ["Declaracion de Importacion/P-oliza o DUI y Formulario de Registro Vehicular (FRV)", "Fotocopia de CI vigente del propietario o representante legal", "Certificado de inscripcion a Impuestos Nacionales (persona juridica)", "Testimonio de poder (si compra una sociedad)", "Fotografia fondo rojo 3x3 cm (persona natural)", "Folder comun"],
            "como": ["Reune la documentacion de importacion o factura comercial", "Adjunta CI, fotografia y folder", "Presenta en la Unidad de Vehiculos", "Cancela los valores", "Se inscribe tu vehiculo en RUAT"],
            "cuanto_tarda": "Gestion en la Unidad de Vehiculos.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "El decreto municipal 015/2024 regula todos los tramites de vehiculos en Sacaba.",
            "c": "Segun tramite", "t": "Gestion directa", "dep": "Vehiculos",
            "u": "",
        },
        "qu": {
            "n": "Vehiculo Inscripcion",
            "icon": "\U0001F697",
            "d": "Mushuq vehiculo automator RUAT qillchachiy (importacion directa utaq casa comercial) Sacabapi.",
            "donde": "Vehiculos Unidadpi, Municipalidad de Sacaba.",
            "cuanto": "Folder administrativo nitaq valores (Decreto Municipal 015/2024).",
            "que_necesito": ["Importacion/P-oliza utaq DUI nitaq FRV formulario", "CI fotocopia (propietario)", "Impuestos Nacionales inscripcion (juridico)", "Poder testimonio (sociedad nisqa)", "Fondo rojo foto 3x3 cm (natural)", "Folder comun"],
            "como": ["Documentacion apamuy", "CI, foto nitaq folder adjuntay", "Vehiculos Unidadqpi presentay", "Valores pagay", "RUATqpi vehiculoykata qillchay"],
            "cuanto_tarda": "Vehiculos Unidadpi gestionay.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Decreto municipal 015/2024 tukuy vehiculo tramitekunata kamachin Sacabapi.",
            "c": "Segun tramite", "t": "Gestion directa", "dep": "Vehiculos",
            "u": "",
        },
    },
    "vehiculo_transferencia": {
        "es": {
            "n": "Transferencia de Vehiculo",
            "icon": "\U0001F504",
            "d": "Cambio de propietario (traspaso) de un vehiculo automotor registrado en el RUAT.",
            "donde": "Unidad de Vehiculos - Municipalidad de Sacaba.",
            "cuanto": "2 timbres municipales de Bs. 10 y folder administrativo.",
            "que_necesito": ["Minuta de compra-venta (original y 2 ejemplares)", "CRPVA original y fotocopia (RUAT 03)", "Fotocopia de CI del comprador y vendedor", "Fotografia fondo rojo 3x3 cm (persona natural)", "2 timbres de Bs. 10", "Folder administrativo", "El vehiculo sin deudas tributarias"],
            "como": ["Firma la minuta de compra-venta", "Reune CRPVA, CI y fotografia", "Cancela los timbres municipales", "Presenta el expediente en la Unidad de Vehiculos", "Se registra el cambio de propietario"],
            "cuanto_tarda": "Gestion en la Unidad de Vehiculos.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "El vehiculo no debe tener deudas: impuesto, gravamenes, reporte de robado ni bloqueos.",
            "c": "2 timbres Bs. 10", "t": "Gestion directa", "dep": "Vehiculos",
            "u": "",
        },
        "qu": {
            "n": "Vehiculo Transferencia",
            "icon": "\U0001F504",
            "d": "Vehiculoq propietario cambiachiy (traspaso) RUATqpi registrasqa.",
            "donde": "Vehiculos Unidadpi, Municipalidad de Sacaba.",
            "cuanto": "2 timbres municipales Bs. 10 nitaq folder administrativo.",
            "que_necesito": ["Minuta compra-venta (original, 2 kopia)", "CRPVA original nitaq fotocopia (RUAT 03)", "CI fotocopia (rantiq nitaq rantiyuq)", "Fondo rojo foto 3x3 cm (natural)", "2 timbres Bs. 10", "Folder administrativo", "Vehiculo mana deuda"],
            "como": ["Minuta compra-ventata firmay", "CRPVA, CI nitaq foto apamuy", "Timbres municipales pagay", "Expediente Vehiculos Unidadqpi presentay", "Propietario cambio registray"],
            "cuanto_tarda": "Vehiculos Unidadpi gestionay.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Vehiculo mana deuda kanan tiyan: impuesto, gravamen, robado nitaq bloqueo.",
            "c": "2 timbres Bs. 10", "t": "Gestion directa", "dep": "Vehiculos",
            "u": "",
        },
    },
    "vehiculo_radicatoria": {
        "es": {
            "n": "Cambio de Radicatoria",
            "icon": "\U0001F698",
            "d": "Traslado del registro de un vehiculo desde otro departamento o provincia hacia Sacaba.",
            "donde": "Unidad de Vehiculos - Municipalidad de Sacaba.",
            "cuanto": "Timbre municipal de Bs. 40 y folder administrativo.",
            "que_necesito": ["Minuta de compra-venta si hubo transferencia (original, 2 ejemplares)", "CRPVA (RUAT 03) original y fotocopia", "Fotocopia de CI vigente del propietario", "Certificado de inscripcion a Impuestos Nacionales (si es juridico)", "Fotografia fondo rojo 3x3 cm", "Timbre de Bs. 40", "Folder administrativo"],
            "como": ["Reune CRPVA y documentos de identidad", "Adjunta minuta si hubo transferencia", "Cancela el timbre de Bs. 40", "Presenta en la Unidad de Vehiculos", "Queda radicado en Sacaba"],
            "cuanto_tarda": "Gestion en la Unidad de Vehiculos.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "El vehiculo no debe tener deudas ni reporte de robado para el cambio de radicatoria.",
            "c": "Timbre Bs. 40", "t": "Gestion directa", "dep": "Vehiculos",
            "u": "",
        },
        "qu": {
            "n": "Radicatoria Cambio",
            "icon": "\U0001F698",
            "d": "Vehiculoq registroyta huk departamento/provinciamanta Sacabaman apay.",
            "donde": "Vehiculos Unidadpi, Municipalidad de Sacaba.",
            "cuanto": "Timbre municipal Bs. 40 nitaq folder administrativo.",
            "que_necesito": ["Minuta compra-venta transferencia kaptinqa (original, 2 kopia)", "CRPVA (RUAT 03) original nitaq fotocopia", "CI vigente fotocopia", "Impuestos Nacionales inscripcion (juridico)", "Fondo rojo foto 3x3 cm", "Timbre Bs. 40", "Folder administrativo"],
            "como": ["CRPVA nitaq documentosta apamuy", "Minuta adjuntay (transferencia kaptinqa)", "Timbre Bs. 40 pagay", "Vehiculos Unidadqpi presentay", "Sacabapi radicasqa kan"],
            "cuanto_tarda": "Vehiculos Unidadpi gestionay.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Vehiculo mana deuda nitaq robado reporte kanan tiyan radicatoria cambiospaq.",
            "c": "Timbre Bs. 40", "t": "Gestion directa", "dep": "Vehiculos",
            "u": "",
        },
    },
    "vehiculo_baja": {
        "es": {
            "n": "Baja Tributaria del Vehiculo",
            "icon": "\U0001F6A9",
            "d": "Dar de baja el vehiculo en el RUAT por siniestro, robo, exportacion o fuera de circulacion.",
            "donde": "Unidad de Vehiculos - Municipalidad de Sacaba.",
            "cuanto": "Timbre municipal de Bs. 20 y folder administrativo.",
            "que_necesito": ["Formulario de solicitud (ANEXO 1)", "CI vigente del propietario", "CRPVA (RUAT 03) original y placas", "Informe de Transito o DIPROVE (siniestro), denuncia (robo) o resolucion de Aduana (exportacion)", "Sin deudas de impuestos", "Timbre de Bs. 20", "Folder administrativo"],
            "como": ["Solicita el formulario ANEXO 1", "Entrega CRPVA y placas originales", "Acompaña el informe de transito, denuncia o resolucion", "Cancela el timbre de Bs. 20", "Se da de baja el vehiculo"],
            "cuanto_tarda": "Gestion en la Unidad de Vehiculos.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "Para baja por fuera de circulacion el vehiculo debe tener al menos 5 anios de radicatoria en Sacaba.",
            "c": "Timbre Bs. 20", "t": "Gestion directa", "dep": "Vehiculos",
            "u": "",
        },
        "qu": {
            "n": "Vehiculo Baja Tributaria",
            "icon": "\U0001F6A9",
            "d": "Vehiculota RUATqpi baja ruray siniestro, robo, exportacion utaq mana pasaycashanrayku.",
            "donde": "Vehiculos Unidadpi, Municipalidad de Sacaba.",
            "cuanto": "Timbre municipal Bs. 20 nitaq folder administrativo.",
            "que_necesito": ["Formulario solicitud (ANEXO 1)", "CI vigente propietariop", "CRPVA (RUAT 03) original nitaq plakas", "Transito/DIPROVE informe (siniestro), denuncia (robo) o Aduana resolucion (exportacion)", "Mana impuesto deuda", "Timbre Bs. 20", "Folder administrativo"],
            "como": ["Formulario ANEXO 1 mañay", "CRPVA nitaq plakas original qawqay", "Informe, denuncia utaq resolucion apamuy", "Timbre Bs. 20 pagay", "Vehiculo baja ruray"],
            "cuanto_tarda": "Vehiculos Unidadpi gestionay.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Mana pasaycashanrayku bajapaq, vehiculo 5+ anio radicatoria kanan tiyan Sacabapi.",
            "c": "Timbre Bs. 20", "t": "Gestion directa", "dep": "Vehiculos",
            "u": "",
        },
    },
    "vehiculo_reemplaque": {
        "es": {
            "n": "Reemplaque de Vehiculo",
            "icon": "\U0001F6A8",
            "d": "Obtencion de nuevas placas para vehiculos que no fueron reemplazados (sistema PTA).",
            "donde": "Unidad de Vehiculos - Municipalidad de Sacaba.",
            "cuanto": "Valores segun tramite (folder administrativo).",
            "que_necesito": ["Declaracion Jurada de vehiculo no reemplacado emitida por GAMS", "PTA/COPO original y fotocopia", "Carnet de propiedad (sistema antiguo)", "Fotocopia de CI vigente del propietario", "Folder administrativo"],
            "como": ["Solicita la declaracion jurada en GAMS", "Reune PTA/COPO, carnet de propiedad y CI", "Presenta el expediente en la Unidad de Vehiculos", "Cancela los valores", "Recibe las nuevas placas"],
            "cuanto_tarda": "Gestion en la Unidad de Vehiculos.",
            "horario": "Lunes a viernes en horario habil.",
            "consejo": "Si hay transferencia, se tramita el reemplaque con la minuta de compra-venta.",
            "c": "Segun tramite", "t": "Gestion directa", "dep": "Vehiculos",
            "u": "",
        },
        "qu": {
            "n": "Vehiculo Reemplaque",
            "icon": "\U0001F6A8",
            "d": "Mushuq plakata hurqoy mana reemplazasqa vehiculospaq (sistema PTA).",
            "donde": "Vehiculos Unidadpi, Municipalidad de Sacaba.",
            "cuanto": "Valores segun tramite (folder administrativo).",
            "que_necesito": ["GAMS emitido vehiculo mana reemplacado declaracion jurada", "PTA/COPO original nitaq fotocopia", "Carnet de propiedad (ñawpa sistema)", "CI vigente fotocopia", "Folder administrativo"],
            "como": ["GAMSqpi declaracion jurada mañay", "PTA/COPO, carnet nitaq CI apamuy", "Expediente Vehiculos Unidadqpi presentay", "Valores pagay", "Mushuq plakata chaskiy"],
            "cuanto_tarda": "Vehiculos Unidadpi gestionay.",
            "horario": "Lun-Vie horario habilpi.",
            "consejo": "Transferencia kaptinqa, minuta compra-ventawan reemplaque tramitakun.",
            "c": "Segun tramite", "t": "Gestion directa", "dep": "Vehiculos",
            "u": "",
        },
    },
}

MULTAS = {
    "es": {
        "transito": {
            "n": "Multas de Transito",
            "items": [
                {"f": "Exceso de velocidad", "m": "Bs. 100 - 300"},
                {"f": "Sin licencia de conducir", "m": "Bs. 200 - 500"},
                {"f": "Estacionamiento prohibido", "m": "Bs. 50 - 100"},
                {"f": "Pasar semaforo en rojo", "m": "Bs. 100 - 200"},
                {"f": "Manejar en estado de ebriedad", "m": "Bs. 500 - 1,000"},
                {"f": "Sin cinturon de seguridad", "m": "Bs. 50 - 100"},
                {"f": "Uso de celular manejando", "m": "Bs. 100 - 200"},
            ],
        },
        "municipales": {
            "n": "Multas Municipales",
            "items": [
                {"f": "Arrojar basura en via publica", "m": "Bs. 50 - 100"},
                {"f": "Ruido despues de las 22:00", "m": "Bs. 100 - 200"},
                {"f": "Vender sin permiso", "m": "Bs. 200 - 500"},
                {"f": "Danar mobiliario municipal", "m": "Bs. 100 - 300"},
                {"f": "Construir sin permiso", "m": "Bs. 500 - 2,000"},
            ],
        },
        "pago": "**Procedimiento de Pago de Multas:**\n\n1. **Verifica tu multa** en la Unidad de Multas (Plaza Principal, Sacaba).\n2. **Recibe el recibo/notificacion** con el monto y el codigo de pago.\n3. **Paga en estos puntos de Sacaba:**\n   - Caja Municipal - Plaza Principal 6 de Agosto\n   - Banco Union - Av. Blanco Galindo esq. Av. Eloy Salmon\n   - BNB / BISA (agencia central de Sacaba)\n   - **Con tu banca movil** (QR)\n4. **Pago por QR paso a paso:**\n   - Abre la app de tu banco (Banca Movil)\n   - Busca la opcion \"Pago QR\" o \"Escanear QR\"\n   - Escanea el codigo QR de la municipalidad en la ventanilla\n   - Escribe el monto exacto de la multa\n   - Confirma y guarda el comprobante\n5. **Conserva el comprobante** para acreditar tu pago.\n6. **Apelacion:** tienes 5 dias habiles para apelar la multa.",
    },
    "qu": {
        "transito": {
            "n": "Transito Multakuna",
            "items": [
                {"f": "Exceso de velocidad", "m": "Bs. 100 - 300"},
                {"f": "Mana licencia", "m": "Bs. 200 - 500"},
                {"f": "Prohibido aparca", "m": "Bs. 50 - 100"},
                {"f": "Semaforota mana kasukuy", "m": "Bs. 100 - 200"},
                {"f": "Machasqa maneja", "m": "Bs. 500 - 1,000"},
                {"f": "Cinturon mana churakuy", "m": "Bs. 50 - 100"},
                {"f": "Celularwan maneja", "m": "Bs. 100 - 200"},
            ],
        },
        "municipales": {
            "n": "Munisipyu Multakuna",
            "items": [
                {"f": "Basurata wikchuy", "m": "Bs. 50 - 100"},
                {"f": "Ruido 22:00manta qhipa", "m": "Bs. 100 - 200"},
                {"f": "Mana permiso vendiy", "m": "Bs. 200 - 500"},
                {"f": "Mobiliariota pakiy", "m": "Bs. 100 - 300"},
                {"f": "Mana permiso construir", "m": "Bs. 500 - 2,000"},
            ],
        },
        "pago": "**Multata Pagaypaq:**\n\n1. **Multaykita qhaway** Multas Unidadpi (Plaza Principal, Sacaba).\n2. **Recibo chaskikuy** montowan pago codigowan.\n3. **Kay puntospi pagay Sacabapi:**\n   - Caja Municipal - Plaza Principal 6 de Agosto\n   - Banco Union - Av. Blanco Galindo esq. Av. Eloy Salmon\n   - BNB / BISA (Sacabaq agencia central)\n   - **Banca movil niqkiwan** (QR)\n4. **QRwan pagay paso a paso:**\n   - Banca movil (app) kiqay bankoykiqu\n   - \"Pago QR\" utaq \"Escanear QR\" opcionta maskay\n   - Municipalidad codigo QRta escanay ventanillapi\n   - Multa monto exactu qillqay\n   - Confirmay nitaq comprobanteta waqaychay\n5. **Comprobanteta waqaychay** pagasqaykita riqsichinaykipaq.\n6. **Apelacion:** 5 p'unchay llamkaq multata apelayta atiyki.",
    },
}

UI = {
    "es": {
        "title": "Asistente Municipal",
        "sub": "En linea",
        "ph": "Escribe tu consulta...",
        "powered": "IA - Munic. Sacaba",
        "greeting": "\u00a1Hola! \U0001F60A Soy el chatbot municipal de **Sacaba** y estoy para ayudarte. \u00bfNecesitas sacar tu **carnet de identidad**? \u00bfQuieres informaci\u00f3n sobre **tr\u00e1mites** como residencia, licencias o veh\u00edculos? \u00bfO tal vez sobre **multas y c\u00f3mo pagarlas**? D\u00edme, \u00bfen qu\u00e9 te ayudo hoy?",
        "smalltalk": "\u00a1Bien, muy bien! \U0001F60A Gracias por preguntar. Me alegra estar contigo de esta manera. Soy el asistente oficial de Sacaba y estoy para guiarte en tus tr\u00e1mites: carnet, residencia, licencias, catastro, veh\u00edculos y el pago de multas. \u00bfDe qu\u00e9 te gustar\u00eda informarte?",
        "identity": "Soy **Tu Gobierno en Sacaba**, el asistente virtual oficial con inteligencia artificial del municipio. Te oriento en tr\u00e1mites como **carnet de identidad**, constancias, licencias, catastro, veh\u00edculos, y te ayudo con **multas** (montos y pago en banco o con QR). Adem\u00e1s \u00a1aprendo de cada conversaci\u00f3n para ayudarte mejor!",
        "farewell": "\u00a1Gracias por tu consulta! \U0001F60A Siempre que necesites algo sobre tr\u00e1mites o multas, aqu\u00ed estoy. \u00a1Que tengas un excelente d\u00eda!",
        "default": "\U0001F914 A\u00fan no tengo la respuesta a esa consulta, pero **puedo aprenderla**. Ay\u00fadame escribiendo: **aprende: tu pregunta = tu respuesta**. Por ejemplo:\n`aprende: \u00bfcu\u00e1nto cuesta el certificado? = Bs. 10`\n\nMientras tanto, te recuerdo mis temas:\n\n- \U0001FAAA \"\u00bfC\u00f3mo saco mi carnet?\"\n- \U0001F3E0 \"Constancia de residencia\"\n- \U0001F3E2 \"Licencia de funcionamiento\"\n- \U0001F3D7\uFE0F \"Permiso de construcci\u00f3n\"\n- \U0001F697 \"Tr\u00e1mites de veh\u00edculo\"\n- \U0001F4B0 \"Multas y pagos\"",
        "horarios": "**Horarios de Atencion GAM Sacaba:**\n- Lunes a Viernes: 8:00 - 12:00 / 14:00 - 18:00\n- Sabados: 8:00 - 12:00\n- Domingos: Cerrado",
        "contacto": "**Contacto - Gobierno Autonomo Municipal de Sacaba:**\n- Linea directa: 4701677\n- Email: info@sacaba.gob.bo\n- Web: sacaba.gob.bo\n- Direccion: Consistorial S-002, Sacaba, Cochabamba",
        "subalcaldias": "**Subalcaldias Distritales - 12 distritos:**\n\nUrbana:\n- Distrito 1: Jose Mamani Gallardo - La Paz 161, Sacaba - Tel: 4-4701677\n- Distrito 2: Juan Carlos Chavez Rodriguez - Av. San Maximiliano Kolbe - Tel: 4-4723440\n- Distrito 3: Juan Jose Leon Guarayo - Av. Eliodoro Villazon km 1 1/2 - Tel: 4-4299665\n- Distrito 4: Cristian Boris Maldonado - Av. Chapare - Tel: 4-4276318\n- Distrito 6: Alejandro Veizaga - Av. Bolivia, El Abra - Tel: 4-4712738\n- Distrito 7: Franz Michel Ojalvo Castro - Av. Barrientos - Tel: 4-4289815\n- Lava Lava: Gabriel Garcia Rojas - Mercado Modelo de Canal Pata\n\nRural:\n- Aguirre: Herminio Orosco Zapata - Comunidad Aguirre\n- Chiñata: Tomas Sanchez Marquina - Comunidad Chiñata\n- Distrito 5: Russberth Rojas Castellon - Distrito Rural 5\n- Palca: Alfredo Luna Garcia - Comunidad Palca\n- Ucuchi: Jhimy Orellana Acosta - Comunidad Ucuchi",
        "guia_telefonica": "**Guia Telefonica Institucional:**\n- Linea Directa GAMS: 4-4701677\n- Transparencia y Lucha contra la Corrupcion: 4-4705776\n- Intendencia Municipal: 4-4702369\n- Direccion de Ingresos y Servicios Municipales: 4-4200580\n- Direccion Administrativa de Salud: 4-4700871\n- Hospital Mexico: 4-4702173\n- Hospital Salomon Klein: 4-4715117\n- Matadero Municipal: 4-4704824\n- Cementerio Municipal: 4-4702102\n- Alumbrado Publico: 4-4700461\n- Transportes y Maquinaria: 4-4704825\n- EMAPAS: 4-4706525\n- GERES: 4-4700357\n- Honorable Concejo Municipal: 4-4708526\n- Estadio Municipal: 4-4702261",
    },
    "qu": {
        "title": "Munisipyu Yanapay",
        "sub": "Kachkani",
        "ph": "Tapukuyniykita qillqay...",
        "powered": "IA - Munis. Sakaba",
        "greeting": "\u00a1Imaynallan! \U0001F60A Noqaqa **Sakaba Munisipyuq Gobiernoq** yanapaq kachkani. Cayayoq **carnet horqoyta**, **tr\u00e1mitekuna** (residencia, licencia, catastro, veh\u00edculos) utaq **multas pagayta** yanapayta munayki. \u00bfImawan yanapaykayman?",
        "smalltalk": "\u00a1Allinmi kachkani! \U0001F60A Tapukusqaykimanta yusulpayki. Carnet, residencia, licencia, catastro, veh\u00edculos nitaq multas pagayniqwan yanapayta atiymi. \u00bfImata munanki?",
        "identity": "Noqaqa **Sakaba Munisipyuq Asistente** kachkani, inteligencia artificialwan ruwasqa. Carnet, constancia, licencia, catastro, veh\u00edculos nitaq multakunaq montunmanta (banco utaq QRwan pagay) yachachiyta atiymi. Sapa rimanakuymanta **yanapakuyta yachani**!",
        "farewell": "\u00a1Yusulpayki! \U0001F60A Tr\u00e1mitekuna utaq multakunaq munaqtiykiqa kaypi kachkani. \u00a1Allin p'unchay kachun!",
        "default": "\U0001F914 Kay yachayta manaraq uyariqanichu, ichaqa **yachay atiyman**. Kayjina qillqaway: **aprende: tapukuy = kutichiy**. Eh:\n`aprende: \u00bfhayk'ataq certificado qullqin? = Bs. 10`\n\nKunanqa kaykunapi yanapayta atiymi:\n\n- \U0001FAAA \"Carnetta imaynata horqokuni?\"\n- \U0001F3E0 \"Tiyay constancia\"\n- \U0001F3E2 \"Licencia funcionamiento\"\n- \U0001F3D7\uFE0F \"Construcci\u00f3n permiso\"\n- \U0001F697 \"Veh\u00edculo tramitekuna\"\n- \U0001F4B0 \"Multakuna nitaq pagay\"",
        "horarios": "**Horario Atencion GAM Sakaba:**\n- Lun-Vie: 8:00 - 12:00 / 14:00 - 18:00\n- Sab: 8:00 - 12:00\n- Dom: Wisqasqa",
        "contacto": "**Contacto - Sakaba Munisipyuq Gobierno Autonomo:**\n- Linea directa: 4701677\n- Email: info@sacaba.gob.bo\n- Web: sacaba.gob.bo\n- Direccion: Consistorial S-002, Sacaba, Cochabamba",
        "subalcaldias": "**Subalcaldia Distritalkuna - 12 distritos:**\n\nUrbana:\n- Distrito 1: Jose Mamani Gallardo - La Paz 161, Sacaba - Tel: 4-4701677\n- Distrito 2: Juan Carlos Chavez Rodriguez - Av. San Maximiliano Kolbe - Tel: 4-4723440\n- Distrito 3: Juan Jose Leon Guarayo - Av. Eliodoro Villazon km 1 1/2 - Tel: 4-4299665\n- Distrito 4: Cristian Boris Maldonado - Av. Chapare - Tel: 4-4276318\n- Distrito 6: Alejandro Veizaga - Av. Bolivia, El Abra - Tel: 4-4712738\n- Distrito 7: Franz Michel Ojalvo Castro - Av. Barrientos - Tel: 4-4289815\n- Lava Lava: Gabriel Garcia Rojas - Mercado Modelo de Canal Pata\n\nRural:\n- Aguirre: Herminio Orosco Zapata - Comunidad Aguirre\n- Chiniata: Tomas Sanchez Marquina - Comunidad Chiniata\n- Distrito 5: Russberth Rojas Castellon - Distrito Rural 5\n- Palca: Alfredo Luna Garcia - Comunidad Palca\n- Ucuchi: Jhimy Orellana Acosta - Comunidad Ucuchi",
        "guia_telefonica": "**Guia Telefonica:**\n- Linea Directa GAMS: 4-4701677\n- Transparencia: 4-4705776\n- Intendencia: 4-4702369\n- Ingresos y Servicios: 4-4200580\n- Direccion de Salud: 4-4700871\n- Hospital Mexico: 4-4702173\n- Hospital Salomon Klein: 4-4715117\n- Matadero Municipal: 4-4704824\n- Cementerio: 4-4702102\n- Alumbrado Publico: 4-4700461\n- Transportes: 4-4704825\n- EMAPAS: 4-4706525\n- GERES: 4-4700357\n- Concejo Municipal: 4-4708526\n- Estadio Municipal: 4-4702261",
    },
}

_LABELS = {
    "es": {
        "donde": "Donde", "costo": "Costo", "tiempo": "Tiempo", "tiempo_estimado": "Tiempo estimado",
        "horario": "Horario", "consejo": "Consejo", "ubicacion": "Ubicacion",
        "requisitos": "Requisitos", "procedimiento": "Procedimiento",
        "tramites": "Tramites Disponibles:", "pregunta": "Que tramite te interesa?",
        "multas": "Informacion de Multas:",
    },
    "qu": {
        "donde": "Maypi", "costo": "Qullqi", "tiempo": "Pacha", "tiempo_estimado": "Pacha",
        "horario": "Horario", "consejo": "Kunan", "ubicacion": "Ubicacion",
        "requisitos": "Requisitokuna", "procedimiento": "Ruwanakuna",
        "tramites": "Tramitekuna:", "pregunta": "Ima tramite munanki?",
        "multas": "Multakuna Yachay:",
    },
}

TRAMITE_PATTERNS = [
    ("carnet", ["carnet", "cedula", "identidad", "segepi", "biometrico", "huellas", "documento"]),
    ("carnet_conducta", ["antecedentes", "conducta", "certificado de conducta", "record policial", "papelito"]),
    ("licencia_conducir", ["licencia de conducir", "licencia de manejo", "licencia para manejar", "carnet de conducir"]),
    ("registro_civil", ["certificado de nacimiento", "registro civil", "partida de nacimiento", "acta de nacimiento", "nacimiento", "certificado de matrimonio"]),
    ("residencia", ["residencia", "vivo en", "constancia de residencia"]),
    ("funcionamiento", ["funcionamiento", "licencia de funcionamiento", "negocio", "tienda", "comercio", "abrir negocio", "patente"]),
    ("construccion", ["construccion", "construir", "edificar", "plano de vivienda", "obra nueva"]),
    ("catastro_certificado", ["certificado catastral", "catastral"]),
    ("catastro_empadronamiento", ["empadronamiento", "empadronar", "registro predial", "predio", "catastro"]),
    ("catastro_avaluo", ["avaluo", "avaluar", "tasar", "valor catastral"]),
    ("propiedad", ["registro de propiedad", "mi terreno", "mi casa propia", "derechos reales"]),
    ("solteria", ["solteria", "casarse", "matrimonio", "soltero"]),
    ("prediales", ["predial", "impuesto"]),
    ("agua", ["agua potable", "servicio de agua", "conexion de agua", "agua"]),
    ("eventos", ["evento", "fiesta", "concierto", "festival"]),
    ("urbanismo_plano", ["aprobacion de plano", "aprobacion de planos", "plano de terreno", "division de lotes", "subdivision", "anexion de terreno", "regularizacion predial"]),
    ("urbanismo_ampliacion", ["ampliacion", "ampliar", "remodelacion de casa", "remodelar mi casa", "remodelar"]),
    ("urbanismo_uso_suelo", ["uso de suelo", "rasante", "linea nivel", "zona y distrito", "certificacion de urbanismo"]),
    ("urbanismo_horizontal", ["propiedad horizontal", "condominio"]),
    ("urbanismo_verja", ["verja", "cerco", "muro"]),
    ("nodeuda", ["no deuda", "deuda", "sin deuda", "libre de deuda"]),
    ("vehiculo_transferencia", ["transferencia", "transferir", "traspaso", "traspasar", "cambio de propietario", "compra venta de vehiculo", "comprar carro", "comprar auto"]),
    ("vehiculo_inscripcion", ["inscripcion de vehiculo", "inscribir vehiculo", "registrar mi vehiculo", "registro de vehiculo nuevo", "ruat"]),
    ("vehiculo_radicatoria", ["radicatoria", "cambio de radicatoria"]),
    ("vehiculo_reemplaque", ["reemplaque", "reemplacar", "placas nuevas", "cambio de placas"]),
    ("vehiculo_baja", ["baja tributaria", "dar de baja", "baja del vehiculo", "baja de vehiculo", "siniestro vehicular"]),
    ("vehiculos", ["vehiculo", "vehiculos", "carro", "auto", "camioneta", "placa", "transito y transporte"]),
]

INTENT_PATTERNS = [
    ("greeting", r"^(hola|buenos|buenas|saludos|hey|imaynallan|napa|alli|kamisaki|que tal)\b"),
    ("farewell", r"^(gracias|adios|chau|hasta|yusulpakuy|tupananchiskama|hamusaq)\b"),
    ("smalltalk", r"\b(como estas|como te sientes|como te encuentras|como te va|como estas tu|como van las cosas|allillanchu|allinllachu)\b"),
    ("identity", r"\b(quien eres|quien sos|que eres|como te llamas|para que sirves|para que eres|que puedes hacer|kanki ima|iman kanki)\b"),
    ("donde", r"\b(donde|ubicacion|direccion|mapa|luhuynin|maypitaq|maypi)\b"),
    ("cuanto", r"\b(cuanto|cuesta|costo|precio|chaki|pagan|hayka|hayk'ataq|haykataq|qullqi)\b"),
    ("que_necesito", r"\b(que necesito|requisitos|documentos|papeles|que llevo|que debo|imakunata|requisitokuna|imakunatataq)\b"),
    ("como", r"\b(como|pasos|procedimiento|hacer|tramito|gestiono|obtengo|sacar|proceso|imaynata|imanaspa)\b"),
    ("cuando", r"\b(cuando|tarda|tiempo|plazo|dias|rapido|inmediato|duracion|hayka p un|hayka pacha|imap un)\b"),
    ("horarios", r"\b(horario|atencion|abierto|abren|hora|horariokuna|ura)\b"),
    ("contacto", r"\b(contacto|telefono|correo|email|yupay|telefonokuna)\b"),
    ("multas", r"\b(multa|multas|infraccion|panku|sancion|multakuna)\b"),
    ("menu_tramites", r"\b(tramite|tramites|tramitekuna|tramitekuna|lista|todos|todos los tramites)\b"),
    ("consejo", r"\b(consejo|tip|recomendacion|consejos|kunan)\b"),
    ("subalcaldias", r"\b(subalcaldia|subalcaldias|subalcaldias|distrito|distritos|subalcaldia distrital|alcalde de barrio)\b"),
    ("guia_telefonica", r"\b(guia telefonica|telefonos|numeros|directorio|linea directa|llamar|telefono de)\b"),
]


def normalize(text):
    text = str(text).lower()
    text = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in text if not unicodedata.combining(ch))


QUECHUA_TOKENS = (
    "imaynallan", "allillanmi", "allinllachu", "yusulpakuy", "tupananchiskama",
    "imataq", "imanataq", "imatataq", "imapitaq", "imantataq", "maypitaq", "hayka",
    "munanki", "munankichu", "munani", "munayman", "munasqayki",
    "kachkani", "kachkanichu", "kaykan", "kanchik", "kanku",
    "noqaqa", "nuqaqa", "noqa",
    "wasi", "warmi", "qhari", "runasimi", "qhichwa", "runa simi",
    "tukuyta", "tukuy", "llapan",
    "yachay", "yachayrimanakuy", "rimanakuy", "rimay", "qillqay",
    "waqkuy", "uyariy", "maskaruy", "apaykuy", "hamuy", "kawsay",
    "yanapaykuy", "yanapaykiman", "yanapawanki", "yanapaway", "yanapasqayki",
    "yaku", "kunanqa", "kunan", "mana", "manachu", "ari",
)


def detect_language(text):
    if not isinstance(text, str):
        return "es"
    t = normalize(text)
    for w in QUECHUA_TOKENS:
        if re.search(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", t):
            return "qu"
    return "es"


def detect_tramite(text):
    t = normalize(text)
    for key, words in TRAMITE_PATTERNS:
        for w in words:
            if w in t:
                return key
    return None


def detect_intent(text):
    t = normalize(text)
    for intent, pattern in INTENT_PATTERNS:
        if re.search(pattern, t):
            return intent
    return "question"


# ============================================================
# APRENDIZAJE CONTINUO (memoria local + registro de lo aprendido)
# El chatbot aprende respuestas nuevas con:
#   "aprende: <pregunta> = <respuesta>"
# y cada consulta "sin responder" se guarda en un log.
# ============================================================
def _bundle_dir():
    bundle = getattr(sys, "_MEIPASS", None)
    if bundle:
        return Path(bundle)
    return Path(__file__).resolve().parent


def _data_dir():
    """Directorio donde se guarda lo aprendido (persiste entre reinicios).
    En el .exe compilado guarda junto al ejecutable; en desarrollo en chatbot/."""
    try:
        if getattr(sys, "frozen", False):
            return Path(sys.executable).resolve().parent
    except Exception:
        pass
    return Path(__file__).resolve().parent


LEARN_FILE = _data_dir() / "aprendido.json"
UNKNOWN_LOG = _data_dir() / "preguntas_sin_responder.json"

LANGUAGE_LEARN_OK = {
    "es": "\u00a1Listo! He aprendido esa respuesta. De ahora en adelante la usar\u00e9 para ayudarte mejor.",
    "qu": "\u00a1Listo! Chay kutichiytayachini. Kunanmanta yanapayta atiymi.",
}

# variable global de datos aprendidos (cargada una sola vez)
_learned = None
_unknown = None


def _load_learned():
    global _learned
    if _learned is None:
        try:
            _learned = json.loads(LEARN_FILE.read_text(encoding="utf-8"))
        except Exception:
            _learned = []
    return _learned


def _load_unknown():
    global _unknown
    if _unknown is None:
        try:
            _unknown = json.loads(UNKNOWN_LOG.read_text(encoding="utf-8"))
        except Exception:
            _unknown = []
    return _unknown


def _save_learned():
    try:
        LEARN_FILE.parent.mkdir(parents=True, exist_ok=True)
        LEARN_FILE.write_text(json.dumps(_learned, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def _save_unknown():
    try:
        UNKNOWN_LOG.parent.mkdir(parents=True, exist_ok=True)
        UNKNOWN_LOG.write_text(json.dumps(_unknown, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def _tokens(text):
    words = re.findall(r"[a-z\u00e0-\u00ff]+", normalize(text))
    return set(w for w in words if len(w) > 2)


def _similar(pair, q_tokens):
    if not q_tokens:
        return True if not pair.get("q") else False
    p_tokens = set(pair.get("qt", []))
    if not p_tokens:
        return False
    inter = p_tokens & q_tokens
    return len(inter) / max(len(p_tokens), len(q_tokens)) >= 0.5


def store_learned(pregunta, respuesta, lang="es"):
    """Guarda una pregunta/respuesta aprendida (deduplicada por similitud)."""
    question = str(pregunta).strip()
    answer = str(respuesta).strip()
    if not question or not answer:
        return False
    data = _load_learned()
    qt = list(_tokens(question))
    q_norm = normalize(question)
    for pair in data:
        if pair.get("qf") == q_norm:
            pair["a"] = answer
            pair["lang"] = lang
            _save_learned()
            return True
    data.append({"q": question, "qt": qt, "qf": q_norm, "a": answer, "lang": lang})
    _save_learned()
    return True


def lookup_learned(msg, lang="es"):
    """Busca en la memoria local una respuesta aprendida para el mensaje."""
    data = _load_learned()
    if not data:
        return None
    qt = _tokens(msg)
    q_norm = normalize(msg)
    for pair in data:
        if pair.get("qf") == q_norm:
            return pair.get("a")
    # coincidencia aproximada
    best = None
    best_ratio = 0.0
    for pair in data:
        r = _similar(pair, qt)
        if r:
            ratio = len(set(pair.get("qt", [])) & qt) / max(1, len(set(pair.get("qt", [])) | qt))
            if ratio > best_ratio:
                best_ratio = ratio
                best = pair.get("a")
    return best


def record_unknown(msg, lang="es"):
    """Registra una consulta que el bot no supo responder, para aprenderse luego."""
    text = str(msg).strip()
    if len(text) < 3:
        return
    data = _load_unknown()
    norm = normalize(text)
    for entry in data:
        if entry.get("qf") == norm:
            entry["count"] = entry.get("count", 1) + 1
            _save_unknown()
            return
    data.append({"q": text[:200], "qf": norm, "lang": lang, "count": 1})
    _save_unknown()


def parse_learn_command(msg):
    """Detecta el comando 'aprende: pregunta = respuesta'."""
    low = normalize(msg)
    if "aprende:" not in low and "aprende :" not in low:
        return None
    # quitar 'aprende:'
    m = re.search(r"aprende\s*[:]\s*(.+)", msg, flags=re.IGNORECASE)
    if not m:
        return None
    body = m.group(1)
    if "=" not in body:
        return None
    q, a = body.split("=", 1)
    q = q.strip().lstrip("\"'").strip()
    a = a.strip().lstrip("\"'").strip()
    if not q or not a:
        return None
    return q, a


def build_card(t, lang="es"):
    lb = _LABELS.get(lang, _LABELS["es"])
    lines = [t["icon"] + " **" + t["n"] + "**\n"]
    lines.append(t["d"] + "\n")
    lines.append("**" + lb["donde"] + ":** " + t["donde"])
    lines.append("**" + lb["costo"] + ":** " + t["c"])
    lines.append("**" + lb["tiempo"] + ":** " + t["t"])
    if t.get("consejo"):
        lines.append("**" + lb["consejo"] + ":** " + t["consejo"])
    if t.get("u"):
        lines.append(lb["ubicacion"] + ": " + t["u"])
    return "\n".join(lines)


def _tiempo_es_a_qu(texto_es):
    """Convierte una expresion de tiempo en espanol a quechua natural/fluido."""
    t = texto_es.strip()
    exactos = {
        "Inmediato": "Chaylla",
        "Gestion directa": "Usqaylla gestiona",
        "Gestion directa.": "Usqaylla gestiona",
        "Segun proyecto": "Proyecto nisqaman jina",
        "Segun revision": "Qhawariy nisqaman jina",
        "1 dia": "1 p'unchay",
    }
    claves = {k.lower(): v for k, v in exactos.items()}
    if t.lower() in claves:
        return claves[t.lower()]

    m = re.match(r"^([\d\s\-]+)\s*(dia|dias|semana|semanas)$", t, re.IGNORECASE)
    if m:
        num = re.sub(r"\s*-\s*", "-", m.group(1).strip())
        if m.group(2).lower().startswith("semana"):
            return num + " simana"
        return num + " p'unchay"

    m = re.match(r"^(\d+)\s*(dia|dias)?\s*al?\s*(\d+)\s*(dia|dias|semana|semanas)?$", t, re.IGNORECASE)
    if m:
        a, b = m.group(1), m.group(3)
        if m.group(4) and m.group(4).lower().startswith("semana"):
            return a + "-" + b + " simana"
        return a + "-" + b + " p'unchay"
    return t


def build_tramite_list(lang):
    lb = _LABELS.get(lang, _LABELS["es"])
    keys = list(KB.keys())
    header = lb["tramites"]
    lines = [header]
    for i, k in enumerate(keys):
        t = KB[k].get(lang) or KB[k]["es"]
        tiempo = t["t"] if lang != "qu" or not KB[k].get("es") else _tiempo_es_a_qu(KB[k]["es"].get("t", t["t"]))
        lines.append(str(i + 1) + ". " + t["icon"] + " " + t["n"] + " - " + t["c"] + " | " + tiempo)
    footer = lb["pregunta"]
    lines.append(footer)
    return "\n".join(lines)


def build_multas_string(lang):
    lb = _LABELS.get(lang, _LABELS["es"])
    m = MULTAS[lang]
    title = lb["multas"]
    parts = [title, m["transito"]["n"] + ":"]
    for item in m["transito"]["items"]:
        parts.append("- " + item["f"] + ": " + item["m"])
    parts.append("")
    parts.append(m["municipales"]["n"] + ":")
    for item in m["municipales"]["items"]:
        parts.append("- " + item["f"] + ": " + item["m"])
    parts.append("")
    parts.append(m["pago"])
    return "\n".join(parts)


def _build_knowledge_context():
    lines = [
        "Eres el **Asistente Municipal de Sacaba** (Cochabamba, Bolivia), el chat oficial del Gobierno Autonomo Municipal de Sacaba.",
        "Usa SIEMPRE la base de conocimiento municipal de abajo como tu unica fuente sobre tramites y servicios.",
        "Explica los tramites con detalles (never inventes datos): costos, requisitos, pasos, horarios y dependecias reales.",
        "Responde de forma amistosa, breve, clara y servicial, como un funcionario amable que quiere ayudar al ciudadano.",
        "Habla en espanol simple (palabras faciles para que tambien te entienda gente que habla quechua) o en quechua (runasimi boliviano) cuando el ciudadano escriba o hable en quechua; el quechua es tu responsabilidad principal.",
        "No muestres tu razonamiento, ni metadatos, ni listas de instrucciones internas: responde directo el texto final, con saludos amables cuando corresponda.",
        "Si te preguntan algo ajeno al municipio, redirige amablemente a la informacion municipal de Sacaba.",
        "",
        "BASE DE CONOCIMIENTO MUNICIPAL:",
    ]
    for key, data in KB.items():
        es = data.get("es", {})
        lines.append("")
        lines.append("### " + es.get("n", key))
        if es.get("d"):
            lines.append("Descripcion: " + es["d"])
        if es.get("donde"):
            lines.append("Donde: " + es["donde"])
        if es.get("cuanto"):
            lines.append("Costo: " + es["cuanto"])
        if es.get("cuanto_tarda"):
            lines.append("Tiempo: " + es["cuanto_tarda"])
        if es.get("horario"):
            lines.append("Horario: " + es["horario"])
        if es.get("que_necesito"):
            lines.append("Requisitos: " + "; ".join(es["que_necesito"]))
        if es.get("como"):
            lines.append("Pasos: " + " -> ".join(es["como"]))
        if es.get("consejo"):
            lines.append("Consejo: " + es["consejo"])
    lines.append("")
    lines.append("### MULTAS")
    lines.append("Transito (Bs. 50-1000) y Municipales (Bs. 50-2000). Pago en Caja Municipal o bancos. Apelacion: 5 dias habiles.")
    lines.append("### HORARIOS GENERALES GAM SACABA")
    lines.append("Lun-Vie 8:00-12:00 / 14:00-18:00, Sab 8:00-12:00, Dom cerrado.")
    lines.append("### CONTACTO GAM SACABA")
    lines.append("Linea directa: 4701677, Email: info@sacaba.gob.bo, Web: sacaba.gob.bo")
    lines.append("Direccion: Consistorial S-002, Sacaba, Cochabamba")
    lines.append("### UBICACION")
    lines.append("Consistorial S-002, Sacaba, Cochabamba, Bolivia")
    lines.append("### SUBALCALDIAS DISTRITALES (12 distritos)")
    lines.append("Urbana: Distrito 1 (Tel 4-4701677), Distrito 2 (Tel 4-4723440), Distrito 3 (Tel 4-4299665), Distrito 4 (Tel 4-4276318), Distrito 6 (Tel 4-4712738), Distrito 7 (Tel 4-4289815), Lava Lava")
    lines.append("Rural: Aguirre, Chiñata, Distrito 5, Palca, Ucuchi")
    lines.append("### GUIA TELEFONICA INSTITUCIONAL")
    lines.append("Linea Directa: 4-4701677 | Transparencia: 4-4705776 | Intendencia: 4-4702369 | Ingresos: 4-4200580 | Salud: 4-4700871 | Hospital Mexico: 4-4702173 | Hospital Salomon Klein: 4-4715117 | Matadero: 4-4704824 | Cementerio: 4-4702102 | Alumbrado: 4-4700461 | Transportes: 4-4704825 | EMAPAS: 4-4706525 | GERES: 4-4700357 | Concejo: 4-4708526 | Estadio: 4-4702261")
    return "\n".join(lines)


def get_ai_resp(msg, lang="es"):
    if not _ai_available:
        return get_resp(msg, lang)

    # Pase por el "especialista de quechua" (NLLB): traduce el mensaje del
    # ciudadano a espanol para que ChatGPT lo entienda mejor.
    prompt = msg
    if lang == "qu":
        traducido = _hf_nllb_translate(msg, src=NLLB_QU, tgt=NLLB_ES)
        if traducido:
            prompt = "[QUE] " + traducido + " | [QU] " + msg

    try:
        lang_instruction = (
            "IMPORTANTE: El ciudadano escribio en ESPANOL. Responde en espanol claro, "
            "breve y amistoso, con cordialidad, como un funcionario amable del municipio. "
            "Usa SOLO los datos de la base de conocimiento municipal de abajo y nunca inventes datos. "
            "Si es un saludo o pregunta personal (como 'como estas' o 'quien eres'), respondela "
            "con naturalidad y simpatia, y ofrece ayuda. Responde directo, sin razonamiento interno."
            if lang == "es"
            else "IMPORTANTE: El ciudadano escribio en QUECHUA (runasimi boliviano de Cochabamba). "
                 "Responde en quechua boliviano natural, amable y breve. Usa los prestamos del espanol "
                 "que la gente usa a diario (carnet, licencia, tramite, oficina, multa) cuando sean mas "
                 "claros que el vocabulario quechua. Responde directo y sin listas de instrucciones."
        )
        context = _build_knowledge_context()
        response = _client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": f"{context}\n\n{lang_instruction}"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
            max_tokens=900,
        )
        text = response.choices[0].message.content
        if text and text.strip():
            # Pase de pulido: para quechua, NLLB puede devolver una version mas
            # natural. Si falla, usamos la respuesta de ChatGPT tal cual.
            if lang == "qu":
                pulido = _hf_nllb_translate(text, src=NLLB_ES, tgt=NLLB_QU)
                if pulido:
                    return pulido.strip()
            return text.strip()
        return get_resp(msg, lang)
    except Exception:
        return get_resp(msg, lang)


def transcribe_audio(audio_bytes, language="es"):
    if not _ai_available:
        raise Exception("OpenAI API no configurada. Agrega tu API Key en el archivo .env")

    try:
        response = _client.audio.transcriptions.create(
            model=AUDIO_MODEL,
            file=("audio.webm", audio_bytes, "audio/webm"),
            language="es" if language == "es" else "qu",
        )
        text = getattr(response, "text", "") or ""
        return text.strip()
    except Exception as e:
        raise Exception(f"Error en transcripcion: {str(e)}")


def is_ai_available():
    return _ai_available


def translate_page(items):
    """Traduce una lista de items [(id, texto_espanol)] a quechua boliviano.
    Usa ChatGPT cuando esta disponible (mejor calidad y preserva HTML) y, si no,
    cae al modelo gratuito de quechua NLLB (Hugging Face).
    Devuelve {id: quechua} si tuvo exito, {} si no habia items, o None si todos fallaron."""
    if not items:
        return {}

    # 1) ChatGPT primero (aplica sobre textos con HTML, de forma agrupada).
    if _ai_available:
        res = _translate_page_chatgpt(items)
        if res:
            return res

    # 2) Fallback: NLLB de Hugging Face (solo traduccion de texto plano).
    out = {}
    for orig_id, texto in items:
        qt = _hf_nllb_translate(texto, src=NLLB_ES, tgt=NLLB_QU, timeout=90)
        if isinstance(qt, str) and qt.strip():
            qt = re.sub(r"<br\s*/?>", " ", qt)
            out[orig_id] = qt.strip()
    return out or None


def _translate_page_chatgpt(items):
    """Variante de traduccion de pagina usando ChatGPT (agrupada y con HTML)."""
    system = (
        "Eres un traductor experto de espanol a quechua boliviano "
        "(runasimi de Cochabamba / Sacaba, Bolivia). Reglas: "
        "1. Traduce solo el texto visible entre las etiquetas HTML. "
        "2. Preserva EXACTAMENTE todas las etiquetas HTML (<strong>, <a>, <span>, <i>, <u>, ...) "
        "con sus atributos, links (href), clases, ids y entidades (&amp;, &quot;, ...). "
        "3. Preserva numeros, el nombre de la ciudad (Sacaba), siglas (SEGIP, GERES, ...), "
        "moneda (Bs. 50), telefonos, URLs y emojis exactamente iguales. "
        "4. Usa el quechua claro y cotidiano de la gente (runasimi boliviano): "
        "p'unchay = dia, maypi = donde, qullqi = dinero/costo, pacha = tiempo, "
        "ima p'unchay = cuando. "
        "Prefiere los prestamos del espanol que los bolivianos usan a diario "
        "(tramite, oficina, multa, carnet, licencia, predial, requisito, horario) "
        "cuando sean mas claros que el vocabulario quechua. "
        "5. Se breve y natural: no agregues ni omitas informacion. "
        "6. Responde UNICAMENTE con un JSON valido."
    )
    payload = json.dumps([{"id": str(i), "text": t} for i, t in items], ensure_ascii=False)
    user = (
        "Traduce cada texto al quechua boliviano. No cambies las etiquetas HTML, "
        "los numeros ni los nombres propios. Responde con un unico objeto JSON de la forma "
        '{"translations": {"<id>": "<traduccion>", ...}} usando exactamente los mismos ids.\n\n'
        + payload
    )
    try:
        resp = _client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.4,
            max_tokens=16000,
            response_format={"type": "json_object"},
        )
        text = (resp.choices[0].message.content or "").strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text).strip()
        data = json.loads(text)
        tr = data.get("translations")
        if not isinstance(tr, dict):
            return None
        out = {}
        for i, (orig_id, _t) in enumerate(items):
            val = tr.get(str(i))
            if isinstance(val, str) and val.strip():
                out[orig_id] = val.strip()
        return out or None
    except Exception:
        return None


def get_resp(msg, lang="es"):
    if lang not in LANGUAGES:
        lang = "es"
    msg = str(msg).strip()
    intent = detect_intent(msg)
    tramite = detect_tramite(msg)

    # Comando de aprendizaje
    learn = parse_learn_command(msg)
    if learn:
        q, a = learn
        store_learned(q, a, lang)
        return LANGUAGE_LEARN_OK.get(
            lang,
            "\U0001F4A1 \u00a1Listo! He aprendido esa respuesta. De ahora en adelante, si alguien pregunta \u201c"
            + q
            + "\u201d, te responder\u00e9 lo que me ense\u00f1aste.",
        )

    if intent == "greeting":
        return UI[lang]["greeting"]
    if intent == "farewell":
        return UI[lang]["farewell"]
    if intent == "smalltalk":
        return UI[lang].get("smalltalk", UI["es"]["smalltalk"])
    if intent == "identity":
        return UI[lang].get("identity", UI["es"]["identity"])

    if tramite:
        t = KB[tramite][lang] if lang in KB[tramite] else KB[tramite]["es"]
        lb = _LABELS.get(lang, _LABELS["es"])
        if intent == "donde":
            resp = t["icon"] + " **" + t["n"] + "**\n" + t["donde"]
            if t.get("donde_link"):
                resp += "\n" + lb["ubicacion"] + ": " + t["donde_link"]
            return resp
        if intent == "cuanto":
            detail = t.get("cuanto_detail", "")
            return t["icon"] + " **" + t["n"] + "**\n" + lb["costo"] + ": " + t["cuanto"] + ("\n" + detail if detail else "") + "\n" + lb["tiempo"] + ": " + t["cuanto_tarda"]
        if intent == "que_necesito":
            lines = [t["n"] + " - " + lb["requisitos"] + ":", ""]
            for i, r in enumerate(t["que_necesito"], 1):
                lines.append(str(i) + ". " + r)
            lines.append("\n" + lb["consejo"] + ": " + t["consejo"])
            return "\n".join(lines)
        if intent == "como":
            lines = [t["n"] + " - " + lb["procedimiento"] + ":", ""]
            for i, s in enumerate(t["como"], 1):
                lines.append(str(i) + ". " + s)
            lines.append("\n" + lb["tiempo"] + ": " + t["cuanto_tarda"])
            return "\n".join(lines)
        if intent == "cuando":
            return t["icon"] + " **" + t["n"] + "**\n" + lb["tiempo_estimado"] + ": " + t["cuanto_tarda"] + "\n" + lb["horario"] + ": " + t["horario"]
        if intent == "consejo":
            return t["icon"] + " **" + t["n"] + "**\n" + lb["consejo"] + ": " + t["consejo"]
        return build_card(t, lang)

    if intent == "multas":
        return build_multas_string(lang)
    if intent == "horarios":
        return UI[lang]["horarios"]
    if intent == "contacto":
        return UI[lang]["contacto"]
    if intent == "subalcaldias":
        return UI[lang]["subalcaldias"]
    if intent == "guia_telefonica":
        return UI[lang]["guia_telefonica"]
    if intent == "menu_tramites":
        return build_tramite_list(lang)

    # APRENDIZAJE: memoria local (preguntas que el usuario le enseño)
    learned = lookup_learned(msg, lang)
    if learned:
        return "\U0001F4A1 " + str(learned)

    record_unknown(msg, lang)
    return UI[lang]["default"]


# =====================================================================
# BUSQUEDA AVANZADA DE TRAMITES
# =====================================================================

def _extract_price_number(price_str):
    """Extrae el numero minimo y maximo de un string de precio.
    Ejemplos:
        'Bs. 17' -> (17, 17)
        'Bs. 50 - 200' -> (50, 200)
        'Bs. 30 - 300' -> (30, 300)
        '0.5% - 1%' -> (0.5, 1.0)
        'Valores municipales' -> (None, None)
    """
    if not price_str:
        return None, None
    s = str(price_str).strip()
    if not s:
        return None, None
    nums = re.findall(r'\d+\.?\d*', s)
    if not nums:
        return None, None
    try:
        vals = [float(n) for n in nums]
    except ValueError:
        return None, None
    if len(vals) == 1:
        return vals[0], vals[0]
    return min(vals), max(vals)


def _extract_days(time_str):
    """Extrae los dias estimados de un string de tiempo.
    Ejemplos:
        'Inmediato' -> 0
        '1 a 2 dias habiles' -> 2
        '5 a 10 dias habiles' -> 10
        '15 a 30 dias habiles' -> 30
        '1-2 semanas' -> 14
        '2 a 3 semanas' -> 21
        '1 mes' -> 30
        'Gestion directa' -> None
        'Segun proyecto' -> None
    """
    if not time_str:
        return None
    t = str(time_str).lower().strip()
    if 'inmediato' in t or 'chaylla' in t or 'chay p' in t:
        return 0
    if 'semana' in t:
        nums = re.findall(r'\d+', t)
        if nums:
            max_weeks = max(int(n) for n in nums)
            return max_weeks * 7
    if 'mes' in t:
        nums = re.findall(r'\d+', t)
        if nums:
            return max(int(n) for n in nums) * 30
    if 'dia' in t or 'p' in t and 'unchay' in t:
        nums = re.findall(r'\d+', t)
        if nums:
            return max(int(n) for n in nums)
    return None


def search_tramites(query=None, min_price=None, max_price=None,
                    max_days=None, department=None, category=None, lang="es"):
    """Busqueda avanzada de tramites con filtros opcionales.

    Parametros:
        query: texto libre para buscar en nombre, descripcion, requisitos
        min_price: precio minimo (float o None)
        max_price: precio maximo (float o None)
        max_days: tiempo maximo en dias (int o None)
        department: departamento exacto (str o None)
        category: categoria del tramite (str o None)
        lang: idioma de respuesta ('es' o 'qu')

    Retorna:
        dict con 'results' (lista), 'total' (int), 'filters' (dict aplicados)
    """
    results = []
    applied_filters = {}

    for key, tramite in KB.items():
        lang_data = tramite.get(lang, tramite.get("es", {}))
        if not lang_data:
            continue

        name = lang_data.get("n", "")
        desc = lang_data.get("d", "")
        dep = lang_data.get("dep", "")
        price_str = lang_data.get("c", "")
        time_str = lang_data.get("t", "")
        icon = lang_data.get("icon", "")
        requirements = lang_data.get("que_necesito", [])
        steps = lang_data.get("como", [])

        # Filtro por texto libre
        if query:
            query_lower = query.lower()
            searchable = " ".join([
                name, desc, dep, price_str, time_str,
                " ".join(requirements) if requirements else "",
                " ".join(steps) if steps else ""
            ]).lower()
            if query_lower not in searchable:
                continue

        # Filtro por precio
        if min_price is not None or max_price is not None:
            p_min, p_max = _extract_price_number(price_str)
            if p_min is None:
                continue
            if min_price is not None and p_max < min_price:
                continue
            if max_price is not None and p_min > max_price:
                continue

        # Filtro por tiempo maximo
        if max_days is not None:
            days = _extract_days(time_str)
            if days is not None and days > max_days:
                continue

        # Filtro por departamento
        if department:
            if department.lower() not in dep.lower():
                continue

        # Filtro por categoria
        if category:
            cat_lower = category.lower()
            searchable = (name + " " + desc).lower()
            cat_keywords = {
                "identidad": ["carnet", "identidad", "cedula", "segip"],
                "construccion": ["construccion", "permiso", "plano", "vivienda", "obra"],
                "propiedad": ["propiedad", "registro", "derechos reales", "predial"],
                "transito": ["vehiculo", "conducir", "licencia", "transito"],
                "negocio": ["funcionamiento", "licencia", "negocio", "comercio"],
                "servicios": ["agua", "servicio", "conexion"],
                "eventos": ["evento", "permiso", "fiesta"],
                "certificados": ["constancia", "certificado", "solteria", "conducta", "no deuda"],
                "urbanismo": ["urbanismo", "uso de suelo", "verja", "ampliacion", "horizontal"],
            }
            keywords = cat_keywords.get(cat_lower, [cat_lower])
            if not any(kw in searchable for kw in keywords):
                continue

        result = {
            "id": key,
            "icon": icon,
            "name": name,
            "description": desc,
            "department": dep,
            "cost": price_str,
            "time": time_str,
            "requirements": requirements or [],
            "steps": steps or [],
        }
        results.append(result)

        if query and query not in applied_filters:
            applied_filters["query"] = query
        if min_price is not None:
            applied_filters["min_price"] = min_price
        if max_price is not None:
            applied_filters["max_price"] = max_price
        if max_days is not None:
            applied_filters["max_days"] = max_days
        if department:
            applied_filters["department"] = department
        if category:
            applied_filters["category"] = category

    return {
        "results": results,
        "total": len(results),
        "filters": applied_filters
    }


def get_search_suggestions():
    """Retorna sugerencias de busqueda predefinidas para el usuario."""
    return {
        "categories": [
            {"id": "identidad", "name": "Documentos de Identidad", "icon": "🪪"},
            {"id": "construccion", "name": "Construcción y Vivienda", "icon": "🏗️"},
            {"id": "propiedad", "name": "Propiedad e Inmuebles", "icon": "🏠"},
            {"id": "transito", "name": "Tránsito y Vehículos", "icon": "🚗"},
            {"id": "negocio", "name": "Negocios y Licencias", "icon": "🏪"},
            {"id": "servicios", "name": "Servicios Públicos", "icon": "💧"},
            {"id": "certificados", "name": "Certificados y Constancias", "icon": "✅"},
            {"id": "urbanismo", "name": "Urbanismo", "icon": "🏛️"},
        ],
        "price_ranges": [
            {"label": "Gratuito o muy barato", "min": 0, "max": 15},
            {"label": "Económico (15-50 Bs.)", "min": 15, "max": 50},
            {"label": "Moderado (50-100 Bs.)", "min": 50, "max": 100},
            {"label": "Alto (más de 100 Bs.)", "min": 100, "max": None},
        ],
        "time_ranges": [
            {"label": "Inmediato (mismo día)", "max_days": 0},
            {"label": "Rápido (1-3 días)", "max_days": 3},
            {"label": "Normal (1-2 semanas)", "max_days": 14},
            {"label": "Largo (más de 2 semanas)", "max_days": None},
        ],
        "departments": [
            "SEGIP",
            "Registro Civil",
            "Urbanismo",
            "Catastro",
            "Derechos Reales",
            "Ingresos y Servicios",
            "Seguridad Ciudadana",
            "Transito",
            "Policia (FELCC)",
            "Empresa de Agua",
            "Rentas Internas",
        ],
        "popular_searches": [
            "carnet de identidad",
            "licencia de conducir",
            "certificado de conducta",
            "funcionamiento",
            "constancia de residencia",
            "impuestos prediales",
        ]
    }


# =====================================================================
# GOOGLE MAPS - UBICACIONES DE OFICINAS MUNICIPALES
# =====================================================================

MUNICIPAL_OFFICES = {
    "municipalidad": {
        "name": "Gobierno Autónomo Municipal de Sacaba",
        "address": "Plaza Principal S/N, Sacaba, Cochabamba",
        "lat": -17.3952,
        "lng": -66.0425,
        "phone": "4-4701677",
        "hours": "Lun-Vie 8:00-12:00 / 14:00-18:00",
        "google_maps_url": "https://maps.app.goo.gl/GAMSacaba",
        "description": "Sede principal del gobierno municipal de Sacaba",
    },
    "segip": {
        "name": "SEGIP - Servicio General de Identificación Personal",
        "address": "Sacaba, Cochabamba",
        "lat": -17.3960,
        "lng": -66.0430,
        "phone": "",
        "hours": "Lun-Vie 8:00-12:00 / 14:00-18:00",
        "google_maps_url": "https://maps.app.goo.gl/f27gLh5Accp2UmKW9",
        "description": "Oficina del SEGIP para trámites de cédula de identidad",
    },
    "registro_civil": {
        "name": "Registro Civil - Municipalidad de Sacaba",
        "address": "Plaza Principal, Sacaba, Cochabamba",
        "lat": -17.3950,
        "lng": -66.0420,
        "phone": "",
        "hours": "Lun-Vie 8:00-12:00 / 14:00-18:00",
        "google_maps_url": "",
        "description": "Oficina del Registro Civil para certificados de nacimiento, matrimonio y defunción",
    },
    "urbanismo": {
        "name": "Dirección de Urbanismo - Municipalidad de Sacaba",
        "address": "Consistorial S-002, Sacaba, Cochabamba",
        "lat": -17.3948,
        "lng": -66.0418,
        "phone": "",
        "hours": "Lun-Vie 8:00-12:00 / 14:00-18:00",
        "google_maps_url": "",
        "description": "Dirección de Urbanismo para permisos de construcción y planos",
    },
    "catastro": {
        "name": "Unidad de Catastro - Municipalidad de Sacaba",
        "address": "Consistorial, Sacaba, Cochabamba",
        "lat": -17.3955,
        "lng": -66.0422,
        "phone": "",
        "hours": "Lun-Vie 8:00-12:00 / 14:00-18:00",
        "google_maps_url": "",
        "description": "Unidad de Catastro para empadronamiento y certificados catastrales",
    },
    "derechos_reales": {
        "name": "Dirección de Derechos Reales",
        "address": "Sacaba, Cochabamba",
        "lat": -17.3958,
        "lng": -66.0428,
        "phone": "",
        "hours": "Lun-Vie 8:00-12:00 / 14:00-18:00",
        "google_maps_url": "",
        "description": "Dirección de Derechos Reales para registro de propiedades",
    },
    "ingresos": {
        "name": "Dirección de Ingresos y Servicios Municipales",
        "address": "Municipalidad de Sacaba",
        "lat": -17.3953,
        "lng": -66.0426,
        "phone": "",
        "hours": "Lun-Vie 8:00-12:00 / 14:00-18:00",
        "google_maps_url": "",
        "description": "Dirección de Ingresos para licencias de funcionamiento",
    },
    "seguridad": {
        "name": "Dirección de Seguridad Ciudadana",
        "address": "Sacaba, Cochabamba",
        "lat": -17.3945,
        "lng": -66.0415,
        "phone": "",
        "hours": "Lun-Vie 8:00-12:00 / 14:00-18:00",
        "google_maps_url": "",
        "description": "Dirección de Seguridad Ciudadana para permisos de eventos",
    },
    "transito": {
        "name": "Dirección de Tránsito y Transporte",
        "address": "Sacaba, Cochabamba",
        "lat": -17.3942,
        "lng": -66.0412,
        "phone": "",
        "hours": "Lun-Vie 8:00-12:00 / 14:00-18:00",
        "google_maps_url": "",
        "description": "Dirección de Tránsito para registro de vehículos y licencias",
    },
    "policia": {
        "name": "Policía Boliviana - FELCC",
        "address": "Sacaba, Cochabamba",
        "lat": -17.3940,
        "lng": -66.0410,
        "phone": "",
        "hours": "24 horas",
        "google_maps_url": "",
        "description": "Fuerza Especial de Lucha Contra el Crimen para certificados de conducta",
    },
    "agua": {
        "name": "Empresa de Agua Potable de Sacaba",
        "address": "Sacaba, Cochabamba",
        "lat": -17.3938,
        "lng": -66.0408,
        "phone": "",
        "hours": "Lun-Vie 8:00-12:00 / 14:00-18:00",
        "google_maps_url": "",
        "description": "Empresa de Agua Potable para servicios de conexión",
    },
    "rentas": {
        "name": "Dirección de Rentas Internas",
        "address": "Municipalidad de Sacaba",
        "lat": -17.3951,
        "lng": -66.0424,
        "phone": "",
        "hours": "Lun-Vie 8:00-12:00 / 14:00-18:00",
        "google_maps_url": "",
        "description": "Dirección de Rentas Internas para impuestos y constancias de no deuda",
    },
    "subalcaldia_1": {
        "name": "Subalcaldía de Sacaba Centro",
        "address": "Sacaba Centro, Cochabamba",
        "lat": -17.3950,
        "lng": -66.0420,
        "phone": "",
        "hours": "Lun-Vie 8:00-12:00 / 14:00-18:00",
        "google_maps_url": "",
        "description": "Subalcaldía para trámites municipales de la zona centro",
    },
    "subalcaldia_2": {
        "name": "Subalcaldía de San Pedro",
        "address": "San Pedro, Sacaba, Cochabamba",
        "lat": -17.3880,
        "lng": -66.0350,
        "phone": "",
        "hours": "Lun-Vie 8:00-12:00 / 14:00-18:00",
        "google_maps_url": "",
        "description": "Subalcaldía para trámites municipales de San Pedro",
    },
}


def get_office_location(office_key):
    """Obtiene la información de ubicación de una oficina municipal.

    Args:
        office_key: clave de la oficina (municipalidad, segip, etc.)

    Returns:
        dict con información de ubicación o None si no existe
    """
    office = MUNICIPAL_OFFICES.get(office_key)
    if not office:
        return None
    return office


def search_offices(query=None):
    """Busca oficinas municipales por nombre o descripción.

    Args:
        query: texto de búsqueda

    Returns:
        lista de oficinas encontradas
    """
    if not query:
        return list(MUNICIPAL_OFFICES.values())

    query_lower = query.lower()
    results = []
    for key, office in MUNICIPAL_OFFICES.items():
        searchable = f"{office['name']} {office['description']} {office['address']}".lower()
        if query_lower in searchable:
            results.append({**office, "key": key})
    return results


def get_all_offices():
    """Retorna todas las oficinas municipales disponibles."""
    return MUNICIPAL_OFFICES


def get_directions(from_lat, from_lng, to_office_key):
    """Genera URL de OpenStreetMap para obtener direcciones.

    Args:
        from_lat: latitud de origen
        from_lng: longitud de origen
        to_office_key: clave de la oficina destino

    Returns:
        dict con URL de direcciones o None
    """
    office = MUNICIPAL_OFFICES.get(to_office_key)
    if not office:
        return None

    # URL de OpenStreetMap con ruta
    directions_url = (
        f"https://www.openstreetmap.org/directions?"
        f"engine=fossgis_osrm_car&route={from_lat},{from_lng}"
        f";{office['lat']},{office['lng']}"
    )

    # URL para ver en el mapa
    map_url = (
        f"https://www.openstreetmap.org/?mlat={office['lat']}"
        f"&mlon={office['lng']}&zoom=17"
    )

    return {
        "office": office["name"],
        "address": office["address"],
        "directions_url": directions_url,
        "map_url": map_url,
        "lat": office["lat"],
        "lng": office["lng"],
    }


def geocode_address(address):
    """Convierte una dirección a coordenadas usando Nominatim (OpenStreetMap).

    Args:
        address: dirección a geocodificar

    Returns:
        dict con lat, lng y dirección formateada o None
    """
    import requests as _req

    try:
        url = f"{NOMINATIM_URL}/search"
        params = {
            "q": address,
            "format": "json",
            "limit": 1,
            "countrycodes": "bo",
        }
        headers = {"User-Agent": "ChatbotSacaba/1.0"}
        resp = _req.get(url, params=params, headers=headers, timeout=10)

        if resp.status_code == 200:
            data = resp.json()
            if data:
                return {
                    "lat": float(data[0]["lat"]),
                    "lng": float(data[0]["lon"]),
                    "display_name": data[0].get("display_name", address),
                }
    except Exception:
        pass
    return None


def reverse_geocode(lat, lng):
    """Convierte coordenadas a dirección usando Nominatim (OpenStreetMap).

    Args:
        lat: latitud
        lng: longitud

    Returns:
        dict con dirección formateada o None
    """
    import requests as _req

    try:
        url = f"{NOMINATIM_URL}/reverse"
        params = {
            "lat": lat,
            "lon": lng,
            "format": "json",
        }
        headers = {"User-Agent": "ChatbotSacaba/1.0"}
        resp = _req.get(url, params=params, headers=headers, timeout=10)

        if resp.status_code == 200:
            data = resp.json()
            if data:
                return {
                    "address": data.get("display_name", ""),
                    "lat": lat,
                    "lng": lng,
                }
    except Exception:
        pass
    return None


def get_nearby_places(lat, lng, radius=2000):
    """Busca oficinas cercanas a una ubicación.

    Args:
        lat: latitud
        lng: longitud
        radius: radio en metros (default 2000)

    Returns:
        lista de oficinas cercanas ordenadas por distancia
    """
    nearby = []
    for key, office in MUNICIPAL_OFFICES.items():
        # Calcular distancia aproximada (fórmula de Haversine simplificada)
        lat_diff = abs(office["lat"] - lat)
        lng_diff = abs(office["lng"] - lng)
        distance = ((lat_diff ** 2 + lng_diff ** 2) ** 0.5) * 111000

        if distance <= radius:
            nearby.append({
                "key": key,
                "name": office["name"],
                "address": office["address"],
                "distance_meters": round(distance),
                "lat": office["lat"],
                "lng": office["lng"],
                "map_url": f"https://www.openstreetmap.org/?mlat={office['lat']}&mlon={office['lng']}&zoom=17",
            })

    nearby.sort(key=lambda x: x["distance_meters"])
    return nearby


def generate_map_embed(office_key, zoom=17):
    """Genera código HTML para embeber un mapa de OpenStreetMap.

    Args:
        office_key: clave de la oficina
        zoom: nivel de zoom (default 17)

    Returns:
        dict con información del mapa o None
    """
    office = MUNICIPAL_OFFICES.get(office_key)
    if not office:
        return None

    # URL del mapa embebido de OpenStreetMap
    embed_url = (
        f"https://www.openstreetmap.org/export/embed.html?"
        f"bbox={office['lng']-0.01},{office['lat']-0.01},"
        f"{office['lng']+0.01},{office['lat']+0.01}"
        f"&layer=mapnik&marker={office['lat']},{office['lng']}"
    )

    # URL para abrir en nueva pestaña
    full_url = (
        f"https://www.openstreetmap.org/?mlat={office['lat']}"
        f"&mlon={office['lng']}&zoom={zoom}"
    )

    return {
        "office": office["name"],
        "embed_url": embed_url,
        "full_url": full_url,
        "lat": office["lat"],
        "lng": office["lng"],
        "zoom": zoom,
    }


def search_nearby_osm(lat, lng, query="", radius=1000):
    """Busca lugares cercanos usando Overpass API de OpenStreetMap.

    Args:
        lat: latitud
        lng: longitud
        query: término de búsqueda (opcional)
        radius: radio en metros

    Returns:
        lista de lugares encontrados
    """
    import requests as _req

    try:
        # Overpass API para buscar lugares cercanos
        overpass_url = "https://overpass-api.de/api/interpreter"
        overpass_query = f"""
        [out:json][timeout:10];
        (
          node["amenity"](around:{radius},{lat},{lng});
          way["amenity"](around:{radius},{lat},{lng});
        );
        out center;
        """

        resp = _req.post(overpass_url, data={"data": overpass_query}, timeout=15)

        if resp.status_code == 200:
            data = resp.json()
            places = []
            for element in data.get("elements", [])[:20]:
                tags = element.get("tags", {})
                name = tags.get("name", tags.get("amenity", "Sin nombre"))
                place_lat = element.get("lat", element.get("center", {}).get("lat"))
                place_lng = element.get("lon", element.get("center", {}).get("lon"))

                if place_lat and place_lng:
                    places.append({
                        "name": name,
                        "type": tags.get("amenity", "unknown"),
                        "lat": place_lat,
                        "lng": place_lng,
                        "address": tags.get("addr:street", ""),
                    })
            return places
    except Exception:
        pass
    return []


# =====================================================================
# GLOSBLE DICTIONARY API - DICCIONARIO GRATUITO ES <-> QU
# =====================================================================

# Base de datos local de palabras comunes en quechua (respaldo)
QUECHUA_LOCAL_DB = {
    # Saludos y cortesía
    "hola": {"qu": "Allianchu", "example": "Allianchu, ¿iman allinchu?"},
    "buenos días": {"qu": "Allian puncha", "example": "Allian puncha, ¿imate kachkanki?"},
    "buenas tardes": {"qu": "Allian tuta", "example": "Allian tuta, ¿iman allinchu?"},
    "buenas noches": {"qu": "Allian p'unchay", "example": "Allian p'unchay, txin mast'anki."},
    "gracias": {"qu": "Sulpayki", "example": "Sulpayki, imaynallan."},
    "por favor": {"qu": "Ama hina llachiy", "example": "Ama hina llachiy, yutchhuy."},
    "adiós": {"qu": "Tupananchiskama", "example": "Tupananchiskama, ¡huk p'unchayta sumaqta!"},
    "por favor": {"qu": "Ama hina llachiy", "example": "Ama hina llachiy, yutchhuy."},
    "perdón": {"qu": "Pampachay", "example": "Pampachay, ama hina llachiy."},
    
    # Números
    "uno": {"qu": "Huk", "example": "Huk watukuna."},
    "dos": {"qu": "Ishkay", "example": "Ishkay maki."},
    "tres": {"qu": "Kimsa", "example": "Kimsa p'unchay."},
    "cuatro": {"qu": "Tawa", "example": "Tawa panda."},
    "cinco": {"qu": "Pichqa", "example": "Pichqa chunka."},
    "seis": {"qu": "Suqta", "example": "Suqta maranakuna."},
    "siete": {"qu": "Qanchis", "example": "Qanchis p'unchay."},
    "ocho": {"qu": "Pusaq", "example": "Pusaq maki."},
    "nueve": {"qu": "Isqun", "example": "Isqun p'unchay."},
    "diez": {"qu": "Chunka", "example": "Chunka maki."},
    
    # Familia
    "madre": {"qu": "Mama", "example": "Mamayqa sumaqmi kachkan."},
    "padre": {"qu": "Tayta", "example": "Taytaq llamkachkan."},
    "hermano": {"qu": "Wawqi", "example": "Wawqiyqa urmaqmi."},
    "hermana": {"qu": "Panay", "example": "Panayqa urmaqmi."},
    "hijo": {"qu": "Wawa", "example": "Wawawa yurinchu."},
    "hija": {"qu": "Wawa", "example": "Wawawa yurinchu."},
    "esposo": {"qu": "Aycha", "example": "Aychayqa llamkachkan."},
    "esposa": {"qu": "Ayllu", "example": "Aylluypi tukuy tiyan."},
    
    # Trámites y documentos
    "carnet": {"qu": "Carnet", "example": "Carnet de identidad mañakuy."},
    "trámite": {"qu": "Trámite", "example": "Trámite tukuchiy."},
    "documento": {"qu": "Documento", "example": "Documento riqsichiyninchik."},
    "certificado": {"qu": "Certificado", "example": "Certificado mañakuy."},
    "constancia": {"qu": "Constancia", "example": "Constancia de residencia."},
    "licencia": {"qu": "Licencia", "example": "Licencia de conducir."},
    "permiso": {"qu": "Permiso", "example": "Permiso de construcción."},
    "pago": {"qu": "Pago", "example": "Pago ruway."},
    "costo": {"qu": "Costo", "example": "¿Ima chay costo?"},
    "precio": {"qu": "Chanin", "example": "¿Ima chaninchu?"},
    
    # Ubicaciones
    "municipalidad": {"qu": "Municipalidad", "example": "Municipalidadman riy."},
    "oficina": {"qu": "Oficina", "example": "Oficinapi tukuchiy."},
    "dirección": {"qu": "Dirección", "example": "Dirección maskay."},
    "ubicación": {"qu": "Maypi", "example": "¿Maypi tiyan?"},
    "direcciones": {"qu": "Maypi", "example": "¿Maypi tiyan?"},
    
    # Tiempo
    "hoy": {"qu": "Kunan p'unchay", "example": "Kunan p'unchay tukuchiy."},
    "mañana": {"qu": "Paqarin", "example": "Paqarin riy."},
    "ayer": {"qu": "Paqarina", "example": "Paqarinami ruarqani."},
    "tarde": {"qu": "Tuta", "example": "Tutapi ruway."},
    "temprano": {"qu": "Mushuk", "example": "Mushukta riy."},
    "siempre": {"qu": "Wiñaypaq", "example": "Wiñaypaq tiyan."},
    "nunca": {"qu": "Mana wiñaypaq", "example": "Mana wiñaypaq ruwani."},
    
    # Preguntas
    "¿cómo?": {"qu": "Imaynallan", "example": "¿Imaynallan ruway?"},
    "¿dónde?": {"qu": "Maypi", "example": "¿Maypi tiyan?"},
    "¿cuándo?": {"qu": "Ima p'unchay", "example": "¿Ima p'unchay ruway?"},
    "¿cuánto?": {"qu": "Ima chay", "example": "¿Ima chay chaninchu?"},
    "¿qué?": {"qu": "Ima", "example": "¿Ima ruwayki?"},
    "¿quién?": {"qu": "Ayllu", "example": "Ayllu ruwasqan?"},
    
    # Acciones
    "ir": {"qu": "Riy", "example": "Oficinaman riy."},
    "venir": {"qu": "Hamuy", "example": "Hamuy, ñuqapaq."},
    "hacer": {"qu": "Ruway", "example": "Trámite ruway."},
    "buscar": {"qu": "Maskay", "example": "Dirección maskay."},
    "pagar": {"qu": "Pagay", "example": "Chayta pagay."},
    "esperar": {"qu": "Suyay", "example": "Chayta suyay."},
    "hablar": {"qu": "Arinay", "example": "Quechuapi arinay."},
    "entender": {"qu": "Uyarikuy", "example": "¡Uyarikuyki!"},
    
    # Trámites específicos
    "identidad": {"qu": "Identidad", "example": "Identidad documento."},
    "construcción": {"qu": "Construcción", "example": "Construcción permiso."},
    "propiedad": {"qu": "Propiedad", "example": "Propiedad registro."},
    "vehículo": {"qu": "Vehículo", "example": "Vehículo registro."},
    "agua": {"qu": "Yaku", "example": "Yaku servicio."},
    "impuesto": {"qu": "Impuesto", "example": "Impuesto predial."},
    "multa": {"qu": "Multa", "example": "Multa de tránsito."},
    
    # Departamentos
    "segip": {"qu": "SEGIP", "example": "SEGIP oficinaman riy."},
    "registro civil": {"qu": "Registro Civil", "example": "Registro Civil man riy."},
    "urbanismo": {"qu": "Urbanismo", "example": "Urbanismo oficinaman riy."},
    "catastro": {"qu": "Catastro", "example": "Catastro oficinaman riy."},
    
    # Frases comunes del chatbot
    "¿en qué puedo ayudarle?": {"qu": "¿Imatanpas ruwayki?", "example": "¿Imatanpas ruwayki? Ñuqapaq yanapaway."},
    "¿cómo estás?": {"qu": "¿Iman allinchu?", "example": "Allianchu, ¿iman allinchu?"},
    "bien": {"qu": "Allin", "example": "Allinmi kachkani."},
    "mal": {"qu": "Mana allin", "example": "Mana allinmi."},
}


def translate_word(word, source_lang="es", target_lang="qu"):
    """Traduce una palabra usando Glosbe Dictionary API.

    Args:
        word: palabra a traducir
        source_lang: idioma fuente (es, qu)
        target_lang: idioma destino (es, qu)

    Returns:
        dict con traducción y ejemplos o None
    """
    import requests as _req

    # Primero buscar en la base local
    word_lower = word.lower().strip()
    if source_lang == "es" and word_lower in QUECHUA_LOCAL_DB:
        data = QUECHUA_LOCAL_DB[word_lower]
        return {
            "word": word,
            "translation": data["qu"],
            "source_lang": source_lang,
            "target_lang": target_lang,
            "examples": [data.get("example", "")],
            "source": "local",
        }

    # Intentar con Glosbe API
    try:
        url = f"{GLOSBLE_API_URL}/translate"
        params = {
            "from": source_lang,
            "dest": target_lang,
            "phrase": word,
            "format": "json",
        }
        headers = {"User-Agent": "ChatbotSacaba/1.0"}
        resp = _req.get(url, params=params, headers=headers, timeout=10)

        if resp.status_code == 200:
            data = resp.json()
            translations = []
            examples = []

            # Extraer traducciones
            if "tuc" in data:
                for item in data["tuc"][:5]:
                    if "phrase" in item:
                        translations.append(item["phrase"]["text"])

            # Extraer ejemplos
            if "examples" in data:
                for ex in data["examples"][:3]:
                    if "text" in ex:
                        examples.append(ex["text"])

            if translations:
                return {
                    "word": word,
                    "translation": translations[0],
                    "all_translations": translations,
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                    "examples": examples,
                    "source": "glosbe",
                }
    except Exception:
        pass

    # Si no se encuentra, retornar None
    return None


def search_quechua_dictionary(query):
    """Busca palabras en quechua en el diccionario local.

    Args:
        query: término de búsqueda

    Returns:
        lista de resultados encontrados
    """
    query_lower = query.lower().strip()
    results = []

    for es_word, data in QUECHUA_LOCAL_DB.items():
        qu_word = data["qu"].lower()
        # Buscar en español o en quechua
        if query_lower in es_word or query_lower in qu_word:
            results.append({
                "spanish": es_word,
                "quechua": data["qu"],
                "example": data.get("example", ""),
            })

    return results


def get_quechua_phrases(category="common"):
    """Retorna frases comunes en quechua por categoría.

    Args:
        category: categoría (common, greetings, numbers, tramites, locations)

    Returns:
        lista de frases
    """
    categories = {
        "common": [
            {"es": "Hola", "qu": "Allianchu"},
            {"es": "Gracias", "qu": "Sulpayki"},
            {"es": "Por favor", "qu": "Ama hina llachiy"},
            {"es": "Adiós", "qu": "Tupananchiskama"},
            {"es": "¿Cómo estás?", "qu": "¿Iman allinchu?"},
            {"es": "Bien", "qu": "Allin"},
            {"es": "Mal", "qu": "Mana allin"},
            {"es": "Perdón", "qu": "Pampachay"},
        ],
        "greetings": [
            {"es": "Buenos días", "qu": "Allian puncha"},
            {"es": "Buenas tardes", "qu": "Allian tuta"},
            {"es": "Buenas noches", "qu": "Allian p'unchay"},
            {"es": "¿Qué tal?", "qu": "¿Iman allinchu?"},
            {"es": "¿Cómo te va?", "qu": "¿Iman kaniki?"},
        ],
        "numbers": [
            {"es": "Uno", "qu": "Huk"},
            {"es": "Dos", "qu": "Ishkay"},
            {"es": "Tres", "qu": "Kimsa"},
            {"es": "Cuatro", "qu": "Tawa"},
            {"es": "Cinco", "qu": "Pichqa"},
            {"es": "Seis", "qu": "Suqta"},
            {"es": "Siete", "qu": "Qanchis"},
            {"es": "Ocho", "qu": "Pusaq"},
            {"es": "Nueve", "qu": "Isqun"},
            {"es": "Diez", "qu": "Chunka"},
        ],
        "tramites": [
            {"es": "Trámite", "qu": "Trámite"},
            {"es": "Documento", "qu": "Documento"},
            {"es": "Certificado", "qu": "Certificado"},
            {"es": "Permiso", "qu": "Permiso"},
            {"es": "Licencia", "qu": "Licencia"},
            {"es": "Pago", "qu": "Pago"},
            {"es": "Costo", "qu": "Costo"},
            {"es": "Requisitos", "qu": "Requisitos"},
        ],
        "locations": [
            {"es": "Municipalidad", "qu": "Municipalidad"},
            {"es": "Oficina", "qu": "Oficina"},
            {"es": "¿Dónde está?", "qu": "¿Maypi tiyan?"},
            {"es": "Dirección", "qu": "Dirección"},
            {"es": "Ubicación", "qu": "Maypi"},
        ],
        "time": [
            {"es": "Hoy", "qu": "Kunan p'unchay"},
            {"es": "Mañana", "qu": "Paqarin"},
            {"es": "Ayer", "qu": "Paqarina"},
            {"es": "Siempre", "qu": "Wiñaypaq"},
            {"es": "Nunca", "qu": "Mana wiñaypaq"},
            {"es": "¿Cuándo?", "qu": "¿Ima p'unchay?"},
        ],
    }

    return categories.get(category, categories["common"])


def learn_quechua_word(es_word, qu_word, example=""):
    """Añade una nueva palabra al diccionario local de quechua.

    Args:
        es_word: palabra en español
        qu_word: traducción en quechua
        example: ejemplo de uso (opcional)

    Returns:
        dict con la palabra guardada
    """
    es_lower = es_word.lower().strip()
    QUECHUA_LOCAL_DB[es_lower] = {
        "qu": qu_word.strip(),
        "example": example if example else f"{es_word} = {qu_word}",
    }
    return {
        "word": es_lower,
        "translation": qu_word,
        "example": QUECHUA_LOCAL_DB[es_lower]["example"],
        "status": "learned",
    }


# =====================================================================
# GOOGLE GEMINI API - IA GRATUITA PARA QUECHUA
# =====================================================================

def _get_gemini_client():
    """Crea un cliente de Google Gemini API."""
    if not GEMINI_AVAILABLE:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        return genai
    except ImportError:
        return None


def gemini_chat(message, language="es", context=None):
    """Envía un mensaje a Google Gemini y retorna la respuesta.

    Args:
        message: mensaje del usuario
        language: idioma del usuario (es/qu)
        context: contexto adicional (opcional)

    Returns:
        dict con la respuesta o error
    """
    if not GEMINI_AVAILABLE:
        return {
            "success": False,
            "error": "Google Gemini API no configurada.",
            "fallback": True,
        }

    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(GEMINI_MODEL)

        # System prompt para el chatbot municipal
        system_prompt = """Eres el asistente virtual del Gobierno Autónomo Municipal de Sacaba, Bolivia. 
Tu función es ayudar a los ciudadanos con información sobre:
- Trámites municipales (25 tipos: carnet, licencias, permisos, certificados, etc.)
- Multas de tránsito y municipales
- Horarios y ubicación de oficinas
- Requisitos y costos de cada trámite

Reglas:
1. Responde en el idioma del usuario (español o quechua)
2. Sé conciso y claro
3. Si no sabes algo, di "No tengo esa información, contacta al 4-4701677"
4. Para trámites, menciona: nombre, costo, tiempo y requisitos
5. Horario de atención: Lun-Vie 8:00-12:00 / 14:00-18:00
6. Teléfono: 4-4701677
7. Si el usuario escribe en quechua, responde en quechua"""

        if language == "qu":
            system_prompt += "\n8. El usuario habla quechua boliviano (runasimi). Responde en quechua."

        # Construir el contenido
        full_prompt = f"{system_prompt}\n\nUsuario: {message}"

        if context:
            full_prompt = f"{context}\n\n{full_prompt}"

        response = model.generate_content(full_prompt)

        if response.text:
            return {
                "success": True,
                "response": response.text.strip(),
                "model": GEMINI_MODEL,
                "language": language,
                "source": "gemini",
            }
        else:
            return {
                "success": False,
                "error": "Gemini no retornó respuesta.",
                "fallback": True,
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "fallback": True,
        }


def gemini_translate(text, source_lang="es", target_lang="qu"):
    """Traduce texto usando Google Gemini.

    Args:
        text: texto a traducir
        source_lang: idioma fuente
        target_lang: idioma destino

    Returns:
        dict con la traducción
    """
    if not GEMINI_AVAILABLE:
        return {"success": False, "error": "Gemini API no disponible."}

    lang_names = {"es": "español", "qu": "quechua boliviano"}
    source_name = lang_names.get(source_lang, source_lang)
    target_name = lang_names.get(target_lang, target_lang)

    prompt = f"""Traduce el siguiente texto de {source_name} a {target_name}.
Reglas:
- Preserva el formato (negritas, listas, etc.)
- Usa quechua boliviano natural (runasimi de Cochabamba/Sacaba)
- No agregues ni omitas información
- Responde SOLO con la traducción, sin explicaciones

Texto: {text}"""

    result = gemini_chat(prompt, target_lang)
    if result.get("success"):
        return {
            "success": True,
            "translation": result["response"],
            "source_lang": source_lang,
            "target_lang": target_lang,
        }
    return result


def gemini_quechua_tutor(word_or_phrase, language="es"):
    """Usa Gemini como tutor de quechua.

    Args:
        word_or_phrase: palabra o frase en español o quechua
        language: idioma del usuario

    Returns:
        dict con información educativa
    """
    if not GEMINI_AVAILABLE:
        return {"success": False, "error": "Gemini API no disponible."}

    prompt = f"""Eres un profesor de quechua boliviano (runasimi) de Sacaba, Bolivia.
El usuario pregunta sobre: "{word_or_phrase}"

Proporciona:
1. La traducción al quechua boliviano
2. Pronunciación (fonética)
3. Ejemplo de uso en una oración
4. Contexto cultural si aplica

Responde en el idioma del usuario ({language}). Sé breve y didáctico."""

    result = gemini_chat(prompt, language)
    if result.get("success"):
        return {
            "success": True,
            "lesson": result["response"],
            "word": word_or_phrase,
            "source": "gemini_tutor",
        }
    return result


def gemini_analyze_tramite(tramite_name):
    """Analiza un trámite usando Gemini para dar información detallada.

    Args:
        tramite_name: nombre del trámite

    Returns:
        dict con análisis del trámite
    """
    # Buscar en la KB local primero
    tramite_key = detect_tramite(tramite_name)
    if tramite_key and tramite_key in KB:
        t = KB[tramite_key]["es"]
        return {
            "success": True,
            "source": "kb_local",
            "data": {
                "name": t["n"],
                "cost": t["c"],
                "time": t["t"],
                "department": t["dep"],
                "requirements": t["que_necesito"],
                "steps": t["como"],
            }
        }

    # Si no está en la KB, usar Gemini
    if not GEMINI_AVAILABLE:
        return {"success": False, "error": "Trámite no encontrado y Gemini no disponible."}

    prompt = f"""Información sobre el trámite municipal "{tramite_name}" en Sacaba, Bolivia.

Responde en formato JSON con:
{{
  "name": "nombre del trámite",
  "description": "descripción breve",
  "cost": "costo estimado",
  "time": "tiempo estimado",
  "department": "departamento responsable",
  "requirements": ["requisito1", "requisito2"],
  "steps": ["paso1", "paso2"],
  "tips": "consejos"
}}

Si no tienes información específica de Sacaba, indica que contacte al 4-4701677."""

    result = gemini_chat(prompt, "es")
    if result.get("success"):
        try:
            import json
            data = json.loads(result["response"])
            return {"success": True, "source": "gemini", "data": data}
        except Exception:
            return {"success": True, "source": "gemini", "data": result["response"]}
    return result


def is_gemini_available():
    """Verifica si Google Gemini API está disponible."""
    return GEMINI_AVAILABLE


def get_gemini_status():
    """Retorna el estado de la API de Gemini."""
    return {
        "available": GEMINI_AVAILABLE,
        "model": GEMINI_MODEL,
        "key_configured": bool(GEMINI_API_KEY),
        "free_tier": "15 requests/min, 1M tokens/day",
    }
