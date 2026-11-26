#!/usr/bin/env python3
"""Genera los diagramas de despliegue y de subsistemas de Diseño con la misma
forma que los originales del grupo (hechos en PlantUML): nodos en 3D,
componentes con su ícono, base de datos como cilindro y paquetes con pestaña.

Salida (SVG y PNG):
    "3. Diseño/1_Diagrama de Despliegue.svg" y ".png"
    "3. Diseño/2_Diagrama de Subsistemas.svg" y ".png"

El contenido sale del código actual (CU0001, CU0006 y CU0010); la explicación
de cada nodo y subsistema está en docs/DISEÑO_UMBook.md §5 y §6. **Los nombres
de este script y los del texto tienen que coincidir.**

El .png se genera con ImageMagick (`magick`, con librsvg) si está instalado; si
no, se puede obtener del .svg con cualquier conversor.

Uso: python3 docs/generar_despliegue_subsistemas.py
"""
import shutil
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape

RAIZ = Path(__file__).resolve().parent.parent
CARPETA = RAIZ / "3. Diseño"

# Colores y medidas del estilo por defecto de PlantUML
TINTA = "#181818"
RELLENO = "#F1F1F1"
NOTA = "#FEFFDD"
FUENTE = "Noto Sans, DejaVu Sans, Verdana, sans-serif"
F_TEXTO = 14      # texto de componentes
F_TITULO = 15     # título de nodos y paquetes (negrita)
F_ETIQUETA = 13   # etiquetas de las flechas y notas
PROF = 10         # profundidad del nodo 3D


def ancho_texto(texto, tam=F_TEXTO, negrita=False):
    """Ancho aproximado en píxeles (Noto Sans: ~0,55 em por carácter)."""
    return len(texto) * tam * (0.60 if negrita else 0.55)


