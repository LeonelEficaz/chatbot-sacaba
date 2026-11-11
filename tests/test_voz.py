# -*- coding: utf-8 -*-
"""
PRUEBAS DE LA RUTA DE VOZ - Chatbot Municipal de Sacaba

Cubren el cambio del microfono: el audio se escucha en el modelo (los
reconocedores de voz no tienen quechua), la traduccion es->qu es un paso
obligatorio y el estado de los proveedores se reporta como es.

Ejecutar:
    python -m pytest tests/test_voz.py -v
"""
import unittest
from unittest import mock

from chatbot import engine

QUECHUA_OK = "Allillanchu. Multakuna qullqi pagana tiyan, carnetyki apamuna."


class FakeOpenAIError(Exception):
    """Parece el error 429 de una cuenta sin creditos."""


def cliente_sin_creditos():
    """Cliente de OpenAI simulado: el chat revienta por falta de saldo."""
    completions = mock.Mock()
    completions.create.side_effect = RuntimeError(
        "Error code: 429 - You have no credits remaining (insufficient_quota)")
    chat = mock.Mock()
    chat.completions = completions
    return mock.Mock(chat=chat)


class TestSepararEtiquetas(unittest.TestCase):
    """Unidad: engine._separar_etiquetas()"""

    def test_se01_los_tres_bloques(self):
        dicho, es, qu = engine._separar_etiquetas(
            "TRANSCRIPCION: Imaynanam.\nRESPUESTA: Hola, todo bien.\nQUECHUA: Allillanchu.")
        self.assertEqual(dicho, "Imaynanam.")
        self.assertEqual(es, "Hola, todo bien.")
        self.assertEqual(qu, "Allillanchu.")

    def test_se02_respuesta_sin_etiquetas(self):
        dicho, es, qu = engine._separar_etiquetas("una respuesta suelta")
        self.assertEqual(dicho, "")
        self.assertEqual(es, "una respuesta suelta")
        self.assertIsNone(qu)

    def test_se03_bloques_desordenados(self):
        _, es, qu = engine._separar_etiquetas(
            "QUECHUA: Allillanchu.\nRESPUESTA: Todo bien.")
        self.assertEqual(qu, "Allillanchu.")
        self.assertEqual(es, "Todo bien.")

    def test_se04_etiquetas_en_minusculas(self):
        _, es, qu = engine._separar_etiquetas("respuesta: Hola.\nquechua: Allillanchu.")
        self.assertEqual(es, "Hola.")
        self.assertEqual(qu, "Allillanchu.")


class TestTraducirAQuechua(unittest.TestCase):
    """Unidad: engine.traducir_a_quechua(), el paso obligatorio es->qu."""

    def test_tr01_traduce_con_gemini_y_quita_markdown(self):
        with mock.patch.object(engine, "_gemini_enviar",
                               return_value="```\nAllillanchu, yanapasqayki.\n```") as enviar:
            salida = engine.traducir_a_quechua("Hola, te ayudo.")
        self.assertEqual(salida, "Allillanchu, yanapasqayki.")
        self.assertTrue(enviar.called)

    def test_tr02_usa_nllb_si_gemini_y_google_no_responden(self):
        with mock.patch.object(engine, "_gemini_enviar", return_value=None):
            with mock.patch.object(engine.google_idioma, "traducir", return_value=""):
                with mock.patch.object(engine, "_hf_nllb_translate",
                                       return_value="Yanapasqayki") as nllb:
                    salida = engine.traducir_a_quechua("Te ayudo.")
        self.assertEqual(salida, "Yanapasqayki")
        nllb.assert_called_once()

    def test_tr04_google_traduce_sin_clave_y_antes_que_nllb(self):
        with mock.patch.object(engine, "_gemini_enviar", return_value=None):
            with mock.patch.object(engine.google_idioma, "traducir",
                                   return_value="Yanapañasqayki") as google:
                with mock.patch.object(engine, "_hf_nllb_translate") as nllb:
                    salida = engine.traducir_a_quechua("Te ayudo.")
        self.assertEqual(salida, "Yanapañasqayki")
        google.assert_called_once_with("Te ayudo.", "es", "qu")
        nllb.assert_not_called()

    def test_tr03_texto_vacio_no_sale_a_la_red(self):
        with mock.patch.object(engine, "_gemini_enviar") as enviar:
            with mock.patch.object(engine.google_idioma, "traducir") as google:
                with mock.patch.object(engine, "_hf_nllb_translate") as nllb:
                    self.assertIsNone(engine.traducir_a_quechua("   "))
        self.assertFalse(enviar.called)
        self.assertFalse(google.called)
        self.assertFalse(nllb.called)


