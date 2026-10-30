# -*- coding: utf-8 -*-
"""
Genera la INFOGRAFIA "Tipos de herramientas de automatizacion" (PNG A4 vertical).
Salida: 01_infografia/infografia_herramientas_automatizacion.png
Tecnica: se construye SVG con posiciones calculadas y el texto se mide con PIL
usando las fuentes reales de Windows, de modo que si una linea no cabe el
generador falla (no produce imagenes recortadas).
"""
import os
import sys
import subprocess
import glob
import html

from PIL import ImageFont

sys.stdout.reconfigure(encoding="utf-8")

BASE = glob.glob(r"C:\Users\kanit\OneDrive\Escritorio\*\chatbot-sacaba")[0]
OUT_DIR = os.path.join(BASE, "GESTION_2026_CUARTO_BIMESTRE", "01_infografia")
os.makedirs(OUT_DIR, exist_ok=True)
TMP = os.path.join(OUT_DIR, "_build")
os.makedirs(TMP, exist_ok=True)

W, H = 1400, 1980
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

F_REG = r"C:\Windows\Fonts\segoeui.ttf"
F_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
F_SEMI = r"C:\Windows\Fonts\seguisb.ttf"
_cache = {}


def font(size, bold=False, semi=False):
    key = (size, bold, semi)
    if key not in _cache:
        path = F_BOLD if bold else (F_SEMI if semi else F_REG)
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def width_px(text, size, bold=False, semi=False):
    return font(size, bold, semi).getlength(text)


def wrap(text, max_px, size, bold=False, semi=False):
    """Ajusta el texto a max_px. Falla si una palabra sola no cabe."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if width_px(cand, size, bold, semi) <= max_px or not cur:
            if not cur and width_px(cand, size, bold, semi) > max_px:
                raise SystemExit(f"LINEA DEMASIADO LARGA ({size}px): {cand!r}")
            cur = cand
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def esc(t):
    return html.escape(t, quote=True)


# ----------------------------------------------------------------- contenido
CARDS = [
    {
        "tag": "WEB",
        "color": "#0F766E",
        "color2": "#14B8A6",
        "title": "Pruebas web / E2E",
        "sub": "Automatizan el navegador real",
        "items": ["Selenium WebDriver", "Playwright", "Cypress"],
        "body": "Conducen Chrome, Edge o Firefox como si fueran un usuario: escriben en el chat, "
                "envian mensajes y capturan pantallas. Es la base de las pruebas funcionales del portal.",
        "use": "Ideal para el chatbot de Sacaba",
    },
    {
        "tag": "MOVIL",
        "color": "#1D4ED8",
        "color2": "#3B82F6",
        "title": "Pruebas en dispositivos moviles",
        "sub": "Android e iOS con un solo codigo",
        "items": ["Appium", "Espresso", "XCUITest"],
        "body": "Permiten escribir la prueba una vez y ejecutarla en telefonos reales o emuladores, "
                "verificando formularios, permisos y navegacion de la app.",
        "use": "Para futuras apps de la municipalidad",
    },
    {
        "tag": "DEBUG",
        "color": "#B45309",
        "color2": "#F59E0B",
        "title": "Depuracion (debugging)",
        "sub": "Encontrar y corregir errores",
        "items": ["VS Code", "IntelliJ IDEA", "NetBeans", "Chrome DevTools"],
        "body": "Permiten frenar la ejecucion en un punto exacto, inspeccionar variables, observar las "
                "peticiones HTTP y revisar el DOM para localizar la causa real del fallo.",
        "use": "Indispensable en la Actividad 3",
    },
    {
        "tag": "API",
        "color": "#7E22CE",
        "color2": "#A855F7",
        "title": "Pruebas de servicios / API",
        "sub": "Validan la capa de datos sin navegador",
        "items": ["Postman", "REST Assured", "SoapUI", "pytest + requests"],
        "body": "Comprueban directamente los endpoints /chat, /api/search o /api/translate. Son las "
                "pruebas mas rapidas y las que detectan errores de logica del servidor.",
        "use": "Rapidas y con poco mantenimiento",
    },
    {
        "tag": "CARGA",
        "color": "#BE123C",
        "color2": "#F43F5E",
        "title": "Rendimiento y carga",
        "sub": "Comportamiento con muchos usuarios",
        "items": ["Apache JMeter", "k6", "Locust", "Gatling"],
        "body": "Envian cientos de peticiones simultaneas para medir el tiempo de respuesta, "
                "el throughput y la tasa de errores cuando el portal recibe mas carga de la habitual.",
        "use": "Garantiza que el portal no se caiga",
    },
    {
        "tag": "CI/CD",
        "color": "#334155",
        "color2": "#64748B",
        "title": "Calidad e integracion continua",
        "sub": "Analisis automatico en cada cambio",
        "items": ["SonarQube / SonarLint", "flake8 / pylint", "GitHub Actions", "Jenkins"],
        "body": "Revisan el codigo buscando fallos y malas practicas, y ejecutan toda la bateria de "
                "pruebas automaticamente cada vez que se sube una version.",
        "use": "Evita errores antes de publicar",
    },
]

parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
)
parts.append(
    """<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#0B1220"/><stop offset="100%" stop-color="#152238"/>