class Lienzo:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.out = []

    def texto(self, x, y, s, tam=F_TEXTO, negrita=False, ancla="middle", cursiva=False):
        estilo = ' font-weight="bold"' if negrita else ""
        estilo += ' font-style="italic"' if cursiva else ""
        self.out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{tam}" text-anchor="{ancla}"'
                        f'{estilo} fill="{TINTA}">{escape(s)}</text>')

    def nodo(self, x, y, w, h, titulo):
        """Nodo UML en 3D: cara frontal, tapa y lateral."""
        d = PROF
        self.out.append(
            f'<polygon points="{x},{y + d} {x + d},{y} {x + w},{y} {x + w - d},{y + d}" '
            f'fill="#fff" stroke="{TINTA}" stroke-width="1.5"/>'
            f'<polygon points="{x + w - d},{y + d} {x + w},{y} {x + w},{y + h - d} {x + w - d},{y + h}" '
            f'fill="#fff" stroke="{TINTA}" stroke-width="1.5"/>'
            f'<rect x="{x}" y="{y + d}" width="{w - d}" height="{h - d}" fill="#fff" '
            f'stroke="{TINTA}" stroke-width="1.5"/>')
        self.texto(x + (w - d) / 2, y + d + 20, titulo, F_TITULO, negrita=True)

    def componente(self, x, y, w, h, lineas, estereotipo=None):
        """Componente: rectángulo gris con el ícono de componente arriba a la derecha."""
        self.out.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2.5" fill="{RELLENO}" '
            f'stroke="{TINTA}" stroke-width="0.6"/>'
            f'<rect x="{x + w - 22}" y="{y + 6}" width="15" height="10" fill="{RELLENO}" '
            f'stroke="{TINTA}" stroke-width="0.6"/>'
            f'<rect x="{x + w - 24}" y="{y + 8}" width="4" height="2" fill="{RELLENO}" '
            f'stroke="{TINTA}" stroke-width="0.6"/>'
            f'<rect x="{x + w - 24}" y="{y + 12}" width="4" height="2" fill="{RELLENO}" '
            f'stroke="{TINTA}" stroke-width="0.6"/>')
        filas = ([f"«{estereotipo}»"] if estereotipo else []) + list(lineas)
        alto = 18
        y0 = y + h / 2 - (len(filas) - 1) * alto / 2 + 5
        for i, s in enumerate(filas):
            es_est = estereotipo and i == 0
            tam = F_ETIQUETA if (es_est or i > (1 if estereotipo else 0)) else F_TEXTO
            self.texto(x + w / 2, y0 + i * alto, s, tam, cursiva=bool(es_est))

    def base_de_datos(self, x, y, w, h, lineas):
        """Base de datos: cilindro."""
        e = 9
        self.out.append(
            f'<path d="M{x},{y + e} A{w / 2},{e} 0 0 1 {x + w},{y + e} L{x + w},{y + h - e} '
            f'A{w / 2},{e} 0 0 1 {x},{y + h - e} Z" fill="{RELLENO}" stroke="{TINTA}" stroke-width="0.6"/>'
            f'<path d="M{x},{y + e} A{w / 2},{e} 0 0 0 {x + w},{y + e}" fill="none" '
            f'stroke="{TINTA}" stroke-width="0.6"/>')
        y0 = y + h / 2 + 2 * e / 2 - (len(lineas) - 1) * 9 + 5
        for i, s in enumerate(lineas):
            self.texto(x + w / 2, y0 + i * 18, s, F_TEXTO if i == 0 else F_ETIQUETA)

    def paquete(self, x, y, w, h, titulo):
        """Paquete UML: pestaña con el nombre y cuerpo."""
        tw = ancho_texto(titulo, F_TITULO, True) + 12
        th = 22
        self.out.append(
            f'<path d="M{x},{y + th} L{x},{y + 2.5} Q{x},{y} {x + 2.5},{y} L{x + tw},{y} '
            f'L{x + tw + 7},{y + th}" fill="#fff" stroke="{TINTA}" stroke-width="1.5"/>'
            f'<rect x="{x}" y="{y + th}" width="{w}" height="{h - th}" rx="2.5" fill="#fff" '
            f'stroke="{TINTA}" stroke-width="1.5"/>')
        self.texto(x + 5, y + 16, titulo, F_TITULO, negrita=True, ancla="start")

    def flecha(self, puntos, etiqueta=(), pos=None, ancla="start"):
        """Flecha continua con punta llena (estilo PlantUML) y etiqueta opcional."""
        camino = " ".join(f"{px},{py}" for px, py in puntos)
        self.out.append(f'<polyline points="{camino}" fill="none" stroke="{TINTA}" stroke-width="1"/>')
        (x1, y1), (x2, y2) = puntos[-2], puntos[-1]
        largo = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        ux, uy = (x2 - x1) / largo, (y2 - y1) / largo
        px, py = -uy, ux
        b = (x2 - 10 * ux, y2 - 10 * uy)
        m = (x2 - 6 * ux, y2 - 6 * uy)
        self.out.append(
            f'<polygon points="{x2},{y2} {b[0] + 4 * px:.1f},{b[1] + 4 * py:.1f} '
            f'{m[0]:.1f},{m[1]:.1f} {b[0] - 4 * px:.1f},{b[1] - 4 * py:.1f}" fill="{TINTA}"/>')
        if etiqueta:
            for i, s in enumerate(etiqueta):
                self.texto(pos[0], pos[1] + i * 16, s, F_ETIQUETA, ancla=ancla)

    def nota(self, x, y, w, lineas):
        """Nota con la esquina doblada."""
        h = 16 * len(lineas) + 14
        c = 10
        self.out.append(
            f'<path d="M{x},{y} L{x + w - c},{y} L{x + w},{y + c} L{x + w},{y + h} L{x},{y + h} Z" '
            f'fill="{NOTA}" stroke="{TINTA}" stroke-width="0.6"/>'
            f'<path d="M{x + w - c},{y} L{x + w - c},{y + c} L{x + w},{y + c}" fill="none" '
            f'stroke="{TINTA}" stroke-width="0.6"/>')
        for i, s in enumerate(lineas):
            self.texto(x + 8, y + 20 + i * 16, s, F_ETIQUETA, ancla="start")

    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}" font-family="{FUENTE}">'
                f'<rect width="{self.w}" height="{self.h}" fill="#fff"/>'
                + "\n".join(self.out) + "</svg>")


# ------------------------------------------------------------------ despliegue
def despliegue():
    L = Lienzo(720, 700)

    # Todo lo local corre en el mismo equipo (Flask escucha solo en 127.0.0.1)
    L.nodo(10, 10, 680, 480, "Equipo local (127.0.0.1)")

    L.nodo(210, 55, 280, 125, "Cliente Web")
    L.componente(250, 100, 190, 58, ["Navegador web", "SPA Angular 22"])

    L.nodo(35, 265, 260, 125, "Servidor Frontend")
    L.componente(65, 310, 190, 58, ["Node.js · ng serve", "puerto 4200"])

    L.nodo(355, 245, 315, 230, "Servidor Backend")
    L.componente(380, 290, 250, 58, ["Flask 3 · Python 3", "API REST · puerto 5000"])
    L.base_de_datos(380, 385, 180, 72, ["SQLite", "instance/umbook.db"])

    L.nodo(395, 560, 285, 125, "Servidor de Correo")
    L.componente(430, 605, 205, 58, ["Gmail (SMTP)", "smtp.gmail.com:587"])

    # Comunicaciones
    L.flecha([(300, 158), (160, 310)], ["HTTP", "(descarga la SPA)"], (220, 215), ancla="end")
    L.flecha([(400, 158), (500, 290)], ["HTTP / JSON", "Authorization: Bearer JWT"], (462, 210))
    L.flecha([(470, 348), (470, 385)], ["SQLAlchemy"], (478, 372))
    L.flecha([(609, 348), (609, 605)], ["SMTP + TLS", "(Flask-Mail)"], (617, 520))

    L.nota(20, 560, 330, [
        "Despliegue de demostración: los tres nodos",
        "locales corren en el mismo equipo. Flask",
        "escucha solo en 127.0.0.1 y no hay HTTPS",
        "(RNF-10, no cumplido).",
    ])
    return L.svg()


