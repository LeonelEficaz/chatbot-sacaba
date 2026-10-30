# -*- coding: utf-8 -*-
"""Punto de entrada WSGI para hosting (Render, Railway, etc.).

El servidor de desarrollo integrado de Flask no se usa en produccion: aqui
expone la misma aplicacion a Gunicorn mediante el objeto `app`.
"""

from app import app

application = app
