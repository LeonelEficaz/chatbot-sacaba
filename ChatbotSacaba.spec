# -*- mode: python ; coding: utf-8 -*-

import os
import speech_recognition

_SR = os.path.dirname(speech_recognition.__file__)

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('templates', 'templates'), ('static', 'static'), ('chatbot', 'chatbot'), ('css', 'css'), ('js', 'js'), ('data', 'data'), ('img', 'img'), ('.env', '.'), (os.path.join(_SR, 'flac-win32.exe'), 'speech_recognition')],
    hiddenimports=['openai', 'dotenv', 'speech_recognition'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ChatbotSacaba',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
