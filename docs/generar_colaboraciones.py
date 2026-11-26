#!/usr/bin/env python3
"""Genera los diagramas de colaboración de Análisis con los íconos del
Proceso Unificado (interfaz, control y entidad) y mensajes numerados.

Salida (SVG): "2. Análisis/3_Diagramas de Colaboración/CUxxxx - Nombre.svg"
El .png se obtiene del .svg con cualquier conversor (por ejemplo, abriéndolo
en un navegador). Los mensajes siguen el curso normal de cada ficha; la
explicación está en docs/ANALISIS_UMBook.md §5.

Uso: python3 docs/generar_colaboraciones.py
"""
import math
from pathlib import Path
from xml.sax.saxutils import escape

RAIZ = Path(__file__).resolve().parent.parent
CARPETA = RAIZ / "2. Análisis" / "3_Diagramas de Colaboración"

TINTA = "#1f2937"
AZUL = "#3730a3"
R = 24  # radio de los íconos

# ------------------------------------------------------------------ diagramas
# nodos: id -> (tipo, nombre, x, y); tipo: actor | interfaz | control | entidad
# enlaces: (a, b)
# mensajes: (número, origen, destino, texto)
DIAGRAMAS = [
    {
        "archivo": "CU0001 - Iniciar Sesión",
        "titulo": "CU0001 — Iniciar Sesión",
        "tam": (1180, 500),
        "nodos": {
            "A": ("actor", "Usuario Registrado", 100, 170),
            "PL": ("interfaz", "PantallaLogin", 480, 170),
            "CA": ("control", "ControlAutenticacion", 790, 170),
            "U": ("entidad", "Usuario", 1070, 170),
            "PP": ("interfaz", "PantallaPrincipal", 480, 360),
        },
        "enlaces": [("A", "PL"), ("PL", "CA"), ("CA", "U"), ("PL", "PP")],
        "mensajes": [
            (1, "A", "PL", "ingresar(email, contraseña)"),
            (2, "PL", "CA", "autenticar(email, contraseña)"),
            (3, "CA", "U", "buscarPorEmail(email)"),
            (4, "CA", "U", "verificarContraseña(contraseña)"),
            (5, "CA", "PL", "token de sesión y nombre"),
            (6, "PL", "PP", "guardarToken() y mostrar(nombre)"),
        ],
        "nota": "ca 4.1 y ca 5.1: el mensaje 5 devuelve el error y PantallaLogin lo muestra; no se emite token.",
    },
    {
        "archivo": "CU0006 - Registrar Usuario",
        "titulo": "CU0006 — Registrar Usuario",
        "tam": (1180, 500),
        "nodos": {
            "A": ("actor", "Usuario No Registrado", 100, 170),
            "PR": ("interfaz", "PantallaRegistro", 480, 170),
            "CA": ("control", "ControlAutenticacion", 790, 170),
            "U": ("entidad", "Usuario", 1070, 170),
            "PL": ("interfaz", "PantallaLogin", 480, 360),
        },
        "enlaces": [("A", "PR"), ("PR", "CA"), ("CA", "U"), ("PR", "PL")],
        "mensajes": [
            (1, "A", "PR", "registrarse(nombre, email, contraseña)"),
            (2, "PR", "CA", "registrar(nombre, email, contraseña)"),
            (3, "CA", "U", "existeEmail(email)"),
            (4, "CA", "U", "crear(nombre, email, contraseñaCifrada)"),
            (5, "CA", "PR", "cuenta creada"),
            (6, "PR", "A", "informar(cuenta creada)"),
            (7, "PR", "PL", "mostrar()"),
        ],
        "nota": "ca 5.1 y ca 6.1: el mensaje 5 devuelve el error (datos inválidos o email registrado) y no se crea el usuario.",
    },
    {
        "archivo": "CU0010 - Invitación a la aplicación",
        "titulo": "CU0010 — Invitación a la aplicación",
        "tam": (1320, 640),
        "nodos": {
            "A": ("actor", "Usuario Autenticado", 100, 330),
            "PP": ("interfaz", "PantallaPrincipal", 370, 140),
            "PI": ("interfaz", "PantallaInvitar", 370, 330),
            "CI": ("control", "ControlInvitacion", 690, 330),
            "U": ("entidad", "Usuario", 600, 110),
            "I": ("entidad", "Invitacion", 1000, 210),
            "IC": ("interfaz", "InterfazCorreo", 1000, 460),
            "SC": ("actor", "Servidor de correo", 1220, 460),
        },
        "enlaces": [("A", "PP"), ("PP", "PI"), ("A", "PI"), ("PI", "CI"), ("CI", "U"),
                    ("CI", "I"), ("CI", "IC"), ("IC", "SC")],
        "mensajes": [
            (1, "A", "PP", "elegirInvitar()"),
            (2, "PP", "PI", "mostrar()"),
            (3, "A", "PI", "invitar(email)"),
            (4, "PI", "CI", "invitar(quienInvita, email)"),
            (5, "CI", "U", "obtenerNombre()"),
            (6, "CI", "I", "crear(email) [pendiente]"),
            (7, "CI", "IC", "enviarInvitacion(email, nombre, enlace)"),
            (8, "IC", "SC", "enviar correo"),
            (9, "CI", "I", "marcarEnviada()"),
            (10, "CI", "PI", "invitación enviada"),
            (11, "PI", "A", "mostrar confirmación"),
        ],
        "nota": "ca 4.1: email inválido, no se crea la invitación. ca 5.1: si falla el envío (8), el mensaje 9 es marcarFallida() y se avisa del fallo.",
    },
]


