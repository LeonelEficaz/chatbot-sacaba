import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from chatbot import engine


@pytest.fixture(autouse=True)
def entorno_offline(monkeypatch):
    """Mantiene la suite sin red: el chat usa el motor local y nunca consulta proveedores externos."""
    monkeypatch.setattr(engine, "_openai_dead", True, raising=False)
    monkeypatch.setattr(engine, "_free_ai_enabled", False, raising=False)
    monkeypatch.setattr(engine, "_ai_disabled", False, raising=False)
    monkeypatch.setattr(engine, "GEMINI_AVAILABLE", False, raising=False)
    monkeypatch.setattr(engine, "_ai_cache", {}, raising=False)
