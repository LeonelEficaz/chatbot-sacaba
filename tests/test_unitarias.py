# -*- coding: utf-8 -*-
"""
PRUEBAS UNITARIAS - Chatbot Municipal de Sacaba
Verifican cada unidad (funcion) del motor del chatbot de forma aislada.

Ejecutar:
    python -m pytest tests/test_unitarias.py -v
    python -m unittest tests.test_unitarias -v
"""
import unittest
from unittest import mock

from chatbot import engine
from chatbot.engine import (
    KB,
    MULTAS,
    UI,
    build_card,
    build_multas_string,
    build_tramite_list,
    detect_intent,
    detect_language,
    detect_tramite,
    get_resp,
    normalize,
)


class TestNormalize(unittest.TestCase):
    """Unidad: engine.normalize()"""

    def test_pu01_minusculas(self):
        self.assertEqual(normalize("HOLA MUNDO"), "hola mundo")

    def test_pu02_elimina_tildes(self):
        self.assertEqual(normalize("Construcción"), "construccion")

    def test_pu03_cadena_vacia(self):
        self.assertEqual(normalize(""), "")

    def test_pu04_no_altera_texto_simple(self):
        self.assertEqual(normalize("carnet"), "carnet")


class TestDetectTramite(unittest.TestCase):
    """Unidad: engine.detect_tramite()"""

    def test_pu05_detecta_carnet(self):
        self.assertEqual(detect_tramite("¿Cómo tramito mi carnet?"), "carnet")

    def test_pu06_detecta_por_palabra_secundaria(self):
        self.assertEqual(detect_tramite("necesito sacar huellas"), "carnet")

    def test_pu07_detecta_con_tildes(self):
        self.assertEqual(detect_tramite("Permiso de Construcción"), "construccion")

    def test_pu08_sin_coincidencia_devuelve_none(self):
        self.assertIsNone(detect_tramite("qué clima hace hoy"))

    def test_pu09_detecta_ultimo_patron(self):
        self.assertEqual(detect_tramite("certificado de no deuda"), "nodeuda")


class TestDetectIntent(unittest.TestCase):
    """Unidad: engine.detect_intent()"""

    def test_pu10_saludo(self):
        self.assertEqual(detect_intent("hola buenos dias"), "greeting")

    def test_pu11_despedida(self):
        self.assertEqual(detect_intent("gracias, adios"), "farewell")

    def test_pu12_ubicacion(self):
        self.assertEqual(detect_intent("donde hago el tramite"), "donde")

    def test_pu13_costo(self):
        self.assertEqual(detect_intent("cuánto cuesta"), "cuanto")

    def test_pu14_requisitos(self):
        self.assertEqual(detect_intent("que necesito para tramitar"), "que_necesito")

    def test_pu15_procedimiento(self):
        self.assertEqual(detect_intent("como saco el carnet"), "como")

    def test_pu16_tiempo(self):
        # 'cuanto tarda' activa la intencion cuanto (se evalua antes);
        # se usa una frase que solo coincide con la rama cuando.
        self.assertEqual(detect_intent("cuándo está listo"), "cuando")

    def test_pu17_horarios(self):
        self.assertEqual(detect_intent("horario de atencion"), "horarios")

    def test_pu18_contacto(self):
        self.assertEqual(detect_intent("telefono de la municipalidad"), "contacto")

    def test_pu19_multas(self):
        self.assertEqual(detect_intent("multas de transito"), "multas")

    def test_pu20_menu(self):
        self.assertEqual(detect_intent("lista de tramites"), "menu_tramites")

    def test_pu21_intencion_desconocida(self):
        self.assertEqual(detect_intent("xyzabc"), "question")


class TestDetectLanguage(unittest.TestCase):
    """Unidad: engine.detect_language()"""

    def test_pu36_mensaje_espanol(self):
        self.assertEqual(detect_language("cuanto cuesta el carnet"), "es")

    def test_pu37_mensaje_quechua_saludo(self):
        self.assertEqual(detect_language("Imaynallan, allinllachu?"), "qu")

    def test_pu38_mensaje_quechua_pregunta(self):
        self.assertEqual(detect_language("Maypitaq carnet rurakuna?"), "qu")

    def test_pu39_mensaje_quechua_tramite(self):
        self.assertEqual(detect_language("Carnetta yachayta munani"), "qu")

    def test_pu40_mensaje_vacio_o_mixto_por_defecto(self):
        self.assertEqual(detect_language(""), "es")

    def test_pu41_entrada_no_texto_devuelve_es(self):
        self.assertEqual(detect_language(None), "es")
        self.assertEqual(detect_language(12345), "es")


