# -*- coding: utf-8 -*-
"""Traduccion de Google Translate sin clave de API.

El endpoint que usa la propia pagina de Translate (`translate_a/single`) no
pide registro y si tiene quechua (`qu`), que es justo lo que no tienen Whisper
ni el dictado del navegador. No es un servicio oficial: Google mira la huella
TLS y responde 429 al cliente HTTP de Python, asi que se intenta `requests` y,
si falla, `curl` (que si pasa) o se traduce en el navegador.

Nada de esto es un requisito: si el servicio cae, el boton devuelve el texto en
espanol y la conversacion sigue. Ninguna funcion lanza excepciones.
"""

import json
import os
import re
import shutil
import subprocess
import threading
import time
from urllib.parse import urlencode

import requests

URL_TRADUCCION = 'https://translate.googleapis.com/translate_a/single'
MAX_TEXTO = 1800
CACHE_MAX = 500
CACHE_TTL = 6 * 60 * 60

# El quechua de Google es el del sur (Cusco-Collao); se escribe igual que el
# quechua boliviano en la practica, y el adapter fonetico lo lee bien.
IDIOMAS = {'es': 'es', 'qu': 'qu'}

_lock = threading.Lock()
_cache = {}
_sondeo = {'valor': None, 'hasta': 0.0}


def _codigo(idioma):
    return IDIOMAS.get(str(idioma or 'es').lower()[:2], 'es')


def _exe_curl():
    exe = shutil.which('curl')
    if exe:
        return exe
    windows = r'C:\Windows\System32\curl.exe'
    return windows if os.path.exists(windows) else None


def _curl_url(url, timeout):
    exe = _exe_curl()
    if not exe:
        return None
    try:
        r = subprocess.run([exe, '-s', '--max-time', str(int(timeout)), url],
                           capture_output=True, timeout=timeout + 4)
    except Exception:
        return None
    if r.returncode != 0 or not r.stdout:
        return None
    try:
        return json.loads(r.stdout.decode('utf-8', 'ignore'))
    except Exception:
        return None


def _pedido(params, timeout):
    url = URL_TRADUCCION + '?' + urlencode(params)
    try:
        r = requests.get(url, timeout=timeout,
                         headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return _curl_url(url, timeout)


def _juntas(datos):
    """Arma la traduccion a partir de la respuesta de Translate."""
    if not isinstance(datos, list) or not datos or not isinstance(datos[0], list):
        return ''
    partes = []
    for bloque in datos[0]:
        if isinstance(bloque, list) and bloque and isinstance(bloque[0], str):
            partes.append(bloque[0])
    return ''.join(partes).strip()


def traducir(texto, origen='es', destino='qu', timeout=8):
    """Traduce con el servicio publico; devuelve '' si no hay respuesta."""
    t = re.sub(r'\s+', ' ', str(texto or '')).strip()[:MAX_TEXTO]
    if not t:
        return ''
    origen, destino = _codigo(origen), _codigo(destino)
    if origen == destino:
        return t
    clave = (origen, destino, t)
    ahora = time.time()
    with _lock:
        guardado = _cache.get(clave)
        if guardado and guardado[1] > ahora:
            return guardado[0]
    datos = _pedido({'client': 'gtx', 'sl': origen, 'tl': destino, 'dt': 't', 'q': t},
                    timeout)
    salida = _juntas(datos) if datos else ''
    if not salida:
        return ''
    with _lock:
        if len(_cache) >= CACHE_MAX:
            _cache.clear()
        _cache[clave] = (salida, ahora + CACHE_TTL)
    return salida


def a_espanol(texto, timeout=8):
    return traducir(texto, 'qu', 'es', timeout=timeout)


def disponible(refrescar=False):
    """True si el servicio responde; se recuerda dos minutos."""
    ahora = time.time()
    if not refrescar and _sondeo['valor'] is not None and _sondeo['hasta'] > ahora:
        return _sondeo['valor']
    ok = bool(traducir('hola', 'es', 'en', timeout=6))
    _sondeo['valor'] = ok
    _sondeo['hasta'] = ahora + 120
    return ok


def estado():
    return {
        'traductor': disponible(),
        'motor': 'Google Translate (servicio publico, sin clave)',
        'idiomas': {'es': 'espanol', 'qu': 'quechua del sur'},
        'nota': 'Traduce a quechua sin cuenta ni clave. No es un servicio '
                'oficial: si falla, Sami sigue respondiendo en espanol.',
    }