# ----------------------------------------------------------------- subsistemas
# Cada paquete: (título, columnas, componentes); componente: (líneas, estereotipo)
SUBSISTEMAS = [
    ("Aplicación Específica", 3, [
        (["Gestión de Usuarios", "CU0001 · CU0006 · CU0010"], "implementado"),
        (["Gestión de Relaciones"], None),
        (["Gestión de Contenido"], None),
        (["Notificaciones"], None),
        (["Control de Accesos"], None),
        (["Administración"], None),
    ]),
    ("Aplicación General", 2, [
        (["Autenticación y Seguridad", "JWT · hash de claves · @token_required"], None),
        (["Gestión de Correos", "NotificationService «Singleton»"], None),
        (["Persistencia", "DAO · SQLAlchemy"], None),
        (["Validación de Datos", "esquemas marshmallow"], None),
    ]),
    ("Capa Intermedia", 3, [
        (["Flask 3", "Blueprints · Flask-CORS"], None),
        (["Flask-JWT-Extended"], None),
        (["Flask-SQLAlchemy"], None),
        (["Flask-Mail"], None),
        (["marshmallow"], None),
        (["Angular 22", "Router · HttpClient · RxJS"], None),
    ]),
    ("Software del Sistema", 3, [
        (["Python 3"], None),
        (["Node.js"], None),
        (["SQLite"], None),
        (["Navegador web"], None),
        (["HTTP · SMTP/TLS"], None),
    ]),
]

SEP_X, SEP_Y, MARGEN, TAB = 40, 55, 20, 22


def medir_paquete(columnas, comps):
    cw = max(max(ancho_texto(s, F_TEXTO if i == 0 else F_ETIQUETA) for i, s in enumerate(l)) + 60
             for l, _ in comps)
    ch = 70 if any(e for _, e in comps) else 58
    filas = (len(comps) + columnas - 1) // columnas
    w = 2 * MARGEN + columnas * cw + (columnas - 1) * SEP_X
    h = TAB + 2 * MARGEN + filas * ch + (filas - 1) * SEP_Y
    return cw, ch, w, h


def dibujar_paquete(L, x, y, titulo, columnas, comps):
    cw, ch, w, h = medir_paquete(columnas, comps)
    L.paquete(x, y, w, h, titulo)
    for i, (lineas, est) in enumerate(comps):
        f, c = divmod(i, columnas)
        L.componente(x + MARGEN + c * (cw + SEP_X), y + TAB + MARGEN + f * (ch + SEP_Y),
                     cw, ch, lineas, est)
    return w, h


def subsistemas():
    medidas = [medir_paquete(c, comps) for _, c, comps in SUBSISTEMAS]
    w1 = max(medidas[0][2], medidas[2][2])
    w2 = max(medidas[1][2], medidas[3][2])
    h1 = max(medidas[0][3], medidas[1][3])
    h2 = max(medidas[2][3], medidas[3][3])
    sep = 30
    W = 10 + w1 + sep + w2 + 10
    H = 10 + h1 + sep + h2 + 95
    L = Lienzo(int(W), int(H))
    pos = [(10, 10), (10 + w1 + sep, 10), (10, 10 + h1 + sep), (10 + w1 + sep, 10 + h1 + sep)]
    for (titulo, columnas, comps), (x, y) in zip(SUBSISTEMAS, pos):
        dibujar_paquete(L, x, y, titulo, columnas, comps)
    L.nota(10, 10 + h1 + sep + h2 + 20, 700, [
        "«implementado»: subsistema con casos de uso en el código actual (CU0001, CU0006 y CU0010).",
        "Los otros cinco de Aplicación Específica son los paquetes de Análisis todavía sin implementar.",
        "Cada capa usa solo a las de abajo: Específica → General → Intermedia → Software del Sistema.",
    ])
    return L.svg()


# ----------------------------------------------------------------------- main
def a_png(svg_path):
    magick = shutil.which("magick")
    if not magick:
        print(f"  (sin ImageMagick: convertir {svg_path.name} a PNG a mano)")
        return
    png = svg_path.with_suffix(".png")
    subprocess.run([magick, "-density", "192", f"rsvg:{svg_path}", str(png)], check=True)
    print(f"OK   {png.relative_to(RAIZ)}")


def main():
    for nombre, fn in (("1_Diagrama de Despliegue", despliegue),
                       ("2_Diagrama de Subsistemas", subsistemas)):
        destino = CARPETA / f"{nombre}.svg"
        destino.write_text(fn(), encoding="utf-8")
        print(f"OK   {destino.relative_to(RAIZ)}")
        a_png(destino)


if __name__ == "__main__":
    main()
