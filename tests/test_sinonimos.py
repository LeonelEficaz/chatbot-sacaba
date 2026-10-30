# -*- coding: utf-8 -*-
"""Reconocimiento de trámites con frases naturales y navegación a su ficha."""

import pytest

from chatbot import engine
from chatbot import tramites as tramites_data
from app import app as flask_app


CASOS = [
    ("quiero sacar mi cedula de identidad", "carnet"),
    ("mi documento", "carnet"),
    ("perdi mi carnet", "carnet"),
    ("quiero manejar", "licencia_conducir"),
    ("mi licencia vencida", "licencia_conducir"),
    ("necesito mi papelito de conducta", "antecedentes"),
    ("quiero abrir una tienda", "licencia_funcionamiento"),
    ("quiero registrar mi terrenito", "empadronamiento_predial"),
    ("cuanto vale mi casa", "avaluo_catastral"),
    ("quiero vender mi carro", "transferencia_vehiculo"),
    ("registrar mi moto nueva", "inscripcion_vehiculo"),
    ("me multaron por exceso de velocidad", "multas_transito"),
    ("la revision tecnica de mi auto", "inspeccion_tecnica_vehicular"),
    ("pagar el impuesto de mi casa", "impuesto_predial"),
    ("constancia de no deuda", "no_deuda"),
    ("quiero inscribir a mi bebe", "certificado_nacimiento"),
    ("quiero construir mi casa", "plano_vivienda"),
]


@pytest.mark.parametrize("frase,esperado", CASOS)
def test_detecta_sinonimos(frase, esperado):
    assert tramites_data.detect(frase) == esperado


@pytest.mark.parametrize("frase", ["hola sami", "que haces", "gracias por la ayuda"])
def test_saludos_no_abren_ficha(frase):
    assert tramites_data.detect(frase) is None


def test_chat_devuelve_tramite_para_frase_natural():
    cliente = flask_app.test_client()
    resp = cliente.post("/chat", json={"message": "quiero sacar mi cedula de identidad",
                                       "useAI": False})
    assert resp.status_code == 200
    assert resp.get_json()["tramite"] == "carnet"


def test_todas_las_fichas_tienen_palabras_clave_utiles():
    for ficha in tramites_data.listado():
        assert ficha.get("keywords"), ficha["id"]


def test_respuesta_local_usa_datos_de_la_ficha():
    texto = engine.get_resp("quiero vender mi carro", "es")
    ficha = tramites_data.get("transferencia_vehiculo")
    assert ficha["url"] in texto
    assert ficha["n"] in texto


def test_respuesta_local_enchufa_con_busqueda_por_sinonimo():
    texto = engine.get_resp("mi terrenito", "es")
    ficha = tramites_data.get("empadronamiento_predial")
    assert ficha["url"] in texto
