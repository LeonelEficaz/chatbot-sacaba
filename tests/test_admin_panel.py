# -*- coding: utf-8 -*-
"""Pruebas del panel de funcionarios: acceso, edición de fichas y cuentas.

Cada prueba usa archivos temporales de usuarios y de cambios de trámites
para no tocar data/usuarios.json ni data/tramites_override.json.
"""
import json
import os
import tempfile
import unittest
from pathlib import Path

from werkzeug.security import generate_password_hash

from app import app
from chatbot import auth
from chatbot import tramites as T

ADMIN_ID = 'a1b2c3d4e5f60718'
EDITOR_ID = 'b1b2c3d4e5f60718'
CLAVE_ADMIN = 'secreta123'
CLAVE_EDITOR = 'editor1234'


def _registro(ident, usuario, nombre, rol, clave, activo=True):
    return {
        'id': ident,
        'usuario': usuario,
        'nombre': nombre,
        'rol': rol,
        'activo': activo,
        'creado': '2026-10-01 09:00',
        'password_hash': generate_password_hash(clave),
    }


class BasePanel(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        carpeta = Path(self._tmp.name)
        self.usuarios = carpeta / 'usuarios.json'
        self.overrides = carpeta / 'tramites_override.json'
        self.usuarios.write_text(
            json.dumps({'usuarios': [
                _registro(ADMIN_ID, 'admin', 'Ana Admin', 'administrador', CLAVE_ADMIN),
                _registro(EDITOR_ID, 'editor', 'Eli Editor', 'editor', CLAVE_EDITOR),
            ]}, ensure_ascii=False),
            encoding='utf-8',
        )

        self._previo = {
            clave: os.environ.get(clave)
            for clave in ('SACABA_USERS_FILE', 'SACABA_TRAMITES_FILE')
        }
        os.environ['SACABA_USERS_FILE'] = str(self.usuarios)
        os.environ['SACABA_TRAMITES_FILE'] = str(self.overrides)
        self.addCleanup(self._restaurar)

        T._CACHE_OVERRIDES.update({'mtime': None, 'datos': {}})
        app.config['TESTING'] = True
        self.client = app.test_client()

    def _restaurar(self):
        for clave, valor in self._previo.items():
            if valor is None:
                os.environ.pop(clave, None)
            else:
                os.environ[clave] = valor
        T._CACHE_OVERRIDES.update({'mtime': None, 'datos': {}})

    def token(self, valor='token-prueba'):
        with self.client.session_transaction() as sesion:
            sesion['_csrf'] = valor
        return valor

    def entrar(self, usuario='admin', clave=CLAVE_ADMIN):
        with self.client.session_transaction() as sesion:
            sesion.clear()
            sesion['_csrf'] = 'token-prueba'
        return self.client.post(
            '/login',
            data={'usuario': usuario, 'contrasena': clave, 'csrf': 'token-prueba'},
        )

    def usuario(self, ident):
        return auth.buscar_por_id(ident)


class TestAcceso(BasePanel):
    def test_sin_sesion_redirige_al_login(self):
        for ruta in ('/admin', '/admin/tramites', '/admin/cuenta'):
            with self.subTest(ruta=ruta):
                respuesta = self.client.get(ruta)
                self.assertEqual(respuesta.status_code, 302)
                self.assertIn('/login', respuesta.headers['Location'])
                self.assertIn(ruta, respuesta.headers['Location'])

    def test_sin_sesion_no_entra_a_usuarios(self):
        respuesta = self.client.get('/admin/usuarios')
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn('/login', respuesta.headers['Location'])

    def test_login_exige_csrf(self):
        respuesta = self.client.post(
            '/login', data={'usuario': 'admin', 'contrasena': CLAVE_ADMIN},
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn('expiró', respuesta.get_data(as_text=True))

    def test_login_rechaza_clave_incorrecta(self):
        self.token()
        respuesta = self.client.post(
            '/login', data={'usuario': 'admin', 'contrasena': 'otra-clave', 'csrf': 'token-prueba'},
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn('incorrectos', respuesta.get_data(as_text=True))
        with self.client.session_transaction() as sesion:
            self.assertNotIn('usuario_id', sesion)

    def test_login_rechaza_cuenta_inactiva(self):
        auth.alternar_activo(EDITOR_ID, False)
        respuesta = self.entrar('editor', CLAVE_EDITOR)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn('incorrectos', respuesta.get_data(as_text=True))

    def test_login_correcto_lleva_al_panel(self):
        respuesta = self.entrar()
        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(respuesta.headers['Location'].endswith('/admin'))
        panel = self.client.get('/admin')
        self.assertEqual(panel.status_code, 200)
        self.assertIn('Ana', panel.get_data(as_text=True))

    def test_sesion_abierta_no_vuelve_al_login(self):
        self.entrar()
        respuesta = self.client.get('/login')
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn('/admin', respuesta.headers['Location'])


class TestPanel(BasePanel):
    def setUp(self):
        super().setUp()
        self.entrar()

    def test_panel_muestra_resumen(self):
        respuesta = self.client.get('/admin')
        texto = respuesta.get_data(as_text=True)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn('Trámites publicados', texto)
        self.assertIn('Usuarios del panel', texto)

    def test_lista_de_tramites(self):
        respuesta = self.client.get('/admin/tramites')
        texto = respuesta.get_data(as_text=True)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn('Actualiza costos', texto)
        self.assertIn('Carnet de Identidad', texto)

    def test_buscar_filtra_tramites(self):
        respuesta = self.client.get('/admin/tramites?buscar=carnet')
        texto = respuesta.get_data(as_text=True)
        self.assertIn('Carnet de Identidad', texto)
        self.assertNotIn('Patente de Funcionamiento', texto)

    def test_formulario_de_edicion(self):
        respuesta = self.client.get('/admin/tramites?editar=carnet')
        texto = respuesta.get_data(as_text=True)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn('name="costo"', texto)
        self.assertIn('Oficial:', texto)
        self.assertIn('Guardar cambios', texto)

    def test_pagina_de_cuenta(self):
        respuesta = self.client.get('/admin/cuenta')
        texto = respuesta.get_data(as_text=True)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn('name="actual"', texto)
        self.assertIn('name="nueva"', texto)


class TestEdicionDeFichas(BasePanel):
    def setUp(self):
        super().setUp()
        self.entrar()

    def test_guardar_costo_llega_al_portal_y_al_chat(self):
        original = T.get('carnet')['costo']
        respuesta = self.client.post(
            '/admin/tramites/carnet',
            data={'costo': 'Bs. 20', 'csrf': self.token()},
        )
        self.assertEqual(respuesta.status_code, 303)

        self.assertEqual(T.get('carnet')['costo'], 'Bs. 20')
        self.assertIn('Bs. 20', self.client.get('/tramite/carnet-de-identidad').get_data(as_text=True))
        formulario = self.client.get('/admin/tramites?editar=carnet').get_data(as_text=True)
        self.assertIn('Restaurar datos oficiales', formulario)

        chat = self.client.post(
            '/chat',
            json={'message': 'cuanto cuesta el carnet de identidad', 'language': 'es'},
        )
        self.assertIn('Bs. 20', chat.get_json()['response'])

        self.client.post(
            '/admin/tramites/carnet',
            data={'restablecer': '1', 'csrf': self.token()},
        )
        self.assertEqual(T.get('carnet')['costo'], original)

        chat = self.client.post(
            '/chat',
            json={'message': 'cuanto cuesta el carnet de identidad', 'language': 'es'},
        )
        self.assertNotIn('Bs. 20', chat.get_json()['response'])

    def test_guardar_requisitos_uno_por_linea(self):
        self.client.post(
            '/admin/tramites/carnet',
            data={
                'requisitos': 'Documento vigente\nFotografía reciente\nPago de tasa',
                'csrf': self.token(),
            },
        )
        self.assertEqual(
            T.get('carnet')['requisitos'],
            ['Documento vigente', 'Fotografía reciente', 'Pago de tasa'],
        )

    def test_campos_vacios_no_borran_la_ficha(self):
        self.client.post(
            '/admin/tramites/carnet',
            data={'costo': '', 'tiempo': '', 'csrf': self.token()},
        )
        self.assertEqual(T.overrides().get('carnet'), None)
        self.assertEqual(T.get('carnet')['costo'], T.TRAMITES['carnet']['costo'])

    def test_restablecer_sin_cambios_previos(self):
        respuesta = self.client.post(
            '/admin/tramites/carnet',
            data={'restablecer': '1', 'csrf': self.token()},
            follow_redirects=True,
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn('restauraron', respuesta.get_data(as_text=True))

    def test_tramite_inexistente(self):
        respuesta = self.client.post(
            '/admin/tramites/no-existe',
            data={'costo': 'Bs. 1', 'csrf': self.token()},
            follow_redirects=True,
        )
        self.assertIn('No encontramos ese trámite', respuesta.get_data(as_text=True))

    def test_sin_csrf_no_guarda(self):
        respuesta = self.client.post('/admin/tramites/carnet', data={'costo': 'Bs. 99'})
        self.assertEqual(respuesta.status_code, 303)
        self.assertEqual(T.overrides(), {})


class TestCuentas(BasePanel):
    def setUp(self):
        super().setUp()
        self.entrar()

    def test_desactivar_y_reactivar_usuario(self):
        respuesta = self.client.post(
            '/admin/usuarios/{}/estado'.format(EDITOR_ID), data={'csrf': self.token()},
        )
        self.assertEqual(respuesta.status_code, 303)
        self.assertFalse(self.usuario(EDITOR_ID)['activo'])
        self.assertEqual(self.entrar('editor', CLAVE_EDITOR).status_code, 200)

        self.entrar()
        self.client.post(
            '/admin/usuarios/{}/estado'.format(EDITOR_ID), data={'csrf': self.token()},
        )
        self.assertTrue(self.usuario(EDITOR_ID)['activo'])
        self.assertEqual(self.entrar('editor', CLAVE_EDITOR).status_code, 302)

    def test_no_puede_desactivar_su_propia_cuenta(self):
        respuesta = self.client.post(
            '/admin/usuarios/{}/estado'.format(ADMIN_ID),
            data={'csrf': self.token()},
            follow_redirects=True,
        )
        self.assertIn('No puede desactivar su propia cuenta', respuesta.get_data(as_text=True))
        self.assertTrue(self.usuario(ADMIN_ID)['activo'])

    def test_crear_usuario(self):
        respuesta = self.client.post(
            '/admin/usuarios',
            data={
                'usuario': 'mquispe',
                'nombre': 'María Quispe',
                'contrasena': 'claveSegura1',
                'confirmar': 'claveSegura1',
                'rol': 'editor',
                'csrf': self.token(),
            },
        )
        self.assertEqual(respuesta.status_code, 303)
        creado = auth.buscar_usuario('mquispe')
        self.assertIsNotNone(creado)
        self.assertEqual(creado['rol'], 'editor')
        self.assertIsNotNone(auth.autenticar('mquispe', 'claveSegura1'))

    def test_no_repite_usuario(self):
        respuesta = self.client.post(
            '/admin/usuarios',
            data={
                'usuario': 'admin',
                'nombre': 'Otra Persona',
                'contrasena': 'claveSegura1',
                'confirmar': 'claveSegura1',
                'rol': 'editor',
                'csrf': self.token(),
            },
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn('ya está registrado', respuesta.get_data(as_text=True))

    def test_cambiar_contrasena_actual_incorrecta(self):
        respuesta = self.client.post(
            '/admin/cuenta',
            data={
                'actual': 'no-es-la-clave',
                'nueva': 'nuevaClave99',
                'confirmar': 'nuevaClave99',
                'csrf': self.token(),
            },
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn('contraseña actual no es correcta', respuesta.get_data(as_text=True))

    def test_cambiar_contrasena_valida(self):
        respuesta = self.client.post(
            '/admin/cuenta',
            data={
                'actual': CLAVE_ADMIN,
                'nueva': 'nuevaClave99',
                'confirmar': 'nuevaClave99',
                'csrf': self.token(),
            },
        )
        self.assertEqual(respuesta.status_code, 303)
        self.assertIsNotNone(auth.autenticar('admin', 'nuevaClave99'))
        self.assertIsNone(auth.autenticar('admin', CLAVE_ADMIN))


class TestRolEditor(BasePanel):
    def setUp(self):
        super().setUp()
        self.entrar('editor', CLAVE_EDITOR)

    def test_editor_entra_al_panel_y_edita_fichas(self):
        self.assertEqual(self.client.get('/admin').status_code, 200)
        self.assertEqual(self.client.get('/admin/tramites').status_code, 200)
        self.assertEqual(self.client.get('/admin/cuenta').status_code, 200)

    def test_editor_no_administra_usuarios(self):
        self.assertEqual(self.client.get('/admin/usuarios').status_code, 403)
        self.assertEqual(
            self.client.post(
                '/admin/usuarios/{}/estado'.format(ADMIN_ID), data={'csrf': self.token()},
            ).status_code,
            403,
        )

    def test_editor_guarda_cambios_de_tramites(self):
        respuesta = self.client.post(
            '/admin/tramites/carnet',
            data={'costo': 'Bs. 18', 'csrf': self.token()},
        )
        self.assertEqual(respuesta.status_code, 303)
        self.assertEqual(T.get('carnet')['costo'], 'Bs. 18')


if __name__ == '__main__':
    unittest.main()
