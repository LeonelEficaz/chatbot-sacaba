# -*- coding: utf-8 -*-
"""
PRUEBAS DE CAJA NEGRA - Chatbot Municipal de Sacaba
Se evalua el sistema desde el EXTERIOR: entradas -> salidas observables,
sin conocer el codigo interno. Se usan las tecnicas de:
  - Particion de equivalencia (clases CE)
  - Analisis de valores limite (casos VL)

Sistema bajo prueba: API HTTP de Flask (app.py)
  POST /chat      {message, language}  -> 200 {response, options, language} | 400 {error}
  POST /language  {language}           -> 200 {language} | 400 {error}

Ejecutar:
    python -m pytest tests/test_caja_negra.py -v
"""
import base64
import json
import unittest
from unittest import mock

from app import app


class CajaNegraChat(unittest.TestCase):
    """POST /chat"""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def chat(self, payload=None, raw=None):
        if raw is not None:
            return self.client.post("/chat", data=raw,
                                    content_type="application/json")
        return self.client.post("/chat", data=json.dumps(payload or {}),
                                content_type="application/json")

    # ---------- PARTICION DE EQUIVALENCIA ----------

    def test_ce01_consulta_valida_de_tramite(self):
        r = self.chat({"message": "Â¿CuÃ¡nto cuesta el carnet?", "language": "es"})
        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertIn("Bs.", data["response"])
        self.assertIn("language", data)

    def test_ce02_saludo_valido(self):
        r = self.chat({"message": "hola", "language": "es"})
        self.assertEqual(r.status_code, 200)
        self.assertIn("Sacaba", r.get_json()["response"])

    def test_ce03_pregunta_en_quechua(self):
        r = self.chat({"message": "Imaynallan, lakispa yachay", "language": "qu"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["language"], "qu")

    def test_ce04_texto_no_reconocido_respuesta_default(self):
        r = self.chat({"message": "xyzabc sin sentido", "language": "es"})
        self.assertEqual(r.status_code, 200)
        self.assertIn("puedo aprenderla", r.get_json()["response"])

    def test_ce05_campo_message_ausente(self):
        r = self.chat({"language": "es"})
        self.assertEqual(r.status_code, 400)
        self.assertIn("error", r.get_json())

    def test_ce06_idioma_invalido_auto_detecta(self):
        r = self.chat({"message": "hola", "language": "en"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["language"], "es")

    def test_ce07_cuerpo_no_json(self):
        r = self.chat(raw="esto no es json")
        self.assertEqual(r.status_code, 400)

    def test_ce08_message_no_es_texto(self):
        r = self.chat({"message": 12345, "language": "es"})
        self.assertEqual(r.status_code, 400)

    def test_ce09_metodo_no_permitido_get(self):
        r = self.client.get("/chat")
        self.assertEqual(r.status_code, 405)

    def test_ce10_consulta_multas(self):
        r = self.chat({"message": "multas de transito", "language": "es"})
        self.assertEqual(r.status_code, 200)
        resp = r.get_json()["response"]
        self.assertIn("Exceso de velocidad", resp)
        self.assertIn("Municipales", resp)

    def test_ce11_menu_de_tramites(self):
        r = self.chat({"message": "lista de tramites", "language": "es"})
        resp = r.get_json()["response"]
        for tramite in ("Carnet", "Residencia", "Licencia de Funcionamiento"):
            self.assertIn(tramite, resp)

    # ---------- ANALISIS DE VALORES LIMITE ----------

    def test_vl01_mensaje_vacio(self):
        r = self.chat({"message": "", "language": "es"})
        self.assertEqual(r.status_code, 200)
        self.assertTrue(len(r.get_json()["response"]) > 0)

    def test_vl02_mensaje_solo_espacios(self):
        r = self.chat({"message": "   ", "language": "es"})
        self.assertEqual(r.status_code, 200)
        self.assertNotEqual(r.get_json()["response"], "")

    def test_vl03_un_solo_caracter(self):
        r = self.chat({"message": "?", "language": "es"})
        self.assertEqual(r.status_code, 200)

    def test_vl04_mensaje_muy_largo(self):
        r = self.chat({"message": "carnet " * 1000, "language": "es"})
        self.assertEqual(r.status_code, 200)
        self.assertIn("Bs. 17", r.get_json()["response"])

    def test_vl05_idioma_vacio_auto_detecta(self):
        r = self.chat({"message": "hola", "language": ""})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["language"], "es")

    def test_vl06_idioma_mayusculas_auto_detecta(self):
        r = self.chat({"message": "hola", "language": "ES"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["language"], "es")

    def test_vl07_idioma_nulo_auto_detecta(self):
        r = self.chat({"message": "hola", "language": None})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["language"], "es")

    def test_vl08_idioma_por_defecto_cuando_no_se_envia(self):
        r = self.chat({"message": "hola"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["language"], "es")


class CajaNegraLanguage(unittest.TestCase):
    """POST /language"""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def lang(self, value):
        return self.client.post("/language", data=json.dumps({"language": value}),
                                content_type="application/json")

    def test_cl01_idioma_es_valido(self):
        r = self.lang("es")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json(), {"language": "es"})

    def test_cl02_idioma_qu_valido(self):
        r = self.lang("qu")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json(), {"language": "qu"})

    def test_cl03_idioma_inexistente(self):
        r = self.lang("pt")
        self.assertEqual(r.status_code, 400)

    def test_cl04_campo_language_ausente(self):
        r = self.client.post("/language", data=json.dumps({}),
                             content_type="application/json")
        self.assertEqual(r.status_code, 400)


