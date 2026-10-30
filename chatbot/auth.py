"""Autenticación y gestión de usuarios del panel administrativo."""
import json
import os
import re
import secrets
import sys
from datetime import datetime
from functools import wraps
from pathlib import Path
from threading import Lock

from flask import abort, redirect, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = Path(__file__).resolve().parent.parent
USERS_FILE = BASE_DIR / 'data' / 'usuarios.json'
ROLES = ('administrador', 'editor', 'ciudadano')
_USUARIO_RE = re.compile(r'^[A-Za-z0-9._-]{4,20}$')
_LOCK = Lock()
_HASH_FALSO = generate_password_hash('usuario-inexistente')


def ruta_usuarios() -> Path:
    """Archivo de usuarios editable.

    Dentro del EXE, la carpeta del programa se extrae a un temporal que se
    borra al cerrar: los usuarios creados se perderian. Por eso, si la app
    esta empaquetada, se usa una copia junto al ejecutable (o en %APPDATA%
    si esa carpeta no permite escribir) y se siembra con los usuarios que
    vienen incluidos.
    """
    personalizada = os.environ.get('SACABA_USERS_FILE')
    if personalizada:
        return Path(personalizada)
    if not getattr(sys, 'frozen', False):
        return USERS_FILE

    candidatas = [
        Path(sys.executable).resolve().parent / 'data' / 'usuarios.json',
        Path(os.environ.get('APPDATA', Path.home())) / 'Sacaba' / 'data' / 'usuarios.json',
    ]
    for destino in candidatas:
        try:
            if not destino.exists():
                destino.parent.mkdir(parents=True, exist_ok=True)
                if USERS_FILE.exists():
                    destino.write_bytes(USERS_FILE.read_bytes())
                else:
                    destino.write_text('{"usuarios": []}', encoding='utf-8')
            with destino.open('a', encoding='utf-8'):
                pass
            return destino
        except OSError:
            continue
    return USERS_FILE


def _leer() -> list:
    ruta = ruta_usuarios()
    if not ruta.exists():
        return []
    try:
        with ruta.open(encoding='utf-8') as archivo:
            datos = json.load(archivo)
    except (OSError, ValueError):
        return []
    usuarios = datos.get('usuarios') if isinstance(datos, dict) else None
    return usuarios if isinstance(usuarios, list) else []


def _escribir(usuarios: list) -> None:
    ruta = ruta_usuarios()
    ruta.parent.mkdir(parents=True, exist_ok=True)
    temporal = ruta.with_suffix('.tmp')
    temporal.write_text(
        json.dumps({'usuarios': usuarios}, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )
    os.replace(temporal, ruta)


def listar_usuarios() -> list:
    return sorted(
        _leer(),
        key=lambda u: (u.get('rol') != 'administrador', u['usuario'].lower()),
    )


def buscar_usuario(usuario: str):
    if not usuario:
        return None
    clave = usuario.strip().lower()
    for registro in _leer():
        if registro['usuario'].lower() == clave:
            return registro
    return None


def autenticar(usuario: str, contrasena: str):
    registro = buscar_usuario(usuario)
    if registro is None:
        check_password_hash(_HASH_FALSO, contrasena or '')
        return None
    if not check_password_hash(registro['password_hash'], contrasena or ''):
        return None
    if not registro.get('activo', True):
        return None
    return registro


def buscar_por_id(usuario_id: str):
    for registro in _leer():
        if registro.get('id') == usuario_id:
            return registro
    return None


def cambiar_contrasena(usuario_id: str, actual: str, nueva: str, confirmar: str):
    if len(nueva or '') < 8:
        return None, 'La nueva contraseña debe tener al menos 8 caracteres'
    if nueva != confirmar:
        return None, 'Las contraseñas nuevas no coinciden'
    with _LOCK:
        usuarios = _leer()
        for registro in usuarios:
            if registro.get('id') != usuario_id:
                continue
            if not check_password_hash(registro['password_hash'], actual or ''):
                return None, 'La contraseña actual no es correcta'
            registro['password_hash'] = generate_password_hash(nueva)
            _escribir(usuarios)
            return registro, None
    return None, 'Usuario no encontrado'


def alternar_activo(usuario_id: str, activo: bool):
    with _LOCK:
        usuarios = _leer()
        for registro in usuarios:
            if registro.get('id') != usuario_id:
                continue
            registro['activo'] = bool(activo)
            _escribir(usuarios)
            return registro
    return None


def crear_usuario(datos: dict):
    usuario = (datos.get('usuario') or '').strip()
    nombre = (datos.get('nombre') or '').strip()
    contrasena = datos.get('contrasena') or ''
    confirmar = datos.get('confirmar') or ''
    rol = (datos.get('rol') or '').strip().lower()

    if not usuario or not nombre or not contrasena or not confirmar or not rol:
        return None, 'Todos los campos son obligatorios'
    if not _USUARIO_RE.match(usuario):
        return None, 'El usuario debe tener entre 4 y 20 caracteres: letras, números, punto, guion o guion bajo'
    if len(nombre) < 3:
        return None, 'El nombre completo debe tener al menos 3 caracteres'
    if len(contrasena) < 8:
        return None, 'La contraseña debe tener al menos 8 caracteres'
    if contrasena != confirmar:
        return None, 'Las contraseñas no coinciden'
    if rol not in ROLES:
        return None, 'Seleccione un rol válido'

    with _LOCK:
        usuarios = _leer()
        if any(u['usuario'].lower() == usuario.lower() for u in usuarios):
            return None, 'El nombre de usuario ya está registrado'
        registro = {
            'id': secrets.token_hex(8),
            'usuario': usuario,
            'nombre': nombre,
            'rol': rol,
            'activo': True,
            'creado': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'password_hash': generate_password_hash(contrasena),
        }
        usuarios.append(registro)
        _escribir(usuarios)
    return registro, None


def csrf_token() -> str:
    token = session.get('_csrf')
    if not token:
        token = secrets.token_urlsafe(24)
        session['_csrf'] = token
    return token


def csrf_valido() -> bool:
    enviado = request.form.get('csrf', '')
    return bool(enviado) and secrets.compare_digest(enviado, session.get('_csrf', ''))


def admin_required(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if not session.get('usuario_id'):
            return redirect(url_for('login', siguiente=request.path))
        if session.get('rol') != 'administrador':
            abort(403)
        return vista(*args, **kwargs)

    return envoltura


def panel_required(vista):
    """Acceso al panel: administradores y editores."""
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if not session.get('usuario_id'):
            return redirect(url_for('login', siguiente=request.path))
        if session.get('rol') not in ('administrador', 'editor'):
            abort(403)
        return vista(*args, **kwargs)

    return envoltura
