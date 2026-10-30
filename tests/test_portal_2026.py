# -*- coding: utf-8 -*-
"""Pruebas del portal 2026: fichas de trámites, páginas y voz neuronal.

Cubre la base de datos de 20 trámites (chatbot/tramites.py), las rutas
nuevas de app.py y la detección de trámites desde el chat.
"""
import json
import unittest

from app import app
from chatbot import tramites as T


class BasePortal(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()


class TestFichas(BasePortal):
    def test_hay_veinte_tramites(self):
        self.assertEqual(len(T.TRAMITES), 20)
        self.assertEqual(len(T.listado()), 20)

    def test_cada_ficha_esta_completa(self):
        for t in T.listado():
            with self.subTest(tramite=t["id"]):
                self.assertTrue(t["n"] and t["resumen"] and t["tag"])
                self.assertIn(t["cat"], T.CATEGORIES)
                self.assertGreaterEqual(len(t["intro"]), 3)
                self.assertGreaterEqual(len(t["requisitos"]), 5)
                self.assertGreaterEqual(len(t["pasos"]), 5)
                self.assertGreaterEqual(len(t["recomendaciones"]), 4)
                self.assertTrue(t["oficina"]["nombre"])
                self.assertTrue(t["fuente"])
                self.assertTrue(t["qu"]["resumen"])
                self.assertEqual(t["url"], "/tramite/" + t["slug"])

    def test_cada_tramite_tiene_horarios(self):
        for t in T.listado():
            with self.subTest(tramite=t["id"]):
                self.assertGreaterEqual(len(t["horarios"]), 2)
                self.assertTrue(t["horario_nota"])
                for h in t["horarios"]:
                    self.assertTrue(h["dias"] and h["horas"])

    def test_detecta_consultas_frecuentes(self):
        casos = {
            "quiero sacar mi carnet": "carnet",
            "renovar mi cedula": "carnet",
            "multas de transito": "multas_transito",
            "me multo el policia": "multas_transito",
            "pago con QR": "multas_transito",
            "licencia de conducir": "licencia_conducir",
            "antecedentes policiales": "antecedentes",
            "abrir negocio": "licencia_funcionamiento",
            "empadronar mi terreno": "empadronamiento_predial",
            "certificado catastral": "certificado_catastral",
            "transferencia de vehiculo": "transferencia_vehiculo",
            "ITV": "inspeccion_tecnica_vehicular",
            "no deuda": "no_deuda",
            "partida de nacimiento": "certificado_nacimiento",
        }
        for texto, esperado in casos.items():
            with self.subTest(texto=texto):
                self.assertEqual(T.detect(texto), esperado)

    def test_texto_sin_tramite_devuelve_none(self):
        self.assertIsNone(T.detect("¿cómo está el clima hoy?"))


class TestApiTramites(BasePortal):
    def test_listado(self):
        r = self.client.get("/api/tramites")
        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertEqual(data["total"], 20)
        self.assertEqual(len(data["tramites"]), 20)
        self.assertIn("identidad", data["categorias"])

    def test_filtro_por_categoria(self):
        r = self.client.get("/api/tramites?cat=multas")
        data = r.get_json()
        self.assertGreater(data["total"], 0)
        self.assertTrue(all(t["cat"] == "multas" for t in data["tramites"]))

    def test_categoria_invalida(self):
        r = self.client.get("/api/tramites?cat=inexistente")
        self.assertEqual(r.status_code, 400)

    def test_busqueda_por_texto(self):
        r = self.client.get("/api/tramites?q=carnet")
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(r.get_json()["total"], 1)

    def test_ficha_completa(self):
        r = self.client.get("/api/tramites/carnet")
        self.assertEqual(r.status_code, 200)
        ficha = r.get_json()
        self.assertEqual(ficha["n"], "Carnet de Identidad")
        self.assertIn("SEGIP", ficha["oficina"]["nombre"])

    def test_ficha_inexistente(self):
        self.assertEqual(self.client.get("/api/tramites/no-existe").status_code, 404)

    def test_relacionados(self):
        r = self.client.get("/api/tramites/carnet/relacionados")
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(len(r.get_json()["tramites"]), 1)

    def test_pagina_permalink(self):
        r = self.client.get("/tramite/carnet-de-identidad")
        self.assertEqual(r.status_code, 200)
        html = r.get_data(as_text=True)
        self.assertIn("Carnet de Identidad", html)
        self.assertIn("Requisitos", html)
        self.assertIn("Preguntar a Sami", html)
        self.assertIn("Horarios de atención", html)
        self.assertIn("Lunes a viernes", html)

    def test_las_veinte_paginas_responden(self):
        for t in T.listado():
            with self.subTest(tramite=t["id"]):
                r = self.client.get(t["url"])
                self.assertEqual(r.status_code, 200)
                html = r.get_data(as_text=True)
                self.assertIn("Horarios de atención", html)
                self.assertIn(t["horarios"][0]["horas"], html)

    def test_pagina_inexistente(self):
        r = self.client.get("/tramite/no-existe")
        self.assertEqual(r.status_code, 404)
        self.assertIn("No encontramos", r.get_data(as_text=True))

    def test_portada_carga_fichas(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        html = r.get_data(as_text=True)
        self.assertIn("SACABA_TRAMITES", html)
        self.assertIn("sami-cat", html)
        self.assertIn("Mesa de trabajo", html.replace("MESA DE TRABAJO", "Mesa de trabajo"))


class TestChatIntegrado(BasePortal):
    def test_chat_devuelve_tramite(self):
        r = self.client.post("/chat", data=json.dumps(
            {"message": "quiero sacar mi carnet", "language": "es"}),
            content_type="application/json")
        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertEqual(data["tramite"], "carnet")
        self.assertIn("response", data)

    def test_chat_sin_tramite(self):
        r = self.client.post("/chat", data=json.dumps(
            {"message": "hola", "language": "es"}),
            content_type="application/json")
        self.assertIsNone(r.get_json()["tramite"])


class TestContenidoQuechua(BasePortal):
    def test_todas_las_fichas_tienen_quechua_completo(self):
        campos = ("n", "tag", "resumen", "costo", "costo_detalle", "tiempo",
                  "modalidad", "intro", "requisitos", "pasos", "recomendaciones",
                  "oficina", "horarios", "horario_nota")
        for t in T.listado():
            with self.subTest(tramite=t["id"]):
                qu = t["qu"]
                for campo in campos:
                    self.assertIn(campo, qu)
                self.assertGreaterEqual(len(qu["intro"]), 3)
                self.assertGreaterEqual(len(qu["requisitos"]), 5)
                self.assertGreaterEqual(len(qu["pasos"]), 5)
                self.assertGreaterEqual(len(qu["recomendaciones"]), 4)
                self.assertGreaterEqual(len(qu["horarios"]), 2)
                for paso in qu["pasos"]:
                    self.assertTrue(paso["t"] and paso["d"])
                self.assertTrue(qu["oficina"]["nombre"])
                self.assertTrue(qu["oficina"]["direccion"])

    def test_el_quechua_no_repite_el_espanol(self):
        for t in T.listado():
            with self.subTest(tramite=t["id"]):
                self.assertNotEqual(t["qu"]["resumen"], t["resumen"])
                self.assertNotEqual(t["qu"]["intro"], t["intro"])

    def test_la_portada_entrega_el_contenido_quechua(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        html = r.get_data(as_text=True)
        self.assertIn("SACABA_TRAMITES", html)
        self.assertIn("Killachaw", html)


class TestVozInteractiva(BasePortal):
    def test_la_portada_activa_el_micro_al_entrar(self):
        js = self.client.get("/static/js/main.js").get_data(as_text=True)
        self.assertIn("query({ name: 'microphone' })", js)
        self.assertIn("arrancarConMicro", js)
        self.assertIn("SacabaSkipPresentation", js)

    def test_el_chat_cambia_de_idioma_con_la_voz(self):
        js = self.client.get("/static/chatbot/chatbot-widget.js").get_data(as_text=True)
        self.assertIn("porVoz", js)
        self.assertIn("data.detected", js)
        self.assertIn("QU_SUFIJOS", js)
        self.assertIn("SacabaDetectarIdioma", js)

    def test_chat_detecta_quechua_dictado(self):
        r = self.client.post("/chat", data=json.dumps(
            {"message": "carnetita horjoyta munani", "language": "auto"}),
            content_type="application/json")
        self.assertEqual(r.get_json()["detected"], "qu")


class TestTts(BasePortal):
    def test_estado(self):
        r = self.client.get("/api/tts/status")
        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertIn("disponible", data)
        self.assertIn("voces", data)
        self.assertEqual(data["predeterminada"], "es-BO-SofiaNeural")

    def test_texto_vacio(self):
        r = self.client.post("/api/tts", data=json.dumps({"text": "  "}),
                             content_type="application/json")
        self.assertEqual(r.status_code, 400)

    def test_texto_demasiado_largo(self):
        r = self.client.post("/api/tts", data=json.dumps({"text": "a" * 1501}),
                             content_type="application/json")
        self.assertEqual(r.status_code, 400)


if __name__ == "__main__":
    unittest.main()