class TestVozResponder(unittest.TestCase):
    """Unidad: engine.voz_responder(), el audio directo al modelo."""

    def setUp(self):
        self.audio = b"audio-falso" * 100

    def test_vo01_exige_audio(self):
        for vacio in (b"", None):
            with self.assertRaises(ValueError):
                engine.voz_responder(vacio)

    def test_vo02_rechaza_audio_demasiado_grande(self):
        with mock.patch.object(engine, "_gemini_enviar") as enviar:
            with self.assertRaises(ValueError):
                engine.voz_responder(b"x" * (engine.MAX_AUDIO_BYTES + 1))
        self.assertFalse(enviar.called)

    def test_vo03_manda_el_audio_como_parte_del_pedido(self):
        pedidos = []

        def capturar(payload, timeout=25):
            pedidos.append(payload)
            return "TRANSCRIPCION: Imaynanam.\nRESPUESTA: Hola."

        with mock.patch.object(engine, "_gemini_enviar", side_effect=capturar):
            engine.voz_responder(self.audio, mime="audio/webm;codecs=opus", lang="es")

        partes = pedidos[0]["contents"][-1]["parts"]
        self.assertEqual(partes[0]["inlineData"]["mimeType"], "audio/webm")
        self.assertIn("data", partes[0]["inlineData"])
        sistema = pedidos[0]["systemInstruction"]["parts"][0]["text"]
        self.assertIn("Sami", sistema)

    def test_vo04_usa_el_bloque_quechua_del_modelo(self):
        if engine.detect_language(QUECHUA_OK) != "qu":
            self.skipTest("el motor no detecta el ejemplo de quechua")
        texto = ("TRANSCRIPCION: Imaynanam.\nRESPUESTA: Hola, todo bien.\nQUECHUA: "
                 + QUECHUA_OK)
        with mock.patch.object(engine, "_gemini_enviar", return_value=texto):
            with mock.patch.object(engine, "traducir_a_quechua") as traducir:
                salida = engine.voz_responder(self.audio, lang="qu")
        self.assertEqual(salida["texto"], QUECHUA_OK)
        self.assertEqual(salida["dicho"], "Imaynanam.")
        self.assertEqual(salida["espanol"], "Hola, todo bien.")
        self.assertFalse(traducir.called)

    def test_vo05_sin_bloque_quechua_traduce_aparte(self):
        with mock.patch.object(engine, "_gemini_enviar",
                               return_value="RESPUESTA: Hola, todo bien."):
            with mock.patch.object(engine, "traducir_a_quechua",
                                   return_value=QUECHUA_OK) as traducir:
                salida = engine.voz_responder(self.audio, lang="qu")
        traducir.assert_called_once_with("Hola, todo bien.")
        self.assertEqual(salida["texto"], QUECHUA_OK)
        self.assertEqual(salida["espanol"], "Hola, todo bien.")

    def test_vo06_en_espanol_no_traduce(self):
        with mock.patch.object(engine, "_gemini_enviar",
                               return_value="RESPUESTA: Hola, todo bien."):
            with mock.patch.object(engine, "traducir_a_quechua") as traducir:
                salida = engine.voz_responder(self.audio, lang="es")
        self.assertFalse(traducir.called)
        self.assertEqual(salida["texto"], "Hola, todo bien.")

    def test_vo07_sin_modelo_de_voz_usa_el_dictado_respaldo(self):
        with mock.patch.object(engine, "_gemini_enviar", return_value=None):
            with mock.patch.object(engine, "_stt_desde_audio",
                                   return_value="Que es la multa de transito"):
                with mock.patch.object(engine, "get_ai_resp",
                                       return_value="La multa es 25 Bs.") as chat:
                    salida = engine.voz_responder(self.audio, lang="es")
        self.assertEqual(salida["proveedor"], "stt")
        self.assertEqual(salida["dicho"], "Que es la multa de transito")
        chat.assert_called_once()

    def test_vo08_sin_gemini_ni_dictado_devuelve_nada(self):
        with mock.patch.object(engine, "_gemini_enviar", return_value=None):
            with mock.patch.object(engine, "_stt_desde_audio",
                                   side_effect=RuntimeError("sin speech_recognition")):
                with mock.patch.object(engine, "transcribe_audio",
                                       side_effect=FakeOpenAIError("sin creditos")):
                    self.assertIsNone(engine.voz_responder(self.audio))

    def test_vo09_el_bloque_quechua_solo_se_pide_en_quechua(self):
        pedidos = []

        def capturar(payload, timeout=25):
            pedidos.append(payload)
            return "RESPUESTA: Hola."

        with mock.patch.object(engine, "_gemini_enviar", side_effect=capturar):
            engine.voz_responder(self.audio, lang="es")
        with mock.patch.object(engine, "_gemini_enviar", side_effect=capturar):
            engine.voz_responder(self.audio, lang="qu")
        sistema_es = pedidos[0]["systemInstruction"]["parts"][0]["text"]
        sistema_qu = pedidos[1]["systemInstruction"]["parts"][0]["text"]
        self.assertNotIn("QUECHUA:", sistema_es)
        self.assertIn("QUECHUA:", sistema_qu)


