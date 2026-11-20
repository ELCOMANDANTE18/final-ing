#!/usr/bin/env python3
"""Genera los entregables .docx y .xlsx a partir de los .md de docs/.

  ESPECIFICACIONES_CASOS_DE_USO_UMBook.md
      -> "1. Requerimientos/Casos de Uso/CUxxxx_Nombre.docx"   (una ficha por caso de uso)
  REQUISITOS_NO_FUNCIONALES_UMBook.md
      -> "1. Requerimientos/UMBook_RNF.docx"
  PRUEBAS_UMBook.md
      -> "5. Pruebas/UMBook_Plan_de_Pruebas.docx"              (sección 0)
      -> "5. Pruebas/UMBook_Casos_de_Prueba.xlsx"              (sección 1)
      -> "5. Pruebas/UMBook_Procedimientos_de_Prueba.docx"     (sección 2)

Los .md son la fuente: si un entregable difiere, hay que volver a generarlo.

Uso (desde cualquier carpeta):
    python3 docs/generar_entregables.py

Requisito: pip install python-docx openpyxl
"""
import re
import sys
from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

RAIZ = Path(__file__).resolve().parent.parent
DOCS = RAIZ / "docs"
CASOS = RAIZ / "1. Requerimientos" / "Casos de Uso"
PRUEBAS = RAIZ / "5. Pruebas"

FICHAS = {  # código -> nombre del archivo
    "CU0001": "CU0001_Iniciar_Sesión.docx",
    "CU0006": "CU0006_Registrar_Usuario.docx",
    "CU0011": "CU0011_Solicitar_Amistad.docx",
    "CU0012": "CU0012_Aceptar_Rechazar_Solicitud.docx",
    "CU0013": "CU0013_Notificar_Solicitud_Recibida.docx",
}

INLINE = re.compile(r"(\*\*.+?\*\*|`.+?`|\*.+?\*)")


# ---------------------------------------------------------------- texto

def limpiar(texto: str) -> str:
    return texto.replace("⚠️", "Atención:").replace("✅", "Sí").replace("❌", "No")


def sin_markdown(texto: str) -> str:
    return re.sub(r"\*\*(.+?)\*\*|`(.+?)`|\*(.+?)\*", lambda m: m.group(1) or m.group(2) or m.group(3), limpiar(texto))


def celdas(linea: str):
    return [c.strip() for c in linea.strip().strip("|").split("|")]


def es_separador(linea: str) -> bool:
    return bool(re.fullmatch(r"\|[\s:\-|]+\|", linea.strip()))


# ---------------------------------------------------------------- docx

def agregar_texto(parrafo, texto: str, negrita=False):
    for trozo in INLINE.split(limpiar(texto)):
        if not trozo:
            continue
        if trozo.startswith("**") and trozo.endswith("**"):
            r = parrafo.add_run(trozo[2:-2])
            r.bold = True
        elif trozo.startswith("`") and trozo.endswith("`"):
            r = parrafo.add_run(trozo[1:-1])
            r.font.name = "Consolas"
            r.bold = negrita
        elif trozo.startswith("*") and trozo.endswith("*") and len(trozo) > 2:
            r = parrafo.add_run(trozo[1:-1])
            r.italic = True
            r.bold = negrita
        else:
            r = parrafo.add_run(trozo)
            r.bold = negrita


def sombrear(celda, color="D9E2F3"):
    tcPr = celda._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color)
    tcPr.append(shd)