class CajaNegraInterfazWeb(unittest.TestCase):
    """GET / (pagina principal)"""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_ci01_pagina_principal_responde_200(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)

    def test_ci02_pagina_contiene_widget_del_chatbot(self):
        r = self.client.get("/")
        html = r.get_data(as_text=True)
        self.assertIn("chatbot-widget", html)


class CajaNegraTraduccionIA(unittest.TestCase):
    """POST /api/translate y GET /api/ai-status (traduccion de pagina con IA)"""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def translate(self, payload=None, raw=None):
        if raw is not None:
            return self.client.post("/api/translate", data=raw,
                                    content_type="application/json")
        return self.client.post("/api/translate", data=json.dumps(payload),
                                content_type="application/json")

    @mock.patch("app.translate_page", return_value={"t1": "Buenos p'unchay"})
    def test_tt01_traduccion_valida_con_ia(self, _mock):
        r = self.translate({"items": [{"id": "t1", "text": "Buenos dias"}]})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["translations"], {"t1": "Buenos p'unchay"})

    def test_tt02_campo_items_ausente(self):
        r = self.translate({"texto": "hola"})
        self.assertEqual(r.status_code, 400)

    def test_tt03_items_no_es_lista(self):
        r = self.translate({"items": "hola"})
        self.assertEqual(r.status_code, 400)

    def test_tt04_lista_vacia_de_items(self):
        r = self.translate({"items": []})
        self.assertEqual(r.status_code, 400)

    def test_tt05_lista_muy_grande(self):
        r = self.translate({"items": [{"id": str(i), "text": "hola"} for i in range(501)]})
        self.assertEqual(r.status_code, 400)

    def test_tt06_cuerpo_no_json(self):
        r = self.translate(raw="esto no es json")
        self.assertEqual(r.status_code, 400)

    @mock.patch("app.translate_page", return_value=None)
    def test_tt07_ia_no_disponible_devuelve_503(self, _mock):
        r = self.translate({"items": [{"id": "t1", "text": "Buenos dias"}]})
        self.assertEqual(r.status_code, 503)

    def test_tt08_estado_de_ia(self):
        r = self.client.get("/api/ai-status")
        self.assertEqual(r.status_code, 200)
        self.assertIn("ai", r.get_json())

    def test_tt09_items_invalidos_se_filtran(self):
        # La lista existe pero ningun item es {id, texto} valido -> 400
        r = self.translate({"items": ["texto", {}, {"text": "   "}]})
        self.assertEqual(r.status_code, 400)


class CajaNegraAudio(unittest.TestCase):
    """POST /audio-to-text (transcripcion de audio)"""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def _post(self, payload=None, raw=None):
        if raw is not None:
            return self.client.post("/audio-to-text", data=raw,
                                    content_type="application/json")
        return self.client.post("/audio-to-text", data=json.dumps(payload or {}),
                                content_type="application/json")

    @mock.patch("app.transcribe_audio", return_value="hola que tal")
    def test_ta01_audio_valido_transcribe(self, _mock):
        audio_b64 = base64.b64encode(b"datos de audio").decode("ascii")
        r = self._post({"audio": audio_b64, "language": "es"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json(), {"text": "hola que tal"})

    def test_ta02_falta_campo_audio(self):
        r = self._post({"language": "es"})
        self.assertEqual(r.status_code, 400)
        self.assertIn("error", r.get_json())

    def test_ta03_audio_base64_invalido(self):
        r = self._post({"audio": "%%%no-es-base64%%%", "language": "es"})
        self.assertEqual(r.status_code, 500)

    def test_ta04_error_de_ia_quedara_en_500(self):
        with mock.patch("app.transcribe_audio",
                        side_effect=Exception("API sin configurar")):
            audio_b64 = base64.b64encode(b"audio").decode("ascii")
            r = self._post({"audio": audio_b64, "language": "es"})
        self.assertEqual(r.status_code, 500)
        self.assertIn("Error al procesar audio", r.get_json()["error"])

    def test_ta05_cuerpo_no_json(self):
        r = self._post(raw="esto no es json")
        self.assertEqual(r.status_code, 400)


if __name__ == "__main__":
    unittest.main(verbosity=2)