class TestEstadoProveedores(unittest.TestCase):
    """El estado de la IA dice lo que el .env presume, no lo que responde."""

    def setUp(self):
        engine._sondeos.clear()

    def tearDown(self):
        engine._sondeos.clear()

    def test_ep01_gemini_hueco_del_env_se_reporta_como_tal(self):
        with mock.patch.object(engine, "GEMINI_API_KEY", "tu_api_key_aqui"):
            with mock.patch.object(engine, "GEMINI_AVAILABLE", False):
                vivo, motivo = engine._probar_gemini()
        self.assertFalse(vivo)
        self.assertIn("placeholder", motivo)

    def test_ep02_openai_sin_creditos_se_apaga(self):
        with mock.patch.object(engine, "_ai_available", True):
            with mock.patch.object(engine, "_client", cliente_sin_creditos()):
                with mock.patch.object(engine, "_openai_dead", False):
                    vivo, motivo = engine._probar_openai()
        self.assertFalse(vivo)
        self.assertEqual(motivo, "cuenta sin creditos")
        self.assertTrue(engine._openai_dead)

    def test_ep03_el_sondeo_se_recuerda(self):
        llamadas = []

        def probar():
            llamadas.append(1)
            return True, "activo"

        engine._sondeo("prueba_unitaria", probar)
        engine._sondeo("prueba_unitaria", probar)
        self.assertEqual(len(llamadas), 1)

    def test_ep04_estado_completo_de_los_proveedores(self):
        with mock.patch.object(engine, "_sondeo", return_value=(False, "sin clave")):
            estado = engine.estado_proveedores()
        for clave in ("openai", "gemini", "hf", "free", "voz", "local"):
            self.assertIn(clave, estado)
        self.assertIn("proveedor", estado["voz"])


class TestConfiguracionLeeElEnv(unittest.TestCase):
    """El .env se carga antes de leer las claves: si no, Gemini nunca existe."""

    def setUp(self):
        with open(engine.__file__, encoding="utf-8") as archivo:
            self.fuente = archivo.read()

    def test_cd01_load_env_antes_de_las_claves(self):
        carga = self.fuente.index("_load_env_file()\n")
        for variable in ("GEMINI_API_KEY = os.getenv", "GLOSBLE_API_KEY = os.getenv"):
            self.assertLess(carga, self.fuente.index(variable), variable)

    def test_cd02_detecta_huecos_del_env(self):
        self.assertFalse(engine._clave_real(""))
        self.assertFalse(engine._clave_real("tu_api_key_aqui"))
        self.assertFalse(engine._clave_real("TU_API_KEY_AQUI"))
        self.assertTrue(engine._clave_real("AIza" + "y" * 34))

    def test_cd03_una_clave_hueca_no_activa_proveedor(self):
        with mock.patch.object(engine, "GEMINI_API_KEY", "tu_api_key_aqui"):
            self.assertFalse(engine._clave_real(engine.GEMINI_API_KEY))