def agregar_tabla(doc, filas):
    cabecera, cuerpo = filas[0], filas[1:]
    tabla = doc.add_table(rows=1, cols=len(cabecera))
    tabla.style = "Table Grid"
    for i, texto in enumerate(cabecera):
        c = tabla.rows[0].cells[i]
        c.paragraphs[0].text = ""
        agregar_texto(c.paragraphs[0], texto, negrita=True)
        sombrear(c)
    for fila in cuerpo:
        fila = fila + [""] * (len(cabecera) - len(fila))
        cs = tabla.add_row().cells
        for i, texto in enumerate(fila[: len(cabecera)]):
            cs[i].paragraphs[0].text = ""
            agregar_texto(cs[i].paragraphs[0], texto)
    # columna de códigos angosta; el resto se reparte el ancho útil (17 cm)
    angosta = {"Nº": 1.3, "Cod": 1.8, "Campo": 3.5, "ID": 1.8, "Id": 2.0, "Código": 1.8}.get(cabecera[0])
    if angosta and len(cabecera) > 1:
        tabla.autofit = False
        resto = (17 - angosta) / (len(cabecera) - 1)
        anchos = [angosta] + [resto] * (len(cabecera) - 1)
        for col, ancho in zip(tabla.columns, anchos):
            col.width = Cm(ancho)
        for fila in tabla.rows:
            for c, ancho in zip(fila.cells, anchos):
                c.width = Cm(ancho)
    for fila in tabla.rows:
        for c in fila.cells:
            for p in c.paragraphs:
                p.paragraph_format.space_after = Pt(2)
                for r in p.runs:
                    r.font.size = Pt(9)
    doc.add_paragraph()


def md_a_docx(lineas, destino: Path):
    doc = Document()
    estilo = doc.styles["Normal"]
    estilo.font.name = "Calibri"
    estilo.font.size = Pt(10.5)
    i = 0
    while i < len(lineas):
        l = lineas[i].rstrip()
        if not l.strip() or l.strip() == "---" or l.startswith("<!--"):
            i += 1
        elif l.startswith("|"):
            filas = []
            while i < len(lineas) and lineas[i].startswith("|"):
                if not es_separador(lineas[i]):
                    filas.append(celdas(lineas[i]))
                i += 1
            agregar_tabla(doc, filas)
        elif l.startswith("#"):
            nivel = len(l) - len(l.lstrip("#"))
            h = doc.add_heading(limpiar(l.lstrip("#").strip()), level=min(nivel, 3))
            for r in h.runs:
                r.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)
            i += 1
        elif l.startswith(">"):
            p = doc.add_paragraph()
            agregar_texto(p, l.lstrip("> "))
            p.paragraph_format.left_indent = Pt(18)
            i += 1
        elif re.match(r"^\s*[-*] ", l):
            p = doc.add_paragraph(style="List Bullet")
            agregar_texto(p, re.sub(r"^\s*[-*] ", "", l))
            i += 1
        elif re.match(r"^\s*\d+\. ", l):
            p = doc.add_paragraph(style="List Number")
            agregar_texto(p, re.sub(r"^\s*\d+\. ", "", l))
            i += 1
        else:
            p = doc.add_paragraph()
            agregar_texto(p, l)
            i += 1
    destino.parent.mkdir(parents=True, exist_ok=True)
    doc.save(destino)
    print("OK  ", destino.relative_to(RAIZ))


# ---------------------------------------------------------------- fichas y RNF

def encabezado_ficha(codigo, nombre):
    return [
        f"# CASO DE USO {codigo} – {nombre.upper()}",
        "",
        "**Elaboró:** Victor Gimenez · **Aprobó:** · **Revisó:**",
        "",
        "**Fecha:** 20/11/2026 · **Fecha:** · **Fecha:**",
        "",
    ]


def generar_fichas():
    texto = (DOCS / "ESPECIFICACIONES_CASOS_DE_USO_UMBook.md").read_text(encoding="utf-8")
    for sec in re.split(r"(?m)^## (?=CU\d{4} — )", texto)[1:]:
        cabecera, _, cuerpo = sec.partition("\n")
        codigo, _, nombre = cabecera.partition(" — ")
        cuerpo = cuerpo.split("\n---")[0]
        cuerpo = re.split(r"(?m)^## Control del documento", cuerpo)[0]
        lineas = encabezado_ficha(codigo, nombre.strip()) + cuerpo.splitlines()
        lineas = [re.sub(r"^### ", "## ", x) for x in lineas]  # la ficha es un documento aparte
        md_a_docx(lineas, CASOS / FICHAS[codigo])


