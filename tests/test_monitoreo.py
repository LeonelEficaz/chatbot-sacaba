# -*- coding: utf-8 -*-
"""Pruebas del monitoreo: bitácora de eventos, salud, métricas y glosario persistente.

Cubren lo que hace posibles los reportes de seguimiento: cada consulta deja su
evento, los agregados salen de esos eventos, ningún texto del ciudadano se
guarda, y las palabras que enseña el público sobreviven al reinicio.

Ejecutar:
    python -m pytest tests/test_monitoreo.py -v
"""
import base64
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from app import app
from chatbot import bitacora, engine


class ConBitacoraTemporal(unittest.TestCase):
    """Cada prueba escribe su bitácora en un directorio desmontable."""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        self.dir = Path(tempfile.mkdtemp(prefix="bitacora_prueba_"))
        self.ruta = self.dir / "bitacora_eventos.jsonl"
        parche = mock.patch.object(bitacora, "RUTA", self.ruta)
        parche.start()
        self.addCleanup(parche.stop)
        self.addCleanup(shutil.rmtree, self.dir, True)

    def lineas(self):
        return [json.loads(l) for l in self.ruta.read_text(encoding="utf-8").splitlines()]


class TestRegistroDeConsultas(ConBitacoraTemporal):
    def test_cada_consulta_deja_su_evento(self):
        self.client.post("/chat", json={"message": "cuanto cuesta la licencia de circular"})
        eventos = self.lineas()
        self.assertEqual(len(eventos), 1)
        ev = eventos[0]
        self.assertEqual(ev["tipo"], "consulta")
        self.assertEqual(ev["via"], "texto")
        self.assertIn(ev["capa"], {"ficha", "cache", "openai", "gemini", "free", "local"})
        self.assertTrue(ev["entendio"])
        self.assertGreaterEqual(ev["latencia_ms"], 0)

    def test_la_bitacora_no_guarda_lo_que_escribe_el_ciudadano(self):
        self.client.post("/chat", json={"message": "donde pago la multa de circulacion"})
        ev = self.lineas()[0]
        self.assertEqual(set(ev), {"ts", "tipo", "via", "idioma", "capa",
                                   "entendio", "latencia_ms", "largo"})
        for palabra in ("multa", "circulacion", "pago", "donde"):
            self.assertNotIn(palabra, json.dumps(ev))

    def test_el_repintado_sin_ia_no_cuenta_como_consulta(self):
        """Al cambiar de idioma el widget repasa el historial con useAI=false:
        eso no es una pregunta nueva y no debe inflar los reportes."""
        self.client.post("/chat", json={"message": "licencia de circular", "useAI": False})
        self.assertFalse(self.ruta.exists())

    def test_el_cambio_de_idioma_deja_su_evento(self):
        self.client.post("/chat", json={"message": "habla en quechua"})
        self.assertEqual(self.lineas()[0]["capa"], "comando")

    def test_una_no_entendida_registra_el_fallo(self):
        with mock.patch("app.get_ai_resp", return_value=""):
            self.client.post("/chat", json={"message": "asdfghj"})
        ev = self.lineas()[0]
        self.assertFalse(ev["entendio"])


class TestRutasDeVoz(ConBitacoraTemporal):
    def test_el_dictado_del_servidor_deja_su_evento(self):
        with mock.patch("chatbot.stt.transcribir", return_value="horarios de atencion"):
            r = self.client.post("/api/stt", json={
                "audio": base64.b64encode(b"RIFF").decode(), "language": "es"})
        self.assertEqual(r.status_code, 200)
        ev = self.lineas()[0]
        self.assertEqual(ev["tipo"], "dictado")
        self.assertTrue(ev["entendio"])
        self.assertEqual(ev["largo"], len("horarios de atencion"))

    def test_el_dictado_vacio_registra_el_fallo(self):
        with mock.patch("chatbot.stt.transcribir", return_value=""):
            self.client.post("/api/stt", json={"audio": base64.b64encode(b"RIFF").decode()})
        self.assertFalse(self.lineas()[0]["entendio"])

    def test_la_llamada_de_voz_deja_su_evento(self):
        respuesta = {"texto": "Allinllachu", "dicho": "allinllachu",
                     "espanol": "estoy bien", "proveedor": "gemini"}
        with mock.patch("app.voz_responder", return_value=respuesta):
            r = self.client.post("/api/voice", json={
                "audio": base64.b64encode(b"WEBM").decode(), "language": "qu"})
        self.assertEqual(r.status_code, 200)
        ev = self.lineas()[0]
        self.assertEqual(ev["via"], "voz")
        self.assertEqual(ev["capa"], "audio")
        self.assertEqual(ev["proveedor"], "gemini")

    def test_la_llamada_sin_audio_se_registra_como_fallo(self):
        with mock.patch("app.voz_responder", return_value={"texto": "  "}):
            self.client.post("/api/voice", json={"audio": base64.b64encode(b"WEBM").decode()})
        ev = self.lineas()[0]
        self.assertEqual(ev["via"], "voz")
        self.assertFalse(ev["entendio"])

    def test_la_sintesis_deja_su_evento(self):
        with mock.patch("app.tts_sintetizar", return_value=Path("audio/tts/x.mp3")):
            self.client.post("/api/tts", json={"text": "Buenas tardes, soy Sami"})
        ev = self.lineas()[0]
        self.assertEqual(ev["tipo"], "sintesis")
        self.assertTrue(ev["entendio"])