class TestQuechuaDictado(unittest.TestCase):
    """Unidad: engine.canon_qu() / hablado_quechua(), el quechua que llega mal escrito.
    Decisiones: grafia castellana, sufijos pegados, texto que no es quechua."""

    def test_qd01_la_grafia_del_dictado_suena_a_la_forma_oficial(self):
        self.assertEqual(engine.canon_qu("parlanguichu"), engine.canon_qu("parlankichu"))
        self.assertEqual(engine.canon_qu("jullqui"), engine.canon_qu("qullqi"))

    def test_qd02_reconoce_el_quechua_escrito_como_se_escucha(self):
        for dicho in ("parlanguichu", "parlanchu", "jullqui"):
            self.assertTrue(engine.hablado_quechua(dicho), dicho)
        # Frases completas: aqui manda detect_language, que usa tokens, sufijos
        # y el diccionario ademas del oido.
        for frase in ("imaynallan", "yusulpayki", "maypi nan",
                      "noga mumani carnet muna", "kanki ima"):
            self.assertEqual(engine.detect_language(frase), "qu", frase)

    def test_qd03_el_castellano_no_se_confunde_con_quechua(self):
        for dicho in ("cuanto cuesta el carnet de identidad",
                      "quiero pagar mi multa de transito",
                      "hola buenas tardes"):
            self.assertFalse(engine.hablado_quechua(dicho), dicho)

    def test_qd04_la_normalizacion_no_necesica_ninguna_clave(self):
        # Es el motivo por el que el quechua funciona tambien sin OpenAI ni Gemini.
        self.assertTrue(engine.NORMALIZACION_QUECHUA)
        with mock.patch.object(engine, "_ai_available", False):
            with mock.patch.object(engine, "GEMINI_AVAILABLE", False):
                self.assertEqual(engine.detect_language("parlanguichu"), "qu")
                interpretado = engine.interpret_quechua("parlanguichu")
                self.assertEqual(engine.detect_language(interpretado), "qu")

    def test_qd05_el_chat_detecta_el_idioma_del_dictado(self):
        from app import app
        with app.test_client() as cliente:
            resp = cliente.post("/chat", json={"message": "imaynallan", "lang": "qu"})
        datos = resp.get_json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(datos["detected"], "qu")
        self.assertTrue(datos["response"])


class TestEstadoVoz(unittest.TestCase):
    """El contrato de /api/voice/status: el widget no puede mentir sobre el quechua."""

    def test_ev01_sin_modelo_de_audio_promete_normalizacion(self):
        with mock.patch.object(engine, "GEMINI_AVAILABLE", False):
            estado = engine.estado_voz()
        for clave in ("modelo_de_audio", "audio_quechua", "entiende_quechua",
                      "normalizacion_quechua", "proveedor", "nota"):
            self.assertIn(clave, estado)
        self.assertFalse(estado["modelo_de_audio"])
        self.assertFalse(estado["audio_quechua"])
        self.assertTrue(estado["normalizacion_quechua"])
        self.assertTrue(estado["entiende_quechua"])

    def test_ev02_con_gemini_el_audio_entiende_quechua(self):
        with mock.patch.object(engine, "GEMINI_AVAILABLE", True):
            estado = engine.estado_voz()
        self.assertTrue(estado["modelo_de_audio"])
        self.assertTrue(estado["audio_quechua"])

    def test_ev03_el_estado_del_api_deriva_el_via(self):
        from app import app
        with mock.patch.object(engine, "GEMINI_AVAILABLE", False):
            with app.test_client() as cliente:
                datos = cliente.get("/api/voice/status").get_json()
        self.assertEqual(datos["via"], "texto")
        self.assertTrue(datos["entiende_quechua"])


if __name__ == "__main__":
    unittest.main()
