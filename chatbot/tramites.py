# -*- coding: utf-8 -*-
"""Fichas detalladas de los trámites del portal de Sacaba.

Cada ficha alimenta el artículo que se muestra a la derecha del chat.
La información municipal proviene del portal oficial sacaba.gob.bo
(90 trámites, decretos 014/2024 y 015/2024) y de las entidades
responsables (SEGIP, Policía Boliviana/DNFR, Registro Civil, RUAT).
Los montos marcados como referenciales deben confirmarse en ventanilla.
"""

from urllib.parse import quote_plus
import json
import os
from pathlib import Path

from . import tramites_qu

CAMPOS_EDITABLES = (
    'costo', 'tiempo', 'modalidad', 'resumen',
    'oficina_nombre', 'oficina_direccion', 'horario_dias', 'horario_horas',
)
_CACHE_OVERRIDES = {'mtime': None, 'datos': {}}


def ruta_overrides():
    personalizada = os.environ.get('SACABA_TRAMITES_FILE')
    if personalizada:
        return Path(personalizada)
    return Path(__file__).resolve().parent.parent / 'data' / 'tramites_override.json'


def overrides():
    """Cambios guardados por funcionarios desde el panel administrativo."""
    ruta = ruta_overrides()
    try:
        mtime = ruta.stat().st_mtime
    except OSError:
        return {}
    if _CACHE_OVERRIDES['mtime'] == mtime:
        return _CACHE_OVERRIDES['datos']
    try:
        datos = json.loads(ruta.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        datos = {}
    if not isinstance(datos, dict):
        datos = {}
    _CACHE_OVERRIDES['mtime'] = mtime
    _CACHE_OVERRIDES['datos'] = datos
    return datos


def _con_quechua(ficha):
    extra = tramites_qu.CONTENIDO.get(ficha.get('id'))
    if not extra:
        return ficha
    resultado = dict(ficha)
    qu = dict(ficha.get('qu') or {})
    qu.update(extra)
    resultado['qu'] = qu
    return resultado


def _aplicar_overrides(ficha):
    if not ficha:
        return ficha
    return _con_quechua(_aplicar_overrides_propios(ficha))


def _aplicar_overrides_propios(ficha):
    extra = overrides().get(ficha.get('id'))
    if not extra:
        return ficha
    resultado = dict(ficha)
    for campo in ('costo', 'tiempo', 'modalidad', 'resumen'):
        if extra.get(campo):
            resultado[campo] = extra[campo]
    if extra.get('requisitos'):
        resultado['requisitos'] = list(extra['requisitos'])
    oficina = dict(ficha.get('oficina') or {})
    if extra.get('oficina_nombre'):
        oficina['nombre'] = extra['oficina_nombre']
    if extra.get('oficina_direccion'):
        oficina['direccion'] = extra['oficina_direccion']
    if oficina:
        resultado['oficina'] = oficina
    if extra.get('horario_dias') or extra.get('horario_horas'):
        horarios = [dict(h) for h in (ficha.get('horarios') or [])]
        if horarios:
            horarios[0]['dias'] = extra.get('horario_dias') or horarios[0].get('dias', '')
            horarios[0]['horas'] = extra.get('horario_horas') or horarios[0].get('horas', '')
        else:
            horarios = [{'dias': extra.get('horario_dias', ''), 'horas': extra.get('horario_horas', '')}]
        resultado['horarios'] = horarios
    return resultado


def guardar_override(ident, datos):
    """Guarda solo los campos informados; vacio significa volver al original."""
    if ident not in TRAMITES:
        return False
    limpio = {}
    for campo in CAMPOS_EDITABLES:
        valor = (datos.get(campo) or '').strip()
        if valor:
            limpio[campo] = valor
    requisitos = [r.strip() for r in (datos.get('requisitos') or '').splitlines() if r.strip()]
    if requisitos:
        limpio['requisitos'] = requisitos

    ruta = ruta_overrides()
    ruta.parent.mkdir(parents=True, exist_ok=True)
    actuales = dict(overrides())
    if limpio:
        actuales[ident] = limpio
    else:
        actuales.pop(ident, None)
    temporal = ruta.with_suffix('.tmp')
    temporal.write_text(json.dumps(actuales, ensure_ascii=False, indent=2), encoding='utf-8')
    os.replace(temporal, ruta)
    _CACHE_OVERRIDES['mtime'] = None
    return True

BASE = 'https://sacaba.gob.bo'
SEGIP = 'https://www.segip.gob.bo'
DNFR = 'https://policiadnfr.gob.bo'
RUAT = 'https://www.ruat.gob.bo'
ESTADO_DIGITAL = 'https://estadodigital.mingobierno.gob.bo/infracciones/home'


def _mapa(consulta):
    return 'https://www.google.com/maps/search/?api=1&query=' + quote_plus(consulta)


OFICINAS = {
    'gam': {
        'nombre': 'Palacio Consistorial de Sacaba',
        'direccion': 'Plaza 6 de Agosto, edificio Consistorial S-002, Sacaba',
        'horario': 'Lun-Vie 8:00-12:00 y 14:00-18:00; Sáb 8:00-12:00',
        'telefono': '4701677',
        'mapa': 'https://maps.app.goo.gl/f27gLh5Accp2UmKW9',
    },
    'catastro': {
        'nombre': 'Unidad de Catastro Multifinalitario',
        'direccion': 'Casa Municipal, Plaza 6 de Agosto, Sacaba',
        'horario': 'Lun-Vie 8:00-12:00 y 14:00-18:00',
        'telefono': '4701677',
        'mapa': _mapa('Gobierno Autónomo Municipal de Sacaba, Cochabamba'),
    },
    'urbanismo': {
        'nombre': 'Dirección de Urbanismo y Gestión Territorial',
        'direccion': 'Casa Municipal, Plaza 6 de Agosto, Sacaba',
        'horario': 'Lun-Vie 8:00-12:00 y 14:00-18:00',
        'telefono': '4701677',
        'mapa': _mapa('Gobierno Autónomo Municipal de Sacaba, Cochabamba'),
    },
    'rentas': {
        'nombre': 'Dirección de Ingresos y Rentas Internas',
        'direccion': 'Caja Central, Palacio Consistorial, Sacaba',
        'horario': 'Lun-Vie 8:00-12:00 y 14:00-18:00',
        'telefono': '4701677',
        'mapa': _mapa('Gobierno Autónomo Municipal de Sacaba, Cochabamba'),
    },
    'segip': {
        'nombre': 'Oficinas del SEGIP (Sacaba / Cochabamba)',
        'direccion': 'Consulta la oficina habilitada más cercana en segip.gob.bo',
        'horario': 'Lun-Vie 8:00-16:00 (verifica la oficina)',
        'telefono': '800 101 102',
        'mapa': 'https://maps.app.goo.gl/f27gLh5Accp2UmKW9',
    },
    'transito': {
        'nombre': 'Tránsito / DNFR - Sacaba',
        'direccion': 'Unidad Operativa de Tránsito de Sacaba (consulta la más cercana)',
        'horario': 'Lun-Vie 8:00-16:00',
        'telefono': '110',
        'mapa': _mapa('Transito Sacaba, Cochabamba, Bolivia'),
    },
    'policia': {
        'nombre': 'FELCC / Policía Boliviana - Sacaba',
        'direccion': 'Estación Policial de Sacaba (consulta la más cercana)',
        'horario': 'Lun-Vie 8:00-18:00',
        'telefono': '110',
        'mapa': _mapa('Estacion Policial Sacaba, Cochabamba, Bolivia'),
    },
    'registro': {
        'nombre': 'Registro Civil - Sacaba',
        'direccion': 'Oficina del Registro Civil, Plaza 6 de Agosto, Sacaba',
        'horario': 'Lun-Vie 8:00-12:00 y 14:00-18:00',
        'telefono': '4701677',
        'mapa': _mapa('Registro Civil Sacaba, Cochabamba, Bolivia'),
    },
}

CATEGORIES = {
    'identidad': {'nombre': 'Identidad y documentos', 'icono': 'id-card', 'color': '#0f766e'},
    'vivienda': {'nombre': 'Vivienda y catastro', 'icono': 'map-marked-alt', 'color': '#15803d'},
    'negocio': {'nombre': 'Negocios y actividad económica', 'icono': 'store', 'color': '#b45309'},
    'servicios': {'nombre': 'Vehículos, impuestos y servicios', 'icono': 'car', 'color': '#1d4ed8'},
    'multas': {'nombre': 'Multas y pagos', 'icono': 'triangle-exclamation', 'color': '#b91c1c'},
}


def _ficha(ident, slug, nombre, categoria, icono, etiqueta, resumen, intro,
           costo, costo_detalle, tiempo, modalidad, requisitos, pasos,
           recomendaciones, oficina, fuentes, relacionados, keywords,
           qu_nombre, qu_resumen):
    return {
        'id': ident,
        'slug': slug,
        'n': nombre,
        'cat': categoria,
        'icon': icono,
        'tag': etiqueta,
        'resumen': resumen,
        'intro': intro,
        'costo': costo,
        'costo_detalle': costo_detalle,
        'tiempo': tiempo,
        'modalidad': modalidad,
        'requisitos': requisitos,
        'pasos': [{'t': t, 'd': d} for t, d in pasos],
        'recomendaciones': recomendaciones,
        'oficina': oficina,
        'fuente': fuentes,
        'relacionados': relacionados,
        'keywords': keywords,
        'qu': {'n': qu_nombre, 'resumen': qu_resumen},
        'url': '/tramite/' + slug,
    }


TRAMITES = {}

TRAMITES['carnet'] = _ficha(
    'carnet', 'carnet-de-identidad', 'Carnet de Identidad', 'identidad',
    'id-card', 'El más solicitado',
    'Emisión, renovación o reposición de la cédula de identidad en el SEGIP. Es la llave para casi todos los demás trámites.',
    [
        'La cédula de identidad es el documento que acredita tu identidad y nacionalidad boliviana. Sin ella no puedes firmar contratos, abrir una cuenta bancaria, matricularte, cobrar un sueldo ni iniciar la mayoría de los trámites municipales.',
        'En Sacaba el trámite se realiza en las oficinas del SEGIP. Puedes renovarla antes de que venza, reponerla si la perdiste o tramitarla por primera vez con tu certificado de nacimiento.',
        'El proceso es biométrico: registran tus huellas, tomas una fotografía digital y firmas en pantalla. En condiciones normales el carnet se entrega el mismo día.',
    ],
    'Bs. 17 (referencial)',
    'El pago se realiza en Banco Unión o en las entidades financieras autorizadas por SEGIP. Guarda el comprobante: sin él no se inicia el trámite.',
    'Mismo día (30-60 minutos en ventanilla)',
    'Presencial, con cita o por orden de llegada',
    [
        'Comprobante de pago de Bs. 17 (monto referencial vigente)',
        'Cédula anterior, si es renovación',
        'Certificado de nacimiento para la primera emisión',
        'Denuncia policial o declaración de pérdida, si es reposición',
        'Estar presente físicamente para el registro biométrico',
    ],
    [
        ('Agenda tu atención', 'Ingresa a segip.gob.bo o llama a la línea gratuita 800 101 102 para conocer horarios y disponibilidad de la oficina de Sacaba o Cochabamba.'),
        ('Paga la tasa', 'Cancela el valor del carnet en Banco Unión o en una entidad autorizada y conserva el comprobante original.'),
        ('Llega con anticipación', 'Preséntate 15 minutos antes con tu comprobante y documentos. En renovaciones lleva la cédula anterior; en reposiciones, la denuncia.'),
        ('Registro biométrico', 'El funcionario verifica tus datos, captura huellas digitales, toma la fotografía y recoge tu firma en el sistema.'),
        ('Firma y recibe', 'Revisa que nombres, apellidos, fecha de nacimiento y estado civil estén correctos. Firma el acta y retira tu cédula el mismo día.'),
    ],
    [
        'Revisa la ortografía de tus nombres y apellidos antes de firmar; corregir después requiere un trámite adicional.',
        'Renueva tu carnet hasta 90 días antes del vencimiento para no quedarte sin documento vigente.',
        'Para la fotografía usa ropa de color distinto al fondo y evita lentes oscuros o gorras.',
        'Si tienes un trámite urgente, lleva una fotocopia de tu cédula anterior mientras esperas la nueva.',
    ],
    OFICINAS['segip'],
    [{'nombre': 'SEGIP - Cédula de Identidad', 'url': SEGIP + '/cedula-de-identidad/'},
     {'nombre': 'SEGIP - Nuestras oficinas', 'url': SEGIP + '/oficina/'}],
    ['licencia_conducir', 'antecedentes', 'residencia'],
    ['carnet', 'cedula', 'ci', 'identidad', 'segip', 'huellas', 'renovar', 'reposicion', 'perdi', 'primera vez'],
    'Carnet de Identidad',
    "Identidad documento, Boliviap tukuy runapaq obligatorio. SEGIP oficinaspi musuqmanta hurqokunki utaq renovakunki; huellakunata, fotografíata nitaq firmaykita chaskinku.",
)

TRAMITES['licencia_conducir'] = _ficha(
    'licencia_conducir', 'licencia-de-conducir', 'Licencia de Conducir', 'identidad',
    'car-side', 'Trámite frecuente',
    'Obtención, renovación o cambio de categoría de la licencia para conducir vehículos livianos, pesados o motocicletas.',
    [
        'La licencia de conducir es el permiso oficial que te habilita a manejar en todo el territorio boliviano. Se tramita en el SEGIP y requiere exámenes teóricos, prácticos y médicos según la categoría.',
        'Existen categorías para motocicleta, vehículo particular, transporte público y carga pesada. Cada una tiene requisitos, edad mínima y costo diferente.',
        'Si ya tienes licencia, puedes renovarla antes de su vencimiento. Si dejaste pasar el plazo, deberás rendir nuevamente los exámenes que correspondan.',
    ],
    'Desde Bs. 200 según categoría',
    'El monto varía por categoría y por los exámenes o curso de educación vial. Confirma el valor vigente en la ventanilla del SEGIP antes de pagar.',
    '1 a 3 semanas (según exámenes)',
    'Presencial, con exámenes y curso',
    [
        'Cédula de identidad vigente',
        'Certificado de antecedentes policiales',
        'Certificado médico de aptitud física y visual',
        'Grupo sanguíneo y factor RH',
        'Fotografías tamaño carnet con fondo rojo',
        'Comprobante de pago de la categoría solicitada',
        'Aprobar el curso y los exámenes teórico y práctico',
    ],
    [
        ('Elige la categoría', 'Define si necesitas licencia para moto, vehículo particular, transporte público o carga. La categoría determina los exámenes y el costo.'),
        ('Reúne los documentos', 'Obtén tu certificado de antecedentes, el certificado médico y las fotografías. Verifica que tu cédula esté vigente.'),
        ('Inscríbete y paga', 'Registra tu solicitud en el SEGIP, cancela la tasa y confirma la fecha del curso o de los exámenes.'),
        ('Rinde las evaluaciones', 'Aprueba el examen teórico de normas de tránsito y el examen práctico de manejo. Algunas categorías exigen horas de instrucción.'),
        ('Recibe tu licencia', 'Si apruebas, el SEGIP emite la licencia con tu fotografía y categoría. Revisa la fecha de vencimiento antes de retirarte.'),
    ],
    [
        'Practica el recorrido y las maniobras antes del examen práctico; la mayoría de los reprobados pierde por nervios, no por falta de habilidad.',
        'No conduzcas con la licencia vencida: además de la multa, el seguro puede rechazar cualquier reclamo.',
        'Lleva el certificado médico vigente; suele tener una validez corta.',
        'Si cambias de categoría, consulta si debes rendir un examen adicional o solo actualizar el registro.',
    ],
    OFICINAS['segip'],
    [{'nombre': 'SEGIP - Licencia para conducir', 'url': SEGIP},
     {'nombre': 'Policía Boliviana - Tránsito', 'url': DNFR}],
    ['carnet', 'antecedentes', 'multas_transito'],
    ['licencia', 'conducir', 'manejo', 'moto', 'categoria', 'renovar licencia', 'examen de conducir'],
    'Manejo Licencia',
    "Vehículokunata manejaspa licenciaykita SEGIPpi hurqoy utaq renovay. Categoríaman jina exámenes, certificado médico nitaq antecedentes mañakun.",
)

TRAMITES['antecedentes'] = _ficha(
    'antecedentes', 'certificado-de-antecedentes', 'Certificado de Antecedentes', 'identidad',
    'fingerprint', 'Para trabajo y estudios',
    'Certificado de conducta que acredita que no tienes antecedentes penales ni policiales. Se exige para empleo, universidad y trámites migratorios.',
    [
        'El certificado de antecedentes, también llamado certificado de conducta, es un documento oficial emitido por la Policía Boliviana. Muchas empresas lo piden antes de contratar personal y algunas universidades lo exigen para la matrícula.',
        'El trámite es personal: verifican tu identidad y consultan el sistema de antecedentes. En algunos casos se puede solicitar en línea, pero la entrega suele requerir presencia física.',
        'El certificado tiene vigencia limitada, por lo que conviene tramitarlo cuando tengas una solicitud concreta y no mucho antes.',
    ],
    'Bs. 20 (referencial)',
    'Tasa policial por emisión del certificado. Puede variar según la unidad y el tipo de solicitud.',
    '1 día hábil',
    'Presencial',
    [
        'Cédula de identidad vigente y fotocopia',
        'Formulario de solicitud llenado',
        'Comprobante de pago de la tasa',
        'Fotografía reciente, si la unidad lo solicita',
        'Indicar el motivo del certificado (trabajo, estudio, viaje)',
        'Número de teléfono o correo de contacto para la verificación',
    ],
    [
        ('Acude a la unidad policial', 'Dirígete a la FELCC o a la unidad de antecedentes de Sacaba con tu cédula de identidad.'),
        ('Llena la solicitud', 'Indica tus datos personales y el motivo del certificado. Revisa que el número de cédula sea exacto.'),
        ('Paga la tasa', 'Cancela el valor en caja o en la entidad indicada y conserva el comprobante.'),
        ('Verificación y entrega', 'El sistema confirma que no tienes antecedentes pendientes y emiten el certificado firmado y sellado.'),
        ('Revisa antes de retirarte', 'Confirma nombres, número de cédula y fecha del certificado; si hay un error, pide la corrección en el momento.'),
    ],
    [
        'Pregunta en la unidad si el certificado puede solicitarse en línea; algunos empleadores aceptan el documento digital con código de verificación.',
        'Revisa la fecha de emisión: muchas empresas exigen que tenga menos de 30 o 60 días.',
        'Si tu nombre coincide con el de otra persona con antecedentes, lleva documentación adicional para aclarar la homonimia.',
        'Guarda una copia digital del certificado para futuras postulaciones.',
    ],
    OFICINAS['policia'],
    [{'nombre': 'Policía Boliviana - Certificado de antecedentes', 'url': 'https://www.policia.bo/'}],
    ['carnet', 'licencia_conducir', 'residencia'],
    ['antecedentes', 'conducta', 'certificado de conducta', 'record policial', 'papelito', 'felcc'],
    'Conducta Certificado',
    "Mana penal ni policial antecedentes kasqaykita riqsichiq documento. Llankay, yachay utaq viaje trámitespaq Policía Bolivianapi mañakun.",
)

TRAMITES['residencia'] = _ficha(
    'residencia', 'constancia-de-residencia', 'Constancia de Residencia', 'identidad',
    'house-user', 'Trámite municipal',
    'Documento municipal que certifica que vives en Sacaba. Se usa para colegios, universidades, trabajo y servicios básicos.',
    [
        'La constancia de residencia acredita tu domicilio dentro del municipio de Sacaba. Es un requisito habitual para la matrícula escolar, postulaciones laborales, trámites bancarios y solicitudes de servicios.',
        'El trámite se presenta en la Dirección de Registro Social o en la ventanilla única de la municipalidad, con documentos que demuestren que efectivamente vives en la dirección declarada.',
        'La constancia suele tener vigencia de 30 a 90 días, por lo que debes solicitarla cerca de la fecha en que la necesitas.',
    ],
    'Bs. 15 (referencial)',
    'Tasa municipal que se paga en caja. Confirma el monto en ventanilla al presentar tu solicitud.',
    '2 a 3 días hábiles',
    'Presencial',
    [
        'Fotocopia de cédula de identidad',
        'Recibo de luz, agua o gas de los últimos 3 meses',
        'Declaración jurada de residencia',
        'Dos fotografías tamaño carnet',
        'Fotocopia de libreta de servicio militar, si corresponde',
    ],
    [
        ('Recoge el formulario', 'Solicita el formulario de declaración jurada en la ventanilla única o en Registro Social.'),
        ('Completa tus datos', 'Escribe tu nombre, número de cédula y la dirección exacta donde vives, con referencia de la zona.'),
        ('Presenta los requisitos', 'Adjunta la fotocopia de cédula, el recibo de servicios y las fotografías. Lleva los originales para verificación.'),
        ('Paga en caja', 'Cancela la tasa municipal y conserva el comprobante.'),
        ('Retira la constancia', 'Vuelve en 2 o 3 días hábiles con tu comprobante y cédula para recoger el documento.'),
    ],
    [
        'El recibo de servicios debe estar a tu nombre o al de un familiar directo; si no, adjunta una carta de autorización.',
        'Verifica que la dirección coincida exactamente con la del recibo para evitar observaciones.',
        'Si vives en una zona periurbana, indica la subalcaldía y la comunidad para facilitar la verificación.',
        'Solicita la constancia con anticipación si la necesitas para una matrícula o contrato.',
    ],
    OFICINAS['gam'],
    [{'nombre': 'GAM Sacaba - Trámites', 'url': BASE + '/tramites/'}],
    ['carnet', 'certificado_nacimiento', 'no_deuda'],
    ['residencia', 'vivo en sacaba', 'domicilio', 'constancia', 'registro social'],
    'Tiyay Constancia',
    "Sacaba munisipyupi tiyaq kasqaykita riqsichin. Colegio, universidad, llankay utaq servicios básicos trámitespaq Registro Socialpi mañakun.",
)

TRAMITES['certificado_nacimiento'] = _ficha(
    'certificado_nacimiento', 'certificado-de-nacimiento', 'Certificado de Nacimiento', 'identidad',
    'baby', 'Registro Civil',
    'Certificado oficial de nacimiento emitido por el Registro Civil. Es la base para la cédula, la matrícula y muchos derechos ciudadanos.',
    [
        'El certificado de nacimiento es la prueba legal de tu inscripción en el Registro Civil. Sin él no se puede tramitar la cédula de identidad ni acceder a servicios educativos y de salud.',
        'En Sacaba se solicita en la oficina del Registro Civil. Si la partida está digitalizada, la búsqueda es inmediata; si es antigua o tiene errores, puede requerir una revisión adicional.',
        'También se emiten certificados de matrimonio y de defunción con un procedimiento similar.',
    ],
    'Bs. 10 (referencial)',
    'Tasa por certificado. La primera inscripción de nacimiento es gratuita y se realiza dentro del plazo legal; las inscripciones tardías pueden generar un trámite adicional.',
    'Inmediato a 2 días',
    'Presencial',
    [
        'Cédula de identidad del solicitante',
        'Datos completos del inscrito: nombres, fecha y lugar de nacimiento',
        'Nombres completos de los padres',
        'Partida original, si se pide una aclaración o corrección',
        'Número de partida, tomo y folio, si lo conoces',
        'Comprobante de pago de la tasa',
    ],
    [
        ('Acude al Registro Civil', 'Preséntate en la oficina de Sacaba con tu cédula y los datos del inscrito.'),
        ('Solicita la búsqueda', 'Indica el nombre completo, la fecha aproximada y el lugar de nacimiento. Si conoces el número de partida, facilita el trabajo.'),
        ('Verifica los datos', 'Revisa en pantalla que el certificado corresponda a la persona correcta antes de pagar.'),
        ('Paga y recibe', 'Cancela la tasa y retira el certificado firmado y sellado.'),
        ('Verifica los datos impresos', 'Revisa nombres, apellidos, fecha y lugar de nacimiento antes de salir; cualquier error debe corregirse en la misma oficina.'),
    ],
    [
        'Lleva los datos exactos: un error en la fecha o en el orden de los apellidos puede generar una búsqueda infructuosa.',
        'Si el certificado es para el exterior, consulta si necesita apostilla o legalización.',
        'Solicita dos copias si el documento se presentará en varias instituciones.',
        'Para corregir nombres o fechas, primero debe tramitarse la aclaración en el Registro Civil.',
    ],
    OFICINAS['registro'],
    [{'nombre': 'Registro Civil - Bolivia', 'url': 'https://www.registrocivil.gob.bo/'}],
    ['carnet', 'residencia', 'antecedentes'],
    ['nacimiento', 'partida', 'registro civil', 'acta', 'matrimonio', 'defuncion'],
    'Nacimiento Certificado',
    "Registro Civilpi nacimientoykita certificadota hurqokunki. Carnetta hurqonapaq, yachayman qillqakunapaq nitaq tukuy derechosniykikunapaq importante.",
)

TRAMITES['licencia_funcionamiento'] = _ficha(
    'licencia_funcionamiento', 'licencia-de-funcionamiento', 'Licencia de Funcionamiento', 'negocio',
    'store', 'Actividad económica',
    'Patente municipal para abrir o renovar un negocio en Sacaba. El costo base es Bs. 60 para licencia nueva y Bs. 40 para renovación.',
    [
        'La licencia de funcionamiento es el permiso municipal que habilita una actividad económica en Sacaba. Se exige a tiendas, restaurantes, talleres, industrias, servicios y empresas de transporte.',
        'El trámite se presenta con una declaración jurada y documentos del local. Según el rubro, se suman requisitos ambientales, sanitarios y de GERES.',
        'La licencia debe renovarse cada gestión. Funcionar sin ella expone al negocio a multas, clausura temporal y decomiso de mercadería.',
    ],
    'Bs. 60 nueva / Bs. 40 renovación',
    'Los valores municipales se compran en la caja central o en las subalcaldías. Pueden sumarse tasas ambientales o sectoriales según el rubro.',
    '5 a 15 días hábiles',
    'Presencial',
    [
        'Formulario de solicitud con declaración jurada',
        'Fotocopia de cédula de identidad del propietario',
        'Contrato de alquiler o anticrético del local, si corresponde',
        'Licencia ambiental o certificación, según el rubro',
        'Carnet sanitario de SEDES para el personal, en alimentos y bebidas',
        'Autorización de SENASAG, en rubros alimenticios',
        'Contrato o certificación GERES, según la actividad',
        'Valores municipales de Bs. 60 (nueva) o Bs. 40 (renovación)',
    ],
    [
        ('Identifica tu rubro', 'Consulta en la Dirección de Ingresos si tu actividad exige licencia ambiental, carnet sanitario, SENASAG o contrato GERES.'),
        ('Reúne los documentos', 'Consigue el contrato del local, la fotocopia de cédula y los permisos sectoriales que correspondan.'),
        ('Compra los valores', 'Adquiere los valores municipales en la caja central o en tu subalcaldía: Bs. 60 si es nueva y Bs. 40 si es renovación.'),
        ('Presenta el expediente', 'Entrega el formulario con declaración jurada y todos los anexos en la ventanilla de Ingresos y Servicios.'),
        ('Inspección y emisión', 'Si el rubro lo requiere, un inspector verifica el local. Luego se emite la licencia para su retiro.'),
    ],
    [
        'No firmes el contrato de alquiler antes de confirmar que la zona permite tu actividad económica.',
        'Los rubros de alimentos necesitan carnet sanitario y, en varios casos, autorización de SENASAG.',
        'Guarda la licencia en un lugar visible del local: la inspección municipal puede solicitarla en cualquier momento.',
        'Renueva antes del vencimiento para evitar la multa por funcionamiento sin licencia.',
    ],
    OFICINAS['rentas'],
    [{'nombre': 'GAM Sacaba - Licencia de funcionamiento', 'url': BASE + '/tramites/'}],
    ['empadronamiento_predial', 'no_deuda', 'impuesto_predial'],
    ['licencia', 'funcionamiento', 'patente', 'negocio', 'tienda', 'restaurante', 'abrir negocio', 'rubro'],
    'Funcionamiento Licencia',
    "Sacabapi negocioyta kichanapaq utaq renovanapaq munisipyu permiso. Bs. 60 musuqpaq, Bs. 40 renovacionpaq; rubroman jina huk requisitokunapas kan.",
)

TRAMITES['empadronamiento_predial'] = _ficha(
    'empadronamiento_predial', 'empadronamiento-predial', 'Empadronamiento Predial', 'vivienda',
    'map-marked-alt', 'Catastro municipal',
    'Registro oficial de tu terreno o vivienda en el sistema catastral de Sacaba, con título de propiedad o como poseedor.',
    [
        'El empadronamiento predial incorpora tu inmueble al catastro municipal. A partir de ese registro se genera el código catastral, se calcula el impuesto predial y se pueden tramitar certificados y planos.',
        'Pueden empadronar los propietarios con título inscrito en Derechos Reales y también los poseedores que acrediten posesión continua y pacífica, según el reglamento municipal.',
        'El expediente incluye un plano georreferenciado elaborado por un profesional colegiado. Sin ese plano no se puede ubicar correctamente el predio en el sistema.',
    ],
    'Valores municipales + Bs. 10 y 2 timbres de Bs. 5',
    'Se compra el folder administrativo municipal, un timbre de Bs. 10 para el título y dos timbres de Bs. 5. El precio del folder se confirma en caja.',
    '10 a 20 días hábiles',
    'Presencial, con verificación técnica',
    [
        'Memorial al Alcalde o Subalcalde firmado por el propietario o apoderado',
        'Título de propiedad inscrito en Derechos Reales y folio real con antigüedad máxima de 1 año',
        'Fotocopia autenticada del título con timbre de Bs. 10',
        'Plano de lote georreferenciado impreso y en Shapefile (CD)',
        'Formulario de Declaración Jurada EMP-CAT-01 con respaldo fotográfico',
        'Fotocopia vigente de cédula de identidad o cédula de extranjería',
        'Poder legalizado y cédula del apoderado, si corresponde',
        'NIT, escritura de constitución y poder, si es persona jurídica',
    ],
    [
        ('Prepara el plano', 'Contrata un profesional colegiado para el levantamiento georreferenciado con coordenadas, colindancias, dimensiones y superficie.'),
        ('Reúne el título', 'Obtén el folio real actualizado y la fotocopia autenticada con timbre de Bs. 10. Verifica que el título esté inscrito.'),
        ('Compra los valores', 'Adquiere el folder administrativo y los timbres en caja central o subalcaldía.'),
        ('Presenta el expediente', 'Entrega el memorial, el formulario EMP-CAT-01, el plano y los documentos en la Unidad de Catastro.'),
        ('Verificación y registro', 'Catastro revisa la documentación y el plano, realiza la verificación técnica y asigna el código catastral al predio.'),
    ],
    [
        'El folio real debe tener menos de un año; si está vencido, actualízalo antes de iniciar el trámite.',
        'Revisa que el plano incluya construcciones existentes: omitirlas puede generar diferencias en el avalúo.',
        'Si eres poseedor sin título, consulta el trámite específico para poseedores y lleva boletas de servicios y declaración notariada.',
        'Conserva una copia digital del Shapefile: la necesitarás para planos y certificados futuros.',
    ],
    OFICINAS['catastro'],
    [{'nombre': 'GAM Sacaba - Empadronamiento predial con título', 'url': BASE + '/tramites/empadronamiento-predial-con-titulo-de-propiedad/'},
     {'nombre': 'Decreto Municipal 014/2024', 'url': BASE + '/tramites/'}],
    ['certificado_catastral', 'avaluo_catastral', 'plano_vivienda', 'impuesto_predial'],
    ['empadronamiento', 'catastro', 'predio', 'terreno', 'lote', 'registro predial', 'poseedor', 'shapefile'],
    'Empadronamiento Predial',
    "Terrenoykita utaq wasiykita Sacabaq catastro sistemapi qillqachiy. Título, folio real, plano georreferenciado nitaq formulario EMP-CAT-01 apamuy.",
)

TRAMITES['certificado_catastral'] = _ficha(
    'certificado_catastral', 'certificado-catastral', 'Certificado Catastral', 'vivienda',
    'file-lines', 'Catastro municipal',
    'Documento que certifica ubicación, superficie, código catastral y datos técnicos de tu predio.',
    [
        'El certificado catastral es la radiografía oficial de tu inmueble: indica dónde está, cuánto mide, cómo está construido y cuál es su código catastral.',
        'Se exige para vender, hipotecar, tramitar planos, solicitar servicios o demostrar la situación del predio ante otras instituciones.',
        'Si el predio no está empadronado, primero debe regularizarse. El certificado se emite únicamente sobre información catastral actualizada.',
    ],
    'Valores municipales (folder y timbres)',
    'Incluye folder administrativo, timbre de Bs. 10 en el título y Bs. 5 en el reporte sin deudas, además de los valores que indique Catastro.',
    '5 a 10 días hábiles',
    'Presencial',
    [
        'Memorial al Alcalde o Subalcalde firmado por el propietario o apoderado',
        'Título de propiedad y folio real actualizado (máximo 1 año)',
        'Reporte sin deudas',
        'Fotocopia legalizada del plano de lote aprobado y de la Resolución Técnica Administrativa',
        'Fotocopia vigente de cédula de identidad o cédula de extranjería',
        'Poder legalizado y cédula del apoderado, si corresponde',
        'En propiedad horizontal: plano de adecuación y certificación individual',
    ],
    [
        ('Verifica tus datos', 'Confirma que el predio esté empadronado y que el título esté a tu nombre. Si hay diferencias, corrígelas antes.'),
        ('Reúne los documentos', 'Obtén el folio real, el reporte sin deudas y las copias legalizadas del plano y la resolución técnica.'),
        ('Presenta el memorial', 'Entrega la solicitud en la Unidad de Catastro con todos los anexos y los valores municipales.'),
        ('Revisión técnica', 'Catastro verifica la información gráfica y alfanumérica del predio. Si hay observaciones, te piden subsanarlas.'),
        ('Recibe el certificado', 'Retira el documento firmado y sellado. Revisa que la superficie y el código catastral coincidan con tu plano.'),
    ],
    [
        'El certificado refleja lo que está registrado: si construiste sin aprobación, la superficie puede no coincidir con la realidad.',
        'Pide el certificado actualizado antes de una compraventa; el comprador necesita verificar linderos y superficie.',
        'Si el predio está en propiedad horizontal, cada departamento, parqueo o baulera requiere su certificación individual.',
        'Conserva el original y una copia digital: muchas entidades no aceptan certificados con más de 90 días.',
    ],
    OFICINAS['catastro'],
    [{'nombre': 'GAM Sacaba - Certificado catastral', 'url': BASE + '/tramites/certificado-catastral/'}],
    ['empadronamiento_predial', 'avaluo_catastral', 'plano_vivienda', 'propiedad_horizontal'],
    ['certificado catastral', 'catastro', 'codigo catastral', 'superficie', 'predio', 'lote'],
    'Certificado Catastral',
    "Predioykimanta maypi kasqan, superficie, código catastral nitaq datos técnicos riqsichiq documento. Venta, hipoteca utaq planos tramitapaq mañakun.",
)

TRAMITES['avaluo_catastral'] = _ficha(
    'avaluo_catastral', 'avaluo-catastral', 'Avalúo Catastral', 'vivienda',
    'scale-balanced', 'Catastro municipal',
    'Cálculo del valor oficial de tu inmueble para impuestos, transferencias, hipotecas o regularizaciones.',
    [
        'El avalúo catastral determina el valor oficial del inmueble. Ese valor es la base para calcular el impuesto predial y para operaciones de compraventa, hipoteca o partición.',
        'El avalúo combina la ubicación, la superficie, la calidad de la construcción y los valores unitarios aprobados por el municipio. No es el precio de mercado, aunque suele usarse como referencia.',
        'Si construiste, ampliaste o modificaste el inmueble sin actualizar el catastro, el avalúo puede estar desactualizado y conviene solicitar una actualización.',
    ],
    'Valores municipales (folder y timbres)',
    'Se paga el folder administrativo y los timbres municipales. El costo del informe técnico se confirma en la Unidad de Catastro.',
    '10 a 20 días hábiles',
    'Presencial, con revisión técnica',
    [
        'Memorial solicitando el avalúo catastral',
        'Título de propiedad y folio real actualizado (máximo 1 año)',
        'Fotocopia del último impuesto predial, si corresponde',
        'Fotocopia vigente de cédula de identidad o cédula de extranjería',
        'Plano de lote aprobado o plano georreferenciado con coordenadas y superficies',
        'Poder legalizado y cédula del apoderado, si corresponde',
        'Escritura de constitución y NIT, si es persona jurídica',
    ],
    [
        ('Solicita el avalúo', 'Presenta el memorial en la Unidad de Catastro indicando el motivo: impuesto, venta, hipoteca o regularización.'),
        ('Adjunta la documentación', 'Entrega título, folio real, plano y el último impuesto. Si no tienes plano aprobado, presenta el georreferenciado.'),
        ('Paga los valores', 'Compra el folder y los timbres municipales en caja central o subalcaldía.'),
        ('Inspección técnica', 'Un técnico verifica el predio y la construcción. Asegúrate de que alguien pueda abrir el inmueble el día de la visita.'),
        ('Recibe el informe', 'Catastro emite el avalúo con el valor oficial. Úsalo como base para el trámite que motivó la solicitud.'),
    ],
    [
        'Solicita el avalúo antes de cerrar una compraventa: el comprador y el vendedor deben conocer la base imponible.',
        'Si ampliaste la vivienda, actualiza el catastro; de lo contrario el avalúo seguirá reflejando la construcción anterior.',
        'El avalúo catastral no reemplaza un avalúo comercial para créditos hipotecarios; el banco puede pedir otro informe.',
        'Guarda el informe junto al folio real y al plano para futuros trámites.',
    ],
    OFICINAS['catastro'],
    [{'nombre': 'GAM Sacaba - Avalúo catastral', 'url': BASE + '/tramites/avaluo-catastral/'}],
    ['certificado_catastral', 'empadronamiento_predial', 'impuesto_predial'],
    ['avaluo', 'valor catastral', 'tasar', 'impuesto', 'hipoteca', 'inmueble'],
    'Avalúo Catastral',
    "Inmuebleykimanta oficial valorta yupay, impuestos, venta utaq hipotecapaq. Título, folio real, plano nitaq último impuesto apamuy Catastroman.",
)

TRAMITES['plano_vivienda'] = _ficha(
    'plano_vivienda', 'aprobacion-de-plano-de-vivienda', 'Aprobación de Plano de Vivienda', 'vivienda',
    'drafting-compass', 'Urbanismo',
    'Aprobación o legalización del plano de construcción de una vivienda nueva, ampliación o remodelación.',
    [
        'La aprobación de plano es el permiso técnico para construir. El municipio revisa que la edificación cumpla con el uso de suelo, los retiros, la altura y las normas de urbanismo.',
        'También permite legalizar una obra que ya fue construida sin autorización. En ese caso se suman declaraciones juradas y fotografías del estado actual.',
        'El expediente debe ser elaborado por un arquitecto con registro profesional. Los planos se presentan impresos y en formato digital.',
    ],
    'Valores municipales (folder y timbres)',
    'Se compran valores municipales y se paga el timbre de Bs. 10 en la copia del título. El costo total depende de la superficie y del tipo de revisión.',
    '15 a 30 días hábiles',
    'Presencial, con revisión técnica',
    [
        'Memorial al Alcalde o Subalcalde firmado por el propietario o apoderado',
        'Título de propiedad y folio real con antigüedad máxima de 1 año',
        'Comprobante de IPBI de la última gestión',
        'Planos por arquitecto: 3 ejemplares en papel y 1 digital en Shapefile',
        'Certificado catastral actualizado y legalizado',
        'Plano de lote y resolución de aprobación legalizados',
        'Fotocopia de cédula de identidad vigente',
        'Poder notariado, si actúa un apoderado',
        'Para legalización: declaración jurada CAT-EMP-01 y fotografías 13x18 cm',
    ],
    [
        ('Contrata al profesional', 'Un arquitecto colegiado elabora el proyecto y los planos con registro de propiedad intelectual.'),
        ('Reúne los documentos', 'Obtén el folio real, el IPBI, el certificado catastral y el plano de lote aprobado.'),
        ('Presenta el expediente', 'Entrega el memorial y los planos en la Dirección de Urbanismo. Guarda el cargo de recepción.'),
        ('Revisión y observaciones', 'Urbanismo revisa el cumplimiento normativo. Si hay observaciones, el arquitecto debe corregir y volver a presentar.'),
        ('Aprobación', 'Si el proyecto cumple, se emite la resolución de aprobación y el plano sellado que habilita la construcción.'),
    ],
    [
        'Verifica el uso de suelo antes de comprar el terreno o diseñar: una zona residencial no permite cualquier actividad.',
        'No inicies la obra sin plano aprobado; la construcción ilegal puede ser paralizada y multada.',
        'Para legalizar una obra terminada, toma fotografías de fachada, interiores y conjunto antes de presentar el expediente.',
        'Pregunta si tu proyecto necesita estudio de suelos o memoria estructural, especialmente en edificios de varios niveles.',
    ],
    OFICINAS['urbanismo'],
    [{'nombre': 'GAM Sacaba - Aprobación de plano de vivienda', 'url': BASE + '/tramites/aprobacion-y-o-legalizacion-de-plano-de-construccion-de-vivienda/'}],
    ['certificado_catastral', 'propiedad_horizontal', 'empadronamiento_predial'],
    ['plano', 'construccion', 'construir', 'vivienda', 'ampliacion', 'remodelacion', 'legalizar obra', 'arquitecto'],
    'Construcción Plano',
    "Wasiyta ruwanapaq utaq legalizanapaq plano aprobación. Arquitectoq planosnin, título, folio real, IPBI nitaq certificado catastral apamuy Urbanismoman.",
)

TRAMITES['propiedad_horizontal'] = _ficha(
    'propiedad_horizontal', 'propiedad-horizontal', 'Propiedad Horizontal o Condominio', 'vivienda',
    'building', 'Urbanismo',
    'Adecuación de un edificio o inmueble a propiedad horizontal para registrar departamentos, parqueos y bauleras.',
    [
        'La propiedad horizontal permite que cada departamento, oficina, parqueo o baulera tenga su propio registro y pueda venderse de forma independiente, compartiendo áreas comunes.',
        'El trámite exige un plano de adecuación elaborado por un arquitecto y una resolución técnica que individualice cada unidad. Luego se actualiza el catastro de cada unidad.',
        'Es habitual en edificios nuevos, pero también se usa para regularizar construcciones antiguas que funcionan como condominio sin documentación.',
    ],
    'Valores municipales (folder y timbres)',
    'Incluye folder administrativo, timbres y los valores de revisión. Cada unidad puede generar costos catastrales adicionales.',
    '20 a 40 días hábiles',
    'Presencial, con revisión técnica',
    [
        'Memorial al Alcalde o Subalcalde',
        'Título de propiedad y folio real',
        'Comprobante de IPBI',
        'Plano de adecuación a propiedad horizontal por arquitecto (3 ejemplares)',
        'Certificado catastral del inmueble',
        'Plano de terreno aprobado',
        'Resolución Técnica Administrativa',
        'Fotocopia de cédula de identidad',
    ],
    [
        ('Define las unidades', 'El arquitecto elabora el plano de adecuación indicando departamentos, parqueos, bauleras y porcentajes de participación en áreas comunes.'),
        ('Reúne los documentos', 'Consigue título, folio real, IPBI, certificado catastral y plano de terreno aprobado.'),
        ('Presenta en Urbanismo', 'Entrega el expediente con el memorial y los planos. Solicita la revisión técnica.'),
        ('Resolución técnica', 'Urbanismo emite la Resolución Técnica Administrativa que aprueba la propiedad horizontal y individualiza las unidades.'),
        ('Registra cada unidad', 'Con la resolución, actualiza el catastro y registra cada departamento o parqueo en Derechos Reales.'),
    ],
    [
        'Define claramente los porcentajes de participación: de ellos dependen los gastos comunes y las decisiones de la junta de propietarios.',
        'Incluye parqueos y bauleras en el plano; si quedan fuera, no tendrán registro independiente.',
        'Revisa que las medidas de cada unidad coincidan con la construcción real para evitar observaciones.',
        'Coordina con un abogado para el reglamento de copropiedad y la inscripción en Derechos Reales.',
    ],
    OFICINAS['urbanismo'],
    [{'nombre': 'GAM Sacaba - Propiedad horizontal', 'url': BASE + '/tramites/aprobacion-de-plano-de-adecuacion-a-propiedad-horizontal-o-condominio/'}],
    ['plano_vivienda', 'certificado_catastral', 'empadronamiento_predial'],
    ['propiedad horizontal', 'condominio', 'departamento', 'parqueo', 'baulera', 'edificio'],
    'Propiedad Horizontal',
    "Edificiomanta sapa departamento, parqueo utaq baulerapaq sapan registro. Arquitectoq adecuación planon, resolución técnica nitaq catastro actualización necesitan.",
)

TRAMITES['inscripcion_vehiculo'] = _ficha(
    'inscripcion_vehiculo', 'inscripcion-de-vehiculo', 'Inscripción de Vehículo (RUAT)', 'servicios',
    'car', 'Vehículos',
    'Registro inicial de un vehículo nuevo o importado en el sistema RUAT del municipio de Sacaba.',
    [
        'La inscripción incorpora el vehículo al Registro Único para la Administración Tributaria Municipal (RUAT). Sin ella no se puede circular legalmente ni pagar impuestos vehiculares.',
        'Se aplica a vehículos comprados en casa comercial, importados directamente o ingresados con transferencia. Cada caso tiene documentos específicos.',
        'El registro genera el CRPVA (RUAT 03), documento que acredita la propiedad y que se exige en transferencias, bajas y trámites de placas.',
    ],
    'Valores municipales según caso',
    'Incluye folder administrativo y los valores del trámite. El monto depende del tipo de inscripción y del valor del vehículo.',
    '1 a 5 días hábiles',
    'Presencial',
    [
        'Factura de casa comercial o Declaración Única de Importación (DUI)',
        'Formulario FRV o documentación aduanera, según el caso',
        'Fotocopia de cédula de identidad del propietario',
        'Certificado de inscripción a Impuestos Nacionales, si es persona jurídica',
        'Testimonio de poder, si compra una sociedad',
        'Fotografía 3x3 con fondo rojo, para persona natural',
        'Folder administrativo y valores municipales',
    ],
    [
        ('Identifica el caso', 'Define si el vehículo es nuevo de casa comercial, importado directamente o ingresó con transferencia.'),
        ('Reúne la documentación', 'Consigue la factura o DUI, el FRV, tu cédula y la fotografía. Si es empresa, agrega NIT y poder.'),
        ('Presenta en Vehículos', 'Entrega el expediente en la Unidad de Vehículos del GAM Sacaba y recibe el cargo.'),
        ('Paga los valores', 'Cancela el folder y los valores municipales en caja central o subalcaldía.'),
        ('Recibe el CRPVA', 'Verifica que marca, modelo, chasis y motor coincidan con la documentación. Guarda el CRPVA original.'),
    ],
    [
        'Revisa el número de chasis y motor antes de firmar la recepción: un error obliga a corregir todo el expediente.',
        'No circules sin seguro ni sin placas; la inscripción no reemplaza la revisión técnica ni el SOAT.',
        'Si el vehículo es importado, conserva la DUI y los comprobantes aduaneros en original.',
        'Consulta deudas pendientes en el RUAT antes de iniciar la inscripción.',
    ],
    OFICINAS['rentas'],
    [{'nombre': 'GAM Sacaba - Trámites de vehículos', 'url': BASE + '/tramites/'},
     {'nombre': 'RUAT', 'url': RUAT}],
    ['transferencia_vehiculo', 'cambio_radicatoria', 'impuesto_predial', 'multas_transito'],
    ['inscripcion', 'vehiculo', 'ruat', 'auto', 'carro', 'moto', 'importacion', 'factura', 'crpva'],
    'Vehículo Inscripción',
    "Musuq vehículota RUATpi qillqachiy. Factura utaq DUI, cédula, fotografía 3x3 nitaq valores municipales apamuy Unidad de Vehículosman.",
)

TRAMITES['transferencia_vehiculo'] = _ficha(
    'transferencia_vehiculo', 'transferencia-de-vehiculo', 'Transferencia de Vehículo', 'servicios',
    'right-left', 'Vehículos',
    'Cambio de propietario de un vehículo registrado en el RUAT. Se paga con dos timbres municipales de Bs. 10.',
    [
        'La transferencia actualiza el nombre del propietario en el RUAT. Es obligatoria después de una compraventa: mientras no se registre, las multas y deudas siguen apareciendo a nombre del vendedor.',
        'El trámite se realiza en la Unidad de Vehículos del GAM Sacaba con la minuta de compraventa, el CRPVA y la documentación de ambas partes.',
        'El vehículo debe estar libre de deudas, gravámenes, bloqueos y reportes de robo. Si hay una deuda pendiente, primero debe regularizarse.',
    ],
    '2 timbres de Bs. 10 + folder',
    'Se compran dos timbres municipales de Bs. 10 y el folder administrativo. No se cobra el valor del vehículo en este trámite.',
    '1 a 3 días hábiles',
    'Presencial',
    [
        'Minuta de compraventa original y dos copias',
        'CRPVA (RUAT 03) original y fotocopia',
        'Fotocopia de cédula del comprador y del vendedor',
        'Fotografía 3x3 con fondo rojo del comprador',
        'Certificado de inscripción a Impuestos Nacionales, si es empresa',
        'Testimonio de poder con facultad de venta, si corresponde',
        'Dos timbres municipales de Bs. 10',
        'Folder administrativo',
    ],
    [
        ('Firma la minuta', 'Comprador y vendedor firman la minuta de compraventa con datos completos y precio. Adjunta dos copias.'),
        ('Verifica el estado del vehículo', 'Consulta en el RUAT que no tenga deudas, gravámenes, bloqueos ni reporte de robo.'),
        ('Reúne los documentos', 'Consigue el CRPVA original, las cédulas, la fotografía y los timbres municipales.'),
        ('Presenta el expediente', 'Entrega todo en la Unidad de Vehículos y recibe el cargo de recepción.'),
        ('Registro del nuevo propietario', 'El sistema actualiza el RUAT. Verifica que el CRPVA nuevo salga a nombre del comprador.'),
    ],
    [
        'No entregues el vehículo sin firmar la minuta y sin verificar el estado de deudas en el RUAT.',
        'Haz la transferencia cuanto antes: si el comprador comete una infracción, la multa puede notificarse al vendedor.',
        'Revisa que la firma del vendedor coincida con la de su cédula; si no, puede exigirse reconocimiento de firmas.',
        'Guarda una copia del CRPVA actualizado y de la minuta para cualquier reclamo posterior.',
    ],
    OFICINAS['rentas'],
    [{'nombre': 'GAM Sacaba - Transferencia de vehículo', 'url': BASE + '/tramites/'},
     {'nombre': 'RUAT - Consulta de vehículos', 'url': RUAT + '/vehiculos/consultageneral/InicioBusquedaVehiculo.jsf'}],
    ['inscripcion_vehiculo', 'cambio_radicatoria', 'baja_tributaria', 'multas_transito'],
    ['transferencia', 'traspaso', 'compra venta', 'vender auto', 'comprar auto', 'cambio de propietario'],
    'Vehículo Transferencia',
    "Vehículota huk runaman traspasay. Minuta, CRPVA, cédulas, fotografía 3x3 nitaq iskay timbres Bs. 10 apamuy; deudas mana kanan tiyan.",
)

TRAMITES['cambio_radicatoria'] = _ficha(
    'cambio_radicatoria', 'cambio-de-radicatoria', 'Cambio de Radicatoria', 'servicios',
    'truck-moving', 'Vehículos',
    'Traslado del registro de un vehículo desde otro departamento o provincia hacia Sacaba.',
    [
        'La radicatoria es el municipio donde el vehículo paga sus impuestos y donde se registran sus trámites. Si te mudaste a Sacaba, debes cambiar la radicatoria para evitar notificaciones y deudas en el municipio anterior.',
        'El trámite se presenta en la Unidad de Vehículos con el CRPVA y los documentos del propietario. Se paga un timbre municipal de Bs. 40.',
        'El vehículo no debe tener deudas pendientes ni reportes de robo o bloqueos. Si hubo transferencia, adjunta la minuta.',
    ],
    'Timbre de Bs. 40 + folder',
    'Se compra un timbre municipal de Bs. 40 y el folder administrativo. Otros valores se confirman en ventanilla.',
    '1 a 3 días hábiles',
    'Presencial',
    [
        'CRPVA (RUAT 03) original y fotocopia',
        'Fotocopia de cédula de identidad del propietario',
        'Minuta de compraventa, si hubo transferencia',
        'Certificado de inscripción a Impuestos Nacionales, si es empresa',
        'Fotografía 3x3 con fondo rojo',
        'Timbre municipal de Bs. 40',
        'Folder administrativo',
    ],
    [
        ('Verifica el estado del vehículo', 'Consulta en el RUAT que no tenga deudas, bloqueos ni reporte de robo.'),
        ('Reúne los documentos', 'Consigue el CRPVA, tu cédula, la fotografía y, si corresponde, la minuta de transferencia.'),
        ('Paga el timbre', 'Compra el timbre de Bs. 40 en caja central o subalcaldía.'),
        ('Presenta la solicitud', 'Entrega el expediente en la Unidad de Vehículos del GAM Sacaba.'),
        ('Confirma la radicatoria', 'Verifica que el registro muestre a Sacaba como municipio de radicatoria.'),
    ],
    [
        'Cambia la radicatoria al mudarte: las notificaciones y multas llegan al municipio donde está registrado el vehículo.',
        'Si el vehículo tiene prenda o gravamen, consulta si necesitas autorización del acreedor.',
        'Actualiza también tu domicilio en el RUAT para recibir notificaciones.',
        'Guarda el comprobante del timbre y el CRPVA actualizado.',
    ],
    OFICINAS['rentas'],
    [{'nombre': 'GAM Sacaba - Trámites de vehículos', 'url': BASE + '/tramites/'},
     {'nombre': 'RUAT', 'url': RUAT}],
    ['inscripcion_vehiculo', 'transferencia_vehiculo', 'baja_tributaria'],
    ['radicatoria', 'cambio de radicatoria', 'mudanza', 'otro departamento', 'registro vehiculo'],
    'Radicatoria Cambio',
    "Vehículoq registron huk departamentomanta Sacabaman apamuy. CRPVA, cédula, fotografía nitaq Bs. 40 timbre apamuy; deudas mana kanan tiyan.",
)

TRAMITES['baja_tributaria'] = _ficha(
    'baja_tributaria', 'baja-tributaria-de-vehiculo', 'Baja Tributaria de Vehículo', 'servicios',
    'ban', 'Vehículos',
    'Retiro definitivo del vehículo del registro RUAT por robo, siniestro, exportación o fuera de circulación.',
    [
        'La baja tributaria saca el vehículo del padrón municipal. Se solicita cuando el automotor fue robado, sufrió un siniestro, se exportó o dejó de circular de forma definitiva.',
        'Cada motivo exige un respaldo distinto: denuncia policial por robo, informe de tránsito o DIPROVE por siniestro, resolución de aduana por exportación o declaración por fuera de circulación.',
        'El vehículo debe estar libre de deudas. Si tiene impuestos pendientes, primero se regulariza la deuda y luego se procesa la baja.',
    ],
    'Timbre de Bs. 20 + folder',
    'Se compra un timbre municipal de Bs. 20 y el folder administrativo. Pueden aplicarse otros valores según el motivo.',
    '3 a 10 días hábiles',
    'Presencial',
    [
        'Formulario ANEXO 1',
        'Cédula de identidad vigente del propietario',
        'CRPVA original y placas del vehículo',
        'Denuncia policial por robo o informe de siniestro',
        'Resolución de Aduana, si es exportación',
        'Declaración jurada, si es fuera de circulación',
        'Timbre municipal de Bs. 20',
        'Folder administrativo',
    ],
    [
        ('Define el motivo', 'Identifica si la baja es por robo, siniestro, exportación o fuera de circulación. Cada caso requiere un respaldo diferente.'),
        ('Reúne los documentos', 'Consigue el CRPVA, las placas, tu cédula y el informe o denuncia que acredite el motivo.'),
        ('Paga el timbre', 'Compra el timbre de Bs. 20 y el folder administrativo.'),
        ('Presenta el ANEXO 1', 'Entrega el formulario y todos los anexos en la Unidad de Vehículos.'),
        ('Confirma la baja', 'Verifica que el vehículo ya no aparezca con obligaciones pendientes en el RUAT.'),
    ],
    [
        'Para baja por robo, presenta la denuncia policial original; sin ella no se procesa.',
        'Si el vehículo fue chatarreado, guarda el certificado del centro de reciclaje o del taller autorizado.',
        'No dejes de pagar impuestos mientras tramitas la baja: las deudas siguen generando recargos.',
        'Solicita una constancia de baja para tus registros y para el seguro.',
    ],
    OFICINAS['rentas'],
    [{'nombre': 'GAM Sacaba - Baja tributaria', 'url': BASE + '/tramites/'},
     {'nombre': 'RUAT', 'url': RUAT}],
    ['transferencia_vehiculo', 'cambio_radicatoria', 'inscripcion_vehiculo'],
    ['baja', 'baja tributaria', 'robo', 'siniestro', 'exportacion', 'chatarra', 'fuera de circulacion'],
    'Vehículo Baja',
    "Vehículota RUATmanta hurquy: robo, siniestro, exportación utaq manaña circulacionpaq. Denuncia utaq informe, CRPVA, placas nitaq Bs. 20 timbre apamuy.",
)

TRAMITES['impuesto_predial'] = _ficha(
    'impuesto_predial', 'impuesto-predial', 'Impuesto Predial (IPBI)', 'servicios',
    'receipt', 'Impuestos',
    'Pago anual del impuesto a la propiedad inmueble, calculado sobre el avalúo catastral.',
    [
        'El Impuesto a la Propiedad de Bienes Inmuebles (IPBI) se paga cada año al municipio donde está registrado el inmueble. La base es el avalúo catastral y la alícuota depende del valor y de la normativa vigente.',
        'Puedes consultar la deuda en el RUAT o en la Dirección de Rentas. El pago se realiza en caja municipal, bancos habilitados o por canales digitales.',
        'Pagar dentro del plazo evita recargos e intereses. Si tienes un inmueble sin empadronar, primero debes regularizar el catastro.',
    ],
    '0,5% a 1% del avalúo (referencial)',
    'La alícuota se aplica sobre el valor catastral. El monto exacto aparece en la consulta de deuda del RUAT o en la boleta municipal.',
    'Pago inmediato',
    'Presencial o en línea',
    [
        'Cédula de identidad del propietario',
        'Código catastral o número de cuenta predial',
        'Título de propiedad o certificado catastral, si es la primera vez',
        'Consulta de deuda actualizada',
        'Fotocopia de cédula del propietario que realiza el pago',
        'Documento de representación, si paga un tercero o apoderado',
    ],
    [
        ('Consulta tu deuda', 'Ingresa al RUAT con el código catastral o acude a Rentas para conocer el monto actualizado.'),
        ('Verifica los datos', 'Confirma que el inmueble, la superficie y el propietario sean correctos. Si hay errores, solicita la actualización catastral.'),
        ('Paga', 'Cancela en caja municipal, banco habilitado o por el canal digital disponible. Guarda el comprobante.'),
        ('Registra el pago', 'Verifica que la deuda aparezca cancelada en el sistema y solicita tu constancia si la necesitas.'),
        ('Solicita tu constancia de pago', 'Pide el comprobante o la constancia de no deuda del periodo cancelado para presentarlo donde te lo exijan.'),
    ],
    [
        'Paga antes de la fecha límite anual: después se aplican recargos e intereses.',
        'Si el inmueble cambió de dueño, actualiza el registro para que las notificaciones lleguen al nuevo propietario.',
        'Revisa el avalúo si construiste o ampliaste; un avalúo desactualizado puede generar diferencias.',
        'Conserva el comprobante de pago por si necesitas demostrar solvencia en otro trámite.',
    ],
    OFICINAS['rentas'],
    [{'nombre': 'RUAT - Consulta de inmuebles', 'url': RUAT + '/inmuebles/consultageneral/InicioBusquedaInmueble.jsf'},
     {'nombre': 'GAM Sacaba - Impuestos', 'url': BASE + '/tramites/'}],
    ['no_deuda', 'certificado_catastral', 'avaluo_catastral'],
    ['impuesto', 'predial', 'ipbi', 'inmueble', 'pago anual', 'deuda predial'],
    'Predial Impuesto',
    "Sapa wata inmuebleykimanta impuestota pagana. Avalúo catastral patapi yupaykun; RUATpi utaq Rentaspi deudata qhawaspa pagay.",
)

TRAMITES['multas_transito'] = _ficha(
    'multas_transito', 'multas-de-transito', 'Multas de Tránsito', 'multas',
    'triangle-exclamation', 'Pago en bancos y QR',
    'Pago de infracciones con la boleta o ficha que entrega el policía. Puedes pagar en bancos o escanear el QR desde tu banca móvil.',
    [
        'Cuando un policía de tránsito te detiene por una infracción, entrega una boleta o ficha de infracción. Ese documento contiene tus datos, la falta cometida, el monto y un código QR de pago.',
        'Con la boleta puedes pagar en las entidades financieras habilitadas o desde tu banca móvil escaneando el QR. El pago se registra en el sistema de la Policía Boliviana y te permite solicitar el descargo o cerrar la infracción.',
        'Si consideras que la multa es injusta, puedes presentar un descargo en el plazo indicado en la notificación. Guarda siempre la ficha y el comprobante de pago.',
    ],
    'Bs. 50 a Bs. 1.000 según la falta',
    'El monto depende de la infracción: estacionamiento prohibido, exceso de velocidad, no respetar semáforo, conducir sin licencia o en estado de ebriedad. La boleta indica el importe exacto.',
    'Pago inmediato; descargo según plazo',
    'Presencial, banco o banca móvil',
    [
        'Boleta o ficha de infracción entregada por el policía',
        'Cédula de identidad del infractor o propietario',
        'Licencia de conducir, si corresponde',
        'Comprobante de pago o código QR de la boleta',
        'Descargo escrito, si se va a impugnar la multa',
    ],
    [
        ('Revisa la boleta', 'Verifica tus datos, la fecha, el lugar, la falta y el monto. Anota el número de infracción y el código QR.'),
        ('Elige el canal de pago', 'Puedes pagar en una entidad financiera habilitada, en la oficina de tránsito o desde tu banca móvil escaneando el QR.'),
        ('Paga el monto exacto', 'Confirma que el monto coincida con la boleta. Guarda el comprobante digital o impreso.'),
        ('Registra el pago', 'El sistema de la Policía Boliviana debe reflejar la infracción como pagada. Solicita la constancia si la necesitas.'),
        ('Presenta descargo, si corresponde', 'Si consideras que la multa es incorrecta, presenta tu descargo dentro del plazo indicado con pruebas y copia de la boleta.'),
    ],
    [
        'Escanea el QR únicamente desde la app oficial de tu banco; desconfía de enlaces enviados por mensajería.',
        'No pagues multas sin verificar el número de boleta y el monto en el sistema oficial.',
        'Conserva la ficha original: es tu respaldo para cualquier reclamo o descargo.',
        'Si la multa llega a nombre del propietario anterior, presenta la transferencia del vehículo para aclarar la responsabilidad.',
    ],
    OFICINAS['transito'],
    [{'nombre': 'Policía Boliviana - Pagos QR', 'url': DNFR},
     {'nombre': 'Infracciones de Tránsito - Estado Digital', 'url': ESTADO_DIGITAL}],
    ['multas_municipales', 'inspeccion_tecnica_vehicular', 'licencia_conducir', 'transferencia_vehiculo'],
    ['multa', 'multas', 'transito', 'infraccion', 'boleta', 'ficha', 'policia', 'qr', 'banca movil', 'pago'],
    'Tránsito Multakuna',
    "Policíaq boletan utaq fichanwan multata pagay: banco utaq banca móvil QRwan. Boleta, cédula nitaq comprobante waqaychay; descargo tiyan.",
)

TRAMITES['inspeccion_tecnica_vehicular'] = _ficha(
    'inspeccion_tecnica_vehicular', 'inspeccion-tecnica-vehicular', 'Inspección Técnica Vehicular (ITV)', 'multas',
    'clipboard-check', 'Pago en bancos y QR',
    'Revisión mecánica y de seguridad del vehículo. Se paga en bancos o por QR y se realiza en los centros autorizados.',
    [
        'La Inspección Técnica Vehicular (ITV) verifica frenos, luces, llantas, emisiones y condiciones generales de seguridad. Es obligatoria para circular y para renovar la revisión anual.',
        'El pago se realiza en entidades financieras habilitadas o mediante QR desde la banca móvil. Luego el vehículo se presenta en el centro de inspección con el comprobante.',
        'Si el vehículo no aprueba, se otorga un plazo para corregir las observaciones y volver a la revisión.',
    ],
    'Bs. 100 (referencial)',
    'El monto depende del tipo de vehículo y de la categoría. Confirma el valor vigente en el pre-registro de la Policía Boliviana.',
    '1 día (previa cita)',
    'Presencial, con pre-registro',
    [
        'Pre-registro en el sistema de la Policía Boliviana',
        'Comprobante de pago de la ITV',
        'Cédula de identidad del propietario',
        'CRPVA o documento del vehículo',
        'Vehículo en condiciones de revisión',
        'Extintor, botiquín y herramientas, si corresponden',
    ],
    [
        ('Haz el pre-registro', 'Ingresa al portal de pre-registro de ITV y agenda el centro, la fecha y la hora.'),
        ('Paga la inspección', 'Cancela en banco habilitado o escanea el QR desde tu banca móvil. Guarda el comprobante.'),
        ('Prepara el vehículo', 'Revisa frenos, luces, llantas, limpiaparabrisas y emisiones. Lleva los implementos de seguridad.'),
        ('Asiste a la inspección', 'Presenta el vehículo, el comprobante y tu cédula en el centro autorizado.'),
        ('Recibe el certificado', 'Si apruebas, se emite el certificado de ITV. Si hay observaciones, corrige y vuelve en el plazo indicado.'),
    ],
    [
        'Agenda con anticipación: los cupos se llenan cerca de la fecha límite.',
        'Corrige las fallas antes de la inspección; una segunda revisión puede generar un costo adicional.',
        'Lleva el comprobante impreso o digital y tu cédula; sin ellos no se permite el ingreso.',
        'Conserva el certificado en el vehículo para cualquier control de tránsito.',
    ],
    OFICINAS['transito'],
    [{'nombre': 'Policía Boliviana - ITV', 'url': DNFR},
     {'nombre': 'Pre-registro ITV', 'url': 'https://preregistroitv.policiadnfr.gob.bo/'}],
    ['multas_transito', 'inscripcion_vehiculo', 'impuesto_predial'],
    ['itv', 'inspeccion tecnica', 'revision vehicular', 'vehiculo', 'pago qr', 'banco'],
    'ITV Inspección',
    "Vehículoq seguridad nitaq mecánica revisión sapa wata. Banco utaq QRwan pagaspa, pre-registro ruwaspa centro autorizadoman riy.",
)

TRAMITES['multas_municipales'] = _ficha(
    'multas_municipales', 'multas-municipales', 'Multas Municipales', 'multas',
    'receipt', 'GAM Sacaba',
    'Sanciones por infracciones a las normas municipales: basura, ruido, venta sin autorización, daño al mobiliario o construcción sin permiso.',
    [
        'Las multas municipales sancionan conductas que afectan el espacio público, el medio ambiente o la convivencia. Las más comunes son arrojar basura, generar ruido excesivo, vender sin autorización y construir sin permiso.',
        'La multa se notifica después de una inspección o denuncia. El monto depende de la gravedad y de la reincidencia, y se paga en caja municipal o en bancos habilitados.',
        'Si consideras que la sanción es incorrecta, puedes presentar un descargo o recurso administrativo dentro del plazo indicado en la notificación.',
    ],
    'Bs. 50 a Bs. 2.000 según la falta',
    'Los montos son referenciales y dependen de la ordenanza municipal, la gravedad y la reincidencia. La notificación indica el importe exacto.',
    'Pago inmediato; descargo según plazo',
    'Presencial o banco',
    [
        'Notificación o papeleta de infracción',
        'Cédula de identidad del infractor',
        'Pruebas o fotografías, si se presenta descargo',
        'Comprobante de pago, si la multa ya fue cancelada',
        'Fotocopia de cédula del propietario o responsable del negocio',
        'Cargo de recepción del descargo, si ya lo presentaste',
    ],
    [
        ('Identifica la infracción', 'Lee la notificación: indica la conducta, la norma aplicada, el monto y el plazo para pagar o reclamar.'),
        ('Reúne tus pruebas', 'Si vas a impugnar, reúne fotografías, testigos o documentos que demuestren que la sanción es incorrecta.'),
        ('Paga o presenta descargo', 'Cancela en caja municipal o presenta el descargo dentro del plazo. Guarda el cargo de recepción.'),
        ('Cierra el trámite', 'Verifica que la multa aparezca como pagada o resuelta en el sistema municipal.'),
        ('Solicita la resolución del descargo', 'Si impugnaste, pide copia de la resolución administrativa y guárdala con la notificación original.'),
    ],
    [
        'Saca la basura en los horarios y lugares establecidos; arrojar residuos en la calle genera multa.',
        'Si tienes un negocio, controla el ruido y mantén la licencia de funcionamiento vigente.',
        'Para una construcción, solicita el permiso antes de iniciar la obra: la multa por construir sin autorización es alta.',
        'Guarda la notificación original y el comprobante de pago por cualquier reclamo posterior.',
    ],
    OFICINAS['gam'],
    [{'nombre': 'GAM Sacaba - Trámites', 'url': BASE + '/tramites/'}],
    ['multas_transito', 'licencia_funcionamiento', 'plano_vivienda', 'no_deuda'],
    ['multa municipal', 'basura', 'ruido', 'vender sin autorizacion', 'mobiliario', 'construir sin permiso'],
    'Munisipyu Multakuna',
    "Basura, ruido, mana autorización jina venta, mobiliario daño utaq mana permiso construccionmanta multakuna. Caja municipalpi utaq bancopi pagay; descargo tiyan.",
)

TRAMITES['no_deuda'] = _ficha(
    'no_deuda', 'constancia-de-no-deuda', 'Constancia de No Deuda', 'servicios',
    'file-circle-check', 'Solvencia municipal',
    'Certifica que no tienes deudas tributarias pendientes con el municipio de Sacaba.',
    [
        'La constancia de no deuda, también llamada solvencia municipal, acredita que estás al día con los impuestos y tasas municipales. Se exige para vender un inmueble, participar en licitaciones o cerrar un negocio.',
        'El documento se emite en la Dirección de Rentas después de verificar el estado de cuenta del contribuyente. Si hay deudas, primero deben cancelarse.',
        'La vigencia suele ser corta, por lo que conviene solicitarla cerca de la fecha en que se presentará.',
    ],
    'Bs. 10 (referencial)',
    'Tasa municipal por emisión de la constancia. Se paga en caja central o en la entidad indicada.',
    '1 a 2 días hábiles',
    'Presencial',
    [
        'Cédula de identidad del titular',
        'Código catastral o número de cuenta, si corresponde',
        'Comprobante de pago de la tasa',
        'Poder legalizado, si actúa un apoderado',
        'NIT o registro tributario, si es contribuyente de actividades económicas',
        'Fotocopia de cédula del titular del inmueble o negocio',
    ],
    [
        ('Consulta tu estado', 'Acude a Rentas con tu cédula o código catastral para verificar si tienes deudas pendientes.'),
        ('Regulariza, si hay deudas', 'Paga los impuestos o tasas pendientes y guarda los comprobantes.'),
        ('Solicita la constancia', 'Presenta tu cédula y paga la tasa municipal.'),
        ('Recibe el documento', 'Retira la constancia firmada y sellada. Revisa que tus datos y el periodo cubierto sean correctos.'),
        ('Verifica la vigencia', 'Confirma la fecha de emisión y el periodo que cubre; si la institución exige otro rango, solicita una nueva constancia.'),
    ],
    [
        'Solicita la constancia después de pagar cualquier deuda pendiente; el sistema debe reflejar el pago.',
        'Verifica que el documento cubra el periodo que te exige la otra institución.',
        'Si eres propietario de varios inmuebles, indica cuál o cuáles deben aparecer en la constancia.',
        'Guarda una copia digital para futuras licitaciones o trámites.',
    ],
    OFICINAS['rentas'],
    [{'nombre': 'GAM Sacaba - Trámites', 'url': BASE + '/tramites/'},
     {'nombre': 'RUAT', 'url': RUAT}],
    ['impuesto_predial', 'licencia_funcionamiento', 'multas_municipales'],
    ['no deuda', 'solvencia', 'libre de deuda', 'deuda municipal', 'constancia'],
    'Mana Deuda Constancia',
    "Munisipyuwan tributaria deudas mana kasqaykita riqsichin. Venta, licitación utaq negocio cierrapaq Rentaspi mañakun; deudas kaptinqa ñawpaqta pagay.",
)


ORDER = [
    'carnet', 'licencia_conducir', 'antecedentes', 'residencia',
    'certificado_nacimiento', 'licencia_funcionamiento', 'empadronamiento_predial',
    'certificado_catastral', 'avaluo_catastral', 'plano_vivienda',
    'propiedad_horizontal', 'inscripcion_vehiculo', 'transferencia_vehiculo',
    'cambio_radicatoria', 'baja_tributaria', 'impuesto_predial',
    'multas_transito', 'inspeccion_tecnica_vehicular', 'multas_municipales',
    'no_deuda',
]

# Horarios por trámite: (días, horas, detalle). Son referenciales y se
# confirman en ventanilla, igual que los montos.
HORARIOS = {
    'carnet': {
        'filas': [
            ('Lunes a viernes', '08:00 – 16:00', 'Emisión, renovación y reposición'),
            ('Sábado', '08:00 – 13:00', 'Solo oficinas habilitadas del SEGIP'),
        ],
        'nota': 'El turno se entrega al abrir la oficina; algunas sedes atienden con cita previa.',
    },
    'licencia_conducir': {
        'filas': [
            ('Lunes a viernes', '08:00 – 15:30', 'Recepción de documentos y examen teórico'),
            ('Examen práctico', 'Según programación', 'Se agenda al aprobar el teórico'),
            ('Sábado', '08:00 – 13:00', 'Solo informes en oficinas habilitadas'),
        ],
        'nota': 'Llega antes de las 10:00 para alcanzar turno de examen el mismo día.',
    },
    'antecedentes': {
        'filas': [
            ('Lunes a viernes', '08:00 – 18:00', 'Ventanilla de certificados'),
            ('Sábado', '08:00 – 12:00', 'Entrega de certificados ya solicitados'),
            ('Denuncias', '24 horas', 'Estación policial de turno'),
        ],
        'nota': 'Si el certificado es para trabajo o viaje, avisa en ventanilla para priorizar la entrega.',
    },
    'residencia': {
        'filas': [
            ('Lunes a viernes', '08:00 – 12:00', 'Ventanilla de atención ciudadana'),
            ('Lunes a viernes', '14:00 – 18:00', 'Continuación de atención'),
            ('Sábado', '08:00 – 12:00', 'Solo informes y entrega'),
        ],
        'nota': 'La verificación de domicilio se programa en la misma semana de la solicitud.',
    },
    'certificado_nacimiento': {
        'filas': [
            ('Lunes a viernes', '08:00 – 12:00', 'Registro Civil, ventanilla de certificados'),
            ('Lunes a viernes', '14:00 – 18:00', 'Continuación de atención'),
            ('Sábado', '08:00 – 12:00', 'Solo entrega de documentos'),
        ],
        'nota': 'Lleva el número de partida si lo conoces: agiliza la búsqueda en el libro.',
    },
    'licencia_funcionamiento': {
        'filas': [
            ('Lunes a viernes', '08:00 – 12:00', 'Rentas: recepción de la solicitud'),
            ('Lunes a viernes', '14:00 – 18:00', 'Continuación de atención'),
            ('Inspección', 'Programada en 48 h', 'Visita al local por la unidad técnica'),
        ],
        'nota': 'Presenta la solicitud por la mañana para que la inspección se programe el mismo día.',
    },
    'empadronamiento_predial': {
        'filas': [
            ('Lunes a viernes', '08:00 – 12:00', 'Catastro: recepción de documentos'),
            ('Lunes a viernes', '14:00 – 18:00', 'Continuación de atención'),
            ('Verificación', '3 a 5 días hábiles', 'Revisión en campo del predio'),
        ],
        'nota': 'El sábado no hay atención en Catastro; coordina la verificación con anticipación.',
    },
    'certificado_catastral': {
        'filas': [
            ('Lunes a viernes', '08:00 – 12:00', 'Catastro: solicitud y pago'),
            ('Lunes a viernes', '14:00 – 18:00', 'Continuación de atención'),
        ],
        'nota': 'Si el plano no está actualizado, el certificado puede tardar un día más.',
    },
    'avaluo_catastral': {
        'filas': [
            ('Lunes a viernes', '08:00 – 12:00', 'Catastro: recepción de la solicitud'),
            ('Lunes a viernes', '14:00 – 18:00', 'Continuación de atención'),
            ('Valuación', 'Según programación', 'Visita del técnico al inmueble'),
        ],
        'nota': 'Ten a mano el plano aprobado y el último recibo del impuesto predial.',
    },
    'plano_vivienda': {
        'filas': [
            ('Lunes a viernes', '08:00 – 12:00', 'Urbanismo: recepción del expediente'),
            ('Lunes a viernes', '14:00 – 18:00', 'Continuación de atención'),
            ('Revisión técnica', '5 a 10 días hábiles', 'Observaciones por escrito'),
        ],
        'nota': 'Pregunta por el número de expediente para seguir el estado de la revisión.',
    },
    'propiedad_horizontal': {
        'filas': [
            ('Lunes a viernes', '08:00 – 12:00', 'Urbanismo: ingreso del expediente'),
            ('Lunes a viernes', '14:00 – 18:00', 'Continuación de atención'),
            ('Revisión técnica', '10 días hábiles', 'Informe de adecuación a condominio'),
        ],
        'nota': 'La revisión de planos se atiende por orden de ingreso; entrega copias completas.',
    },
    'inscripcion_vehiculo': {
        'filas': [
            ('Lunes a viernes', '08:00 – 16:00', 'Tránsito: verificación y matrícula'),
            ('RUAT en línea', '24 horas', 'Consulta y preinscripción desde casa'),
            ('Sábado', 'Cerrado', 'Solo pagos en entidades bancarias'),
        ],
        'nota': 'La revisión física del motor y chasis se hace en el patio de Tránsito por orden de llegada.',
    },
    'transferencia_vehiculo': {
        'filas': [
            ('Lunes a viernes', '08:00 – 16:00', 'Tránsito: cambio de propietario'),
            ('RUAT', '24 horas', 'Consulta de gravámenes y estado del vehículo'),
            ('Sábado', 'Cerrado', 'Solo pagos en entidades bancarias'),
        ],
        'nota': 'Ambas partes deben firmar; si falta el vendedor, se exige poder notariado.',
    },
    'cambio_radicatoria': {
        'filas': [
            ('Lunes a viernes', '08:00 – 16:00', 'Tránsito: cambio de radicatoria'),
            ('Sábado', 'Cerrado', 'Solo pagos en entidades bancarias'),
        ],
        'nota': 'Verifica antes en el RUAT si el vehículo tiene multas o restricciones pendientes.',
    },
    'baja_tributaria': {
        'filas': [
            ('Lunes a viernes', '08:00 – 12:00', 'Rentas: solicitud de baja'),
            ('Lunes a viernes', '14:00 – 18:00', 'Continuación de atención'),
            ('Vehículos', '08:00 – 16:00', 'Tránsito, si la baja es de un motorizado'),
        ],
        'nota': 'Presenta la baja antes del cierre del periodo para no generar deuda del siguiente año.',
    },
    'impuesto_predial': {
        'filas': [
            ('Lunes a viernes', '08:00 – 12:00', 'Caja central y ventanillas de Rentas'),
            ('Lunes a viernes', '14:00 – 18:00', 'Continuación de atención'),
            ('Bancos', '08:30 – 18:00', 'Pago en ventanilla bancaria'),
            ('Sábado (bancos)', '09:00 – 13:00', 'Solo pago en entidades habilitadas'),
        ],
        'nota': 'Aprovecha el descuento por pronto pago si pagas dentro del plazo de la gestión.',
    },
    'multas_transito': {
        'filas': [
            ('Lunes a viernes', '08:00 – 16:00', 'Tránsito / DNFR: consulta y descargos'),
            ('Bancos', '08:30 – 18:00', 'Pago con la boleta o ficha de infracción'),
            ('Sábado (bancos)', '09:00 – 13:00', 'Pago en entidades habilitadas'),
            ('Pago QR', '24 horas', 'Desde la banca móvil, todos los días'),
        ],
        'nota': 'El descuento por pago voluntario depende del plazo: revisa la fecha límite impresa en la boleta.',
    },
    'inspeccion_tecnica_vehicular': {
        'filas': [
            ('Lunes a viernes', '08:00 – 16:00', 'Línea de inspección por orden de llegada'),
            ('Sábado', '08:00 – 12:00', 'Solo vehículos particulares'),
        ],
        'nota': 'Llega con el vehículo limpio y sin accesorios sueltos para no repetir la revisión.',
    },
    'multas_municipales': {
        'filas': [
            ('Lunes a viernes', '08:00 – 12:00', 'Rentas: consulta y descargos'),
            ('Lunes a viernes', '14:00 – 18:00', 'Continuación de atención'),
            ('Bancos', '08:30 – 18:00', 'Pago con el código de la multa'),
            ('Pago QR', '24 horas', 'Desde la banca móvil, todos los días'),
        ],
        'nota': 'Si presentas descargo, pide el número de trámite para seguir la resolución.',
    },
    'no_deuda': {
        'filas': [
            ('Lunes a viernes', '08:00 – 12:00', 'Rentas: solicitud de la constancia'),
            ('Lunes a viernes', '14:00 – 18:00', 'Continuación de atención'),
            ('Sábado', '08:00 – 12:00', 'Solo informes'),
        ],
        'nota': 'Pide la constancia cerca de la fecha de presentación: la vigencia es corta.',
    },
}

for _ident, _horario in HORARIOS.items():
    if _ident in TRAMITES:
        TRAMITES[_ident]['horarios'] = [
            {'dias': d, 'horas': h, 'nota': n} for d, h, n in _horario['filas']
        ]
        TRAMITES[_ident]['horario_nota'] = _horario.get('nota', '')

# Expresiones naturales con las que la gente pide cada trámite. Se suman a las
# palabras clave de la ficha para que el panel se abra aunque no usen el nombre oficial.
_EXTRA_KEYWORDS = {
    'carnet': [
        'carnet de identidad', 'cedula de identidad', 'mi cedula', 'mi carnet',
        'carnet vencido', 'cedula vencida', 'mi ci', 'renovar carnet', 'renovar cedula',
        'sacar carnet', 'sacar mi carnet', 'primera cedula', 'perdi mi carnet',
        'perdi mi cedula', 'me robaron el carnet', 'me robaron la cedula', 'reponer carnet',
    ],
    'licencia_conducir': [
        'licencia', 'mi licencia', 'licencia de moto', 'licencia para moto', 'brevete',
        'licencia vencida', 'quiero manejar', 'aprender a manejar', 'sacar mi licencia',
        'renovar mi licencia', 'examen de conducir', 'examen teorico', 'examen practico',
    ],
    'antecedentes': [
        'antecedentes penales', 'antecedentes policiales', 'certificado de antecedentes',
        'record policial', 'certificado de conducta', 'papelito de conducta',
    ],
    'residencia': [
        'constancia de residencia', 'constancia de domicilio', 'certificado de domicilio',
        'donde vivo', 'vivo en sacaba', 'residencia habitual',
    ],
    'certificado_nacimiento': [
        'partida de nacimiento', 'acta de nacimiento', 'certificado de nacimiento',
        'registrar a mi bebe', 'inscribir a mi bebe', 'inscribir a mi hijo',
        'nacimiento de mi hijo', 'registro civil',
    ],
    'licencia_funcionamiento': [
        'mi negocio', 'abrir mi negocio', 'abrir una tienda', 'poner una tienda',
        'mi tienda', 'puesto de venta', 'patente municipal', 'permiso de funcionamiento',
        'licencia de negocio', 'restaurante',
    ],
    'empadronamiento_predial': [
        'mi terreno', 'mi terrenito', 'mi lote', 'mi casa', 'mi inmueble',
        'registrar mi terreno', 'registrar mi casa', 'empadronar mi terreno',
        'datos de mi terreno', 'registro de mi propiedad', 'titulo de mi terreno',
    ],
    'certificado_catastral': [
        'catastro', 'codigo catastral', 'certificado de catastro', 'ficha catastral',
        'datos catastrales', 'numero catastral',
    ],
    'avaluo_catastral': [
        'avaluo de mi casa', 'avaluo de mi terreno', 'cuanto vale mi terreno',
        'cuanto vale mi casa', 'valor de mi propiedad', 'avaluo catastral',
    ],
    'plano_vivienda': [
        'planos de mi casa', 'planos de construccion', 'permiso para construir',
        'ampliar mi casa', 'ampliacion de mi casa', 'construir mi casa',
        'legalizar mi construccion', 'aprobar planos', 'remodelar mi casa',
    ],
    'propiedad_horizontal': [
        'mi departamento', 'departamento propio', 'division de mi edificio',
        'baulera', 'parqueo propio',
    ],
    'inscripcion_vehiculo': [
        'registrar mi auto', 'registrar mi carro', 'registrar mi moto',
        'inscribir mi auto', 'inscribir mi carro', 'inscribir mi moto',
        'auto nuevo', 'carro nuevo', 'moto nueva', 'matricular mi auto',
    ],
    'transferencia_vehiculo': [
        'vender mi auto', 'vender mi carro', 'vender mi moto', 'vender mi vehiculo',
        'comprar un auto', 'comprar un carro', 'comprar una moto', 'pasar mi carro',
        'transferir mi auto', 'traspaso de vehiculo', 'cambio de dueno',
    ],
    'cambio_radicatoria': [
        'cambiar mi radicatoria', 'traer mi auto a sacaba', 'radicatoria de mi vehiculo',
        'cambiar de departamento mi auto',
    ],
    'baja_tributaria': [
        'dar de baja mi auto', 'baja de mi vehiculo', 'mi auto fue robado',
        'auto siniestrado', 'sacar de circulacion mi auto',
    ],
    'impuesto_predial': [
        'pagar el impuesto', 'impuesto de mi casa', 'impuesto de mi terreno',
        'impuesto anual', 'impuesto inmueble', 'pagar impuestos',
    ],
    'multas_transito': [
        'multa', 'multas', 'multa de transito', 'multa de mi auto', 'me multaron',
        'me multo la policia', 'boleta de multa', 'exceso de velocidad',
        'multa por velocidad', 'pagar mi multa', 'pagar multa',
    ],
    'inspeccion_tecnica_vehicular': [
        'revision tecnica', 'inspeccion tecnica', 'revision vehicular',
        'revision de mi auto', 'revision anual de mi carro',
    ],
    'multas_municipales': [
        'multa municipal', 'multa por basura', 'multa por ruido', 'multa de intendencia',
        'multa del municipio', 'sancion municipal',
    ],
    'no_deuda': [
        'no deuda', 'constancia de no deuda', 'solvencia municipal', 'no debo nada',
        'libre de deudas', 'constancia de no adeudo',
    ],
}

for _ident, _extras in _EXTRA_KEYWORDS.items():
    if _ident in TRAMITES:
        TRAMITES[_ident]['keywords'] = list(
            dict.fromkeys(TRAMITES[_ident]['keywords'] + _extras)
        )

# Patrones ordenados de lo más específico a lo más general.
_PATTERNS = [
    ('multas_transito', ['multa de transito', 'multas de transito', 'infraccion de transito', 'boleta de infraccion',
                         'ficha de infraccion', 'me multo', 'me engrapo', 'pago qr', 'pago con qr',
                         'pagar con qr', 'pago por qr', 'codigo qr', 'banca movil']),
    ('inspeccion_tecnica_vehicular', ['itv', 'inspeccion tecnica', 'revision tecnica vehicular', 'revision vehicular']),
    ('multas_municipales', ['multa municipal', 'multas municipales', 'basura', 'ruido', 'mobiliario']),
    ('licencia_conducir', ['licencia de conducir', 'licencia de manejo', 'licencia para manejar', 'carnet de conducir',
                           'sacar licencia', 'renovar licencia', 'examen de conducir']),
    ('antecedentes', ['antecedente', 'conducta', 'record policial', 'papelito']),
    ('certificado_nacimiento', ['nacimiento', 'partida', 'acta de nacimiento', 'registro civil', 'matrimonio', 'defuncion']),
    ('carnet', ['carnet', 'cedula', 'ci ', 'identidad', 'segip', 'huella', 'renovar ci', 'perdi mi ci']),
    ('residencia', ['residencia', 'vivo en sacaba', 'domicilio', 'constancia de residencia']),
    ('licencia_funcionamiento', ['licencia de funcionamiento', 'funcionamiento', 'patente', 'abrir negocio', 'tienda',
                                 'restaurante', 'comercio']),
    ('empadronamiento_predial', ['empadronamiento', 'empadronar', 'registro predial', 'poseedor', 'shapefile']),
    ('certificado_catastral', ['certificado catastral', 'codigo catastral']),
    ('avaluo_catastral', ['avaluo', 'valor catastral', 'tasar']),
    ('plano_vivienda', ['plano de vivienda', 'plano de construccion', 'permiso de construccion', 'construir',
                        'ampliacion', 'remodelacion', 'legalizar obra', 'arquitecto']),
    ('propiedad_horizontal', ['propiedad horizontal', 'condominio', 'departamento', 'baulera']),
    ('inscripcion_vehiculo', ['inscripcion de vehiculo', 'inscribir vehiculo', 'registrar vehiculo', 'importacion',
                              'ruat']),
    ('transferencia_vehiculo', ['transferencia', 'traspaso', 'compra venta', 'vender auto', 'comprar auto',
                                'cambio de propietario']),
    ('cambio_radicatoria', ['radicatoria']),
    ('baja_tributaria', ['baja tributaria', 'dar de baja', 'siniestro', 'chatarra', 'fuera de circulacion']),
    ('impuesto_predial', ['impuesto predial', 'predial', 'ipbi', 'impuesto inmueble', 'impuesto']),
    ('no_deuda', ['no deuda', 'solvencia', 'libre de deuda']),
]


def _normalize(text):
    import unicodedata
    text = unicodedata.normalize('NFD', (text or '').lower())
    return ''.join(c for c in text if unicodedata.category(c) != 'Mn')


def _score_key(t, key):
    """Puntúa una palabra o frase dentro del texto ya normalizado y con espacios.

    Las palabras cortas exigen coincidencia completa (evita que "ci" gane dentro
    de "licencia"); las largas aceptan sufijos del habla real ("carnetta").
    """
    key = _normalize(key).strip()
    if not key:
        return 0
    if ' ' in key or len(key) <= 4:
        return len(key) if (' ' + key + ' ') in t else 0
    return len(key) if (' ' + key) in t else 0


# Palabras que aparecen en muchos contextos: no bastan por sí solas para abrir una ficha.
_DEBILES = {'auto', 'carro', 'moto', 'vehiculo', 'placa', 'casa', 'terreno', 'lote',
            'documento', 'documentos', 'identificacion', 'ci'}

# Palabras demasiado generales: solo se usan cuando ninguna frase específica coincide.
_GENERICAS = [
    ('multas_transito', ['multa', 'multas', 'infraccion', 'sancion']),
    ('carnet', ['documento', 'documentos', 'identificacion', 'ci']),
    ('licencia_funcionamiento', ['negocio', 'tienda', 'comercio', 'patente']),
    ('empadronamiento_predial', ['terreno', 'lote', 'inmueble', 'casa', 'propiedad']),
    ('impuesto_predial', ['impuesto', 'impuestos', 'tributo']),
]

_PATRONES_POR_ID = {ident: keys for ident, keys in _PATTERNS}


def detect(text):
    """Devuelve el id del trámite mencionado, o None.

    Compara contra patrones y palabras clave con coincidencia por palabra y elige
    la frase más específica, para entender «mi cédula de identidad» o «quiero
    vender mi carro» sin exigir el nombre oficial del trámite.
    """
    t = ' ' + _normalize(text) + ' '
    best, best_score = None, 0
    for ident in ORDER:
        ficha = TRAMITES.get(ident)
        claves = list(_PATRONES_POR_ID.get(ident, ()))
        if ficha:
            claves += ficha.get('keywords') or []
        for key in claves:
            if _normalize(key).strip() in _DEBILES:
                continue
            score = _score_key(t, key)
            if score > best_score:
                best, best_score = ident, score
    if best:
        return best
    for ident, palabras in _GENERICAS:
        for key in palabras:
            if _score_key(t, key):
                return ident
    return None


def get(ident):
    return _aplicar_overrides(TRAMITES.get(ident))


def get_by_slug(slug):
    for t in TRAMITES.values():
        if t['slug'] == slug:
            return _aplicar_overrides(t)
    return None


def listado():
    return [_aplicar_overrides(TRAMITES[i]) for i in ORDER]


def resumen(ident):
    """Versión liviana para tarjetas y listas."""
    t = _aplicar_overrides(TRAMITES.get(ident))
    if not t:
        return None
    return {k: t[k] for k in ('id', 'slug', 'n', 'cat', 'icon', 'tag', 'resumen',
                              'costo', 'tiempo', 'modalidad', 'url', 'qu')}
