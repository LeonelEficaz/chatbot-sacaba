import os
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from chatbot import bitacora, engine


@pytest.fixture(autouse=True)
def datos_en_temporal(monkeypatch, tmp_path):
    """Ninguna prueba escribe en el proyecto: la bitacora y el glosario aprendido
    se redirigen a un directorio desmontable."""
    monkeypatch.setattr(bitacora, "RUTA", tmp_path / "bitacora_eventos.jsonl")
    monkeypatch.setattr(engine, "GLOSARIO_FILE", tmp_path / "glosario_aprendido.json")
    engine._GLOSARIO_APRENDIDO.clear()


@pytest.fixture(autouse=True)
def entorno_offline(monkeypatch):
    """Mantiene la suite sin red: el chat usa el motor local y nunca consulta proveedores externos."""
    monkeypatch.setattr(engine, "_openai_dead", True, raising=False)
    monkeypatch.setattr(engine, "_free_ai_enabled", False, raising=False)
    monkeypatch.setattr(engine, "_ai_disabled", False, raising=False)
    monkeypatch.setattr(engine, "GEMINI_AVAILABLE", False, raising=False)
    monkeypatch.setattr(engine, "_ai_cache", {}, raising=False)
