# -*- coding: utf-8 -*-
"""Reconocimiento de voz gratuito en el servidor.

El dictado del navegador (Web Speech API) depende del servicio de voz de
Microsoft/Google y de la opcion "Reconocimiento de voz en linea" de Windows;
cuando no esta disponible, la app graba el audio con MediaRecorder y lo
transcribe aqui. Usa el servicio gratuito de Google a traves de
`speech_recognition`, que acepta el codigo es-BO.
"""

import io

try:
  import speech_recognition as sr
  DISPONIBLE = True
except ImportError:  # la app sigue funcionando con el dictado del navegador
  sr = None
  DISPONIBLE = False

# El quechua se transcribe con el modelo castellano: la ortografia quechua
# usa grafias castellanas y el detector de idioma decide despues.
IDIOMAS = {'es': 'es-BO', 'qu': 'es-BO'}
MAX_BYTES = 6 * 1024 * 1024


def estado():
  return {'disponible': DISPONIBLE}


def transcribir(audio_bytes, language='es'):
  if not DISPONIBLE:
    raise RuntimeError('El reconocimiento de voz del servidor no esta instalado.')
  if not audio_bytes:
    raise ValueError('Audio vacio.')
  if len(audio_bytes) > MAX_BYTES:
    raise ValueError('El audio supera el maximo permitido.')

  idioma = IDIOMAS.get(language, 'es-BO')
  reconocedor = sr.Recognizer()
  reconocedor.energy_threshold = 220
  reconocedor.dynamic_energy_threshold = True
  with sr.AudioFile(io.BytesIO(audio_bytes)) as fuente:
    audio = reconocedor.record(fuente)
  return reconocedor.recognize_google(audio, language=idioma).strip()