# ------------------------------------------------------------------- dibujo
class Lienzo:
    def __init__(self, w, h):
        self.w, self.h, self.out = w, h, []

    def add(self, s):
        self.out.append(s)

    def texto(self, x, y, s, size=13, weight="normal", anchor="middle", color=TINTA, italic=False):
        st = ' font-style="italic"' if italic else ""
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
                 f'text-anchor="{anchor}" fill="{color}"{st}>{escape(s)}</text>')

    def linea(self, x1, y1, x2, y2, w=1.4, extra=""):
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'stroke="{TINTA}" stroke-width="{w}" {extra}/>')

    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}" font-family="Segoe UI, Helvetica, Arial, sans-serif">'
                '<defs><marker id="m" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" '
                f'markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="{AZUL}"/></marker></defs>'
                f'<rect width="{self.w}" height="{self.h}" fill="#fff"/>' + "\n".join(self.out) + "</svg>")


def icono(L, tipo, nombre, x, y):
    c = f'fill="#fff" stroke="{TINTA}" stroke-width="2"'
    if tipo == "actor":
        L.add(f'<circle cx="{x}" cy="{y-30}" r="11" {c}/>')
        L.linea(x, y - 19, x, y + 12, 2)
        L.linea(x - 20, y - 8, x + 20, y - 8, 2)
        L.linea(x, y + 12, x - 16, y + 36, 2)
        L.linea(x, y + 12, x + 16, y + 36, 2)
        ly = y + 56
    else:
        L.add(f'<circle cx="{x}" cy="{y}" r="{R}" {c}/>')
        if tipo == "interfaz":
            L.linea(x - R - 14, y - R + 4, x - R - 14, y + R - 4, 2)
            L.linea(x - R - 14, y, x - R, y, 2)
        elif tipo == "control":
            L.add(f'<path d="M{x+7},{y-R-7} L{x-1},{y-R} L{x+7},{y-R+7}" fill="none" '
                  f'stroke="{TINTA}" stroke-width="2" stroke-linejoin="round"/>')
        elif tipo == "entidad":
            L.linea(x - R, y + R, x + R, y + R, 2)
        ly = y + R + 20
    L.texto(x, ly, nombre, size=13.5, weight="bold")


def borde(nodo, hacia):
    """Punto donde el enlace toca el ícono."""
    tipo, _, x, y = nodo
    hx, hy = hacia[2], hacia[3]
    dx, dy = hx - x, hy - y
    d = math.hypot(dx, dy) or 1
    if dy > 0 and abs(dy) > 1.5 * abs(dx):
        # Enlace hacia abajo: sale por debajo del nombre, no lo cruza.
        return x + dx / d * 10, y + (64 if tipo == "actor" else R + 28)
    if tipo == "actor":
        return x + dx / d * 30, y - 6 + dy / d * 30
    if tipo == "interfaz" and dx < 0 and abs(dx) > abs(dy):
        return x - R - 14, y  # se engancha en la barra de la interfaz
    return x + dx / d * (R + 3), y + dy / d * (R + 3)