class TestBuilders(unittest.TestCase):
    """Unidades: build_card, build_tramite_list, build_multas_string"""

    def test_pu22_tarjeta_contiene_datos_clave(self):
        card = build_card(KB["carnet"]["es"])
        for esperado in ("Carnet de Identidad", "SEGIP", "Bs. 17", "Inmediato"):
            self.assertIn(esperado, card)

    def test_pu23_lista_todos_los_tramites(self):
        lista = build_tramite_list("es")
        self.assertGreaterEqual(len(KB), 24)
        for clave in KB:
            self.assertIn(KB[clave]["es"]["n"], lista)

    def test_pu24_lista_en_quechua_usa_es_como_respaldo(self):
        lista = build_tramite_list("qu")
        self.assertIn("Carnet de Identidad (Cedula)", lista)

    def test_pu25_multas_incluye_transito_y_municipales(self):
        multas = build_multas_string("es")
        self.assertIn("Exceso de velocidad", multas)
        self.assertIn("Arrojar basura", multas)
        self.assertIn("Procedimiento de Pago", multas)

    def test_pu26_multas_version_quechua(self):
        multas = build_multas_string("qu")
        self.assertIn("Multakuna Yachay", multas)
        self.assertIn("Transito Multakuna", multas)


class TestGetResp(unittest.TestCase):
    """Unidad: engine.get_resp()"""

    def test_pu27_saludo_es(self):
        resp = get_resp("hola")
        self.assertIn("chatbot municipal", resp)
        self.assertIn("carnet de identidad", resp)

    def test_pu28_costo_tramite(self):
        resp = get_resp("¿Cuánto cuesta el carnet?", "es")
        self.assertIn("Bs. 17", resp)

    def test_pu29_requisitos_numerados(self):
        resp = get_resp("¿Qué necesito para la residencia?", "es")
        self.assertIn("1. ", resp)
        self.assertIn("Fotocopia de cedula", resp)

    def test_pu30_pasos_procedimiento(self):
        resp = get_resp("¿Cómo tramito la licencia de funcionamiento?", "es")
        self.assertIn("- Procedimiento:", resp)
        self.assertIn("1. Acude a la caja central", resp)
        self.assertIn("Bs. 60", resp)

    def test_pu31_respuesta_default(self):
        resp = get_resp("abcxyz", "es")
        self.assertIn("puedo aprenderla", resp)

    def test_pu32_idioma_invalido_retorna_espanol(self):
        resp = get_resp("hola", "fr")
        self.assertIn("Sacaba", resp)

    def test_pu33_kb_sin_valores_undefined(self):
        """Regresion BUG-02: ninguna entrada debe tener claves mal escritas."""
        for clave, idiomas in KB.items():
            for lang, t in idiomas.items():
                self.assertIn("cuanto", t, msg="Falta 'cuanto' en %s/%s" % (clave, lang))
                self.assertIn("cuanto_tarda", t, msg="Falta 'cuanto_tarda' en %s/%s" % (clave, lang))
                self.assertNotIn("quanto", t, msg="'quanto' obsoleto en %s/%s" % (clave, lang))

    def test_pu34_integridad_base_conocimiento(self):
        campos = ["n", "icon", "d", "donde", "cuanto", "que_necesito", "como",
                  "cuanto_tarda", "horario", "consejo", "c", "t", "dep"]
        for clave, idiomas in KB.items():
            for lang in idiomas:
                for campo in campos:
                    self.assertIn(campo, KB[clave][lang],
                                  msg="%s/%s falta campo %s" % (clave, lang, campo))
                self.assertGreater(len(KB[clave][lang]["como"]), 0)
                self.assertGreater(len(KB[clave][lang]["que_necesito"]), 0)

    def test_pu35_ui_idiomas_completos(self):
        for lang in ("es", "qu"):
            for campo in ("title", "sub", "ph", "powered", "greeting",
                          "farewell", "default", "horarios", "contacto"):
                self.assertIn(campo, UI[lang])
        self.assertIn("transito", MULTAS["es"])
        self.assertIn("municipales", MULTAS["qu"])