def generar_rnf():
    rnf = (DOCS / "REQUISITOS_NO_FUNCIONALES_UMBook.md").read_text(encoding="utf-8")
    md_a_docx(rnf.splitlines(), RAIZ / "1. Requerimientos" / "UMBook_RNF.docx")


# ---------------------------------------------------------------- pruebas

def seccion(texto: str, numero: int) -> str:
    """Devuelve el cuerpo de '## <numero>. ...' hasta el próximo '## ' de ese nivel."""
    m = re.search(rf"(?m)^## {numero}\. [^\n]*\n(.*?)(?=^## \d+\. |^## Control del documento)", texto, re.S)
    if not m:
        raise SystemExit(f"No se encontró la sección {numero} en PRUEBAS_UMBook.md")
    return m.group(1)


def generar_pruebas():
    texto = (DOCS / "PRUEBAS_UMBook.md").read_text(encoding="utf-8")
    ficha = [
        "**Versión:** 1.0 · **Última modificación:** 20/11/2026 · **Etapa:** Prueba",
        "",
    ]
    bajar = lambda cuerpo: [re.sub(r"^### ", "## ", l) for l in cuerpo.splitlines()]

    md_a_docx(["# PLAN DE PRUEBAS — UMBook", ""] + ficha + bajar(seccion(texto, 0)),
              PRUEBAS / "UMBook_Plan_de_Pruebas.docx")
    md_a_docx(["# PROCEDIMIENTOS DE PRUEBA — UMBook", ""] + ficha + bajar(seccion(texto, 2)),
              PRUEBAS / "UMBook_Procedimientos_de_Prueba.docx")
    generar_casos_xlsx(seccion(texto, 1))


def generar_casos_xlsx(cuerpo: str):
    wb = Workbook()
    ws = wb.active
    ws.title = "Casos de Prueba"
    cab = ["Id", "Caso de uso", "Objetivo", "Estado inicial", "Datos de Prueba", "Resultado Esperado", "Tipo", "Antes"]
    relleno = PatternFill("solid", fgColor="D9E2F3")
    ws.append(["Casos de Prueba — UMBook"])
    ws["A1"].font = Font(bold=True, size=14)
    ws.append(["Plan, casos y procedimientos: docs/PRUEBAS_UMBook.md. Los códigos de CU están en docs/CATALOGO_CASOS_DE_USO_UMBook.md."])
    ws.append([])
    ws.append(cab)
    for c in ws[4]:
        c.font = Font(bold=True)
        c.fill = relleno

    caso = ""
    lineas = cuerpo.splitlines()
    i = 0
    while i < len(lineas):
        l = lineas[i]
        m = re.match(r"### (CU\d{4}) — (.+)", l)
        if m:
            caso = f"{m.group(1)} {m.group(2).strip()}"
        elif l.startswith("|") and not es_separador(l) and not l.startswith("| Id "):
            f = [sin_markdown(c) for c in celdas(l)]
            if len(f) == 7:
                ws.append([f[0], caso] + f[1:])
        i += 1

    for col, ancho in zip("ABCDEFGH", (12, 30, 38, 34, 38, 55, 40, 18)):
        ws.column_dimensions[col].width = ancho
    for fila in ws.iter_rows(min_row=5):
        for c in fila:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A5"
    destino = PRUEBAS / "UMBook_Casos_de_Prueba.xlsx"
    wb.save(destino)
    print("OK  ", destino.relative_to(RAIZ), f"({ws.max_row - 4} casos)")


def main() -> int:
    generar_fichas()
    generar_rnf()
    generar_pruebas()
    return 0


if __name__ == "__main__":
    sys.exit(main())
