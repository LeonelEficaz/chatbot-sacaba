# Sami Sacaba — Chatbot bilingüe español–quechua

Asistente virtual y portal de trámites del **Gobierno Autónomo Municipal de Sacaba**
(Cochabamba, Bolivia). Responde en español y quechua, muestra las 20 fichas de
trámites, incluye voz neuronal (Edge TTS), dictado por micrófono, mapas con
OpenStreetMap y un panel administrativo con roles.

- **Aplicación publicada:** <https://sami-sacaba.onrender.com> (Render, plan Free)
- **Repositorio:** <https://github.com/LeonelEficaz/chatbot-sacaba>

## Requisitos

- Python 3.12 o superior (en local se probó con 3.14)
- Dependencias de `requirements.txt`

## Ejecución local

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env        # completar claves si se usan servicios de IA
python app.py                 # abre http://127.0.0.1:5000
```

También se puede generar el ejecutable de escritorio con PyInstaller:

```bash
pyinstaller ChatbotSacaba.spec
```

## Pruebas

```bash
pip install pytest
python -m pytest tests -q
```

## Despliegue gratuito (Render)

El repositorio incluye `render.yaml`, `Procfile`, `wsgi.py` y `.python-version`
para publicarlo como *Web Service* gratuito sin dominio propio ni hosting de pago.

1. Entrar a <https://dashboard.render.com> e iniciar sesión con GitHub.
2. **New → Blueprint**, elegir el repositorio `LeonelEficaz/chatbot-sacaba`.
3. Render lee `render.yaml` y crea el servicio `sami-sacaba` con Gunicorn.
4. Configurar en *Environment* las variables secretas que se usen
   (`OPENAI_API_KEY`, `GEMINI_API_KEY`, etc.). `SECRET_KEY` se genera sola.
5. Al terminar el despliegue, la URL queda como
   `https://sami-sacaba.onrender.com`.

Cada `git push` a `main` vuelve a desplegar automáticamente.

### Variables de entorno

| Variable | Uso |
| --- | --- |
| `SECRET_KEY` | Firma de sesiones y formularios (obligatoria en producción) |
| `PORT` | Puerto que asigna el hosting (Render lo define solo) |
| `HOST` | Interfaz de escucha; en el hosting se usa `0.0.0.0` |
| `OPENAI_API_KEY`, `OPENAI_MODEL` | Proveedor principal de IA |
| `GEMINI_API_KEY`, `GEMINI_MODEL` | Respaldo de IA |
| `SACABA_FREE_AI`, `SACABA_FREE_AI_URL` | IA gratuita de respaldo sin clave |
| `SACABA_USERS_FILE` | Ruta del archivo de usuarios del panel |
| `SACABA_DISABLE_AI=1` | Deja solo el motor local de respuestas |

## Seguridad

- `.env` **nunca** se versiona: contiene credenciales reales. Solo se publica
  `.env.example` con valores de ejemplo.
- `data/usuarios.json`, los registros de aprendizaje y los audios TTS se generan
  en tiempo de ejecución y están excluidos por `.gitignore`.
- En el plan gratuito el disco es efímero: los usuarios creados en el panel y la
  caché de voz se pierden al reiniciar el servicio.

## Estructura

```
app.py                  Rutas Flask y configuración
wsgi.py                 Punto de entrada para Gunicorn
chatbot/                Motor de diálogo, trámites, TTS, STT y autenticación
templates/              Vistas Jinja (portada, trámites, panel, login)
static/                 CSS, JS, imágenes y audios generados
tests/                  Pruebas unitarias, de caja blanca y de portal
render.yaml             Blueprint de despliegue gratuito
```