def _fake_chat(content):
    """Construye un objeto respuesta de OpenAI simulado para get_ai_resp."""
    resp = mock.Mock()
    resp.choices = [mock.Mock(message=mock.Mock(content=content))]
    return resp


class TestGetAiResp(unittest.TestCase):
    """Unidad: engine.get_ai_resp() con la API de OpenAI simulada (mock).
    Decisiones: IA no disponible, IA con texto, IA vacia, IA con error."""

    def test_pu42_ia_no_disponible_usa_respuesta_local(self):
        with mock.patch.object(engine, "_ai_available", False):
            resp = engine.get_ai_resp("hola", "es")
        self.assertIn("Sacaba", resp)

    def test_pu43_ia_devuelve_texto(self):
        with mock.patch.object(engine, "_client") as client:
            client.chat.completions.create.return_value = _fake_chat("Hola, en que te ayudo?")
            resp = engine.get_ai_resp("hola", "es")
        self.assertEqual(resp, "Hola, en que te ayudo?")

    def test_pu44_ia_responde_vacio_usa_respuesta_local(self):
        with mock.patch.object(engine, "_client") as client:
            client.chat.completions.create.return_value = _fake_chat("   ")
            resp = engine.get_ai_resp("hola", "es")
        self.assertIn("Sacaba", resp)

    def test_pu45_ia_error_usa_respuesta_local(self):
        with mock.patch.object(engine, "_client") as client:
            client.chat.completions.create.side_effect = Exception("timeout")
            resp = engine.get_ai_resp("hola", "es")
        self.assertIn("Sacaba", resp)


class TestTranscribeAudio(unittest.TestCase):
    """Unidad: engine.transcribe_audio() (openai.whisper simulado).
    Decisiones: IA no disponible, transcripcion exitosa, error de API."""

    def test_pu46_sin_ia_levanta_excepcion(self):
        with mock.patch.object(engine, "_ai_available", False):
            with self.assertRaises(Exception) as cm:
                engine.transcribe_audio(b"audio")
        self.assertIn("no configurada", str(cm.exception))

    def test_pu47_con_ia_devuelve_texto(self):
        with mock.patch.object(engine, "_client") as client:
            client.audio.transcriptions.create.return_value = mock.Mock(text="hola")
            self.assertEqual(engine.transcribe_audio(b"audio"), "hola")

    def test_pu48_error_de_transcripcion(self):
        with mock.patch.object(engine, "_client") as client:
            client.audio.transcriptions.create.side_effect = Exception("audio invalido")
            with self.assertRaises(Exception) as cm:
                engine.transcribe_audio(b"audio")
        self.assertIn("Error en transcripcion", str(cm.exception))


class TestTranslatePage(unittest.TestCase):
    """Unidad: engine.translate_page() (traduccion de pagina con IA, simulada).
    Decisiones: IA no disponible, sin items, exito, JSON con/ sin markdown,
    JSON invalido, sin traducciones."""

    def test_pu49_sin_ia_devuelve_none(self):
        with mock.patch.object(engine, "_ai_available", False):
            self.assertIsNone(engine.translate_page([("t1", "Buenos dias")]))

    def test_pu50_sin_items_devuelve_vacio(self):
        self.assertEqual(engine.translate_page([]), {})

    def test_pu51_traduccion_valida(self):
        with mock.patch.object(engine, "_client") as client:
            client.chat.completions.create.return_value = _fake_chat(
                '{"translations": {"0": "Allin p\'unchay"}}')
            result = engine.translate_page([("t1", "Buenos dias")])
        self.assertEqual(result, {"t1": "Allin p'unchay"})

    def test_pu52_json_con_markdown_se_limpia(self):
        with mock.patch.object(engine, "_client") as client:
            client.chat.completions.create.return_value = _fake_chat(
                '```json\n{"translations": {"0": "Allin p\'unchay"}}\n```')
            result = engine.translate_page([("t1", "Buenos dias")])
        self.assertEqual(result, {"t1": "Allin p'unchay"})

    def test_pu53_json_invalido_devuelve_none(self):
        with mock.patch.object(engine, "_client") as client:
            client.chat.completions.create.return_value = _fake_chat("texto sin json")
            self.assertIsNone(engine.translate_page([("t1", "hola")]))

    def test_pu54_sin_traducciones_devuelve_none(self):
        with mock.patch.object(engine, "_client") as client:
            client.chat.completions.create.return_value = _fake_chat('{"translations": {}}')
            self.assertIsNone(engine.translate_page([("t1", "hola")]))

    def test_pu59_translations_no_es_dict_devuelve_none(self):
        with mock.patch.object(engine, "_client") as client:
            client.chat.completions.create.return_value = _fake_chat(
                '{"translations": "texto invalido"}')
            self.assertIsNone(engine.translate_page([("t1", "hola")]))