class TestMetricas(ConBitacoraTemporal):
    def proveedores_falsos(self):
        return {
            "openai": {"vivo": False, "motivo": "cuenta sin creditos"},
            "gemini": {"vivo": False, "motivo": "clave marcador de posicion"},
            "traductor": {"vivo": True, "gratis": True},
            "free": {"vivo": True, "activa": True},
            "local": {"vivo": True, "motivo": "siempre responde sin internet"},
        }

    def test_health_responde_y_confirma_la_atencion(self):
        with mock.patch("app.estado_proveedores", return_value=self.proveedores_falsos()):
            r = self.client.get("/health")
        self.assertEqual(r.status_code, 200)
        datos = r.get_json()
        self.assertEqual(datos["estado"], "ok")
        self.assertTrue(datos["atencion_garantizada"])
        self.assertEqual(datos["proveedores_vivos"], 3)
        self.assertGreaterEqual(datos["minutos_activo"], 0)

    def test_metricas_agrega_las_consultas(self):
        for pregunta in ("licencia de circular", "multa de circulacion", "horarios de atencion"):
            self.client.post("/chat", json={"message": pregunta})
        with mock.patch("app.estado_proveedores", return_value=self.proveedores_falsos()):
            r = self.client.get("/api/metricas?dias=7")
        self.assertEqual(r.status_code, 200)
        datos = r.get_json()
        self.assertEqual(datos["consultas"], 3)
        self.assertEqual(datos["por_via"], {"texto": 3})
        self.assertEqual(datos["tasa_de_respuesta"], 100.0)
        self.assertIsNotNone(datos["latencia_ms"]["p50"])
        self.assertIn("local", datos["proveedores"])

    def test_metricas_sin_bitacora_no_rompe(self):
        with mock.patch("app.estado_proveedores", return_value=self.proveedores_falsos()):
            r = self.client.get("/api/metricas")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["consultas"], 0)
        self.assertIsNone(r.get_json()["latencia_ms"]["p95"])

    def test_el_dia_pide_entero_y_se_sujeta_al_rango(self):
        with mock.patch("app.estado_proveedores", return_value=self.proveedores_falsos()):
            self.assertEqual(self.client.get("/api/metricas?dias=noesnumero"
                                             ).get_json()["periodo_dias"], 7)
            self.assertEqual(self.client.get("/api/metricas?dias=99999"
                                             ).get_json()["periodo_dias"], 365)


class TestGlosarioPersistido(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp(prefix="glosario_prueba_"))
        parche = mock.patch.object(engine, "GLOSARIO_FILE", self.dir / "glosario.json")
        parche.start()
        self.addCleanup(parche.stop)
        self.addCleanup(shutil.rmtree, self.dir, True)
        engine._GLOSARIO_APRENDIDO.clear()

    def test_lo_que_ensena_el_publico_queda_en_disco(self):
        engine.learn_quechua_word("mercado", "qhatuwia")
        self.assertTrue((self.dir / "glosario.json").exists())
        guardado = json.loads((self.dir / "glosario.json").read_text(encoding="utf-8"))
        self.assertEqual(guardado["mercado"]["qu"], "qhatuwia")

    def test_sobrevive_al_reinicio_del_servidor(self):
        engine.learn_quechua_word("feria", "qhatuwi")
        engine._GLOSARIO_APRENDIDO.clear()
        engine.QUECHUA_LOCAL_DB.pop("feria")
        engine._cargar_glosario_aprendido()
        self.assertEqual(engine.QUECHUA_LOCAL_DB["feria"]["qu"], "qhatuwi")

    def test_la_ruta_devuelve_el_conteo_aprendido(self):
        app.config["TESTING"] = True
        cliente = app.test_client()
        cliente.post("/api/dictionary/learn", json={"spanish": "olleria", "quechua": "qhatuwi"})
        datos = cliente.get("/api/dictionary/stats").get_json()
        self.assertEqual(datos["aprendidas_por_el_publico"], 1)


class TestTopeDeBitacora(ConBitacoraTemporal):
    def test_el_archivo_no_crece_sin_freno(self):
        with mock.patch.object(bitacora, "MAX_BYTES", 600):
            for i in range(60):
                bitacora.registrar("consulta", via="texto", idioma="es", capa="local",
                                   latencia_ms=i, entendio=True)
        self.assertLessEqual(self.ruta.stat().st_size, 1400)
        self.assertGreater(len(self.lineas()), 0)

    def test_una_bitacora_irlegible_no_rompe_el_reporte(self):
        self.ruta.write_text("no es json\n{}\n", encoding="utf-8")
        self.assertEqual(bitacora.resumen(0)["registros"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