</linearGradient>
<linearGradient id="head" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0%" stop-color="#0F766E"/><stop offset="55%" stop-color="#0E7490"/>
  <stop offset="100%" stop-color="#1D4ED8"/>
</linearGradient>
</defs>"""
)
parts.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')

# ------------------------------------------------------------------ cabecera
parts.append('<rect x="0" y="0" width="%d" height="250" fill="url(#head)"/>' % W)
parts.append('<rect x="70" y="52" width="86" height="86" rx="18" fill="#ffffff" opacity="0.16"/>')
parts.append(
    '<path d="M92 95 h14 l7 12 7-12 h14 v30 h-11 v-19 l-10 16 -10-16 v19 h-11 z" fill="#ffffff"/>'
)
parts.append(
    '<text x="176" y="88" font-family="Segoe UI" font-size="26" font-weight="600" '
    'fill="#A7F3D0" letter-spacing="3">GESTION DE PROYECTOS DE SOFTWARE</text>'
)
parts.append(
    '<text x="176" y="140" font-family="Segoe UI" font-size="46" font-weight="700" fill="#ffffff">'
    "Tipos de herramientas de automatizacion</text>"
)
sub = wrap(
    "Familias de herramientas y para que se usan dentro del ciclo de pruebas del chatbot municipal",
    1260, 24, semi=True,
)
for i, ln in enumerate(sub):
    parts.append(
        '<text x="70" y="%d" font-family="Segoe UI" font-size="24" font-weight="600" fill="#C7D2FE">%s</text>'
        % (172 + i * 32, esc(ln))
    )

# ------------------------------------------------------------------ tarjetas
MG = 70
GAP = 30
CARD_W = (W - MG * 2 - GAP) // 2
CARD_H = 494
TOP = 292

for idx, card in enumerate(CARDS):
    col, row = idx % 2, idx // 2
    x = MG + col * (CARD_W + GAP)
    y = TOP + row * (CARD_H + GAP)
    c, c2 = card["color"], card["color2"]

    parts.append(
        '<rect x="%d" y="%d" width="%d" height="%d" rx="22" fill="#1E293B" stroke="#334155" stroke-width="2"/>'
        % (x, y, CARD_W, CARD_H)
    )
    parts.append(
        '<path d="M%d %d h%d v8 a18 18 0 0 1 -18 18 h-%d a18 18 0 0 1 -18 -18 z" fill="%s"/>'
        % (x, y, CARD_W, CARD_W - 36, c)
    )

    # tag
    tw = width_px(card["tag"], 17, bold=True) + 34
    parts.append(
        '<rect x="%d" y="%d" width="%.0f" height="32" rx="16" fill="%s"/>'
        % (x + 28, y + 34, tw, c2)
    )
    parts.append(
        '<text x="%.0f" y="%d" font-family="Segoe UI" font-size="17" font-weight="700" fill="#0B1220" '
        'text-anchor="middle" letter-spacing="1">%s</text>'
        % (x + 28 + tw / 2, y + 56, esc(card["tag"]))
    )

    # titulo + subtitulo
    parts.append(
        '<text x="%d" y="%d" font-family="Segoe UI" font-size="29" font-weight="700" fill="#F8FAFC">%s</text>'
        % (x + 28, y + 108, esc(card["title"]))
    )
    parts.append(
        '<text x="%d" y="%d" font-family="Segoe UI" font-size="19" font-weight="600" fill="%s">%s</text>'
        % (x + 28, y + 136, c2, esc(card["sub"]))
    )

    # chips de herramientas (2 por fila como maximo)
    cy = y + 160
    cx = x + 28
    for it in card["items"]:
        fs = 19
        wpx = width_px(it, fs, semi=True)
        if wpx + 30 > CARD_W - 56:
            cy += 46
            cx = x + 28
        parts.append(
            '<rect x="%.0f" y="%d" width="%.0f" height="38" rx="10" fill="#0F172A" stroke="%s" stroke-width="1.5"/>'
            % (cx, cy, wpx + 30, c)
        )
        parts.append(
            '<text x="%.0f" y="%d" font-family="Segoe UI" font-size="%d" font-weight="600" fill="#E2E8F0">%s</text>'
            % (cx + 15, cy + 25, fs, esc(it))
        )
        cx += wpx + 30 + 12

    # cuerpo
    by = cy + 66
    for ln in wrap(card["body"], CARD_W - 56, 19):
        parts.append(
            '<text x="%d" y="%d" font-family="Segoe UI" font-size="19" fill="#CBD5E1">%s</text>'
            % (x + 28, by, esc(ln))
        )
        by += 29

    # pie: para que sirve
    fy = y + CARD_H - 54
    parts.append(
        '<rect x="%d" y="%d" width="%d" height="40" rx="10" fill="#0F172A" stroke="%s" stroke-width="1.5"/>'
        % (x + 28, fy - 28, CARD_W - 56, c)
    )
    parts.append(
        '<text x="%d" y="%d" font-family="Segoe UI" font-size="17" font-weight="600" fill="%s">%s</text>'
        % (x + 44, fy, c2, esc(card["use"]))
    )

# -------------------------------------------------------------------- footer
fy = TOP + 3 * (CARD_H + GAP) + 6
parts.append('<rect x="%d" y="%d" width="%d" height="2" fill="#334155"/>' % (MG, fy, W - MG * 2))
parts.append(
    '<text x="%d" y="%d" font-family="Segoe UI" font-size="20" font-weight="600" fill="#94A3B8">'
    "Alumno: Alfredo Ramirez Espinoza  ·  Sistemas Informaticos  ·  ITSA  ·  Gestion 2026</text>"
    % (MG, fy + 40)
)
parts.append(
    '<text x="%d" y="%d" font-family="Segoe UI" font-size="20" font-weight="600" fill="#94A3B8" '
    'text-anchor="end">Sistema evaluado: Chatbot Municipal G.A.M. Sacaba (Flask + Python)</text>'
    % (W - MG, fy + 40)
)

svg = "\n".join(parts) + "\n</svg>\n"
svg_path = os.path.join(TMP, "infografia.svg")
with open(svg_path, "w", encoding="utf-8") as f:
    f.write(svg)

html_path = os.path.join(TMP, "infografia.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(
        "<!DOCTYPE html><html><head><meta charset='utf-8'><style>"
        "html,body{margin:0;padding:0;background:#0B1220;width:%dpx;height:%dpx;overflow:hidden}"
        "svg{display:block}</style></head><body>%s</body></html>" % (W, H, svg)
    )

png = os.path.join(OUT_DIR, "infografia_herramientas_automatizacion.png")
if os.path.exists(png):
    os.remove(png)
r = subprocess.run(
    [EDGE, "--headless", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
     "--window-size=%d,%d" % (W, H), "--screenshot=" + png, "file:///" + html_path.replace("\\", "/")],
    capture_output=True, text=True, timeout=180,
)

from PIL import Image

im = Image.open(png)
px = im.convert("L")
hist = px.histogram()
ink = sum(hist[:245]) / (im.width * im.height)
print("PNG:", os.path.getsize(png), "bytes |", im.size)
print("densidad de tinta: %.4f (control 0.03-0.35)" % ink)
print("ultimas lineas: unique=%d" % len(set(px.crop((0, im.height - 6, im.width, im.height)).getdata())))
print("edge rc:", r.returncode)