class TestSmalltalkIdentity(unittest.TestCase):
    """Unidad: intenciones smalltalk e identity dentro de engine.get_resp()."""

    def test_pu55_smalltalk_es(self):
        resp = get_resp("como estas", "es")
        self.assertIn("guiarte", resp)

    def test_pu56_identity_es(self):
        resp = get_resp("quien eres", "es")
        self.assertIn("Tu Gobierno en Sacaba", resp)

    def test_pu57_smalltalk_qu(self):
        resp = get_resp("como estas", "qu")
        self.assertIn("Allinmi", resp)

    def test_pu58_identity_qu(self):
        resp = get_resp("quien eres", "qu")
        self.assertIn("Asistente", resp)

    def test_pu33_kb_sin_valores_undefined(self):
        """Regresion BUG-02: ninguna entrada debe tener claves mal escritas."""
        for clave, idiomas in KB.items():
            for lang, t in idiomas.items():
                self.assertIn("cuanto", t, msg="Falta 'cuanto' en %s/%s" % (clave, lang))
                self.assertIn("cuanto_tarda", t, msg="Falta 'cuanto_tarda' en %s/%s" % (clave, lang))
                self.assertNotIn("quanto", t, msg="'quanto' obsoleto en %s/%s" % (clave, lang))

    def test_pu34_integridad_base_conocimiento(self):
        campos = ["n", "icon", "d", "donde", "cuanto", "que_necesito", "como",
                  "cuanto_tarda", "horario", "consejo", "c", "t", "dep"]
        for clave, idiomas in KB.items():
            for lang in idiomas:
                for campo in campos:
                    self.assertIn(campo, KB[clave][lang],
                                  msg="%s/%s falta campo %s" % (clave, lang, campo))
                self.assertGreater(len(KB[clave][lang]["como"]), 0)
                self.assertGreater(len(KB[clave][lang]["que_necesito"]), 0)

    def test_pu35_ui_idiomas_completos(self):
        for lang in ("es", "qu"):
            for campo in ("title", "sub", "ph", "powered", "greeting",
                          "farewell", "default", "horarios", "contacto"):
                self.assertIn(campo, UI[lang])
        self.assertIn("transito", MULTAS["es"])
        self.assertIn("municipales", MULTAS["qu"])


# =====================================================================
# PRUEBAS: BUSQUEDA AVANZADA
# =====================================================================

class TestSearchTramites(unittest.TestCase):
    """Unidad: engine.search_tramites()"""

    def test_pu36_busqueda_vacia_retorna_todos(self):
        from chatbot.engine import search_tramites
        result = search_tramites()
        self.assertIn("results", result)
        self.assertIn("total", result)
        self.assertGreater(result["total"], 0)

    def test_pu37_busqueda_por_texto(self):
        from chatbot.engine import search_tramites
        result = search_tramites(query="carnet")
        self.assertGreater(result["total"], 0)
        # Al menos un resultado debe contener "carnet" en algun campo
        found = any("carnet" in (r["name"] + r["description"]).lower() for r in result["results"])
        self.assertTrue(found)

    def test_pu38_busqueda_por_precio_max(self):
        from chatbot.engine import search_tramites
        result = search_tramites(max_price=20)
        self.assertGreater(result["total"], 0)

    def test_pu39_busqueda_por_departamento(self):
        from chatbot.engine import search_tramites
        result = search_tramites(department="SEGIP")
        self.assertGreater(result["total"], 0)
        for r in result["results"]:
            self.assertIn("SEGIP", r["department"])

    def test_pu40_busqueda_por_categoria(self):
        from chatbot.engine import search_tramites
        result = search_tramites(category="identidad")
        self.assertGreater(result["total"], 0)

    def test_pu41_busqueda_combinada(self):
        from chatbot.engine import search_tramites
        result = search_tramites(query="permiso", department="Urbanismo")
        self.assertGreater(result["total"], 0)
        for r in result["results"]:
            self.assertIn("Urbanismo", r["department"])

    def test_pu42_busqueda_sin_resultados(self):
        from chatbot.engine import search_tramites
        result = search_tramites(query="avion espacial")
        self.assertEqual(result["total"], 0)
        self.assertEqual(len(result["results"]), 0)

    def test_pu43_filtros_aplicados(self):
        from chatbot.engine import search_tramites
        result = search_tramites(query="carnet", max_price=20)
        # Los filtros se registran solo si hay resultados
        self.assertIsInstance(result["filters"], dict)

    def test_pu44_idioma_quechua(self):
        from chatbot.engine import search_tramites
        result = search_tramites(query="carnet", lang="qu")
        self.assertGreater(result["total"], 0)

    def test_pu45_sugerencias_busqueda(self):
        from chatbot.engine import get_search_suggestions
        suggestions = get_search_suggestions()
        self.assertIn("categories", suggestions)
        self.assertIn("price_ranges", suggestions)
        self.assertIn("departments", suggestions)
        self.assertGreater(len(suggestions["categories"]), 0)


