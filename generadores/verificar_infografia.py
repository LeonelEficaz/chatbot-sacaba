# -*- coding: utf-8 -*-
"""Verificacion geometrica de la infografia: comprueba que el texto que se
renderizo queda siempre dentro de los margenes de cada tarjeta (sin recortes)."""
import glob
import os
import sys

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

BASE = [p for p in glob.glob(r"C:\Users\kanit\OneDrive\Escritorio\*\chatbot-sacaba") if os.path.isdir(p)][0]
PNG = os.path.join(
    BASE, "GESTION_2026_CUARTO_BIMESTRE", "01_infografia", "infografia_herramientas_automatizacion.png"
)

im = Image.open(PNG).convert("L")
W, H = im.size
px = im.load()

MG, GAP, CARD_W, CARD_H, TOP = 70, 30, (1400 - 140 - 30) // 2, 494, 292
problems = []


def bright_bbox(x0, y0, x1, y1, thr=205):
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if px[x, y] > thr:
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    return min(xs), min(ys), max(xs), max(ys)


def count_bright(x0, y0, x1, y1, thr=205):
    return sum(1 for y in range(y0, y1) for x in range(x0, x1) if px[x, y] > thr)


print("Imagen:", W, "x", H)
names = [
    "Pruebas web / E2E", "Pruebas moviles", "Depuracion",
    "Pruebas API", "Rendimiento", "Calidad e CI/CD",
]
for i, name in enumerate(names):
    col, row = i % 2, i // 2
    x = MG + col * (CARD_W + GAP)
    y = TOP + row * (CARD_H + GAP)
    bb = bright_bbox(x + 10, y + 10, x + CARD_W - 10, y + CARD_H - 10)
    if bb is None:
        problems.append(f"Tarjeta {i} ({name}): sin texto renderizado")
        continue
    bx0, by0, bx1, by1 = bb
    n = count_bright(x + 10, y + 10, x + CARD_W - 10, y + CARD_H - 10)
    print(
        f"Tarjeta {i} ({name}): texto en x[{bx0 - x}..{bx1 - x}] "
        f"y[{by0 - y}..{by1 - y}] pixeles_texto={n}"
    )
    if bx1 - x > CARD_W - 18:
        problems.append(f"Tarjeta {i}: texto pegado al borde derecho ({bx1 - x}px)")
    if bx0 - x < 18:
        problems.append(f"Tarjeta {i}: texto pegado al borde izquierdo ({bx0 - x}px)")
    if by1 - y > CARD_H - 18:
        problems.append(f"Tarjeta {i}: texto se sale por abajo ({by1 - y}px)")
    if n < 1500:
        problems.append(f"Tarjeta {i}: suspiciously pocos pixeles de texto ({n})")

# cabecera y pie
if count_bright(70, 40, 1330, 210) < 3000:
    problems.append("Cabecera: falta el titulo")
else:
    print("Cabecera: titulo OK")

if count_bright(70, 1880, 1330, 1945, thr=140) < 1200:
    problems.append("Pie: falta el texto de autoria")
else:
    print("Pie: autoria OK (umbral 140, color #94A3B8)")

# recortes de revision visual
OUT = os.path.join(os.path.dirname(PNG), "_build")
color = Image.open(PNG)
for nombre, caja in [
    ("recorte_cabecera", (0, 0, 1400, 250)),
    ("recorte_tarjeta_web", (MG, TOP, MG + CARD_W, TOP + CARD_H)),
    ("recorte_tarjeta_debug", (MG + CARD_W + GAP, TOP, 1400, TOP + CARD_H)),
    ("recorte_pie", (0, 1834, 1400, 1980)),
]:
    color.crop(caja).save(os.path.join(OUT, nombre + ".png"))
print("Recortes de revision guardados en:", OUT)

# areas vacias (posible motor de render sin fuente)
dark_rows = sum(1 for y in range(H) if count_bright(0, y, W, y + 1) == 0)
print("Filas completamente vacias de texto:", dark_rows)

if problems:
    print("\nPROBLEMAS:")
    for p in problems:
        print("  -", p)
    raise SystemExit(1)
print("\nLAYOUT CORRECTO: sin desbordes ni texto recortado.")