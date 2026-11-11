# -*- coding: utf-8 -*-
"""Voz neuronal gratuita para el asistente.

Usa edge-tts (voces neuronales de Microsoft Edge) con la voz boliviana
es-BO-SofiaNeural. El quechua se pronuncia con la misma voz, pero antes se
adapta la grafía (aspiradas, uvular, semivocal) y la acentuación al sistema
castellano para que se entienda; si el navegador tiene una voz nativa `qu`,
el cliente la prefiere.
"""

import asyncio
import hashlib
import re
from pathlib import Path

try:
    import edge_tts
    DISPONIBLE = True
except ImportError:  # la app sigue funcionando con la voz del navegador
    edge_tts = None
    DISPONIBLE = False

VOCES = {
    'es-BO-SofiaNeural': {'nombre': 'Sofía (Bolivia)', 'genero': 'femenina'},
    'es-BO-MarceloNeural': {'nombre': 'Marcelo (Bolivia)', 'genero': 'masculina'},
}
VOZ_PREDETERMINADA = 'es-BO-SofiaNeural'

CACHE_DIR = Path(__file__).resolve().parent.parent / 'static' / 'audio' / 'tts'
MAX_CARACTERES = 900


VOCALES = 'aeiou'
ACENTOS = {'a': 'á', 'e': 'é', 'i': 'í', 'o': 'ó', 'u': 'ú'}
LETRAS = re.compile(r'[A-Za-zÁÉÍÓÚÑáéíóúñ\x03]+')

# Palabras frecuentes que la voz castellana lee mal con las reglas generales.
LEXICO = {
    'quechua': 'kechua', 'quechuapi': 'kechuapi', 'quechuata': 'kechuata',
    'quechuamanta': 'kechuamanta', 'quichua': 'kichua',
    'qhapaq': 'japak', 'qhapaqnan': 'japakñan', 'qhapaqñan': 'japakñan',
    'ñoqanchik': 'nukanchik', 'ñuqanchik': 'nukanchik',
    'ñoqayku': 'nukayku', 'ñuqayku': 'nukayku',
    'tupananchiskama': 'tupanchiskama', 'tupananchikama': 'tupanchikama',
}
# Préstamos castellanos con h muda: en quechua se mantiene el sonido español.
H_MUDA = {
    'hospital', 'hospitales', 'hotel', 'hora', 'horas', 'horario', 'horarios',
    'humano', 'humana', 'historia', 'hielo', 'alcohol', 'hola', 'hasta',
}


def _acentuar_palabra(palabra):
    """Marca la penúltima sílaba (ritmo quechua) en palabras graves.

    El castellano ya acentúa así las terminadas en vocal, n o s; las demás
    (k, l, r, y...) las leería agudas y el quechua sonaría cortado."""
    minus = palabra.lower()
    if any(c in 'áéíóú' for c in minus):
        return palabra
    inicios = [
        i for i, c in enumerate(minus)
        if c in VOCALES and (i == 0 or minus[i - 1] not in VOCALES)
    ]
    if len(inicios) < 2:
        return palabra
    if palabra.isupper() and len(palabra) <= 6:
        return palabra
    # Solo finales propios del quechua: evita acentuar prestamos como carnet.
    if minus[-1] not in 'kqylrmpw\x03':
        return palabra
    # Sufijos del castellano: un infinitivo o un adjetivo en -al tampoco es
    # quechua, por mucho que termine en consonante.
    if minus[-2:] in ('al', 'ar', 'er', 'ir', 'oz', 'uz'):
        return palabra
    pos = inicios[-2]
    letra = palabra[pos]
    acento = ACENTOS.get(letra.lower())
    if not acento:
        return palabra
    return palabra[:pos] + (acento.upper() if letra.isupper() else acento) + palabra[pos + 1:]


def _preparar_palabra(palabra):
    minus = palabra.lower()
    if minus in H_MUDA:
        # Préstamo castellano: la h no se pronuncia (horario -> orario).
        return re.sub(r'^h', '', palabra, flags=re.I)
    if any(c in 'áéíóú' for c in minus):
        return palabra
    # "qu" + e/i es préstamo castellano (quechua -> kechua); "qu" + consonante
    # o a/o es quechua y la u se pronuncia (qullqi -> kullki).
    palabra = re.sub(r'qu(?=[ei])', 'k', palabra, flags=re.I)
    palabra = re.sub(r'q', 'k', palabra, flags=re.I)
    # h aspirada del quechua -> j (hamuy -> jamuy); la h de "ch" no cambia.
    palabra = re.sub(r'(?<!c)h', 'j', palabra, flags=re.I)
    return palabra


