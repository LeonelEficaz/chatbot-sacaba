# -*- coding: utf-8 -*-
"""Bitácora de eventos del chatbot Sami.

Cada consulta atendida deja una línea en un archivo JSONL. Es la fuente de
datos de los reportes de seguimiento: sin ella el sistema no puede decir
cuántas preguntas recibió, qué capa del motor las respondió ni cuánto tardó.

No registra datos personales: se guarda el conteo y el resultado de cada
vuelta, no la identidad del ciudadano.
"""

import json
import threading
import time
from datetime import datetime

from chatbot.engine import _data_dir

RUTA = _data_dir() / 'bitacora_eventos.jsonl'
MAX_BYTES = 2_000_000

_lock = threading.Lock()
_ARRANQUE = time.monotonic()


def _ahora():
    return datetime.now().astimezone().isoformat(timespec='seconds')


def minutos_activo():
    """Minutos del proceso en pie; sirve para saber si la bitácora está viva."""
    return (time.monotonic() - _ARRANQUE) / 60.0


def _escribir(evento):
    RUTA.parent.mkdir(parents=True, exist_ok=True)
    if RUTA.exists() and RUTA.stat().st_size > MAX_BYTES:
        viejas = RUTA.read_text(encoding='utf-8').splitlines()
        RUTA.write_text('\n'.join(viejas[len(viejas) // 2:]) + '\n', encoding='utf-8')
    with RUTA.open('a', encoding='utf-8') as archivo:
        archivo.write(json.dumps(evento, ensure_ascii=False) + '\n')


def registrar(tipo, **datos):
    """Anota un evento. Nunca lanza excepción: la bitácora no puede cortar la atención."""
    evento = {'ts': _ahora(), 'tipo': tipo}
    evento.update({clave: valor for clave, valor in datos.items() if valor is not None})
    try:
        with _lock:
            _escribir(evento)
    except Exception:
        pass
    return evento


def eventos(ultima=2000):
    """Los últimos eventos guardados, del más antiguo al más nuevo."""
    try:
        lineas = RUTA.read_text(encoding='utf-8').splitlines()[-ultima:]
    except Exception:
        return []
    salida = []
    for linea in lineas:
        try:
            dato = json.loads(linea)
        except Exception:
            continue
        if isinstance(dato, dict):
            salida.append(dato)
    return salida


def _momento(evento):
    try:
        return datetime.fromisoformat(evento.get('ts')).timestamp()
    except Exception:
        return 0.0


def _recientes(evs, dias):
    if not dias:
        return evs
    corte = time.time() - dias * 86400
    return [ev for ev in evs if _momento(ev) >= corte]


def _conteo(evs, clave):
    resultado = {}
    for ev in evs:
        valor = ev.get(clave)
        if valor is not None:
            resultado[str(valor)] = resultado.get(str(valor), 0) + 1
    return resultado


def _pct(a, b):
    return round(100.0 * a / b, 1) if b else 0.0


def _percentil(ordenado, fraccion):
    if not ordenado:
        return None
    return ordenado[min(len(ordenado) - 1, int((len(ordenado) - 1) * fraccion))]


def resumen(dias=7):
    """Agregados de la bitácora: la base de los reportes R-01 a R-05."""
    evs = _recientes(eventos(), dias)
    consultas = [ev for ev in evs if ev.get('tipo') == 'consulta']
    dictado = [ev for ev in evs if ev.get('tipo') == 'dictado']
    sintesis = [ev for ev in evs if ev.get('tipo') == 'sintesis']
    latencias = sorted(ev['latencia_ms'] for ev in consultas
                       if isinstance(ev.get('latencia_ms'), int))
    entendidas = sum(1 for ev in consultas if ev.get('entendio'))
    dictados_ok = sum(1 for ev in dictado if ev.get('entendio'))
    sintesis_ok = sum(1 for ev in sintesis if ev.get('entendio'))

    return {
        'periodo_dias': dias,
        'consultas': len(consultas),
        'tasa_de_respuesta': _pct(entendidas, len(consultas)),
        'por_via': _conteo(consultas, 'via'),
        'por_idioma': _conteo(consultas, 'idioma'),
        'por_capa': _conteo(consultas, 'capa'),
        'por_proveedor': _conteo(consultas, 'proveedor'),
        'latencia_ms': {
            'p50': _percentil(latencias, 0.50),
            'p95': _percentil(latencias, 0.95),
            'max': latencias[-1] if latencias else None,
            'promedio': round(sum(latencias) / len(latencias)) if latencias else None,
        },
        'dictado': {'intentos': len(dictado), 'entendidos': dictados_ok,
                    'tasa': _pct(dictados_ok, len(dictado))},
        'sintesis': {'pedidos': len(sintesis), 'logrados': sintesis_ok,
                     'tasa': _pct(sintesis_ok, len(sintesis))},
        'registros': len(evs),
        'primera_actividad': evs[0].get('ts') if evs else None,
        'ultima_actividad': evs[-1].get('ts') if evs else None,
        'minutos_activo': round(minutos_activo(), 1),
    }
