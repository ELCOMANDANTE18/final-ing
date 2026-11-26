#!/usr/bin/env python3
"""Genera los .png de los diagramas a partir de los bloques Mermaid de los .md.

Cada bloque ```mermaid que lleve justo encima una línea
    <!-- png: ruta/relativa/a/la/raíz/del/repo.png -->
se renderiza en esa ruta. Los .md son la fuente; los .png se regeneran.

Uso (desde cualquier carpeta):
    python3 docs/generar_diagramas.py            # genera todos
    python3 docs/generar_diagramas.py CU0011     # solo los que tengan ese texto en la ruta

Requisito: Mermaid CLI 12 (`npm install -g @mermaid-js/mermaid-cli@12`), que trae
el tema `redux-color` de los diagramas de secuencia de la compañera. Si `mmdc`
no está en el PATH, indicar su ruta con la variable de entorno MMDC (por
ejemplo, un script que ejecute `npx -y @mermaid-js/mermaid-cli@12 "$@"`).
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PATRON = re.compile(r"<!-- png: (.+?) -->\s*\n```mermaid\n(.*?)\n```", re.S)


def encontrar_fuentes():
    for carpeta in (RAIZ / "docs", RAIZ / "3. Diseño"):
        yield from sorted(carpeta.rglob("*.md"))


def main(filtro: str = "") -> int:
    mmdc = os.environ.get("MMDC") or shutil.which("mmdc")
    if not mmdc:
        print("No se encontró mmdc. Instalarlo o indicar su ruta en MMDC.", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        config = Path(tmp) / "puppeteer.json"
        config.write_text(json.dumps({"args": ["--no-sandbox"]}))
        generados = fallidos = 0
        for md in encontrar_fuentes():
            for destino, codigo in PATRON.findall(md.read_text(encoding="utf-8")):
                if filtro and filtro not in destino:
                    continue
                salida = RAIZ / destino
                salida.parent.mkdir(parents=True, exist_ok=True)
                fuente = Path(tmp) / "diagrama.mmd"
                fuente.write_text(codigo, encoding="utf-8")
                r = subprocess.run(
                    [mmdc, "-i", str(fuente), "-o", str(salida), "-p", str(config),
                     "-b", "white", "-s", "2", "--size", "1800"],
                    capture_output=True, text=True,
                )
                if r.returncode == 0:
                    generados += 1
                    print(f"OK   {destino}")
                else:
                    fallidos += 1
                    print(f"FALLO {destino}\n{r.stderr.strip()}", file=sys.stderr)
    print(f"\n{generados} generados, {fallidos} con error.")
    return 1 if fallidos else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