def _aplicar_lexico(palabra):
    reemplazo = LEXICO.get(palabra.lower())
    if not reemplazo:
        return palabra
    if palabra.isupper():
        return reemplazo.upper()
    if palabra[:1].isupper():
        return reemplazo.capitalize()
    return reemplazo


def adaptar_quechua(texto):
    """Reescribe el quechua con grafías que una voz castellana lee bien.

    - Quita el apóstrofo de las oclusivas glotalizadas (p'unchay -> punchay).
    - q uvular -> k, sh -> s, h aspirada -> j (hamuy -> jamuy).
    - w se lee "hu" ante vocal (wasi -> huasi) y "u" al final (punchaw -> punchau).
    - Acentúa la penúltima sílaba en palabras graves para conservar el ritmo
      del quechua; los préstamos castellanos no se tocan.
    """
    t = str(texto or '')
    if not t:
        return t
    t = t.replace("'", '').replace('’', '').replace('`', '')
    t = LETRAS.sub(lambda m: _aplicar_lexico(m.group(0)), t)
    t = re.sub(r'chh', 'ch', t, flags=re.I)
    t = re.sub(r'qh', 'k', t, flags=re.I)
    t = re.sub(r'sh', 's', t, flags=re.I)
    t = LETRAS.sub(lambda m: _preparar_palabra(m.group(0)), t)
    # La w se convierte en "hu" ante vocal (lectura /w/ del castellano) y en
    # "u" al final o ante consonante; se marca para no contar sílaba aparte.
    t = re.sub(r'w(?=[aeiouáéíóú])', '\x03', t, flags=re.I)
    t = re.sub(r'w', 'u', t, flags=re.I)
    t = LETRAS.sub(lambda m: _acentuar_palabra(m.group(0)), t)
    return t.replace('\x03', 'hu')


def _cifras(texto):
    """Escribe las cifras como las diria una persona.

    "Bs. 100 - 300" pasa a "100 a 300 bolivianos"; sin esto la voz se queda en
    un "Bs." suelto y el punto de la abreviatura parte la frase por la mitad.
    El lookbehind y el lookahead evitan romper las horas ("08:00 - 12:00").
    """
    # Las horas se dicen con "a": "08:00 – 12:00" -> "8:00 a 12:00".
    t = re.sub(r'(\d{1,2}:\d{2})\s*[-\u2013]\s*(\d{1,2}:\d{2})', r'\1 a \2', texto)
    # La moneda con rango va primero, si no "bolivianos" cae en medio del rango.
    t = re.sub(r'\bBs\.?\s*(\d[\d.,]*)\s*[-\u2013]\s*(\d[\d.,]*)',
               r'\1 a \2 bolivianos', t, flags=re.I)
    t = re.sub(r'(?<![\d:])(\d[\d.]{0,3})\s*[-\u2013]\s*(\d[\d.]{0,3})(?![\d:])',
               r'\1 a \2', t)
    t = re.sub(r'\bBs\.?\s*(\d[\d.,]*)', r'\1 bolivianos', t, flags=re.I)
    t = re.sub(r'(?<=\d),(\d{3})\b', r'.\1', t)
    return re.sub(r'\b0(\d{1,2}:\d{2}\b)', r'\1', t)


def limpiar(texto):
    limpio = str(texto or '')
    limpio = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', limpio)
    limpio = re.sub(r'https?://\S+', ' ', limpio)
    limpio = limpio.replace('**', '').replace('*', '').replace('`', '')
    limpio = _cifras(limpio)
    limpio = re.sub(r'^\s*[-•·]\s*', '', limpio, flags=re.M)
    limpio = re.sub(r'[\U0001F000-\U0001FAFF\u2600-\u27BF]', '', limpio)
    limpio = re.sub(r'\s+', ' ', limpio).strip()
    if len(limpio) > MAX_CARACTERES:
        corte = limpio[:MAX_CARACTERES]
        limpio = corte[:corte.rfind('.') + 1] if '.' in corte else corte
    return limpio


# Lo que Sami dice en voz alta es mas corto que la ficha que se ve en pantalla.
MAX_FRASES = 3
MAX_HABLADO = 260

# Las etiquetas de datos ("**Costo:** Bs. 17") se leen sin la etiqueta.
ETIQUETA = re.compile(
    r'^(?:donde|d\u00f3nde|c[o\u00f3]mo|cu[a\u00e1]ndo|costo|precio|tiempo|duraci\u00f3n|'
    r'consejo|requisitos|documentos|horario|horarios|contacto|tel\u00e9fono|'
    r'ubicaci\u00f3n|ubicacion|respuesta|quechua|ficha)\s*[:.\u2013-]\s*', re.I)

