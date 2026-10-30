# -*- coding: utf-8 -*-
"""Exporta un PPTX a PNG usando PowerPoint COM (resuelve la ruta con NBSP)."""
import glob
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

BASE = [p for p in glob.glob(r"C:\Users\kanit\OneDrive\Escritorio\*\chatbot-sacaba") if os.path.isdir(p)][0]
ROOT = os.path.join(BASE, "GESTION_2026_CUARTO_BIMESTRE")

pptxs = []
for root, _dirs, files in os.walk(ROOT):
    for f in files:
        if f.lower().endswith(".pptx") and not f.startswith("~$"):
            pptxs.append(os.path.join(root, f))
pptxs.sort()
if not pptxs:
    raise SystemExit("No hay PPTX en " + ROOT)

from PIL import Image

for pptx in pptxs:
    rel = os.path.relpath(os.path.dirname(pptx), ROOT)
    out = os.path.join(ROOT, rel, "diapositivas_png")
    print("=" * 70)
    print("PPTX:", os.path.basename(pptx), "->", out)
    r = subprocess.run(
        [
            "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
            "-File", r"C:\Users\kanit\AppData\Local\Temp\opencode\exportar_pptx.ps1",
            "-Pptx", pptx, "-OutDir", out, "-Width", "1920", "-Height", "1080",
        ],
        capture_output=True, text=True, timeout=900,
    )
    print(r.stdout.strip())
    if r.returncode != 0:
        print("STDERR:", r.stderr[:1200])
        continue
    for f in sorted(os.listdir(out)):
        if not f.endswith(".png"):
            continue
        p = os.path.join(out, f)
        im = Image.open(p).convert("L")
        colors = im.getcolors(maxcolors=200000) or []
        print(f"  {f}  {os.path.getsize(p)//1024} KB  {im.size[0]}x{im.size[1]}  colores={len(colors)}")