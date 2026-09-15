# -*- coding: utf-8 -*-
"""
PRUEBAS DE CAJA BLANCA - Chatbot Municipal de Sacaba
Casos disenados CONOCIENDO el codigo fuente de chatbot/engine.py.
Objetivo: cobertura de sentencias y de decisiones (ramas).

Tecnica aplicada:
  - Se identifica cada decision (if / for / ternario) del codigo.
  - Para cada decision se construye un caso que recorre la rama
    Verdadera y otro la rama Falsa (o cada salida posible).
  - La cobertura real se mide con la herramienta 'coverage':
      coverage run -m pytest tests ; coverage report

Ejecutar:
    python -m pytest tests/test_caja_blanca.py -v
"""
import unittest

from chatbot import engine


class CajaBlancaNormalize(unittest.TestCase):
    """Funcion: normalize()  |  Decisiones: generador con filtro"""

    def test_cb01_rama_con_combinantes(self):
        self.assertEqual(engine.normalize("Cédula de Identidad"), "cedula de identidad")

    def test_cb02_rama_sin_combinantes(self):
        self.assertEqual(engine.normalize("abc123"), "abc123")


class CajaBlancaDetectTramite(unittest.TestCase):
    """Funcion: detect_tramite()
    Decisiones: for externo, for interno, if coincidencia
    Caminos: retorno temprano (1er patron), retorno intermedio,
             retorno ultimo patron, agotamiento del bucle -> None."""

    def test_cb03_retorno_en_primer_patron(self):
        # Recorre: patron 1, palabra 1 -> return inmediato
        self.assertEqual(engine.detect_tramite("carnet"), "carnet")

    def test_cb04_retorno_en_patron_intermedio(self):
        self.assertEqual(engine.detect_tramite("necesito agua potable"), "agua")

    def test_cb05_retorno_en_ultimo_patron(self):
        # Fuerza el recorrido completo de los bucles hasta nodeuda
        self.assertEqual(engine.detect_tramite("libre de deuda"), "nodeuda")

    def test_cb06_bucles_agotados_devuelve_none(self):
        # Ninguna coincidencia: ambos for llegan al final (rama falsa total)
        self.assertIsNone(engine.detect_tramite("palabras sin sentido"))

    def test_cb07_coincidencia_requiere_normalizacion(self):
        # La entrada con tilde solo coincide tras normalizar (rama del filtro)
        self.assertEqual(engine.detect_tramite("Construcción"), "construccion")


class CajaBlancaDetectIntent(unittest.TestCase):
    """Funcion: detect_intent()
    12 decisiones if + 1 for => complejidad ciclonatica 14.
    Cada caso cubre UNA rama Verdadera distinta; cb21 cubre todas falsas."""

    def test_cb08_rama_greeting(self):
        self.assertEqual(engine.detect_intent("hola"), "greeting")

    def test_cb09_rama_farewell(self):
        self.assertEqual(engine.detect_intent("chau"), "farewell")

    def test_cb10_rama_donde(self):
        self.assertEqual(engine.detect_intent("donde queda"), "donde")

    def test_cb11_rama_cuanto(self):
        self.assertEqual(engine.detect_intent("precio"), "cuanto")

    def test_cb12_rama_que_necesito(self):
        self.assertEqual(engine.detect_intent("requisitos"), "que_necesito")

    def test_cb13_rama_como(self):
        self.assertEqual(engine.detect_intent("pasos"), "como")

    def test_cb14_rama_cuando(self):
        self.assertEqual(engine.detect_intent("tiempo de espera"), "cuando")

    def test_cb15_rama_horarios(self):
        self.assertEqual(engine.detect_intent("horario"), "horarios")

    def test_cb16_rama_contacto(self):
        self.assertEqual(engine.detect_intent("telefono"), "contacto")

    def test_cb17_rama_multas(self):
        self.assertEqual(engine.detect_intent("infraccion"), "multas")

    def test_cb18_rama_menu_tramites(self):
        self.assertEqual(engine.detect_intent("tramites"), "menu_tramites")

    def test_cb19_rama_consejo(self):
        self.assertEqual(engine.detect_intent("dame un consejo"), "consejo")

    def test_cb20_orden_de_prioridad_saludo_sobre_tramite(self):
        # Verifica el orden de evaluacion: greeting se evalua ANTES de tramite
        self.assertEqual(engine.detect_intent("hola, quiero carnet"), "greeting")

    def test_cb21_todas_las_ramas_falsas(self):
        self.assertEqual(engine.detect_intent("zzz"), "question")


class CajaBlancaBuildCard(unittest.TestCase):
    """Funcion: build_card()  |  Decisiones: if consejo, if ubicacion(u)"""

    def test_cb22_ramas_verdaderas_consejo_y_ubicacion(self):
        card = engine.build_card(engine.KB["carnet"]["es"])
        self.assertIn("**Consejo:**", card)
        self.assertIn("https://maps.app.goo.gl", card)

    def test_cb23_ramas_falsas_sin_ubicacion(self):
        card = engine.build_card(engine.KB["residencia"]["es"])
        self.assertNotIn("https://", card)