# Lineas que nunca se leen en voz alta: pie de ficha, enlaces, rutas internas.
SIN_VOZ = re.compile(
    r'^(?:ficha|ubicaci\u00f3n|ubicacion|enlace|link|mapa|'
    r'm\u00e1s\s+informaci\u00f3n|mas\s+informacion)\b', re.I)
ENLACE = re.compile(r'https?://\S+|(?<!\w)/[\w/-]{3,}')


def frase_hablada(texto):
    """Devuelve lo que Sami dice: dos o tres frases sueltas, sin enlaces.

    La ficha completa sigue visible en pantalla; la voz no lee encabezados,
    direcciones web ni la cola de datos porque eso suena a lector de pantalla
    y no a alguien que contesta.
    """
    bruto = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', str(texto or ''))
    bruto = re.sub(r'^\s*#{1,6}\s*', '', bruto, flags=re.M)
    frases = []
    for linea in bruto.split('\n'):
        linea = linea.strip().strip('-\u2022\u00b7*').strip()
        if not linea or SIN_VOZ.match(linea):
            continue
        linea = _cifras(ENLACE.sub(' ', linea))
        linea = ETIQUETA.sub('', linea).replace('**', '').replace('*', '')
        introduccion = linea.rstrip().endswith(':')
        linea = re.sub(r'\s+', ' ', linea).strip(' :.\u2013-')
        if len(linea) < 3:
            continue
        for frase in re.split(r'(?<=[.!?])\s+', linea):
            frase = frase.strip(' \u2013-')
            if len(frase) >= 3:
                frases.append((frase, introduccion))
    if not frases:
        return limpiar(texto)
    hablado = ''
    previa_es_introduccion = False
    for frase, introduccion in frases[:MAX_FRASES]:
        if hablado and len(hablado) + 2 + len(frase) > MAX_HABLADO:
            break
        if hablado:
            if hablado[-1] not in '.!?':
                # Una linea que anuncia datos ("Los horarios son:") sigue
                # hablando; un punto ahi suena a corte y no a frase nueva.
                hablado += ', ' if previa_es_introduccion else '. '
            elif not hablado.endswith(' '):
                hablado += ' '
        hablado += frase
        previa_es_introduccion = introduccion
    return limpiar(hablado)


async def _generar(texto, voz, rate):
    comunicador = edge_tts.Communicate(texto, voz, rate=rate)
    audio = bytearray()
    async for trozo in comunicador.stream():
        if trozo['type'] == 'audio':
            audio.extend(trozo['data'])
    return bytes(audio)


def sintetizar(texto, voz=VOZ_PREDETERMINADA, lang='es'):
    """Devuelve la ruta del MP3 generado, o None si no se pudo sintetizar."""
    if not DISPONIBLE:
        return None
    limpio = frase_hablada(texto)
    if not limpio:
        return None
    if voz not in VOCES:
        voz = VOZ_PREDETERMINADA

    if lang == 'qu':
        limpio = adaptar_quechua(limpio)
        if not limpio:
            return None
    # Sami habla, no deletrea: el quechua solo lleva una ligera pausa para que
    # se distingan las silabas adaptadas, nada de cadencia silabica.
    rate = '-4%' if lang == 'qu' else '+5%'
    clave = hashlib.sha256((voz + '|' + rate + '|' + limpio).encode('utf-8')).hexdigest()[:24]
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    destino = CACHE_DIR / (clave + '.mp3')
    if destino.exists() and destino.stat().st_size > 512:
        return destino

    audio = b''
    for intento in range(2):
        try:
            audio = asyncio.run(_generar(limpio, voz, rate))
        except Exception:
            audio = b''
        if len(audio) >= 512:
            break
    if len(audio) < 512:
        return None
    temporal = destino.with_suffix('.tmp')
    temporal.write_bytes(audio)
    temporal.replace(destino)
    return destino


def estado():
    return {
        'disponible': DISPONIBLE,
        'motor': 'edge-tts (Microsoft Edge)',
        'voces': [{'id': k, **v} for k, v in VOCES.items()],
        'predeterminada': VOZ_PREDETERMINADA,
        'nota': 'Voz neuronal boliviana gratuita. El quechua se adapta a la fonética castellana (q→k, h→j, w→u/hu) y la voz lee dos o tres frases mientras la ficha completa se ve en pantalla; el navegador usa una voz nativa qu si existe.',
    }