class TestExtractHelpers(unittest.TestCase):
    """Unidad: _extract_price_number() y _extract_days()"""

    def test_pu46_extract_price_simple(self):
        from chatbot.engine import _extract_price_number
        mn, mx = _extract_price_number("Bs. 17")
        self.assertEqual(mn, 17.0)
        self.assertEqual(mx, 17.0)

    def test_pu47_extract_price_rango(self):
        from chatbot.engine import _extract_price_number
        mn, mx = _extract_price_number("Bs. 50 - 200")
        self.assertEqual(mn, 50.0)
        self.assertEqual(mx, 200.0)

    def test_pu48_extract_price_vacio(self):
        from chatbot.engine import _extract_price_number
        mn, mx = _extract_price_number("")
        self.assertIsNone(mn)
        self.assertIsNone(mx)

    def test_pu49_extract_days_inmediato(self):
        from chatbot.engine import _extract_days
        self.assertEqual(_extract_days("Inmediato"), 0)

    def test_pu50_extract_days_dias(self):
        from chatbot.engine import _extract_days
        self.assertEqual(_extract_days("5 a 10 dias habiles"), 10)

    def test_pu51_extract_days_semanas(self):
        from chatbot.engine import _extract_days
        self.assertEqual(_extract_days("1-2 semanas"), 14)


# =====================================================================
# PRUEBAS: OPENSTREETMAP / NOMINATIM API
# =====================================================================

class TestMapsFunctions(unittest.TestCase):
    """Unidad: Funciones de OpenStreetMap"""

    def test_pu52_get_office_location(self):
        from chatbot.engine import get_office_location
        office = get_office_location("municipalidad")
        self.assertIsNotNone(office)
        self.assertEqual(office["name"], "Gobierno Autónomo Municipal de Sacaba")
        self.assertIn("lat", office)
        self.assertIn("lng", office)

    def test_pu53_get_office_location_no_existe(self):
        from chatbot.engine import get_office_location
        office = get_office_location("oficina_fantasma")
        self.assertIsNone(office)

    def test_pu54_search_offices(self):
        from chatbot.engine import search_offices
        results = search_offices("SEGIP")
        self.assertGreater(len(results), 0)
        self.assertIn("SEGIP", results[0]["name"])

    def test_pu55_search_offices_vacio(self):
        from chatbot.engine import search_offices
        results = search_offices()
        self.assertGreater(len(results), 0)

    def test_pu56_get_all_offices(self):
        from chatbot.engine import get_all_offices
        offices = get_all_offices()
        self.assertGreater(len(offices), 0)
        self.assertIn("municipalidad", offices)
        self.assertIn("segip", offices)

    def test_pu57_get_directions(self):
        from chatbot.engine import get_directions
        result = get_directions(-17.3950, -66.0420, "segip")
        self.assertIsNotNone(result)
        self.assertIn("directions_url", result)
        self.assertIn("map_url", result)
        self.assertIn("lat", result)
        self.assertIn("lng", result)

    def test_pu58_get_directions_no_existe(self):
        from chatbot.engine import get_directions
        result = get_directions(-17.3950, -66.0420, "oficina_fantasma")
        self.assertIsNone(result)

    def test_pu59_get_nearby_places(self):
        from chatbot.engine import get_nearby_places
        results = get_nearby_places(-17.3952, -66.0425, radius=5000)
        self.assertGreater(len(results), 0)

    def test_pu60_generate_map_embed(self):
        from chatbot.engine import generate_map_embed
        result = generate_map_embed("municipalidad")
        self.assertIsNotNone(result)
        self.assertIn("embed_url", result)
        self.assertIn("full_url", result)
        self.assertIn("lat", result)

    def test_pu61_generate_map_embed_no_existe(self):
        from chatbot.engine import generate_map_embed
        result = generate_map_embed("oficina_fantasma")
        self.assertIsNone(result)

    def test_pu62_municipal_offices_structure(self):
        from chatbot.engine import MUNICIPAL_OFFICES
        self.assertGreater(len(MUNICIPAL_OFFICES), 0)
        for key, office in MUNICIPAL_OFFICES.items():
            self.assertIn("name", office)
            self.assertIn("address", office)
            self.assertIn("lat", office)
            self.assertIn("lng", office)
            self.assertIsInstance(office["lat"], float)
            self.assertIsInstance(office["lng"], float)

    def test_pu63_nominatim_url(self):
        from chatbot.engine import NOMINATIM_URL
        self.assertEqual(NOMINATIM_URL, "https://nominatim.openstreetmap.org")