def dibujar(diag):
    w, h = diag["tam"]
    L = Lienzo(w, h)
    nodos = diag["nodos"]
    L.texto(30, 38, "Diagrama de colaboración — " + diag["titulo"], size=18, weight="bold", anchor="start")

    # Enlaces
    for a, b in diag["enlaces"]:
        x1, y1 = borde(nodos[a], nodos[b])
        x2, y2 = borde(nodos[b], nodos[a])
        L.linea(x1, y1, x2, y2, 1.4)

    # Mensajes: se agrupan por enlace y sentido; cada grupo lleva una flecha
    # paralela al enlace y sus rótulos apilados del mismo lado.
    grupos = {}
    for n, o, d, t in diag["mensajes"]:
        grupos.setdefault((o, d), []).append((n, t))
    for (o, d), msgs in grupos.items():
        _, _, xo, yo = nodos[o]
        _, _, xd, yd = nodos[d]
        ux, uy = xd - xo, yd - yo
        largo = math.hypot(ux, uy)
        ux, uy = ux / largo, uy / largo
        # La normal se calcula sobre el enlace en un sentido fijo (de izquierda a
        # derecha, o de arriba abajo): un sentido de los mensajes va de un lado
        # del enlace y el sentido contrario, del otro.
        cx_, cy_ = (ux, uy) if (ux, uy) > (0, 0) and (ux > 1e-9 or (abs(ux) < 1e-9 and uy > 0)) else (-ux, -uy)
        nx, ny = cy_, -cx_                     # lado "de arriba" del enlace
        if (ux, uy) != (cx_, cy_):
            nx, ny = -nx, -ny                  # sentido contrario: el otro lado
        mx, my = (xo + xd) / 2, (yo + yd) / 2
        ax, ay = mx + nx * 14, my + ny * 14
        L.add(f'<line x1="{ax-ux*22:.1f}" y1="{ay-uy*22:.1f}" x2="{ax+ux*22:.1f}" y2="{ay+uy*22:.1f}" '
              f'stroke="{AZUL}" stroke-width="1.6" marker-end="url(#m)"/>')
        # Rótulos
        if abs(nx) < 0.35:
            anchor = "middle"
        else:
            anchor = "start" if nx > 0 else "end"
        base_x = ax + nx * 12
        paso = 17
        if ny < -0.35:      # rótulos por encima: se apilan hacia arriba
            ys = [ay + ny * 12 - 4 - paso * (len(msgs) - 1 - i) for i in range(len(msgs))]
        elif ny > 0.35:     # por debajo: hacia abajo
            ys = [ay + ny * 12 + 12 + paso * i for i in range(len(msgs))]
        else:               # a un costado: centrados en la flecha
            ys = [ay + 5 - paso * (len(msgs) - 1) / 2 + paso * i for i in range(len(msgs))]
        for (n, t), yy in zip(msgs, ys):
            L.texto(base_x, yy, f"{n}: {t}", size=12.5, anchor=anchor, color=AZUL)

    for tipo, nombre, x, y in nodos.values():
        icono(L, tipo, nombre, x, y)

    # Nota y leyenda
    L.texto(30, h - 58, diag["nota"], size=12.5, anchor="start", italic=True, color="#475569")
    lx, ly = 30, h - 26
    for tipo, nombre in (("interfaz", "Interfaz"), ("control", "Control"), ("entidad", "Entidad")):
        sub = Lienzo(0, 0)
        cx = lx + 30
        # íconos chicos de la leyenda
        r = 9
        c = f'fill="#fff" stroke="{TINTA}" stroke-width="1.5"'
        L.add(f'<circle cx="{cx}" cy="{ly-4}" r="{r}" {c}/>')
        if tipo == "interfaz":
            L.linea(cx - r - 7, ly - 11, cx - r - 7, ly + 3, 1.5)
            L.linea(cx - r - 7, ly - 4, cx - r, ly - 4, 1.5)
        elif tipo == "control":
            L.add(f'<path d="M{cx+4},{ly-4-r-4} L{cx},{ly-4-r} L{cx+4},{ly-4-r+4}" fill="none" stroke="{TINTA}" stroke-width="1.5"/>')
        else:
            L.linea(cx - r, ly - 4 + r, cx + r, ly - 4 + r, 1.5)
        L.texto(cx + 18, ly + 1, nombre, size=12.5, anchor="start")
        lx += 130
    L.add(f'<line x1="{lx+10}" y1="{ly-4}" x2="{lx+46}" y2="{ly-4}" stroke="{AZUL}" stroke-width="1.6" marker-end="url(#m)"/>')
    L.texto(lx + 56, ly + 1, "n: mensaje, en el orden del curso normal de la ficha", size=12.5, anchor="start")
    return L.svg()


def main():
    CARPETA.mkdir(parents=True, exist_ok=True)
    for diag in DIAGRAMAS:
        destino = CARPETA / (diag["archivo"] + ".svg")
        destino.write_text(dibujar(diag), encoding="utf-8")
        print("OK  ", destino.relative_to(RAIZ))


if __name__ == "__main__":
    main()
