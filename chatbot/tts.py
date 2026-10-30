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
    # Solo finales propios del quechua: evita acentuar prestamos como carnet.
    if minus[-1] not in 'kqylrmpw\x03':
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


def limpiar(texto):
    limpio = str(texto or '')
    limpio = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', limpio)
    limpio = re.sub(r'https?://\S+', ' ', limpio)
    limpio = limpio.replace('**', '').replace('*', '').replace('`', '')
    limpio = re.sub(r'\bBs\.?\s*(\d)', r'\1 bolivianos', limpio, flags=re.I)
    limpio = re.sub(r'^\s*[-•·]\s*', '', limpio, flags=re.M)
    limpio = re.sub(r'[\U0001F000-\U0001FAFF\u2600-\u27BF]', '', limpio)
    limpio = re.sub(r'\s+', ' ', limpio).strip()
    if len(limpio) > MAX_CARACTERES:
        corte = limpio[:MAX_CARACTERES]
        limpio = corte[:corte.rfind('.') + 1] if '.' in corte else corte
    return limpio


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
    limpio = limpiar(texto)
    if not limpio:
        return None
    if voz not in VOCES:
        voz = VOZ_PREDETERMINADA

    if lang == 'qu':
        limpio = adaptar_quechua(limpio)
        if not limpio:
            return None
    rate = '-24%' if lang == 'qu' else '+0%'
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
        'nota': 'Voz neuronal boliviana gratuita. El quechua se adapta a la fonética castellana (q→k, h→j, w→u/hu) y se lee más lento; el navegador usa una voz nativa qu si existe.',
    }