# =====================================================================
# PRUEBAS: GLOSBLE DICTIONARY API
# =====================================================================

class TestDictionaryFunctions(unittest.TestCase):
    """Unidad: Funciones del Diccionario Quechua"""

    def test_pu64_translate_word_local(self):
        from chatbot.engine import translate_word
        result = translate_word("hola", "es", "qu")
        self.assertIsNotNone(result)
        self.assertEqual(result["translation"], "Allianchu")
        self.assertEqual(result["source"], "local")

    def test_pu65_translate_word_no_existe(self):
        from chatbot.engine import translate_word
        result = translate_word("xyzabc", "es", "qu")
        self.assertIsNone(result)

    def test_pu66_search_quechua_dictionary(self):
        from chatbot.engine import search_quechua_dictionary
        results = search_quechua_dictionary("hola")
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]["spanish"], "hola")

    def test_pu67_search_quechua_dictionary_vacio(self):
        from chatbot.engine import search_quechua_dictionary
        results = search_quechua_dictionary("xyzabc123")
        self.assertEqual(len(results), 0)

    def test_pu68_get_quechua_phrases(self):
        from chatbot.engine import get_quechua_phrases
        phrases = get_quechua_phrases("common")
        self.assertGreater(len(phrases), 0)
        self.assertIn("es", phrases[0])
        self.assertIn("qu", phrases[0])

    def test_pu69_get_quechua_phrases_numbers(self):
        from chatbot.engine import get_quechua_phrases
        phrases = get_quechua_phrases("numbers")
        self.assertEqual(len(phrases), 10)
        self.assertEqual(phrases[0]["qu"], "Huk")

    def test_pu70_learn_quechua_word(self):
        from chatbot.engine import learn_quechua_word, QUECHUA_LOCAL_DB
        result = learn_quechua_word("test_palabra", "test_traduccion", "ejemplo")
        self.assertEqual(result["status"], "learned")
        self.assertIn("test_palabra", QUECHUA_LOCAL_DB)

    def test_pu71_quechua_local_db_structure(self):
        from chatbot.engine import QUECHUA_LOCAL_DB
        self.assertGreater(len(QUECHUA_LOCAL_DB), 0)
        for key, data in QUECHUA_LOCAL_DB.items():
            self.assertIn("qu", data)
            self.assertIsInstance(data["qu"], str)


# =====================================================================
# PRUEBAS: GOOGLE GEMINI API
# =====================================================================

class TestGeminiFunctions(unittest.TestCase):
    """Unidad: Funciones de Google Gemini API"""

    def test_pu72_gemini_status(self):
        from chatbot.engine import get_gemini_status
        status = get_gemini_status()
        self.assertIn("available", status)
        self.assertIn("model", status)
        self.assertIn("free_tier", status)

    def test_pu73_gemini_available(self):
        from chatbot.engine import is_gemini_available
        result = is_gemini_available()
        self.assertIsInstance(result, bool)

    def test_pu74_gemini_model(self):
        from chatbot.engine import GEMINI_MODEL
        self.assertEqual(GEMINI_MODEL, "gemini-1.5-flash")

    def test_pu75_gemini_api_key_env(self):
        from chatbot.engine import GEMINI_API_KEY
        # Puede estar vacía si no está configurada
        self.assertIsInstance(GEMINI_API_KEY, str)


if __name__ == "__main__":
    unittest.main(verbosity=2)