class CajaBlancaGetResp(unittest.TestCase):
    """Funcion: get_resp()  |  ~17 decisiones.
    Cubre: guarda de idioma, saludo, despedida, bloque tramite x 7 intenciones,
    sub-decisiones (donde_link, cuanto_detail), y las 5 ramas finales."""

    def test_cb24_guarda_idioma_invalido(self):
        resp = engine.get_resp("hola", "it")
        self.assertIn("Sacaba", resp)

    def test_cb24b_rama_farewell(self):
        resp = engine.get_resp("adios", "es")
        self.assertIn("Gracias por tu consulta", resp)

    def test_cb24c_rama_contacto(self):
        resp = engine.get_resp("telefono", "es")
        self.assertIn("Contacto - Gobierno Autonomo Municipal de Sacaba", resp)

    def test_cb25_tramite_donde_con_link(self):
        resp = engine.get_resp("donde tramito mi carnet")
        self.assertIn("SEGIP", resp)
        self.assertIn("Ubicacion:", resp)

    def test_cb26_tramite_donde_sin_link(self):
        resp = engine.get_resp("donde hago la residencia")
        self.assertNotIn("Ubicacion:", resp)

    def test_cb27_tramite_cuanto_con_detalle(self):
        resp = engine.get_resp("cuanto cuesta el carnet")
        self.assertIn("Banco Union", resp)

    def test_cb28_tramite_cuanto_sin_detalle(self):
        resp = engine.get_resp("cuanto cuesta la residencia")
        self.assertIn("Bs. 15", resp)

    def test_cb29_tramite_que_necesito(self):
        resp = engine.get_resp("que necesito para solteria")
        self.assertIn("- Requisitos:", resp)

    def test_cb30_tramite_como(self):
        resp = engine.get_resp("como tramito eventos")
        self.assertIn("- Procedimiento:", resp)
        self.assertIn("1. ", resp)

    def test_cb31_tramite_cuando(self):
        resp = engine.get_resp("cuando esta listo el carnet")
        self.assertIn("Tiempo estimado:", resp)

    def test_cb32_tramite_consejo(self):
        resp = engine.get_resp("consejo para el carnet")
        self.assertIn("Consejo:", resp)
        self.assertIn("Ve temprano", resp)

    def test_cb33_tramite_tarjeta_por_defecto(self):
        resp = engine.get_resp("carnet")
        self.assertIn("**Carnet de Identidad (Cedula)**", resp)

    def test_cb34_rama_multas_es(self):
        self.assertIn("Informacion de Multas", engine.get_resp("multas", "es"))

    def test_cb35_rama_multas_qu(self):
        self.assertIn("Multakuna Yachay", engine.get_resp("panku", "qu"))

    def test_cb36_rama_horarios_qu(self):
        self.assertIn("Horario Atencion", engine.get_resp("horario", "qu"))

    def test_cb37_rama_menu_tramites(self):
        resp = engine.get_resp("tramites", "es")
        self.assertEqual(resp.count("\n") >= 11, True)

    def test_cb38_respuesta_default_es(self):
        self.assertIn("puedo aprenderla", engine.get_resp("qwerty", "es"))

    def test_cb39_respuesta_default_qu(self):
        self.assertIn("yachay atiyman", engine.get_resp("qwerty", "qu"))


class CajaBlancaBuildTramiteList(unittest.TestCase):
    """Funcion: build_tramite_list() | Decision: KB[k].get(lang) or KB[k]['es']"""

    def test_cb40_rama_idioma_existente(self):
        lista = engine.build_tramite_list("es")
        self.assertIn("Carnet de Identidad (Cedula)", lista)

    def test_cb41_rama_respaldo_a_espanol(self):
        # Se inyecta un tramite sin version 'qu' para cubrir la rama de fallback
        original = dict(engine.KB)
        try:
            engine.KB["temporal"] = {"es": {"n": "Tramite Temporal", "icon": "x",
                                            "c": "Bs. 1", "t": "1 dia"}}
            lista = engine.build_tramite_list("qu")
            self.assertIn("Tramite Temporal", lista)
        finally:
            engine.KB.clear()
            engine.KB.update(original)


class CajaBlancaOpenBrowser(unittest.TestCase):
    """Funcion: app._open_browser() | Decision: llamada a webbrowser.open
    con la URL HOST:PORT del servidor."""

    def test_cb42_abre_navegador_en_puerto_local(self):
        from unittest import mock
        import app as app_module
        with mock.patch.object(app_module.webbrowser, "open") as abrir:
            app_module._open_browser()
        abrir.assert_called_once_with("http://127.0.0.1:5000")


if __name__ == "__main__":
    unittest.main(verbosity=2)
