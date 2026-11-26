#!/usr/bin/env python3
"""Genera el diagrama de casos de uso único de UMBook (UML) como SVG.

Salida: "1. Requerimientos/3_Diagrama de Casos de Uso/Diagrama de Casos de Uso - UMBook.svg"

El .png y el .pdf se obtienen del .svg abriéndolo en un navegador (o con
cualquier conversor de SVG). Los códigos y los nombres salen de
docs/CATALOGO_CASOS_DE_USO_UMBook.md: si se cambia uno, hay que cambiarlo en los dos.

Uso: python3 docs/generar_diagrama_casos_de_uso.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "1. Requerimientos" / "3_Diagrama de Casos de Uso" / "Diagrama de Casos de Uso - UMBook.svg"

W, H = 1720, 1480
TINTA = "#1f2937"
IMPL_FONDO, IMPL_BORDE = "#e0e7ff", "#4338ca"
PAQ_FONDO = "#f8fafc"

# ----------------------------------------------------------------- contenido
# (código, nombre, implementado)
IZQ_X, DER_X = 545, 1135          # centro de las elipses de cada columna
RX, RY = 190, 25

PAQUETES = [
    # (título, x, y, ancho, casos con su y). Los paquetes son los del
    # diagrama de paquetes de Análisis (2. Análisis/2_Diagrama de Paquetes.png).
    ("Gestión de Usuarios", 330, 95, 430, [
        ("CU0006", "Registrar Usuario", True, 150),
        ("CU0001", "Iniciar Sesión", True, 210),
        ("CU0010", "Invitación a la aplicación", True, 270),
        ("CU0019", "Modificar Perfil", False, 330),
        ("CU0018", "Buscar Usuarios", False, 390),
    ]),
    ("Gestión de Relaciones", 330, 465, 430, [
        ("CU0005", "Solicitar Amistad", False, 520),
        ("CU0002", "Aceptar / Rechazar solicitud de amistad", False, 580),
        ("CU0016", "Eliminar Amigos", False, 640),
        ("CU0012", "Crear grupos de amigos", False, 700),
        ("CU0015", "Mostrar usuarios con amigos en común", False, 760),
    ]),
    ("Gestión de Contenido", 330, 835, 430, [
        ("CU0013", "Hacer publicaciones en la página", False, 890),
        ("CU0004", "Publicar en el Muro", False, 950),
        ("CU0014", "Comentar Publicación", False, 1010),
        ("CU0011", "Eliminar comentarios", False, 1070),
        ("CU0007", "Gestionar Álbum", False, 1130),
        ("CU0020", "Consultar Página Principal", False, 1190),
    ]),
    ("Administración", 920, 95, 430, [
        ("CU0003", "Gestionar usuarios, comentarios y fotos", False, 150),
        ("CU0008", "Gestionar Comentarios", False, 210),
    ]),
    ("Control de Accesos", 920, 285, 430, [
        ("CU0017", "Gestionar permisos en el sitio", False, 340),
    ]),
    ("Notificaciones", 920, 835, 430, [
        ("CU0023", "Enviar notificación de cumpleaños por email", False, 890),
        ("CU0009", "Notificación de Cumpleaños", False, 950),
        ("CU0021", "Notificar solicitud de amistad recibida", False, 1010),
        ("CU0022", "Notificar comentario en foto propia", False, 1070),
        ("CU0024", "Notificar actualización de perfil de amigo", False, 1130),
    ]),
]


ACTORES = {  # nombre: (x, y de la cabeza)
    "Usuario No Registrado": (130, 120),
    "Usuario Registrado": (130, 290),
    "Usuario Autenticado": (130, 660),
    "Administrador": (1590, 170),
    "Sistema": (1590, 860),
}

ASOCIACIONES = [
    ("Usuario No Registrado", "CU0006"),
    ("Usuario Registrado", "CU0001"),
    *[("Usuario Autenticado", c) for c in (
        "CU0010", "CU0019", "CU0018", "CU0005", "CU0002", "CU0016", "CU0012", "CU0015",
        "CU0013", "CU0004", "CU0014", "CU0011", "CU0007", "CU0020")],
    *[("Administrador", c) for c in ("CU0003", "CU0008", "CU0017")],
    ("Sistema", "CU0023"),
    ("Sistema", "CU0009"),
]

# (origen, destino, estereotipo): flecha punteada del origen al destino
DEPENDENCIAS = [
    ("CU0020", "CU0009", "«include»"),
    ("CU0020", "CU0021", "«include»"),
    ("CU0020", "CU0022", "«include»"),
    ("CU0020", "CU0024", "«include»"),
]

# ------------------------------------------------------------------- dibujo
CASOS = {}
for _, px, _, _, casos in PAQUETES:
    cx = IZQ_X if px < 800 else DER_X
    for cod, nom, impl, y in casos:
        CASOS[cod] = (cx, y, nom, impl)

out = []
add = out.append


def texto(x, y, s, size=13, weight="normal", anchor="middle", color=TINTA, style=""):
    add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
        f'text-anchor="{anchor}" fill="{color}" {style}>{escape(s)}</text>')


def actor(nombre, x, y):
    c = TINTA
    add(f'<circle cx="{x}" cy="{y}" r="13" fill="#fff" stroke="{c}" stroke-width="2"/>')
    add(f'<line x1="{x}" y1="{y+13}" x2="{x}" y2="{y+52}" stroke="{c}" stroke-width="2"/>')
    add(f'<line x1="{x-24}" y1="{y+26}" x2="{x+24}" y2="{y+26}" stroke="{c}" stroke-width="2"/>')
    add(f'<line x1="{x}" y1="{y+52}" x2="{x-20}" y2="{y+82}" stroke="{c}" stroke-width="2"/>')
    add(f'<line x1="{x}" y1="{y+52}" x2="{x+20}" y2="{y+82}" stroke="{c}" stroke-width="2"/>')
    texto(x, y + 102, nombre, size=14, weight="bold")


def borde_elipse(cx, cy, hacia_x, hacia_y):
    """Punto del borde de la elipse en dirección a (hacia_x, hacia_y)."""
    import math
    dx, dy = hacia_x - cx, hacia_y - cy
    if dx == dy == 0:
        return cx, cy
    t = 1 / math.sqrt((dx / RX) ** 2 + (dy / RY) ** 2)
    return cx + dx * t, cy + dy * t


add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="Segoe UI, Helvetica, Arial, sans-serif">')
add('<defs>'
    f'<marker id="abierta" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">'
    f'<path d="M0,0 L10,5 L0,10" fill="none" stroke="{TINTA}" stroke-width="1.5"/></marker>'
    f'<marker id="hueca" viewBox="0 0 12 12" refX="12" refY="6" markerWidth="14" markerHeight="14" orient="auto-start-reverse">'
    f'<path d="M0,0 L12,6 L0,12 Z" fill="#fff" stroke="{TINTA}" stroke-width="1.3"/></marker>'
    '</defs>')
add(f'<rect width="{W}" height="{H}" fill="#fff"/>')

# Límite del sistema
add(f'<rect x="300" y="40" width="1080" height="1240" rx="6" fill="none" stroke="{TINTA}" stroke-width="2"/>')
texto(840, 72, "UMBook", size=20, weight="bold")

# Paquetes
for titulo, px, py, pw, casos in PAQUETES:
    ph = casos[-1][3] - py + 45
    add(f'<rect x="{px}" y="{py+18}" width="{pw}" height="{ph-18}" fill="{PAQ_FONDO}" stroke="#64748b" stroke-width="1.2"/>')
    tw = 14 + 8.2 * len(titulo)
    add(f'<rect x="{px}" y="{py}" width="{tw}" height="20" fill="{PAQ_FONDO}" stroke="#64748b" stroke-width="1.2"/>')
    texto(px + 7, py + 15, titulo, size=12.5, weight="bold", anchor="start", color="#334155")

# Asociaciones (debajo de las elipses)
for act, cod in ASOCIACIONES:
    ax, ay = ACTORES[act]
    cx, cy, _, _ = CASOS[cod]
    # Cada línea llega al extremo de la elipse que mira al actor: así ninguna
    # atraviesa otro caso de uso.
    sx = ax + (30 if cx > ax else -30)
    sy = ay + 30
    ex = cx - RX if cx > ax else cx + RX
    add(f'<line x1="{sx}" y1="{sy}" x2="{ex}" y2="{cy}" stroke="{TINTA}" stroke-width="1.1"/>')

# Generalización: Administrador es un Usuario Autenticado (se rodea el sistema por abajo)
ax, ay = ACTORES["Administrador"]
ux, uy = ACTORES["Usuario Autenticado"]
add(f'<polyline points="{ax},{ay+112} {ax},{ay+135} {W-30},{ay+135} {W-30},{H-120} {ux},{H-120} {ux},{uy+112}" fill="none" '
    f'stroke="{TINTA}" stroke-width="1.3" marker-end="url(#hueca)"/>')

# Dependencias «include» / «extend»
for o, d, est in DEPENDENCIAS:
    ox, oy, _, _ = CASOS[o]
    dx, dy, _, _ = CASOS[d]
    # Del extremo derecho del origen al extremo izquierdo del destino: así
    # las flechas no cruzan otros casos de uso.
    x1, y1 = ox + RX, oy
    x2, y2 = dx - RX, dy
    add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{TINTA}" stroke-width="1.1" '
        f'stroke-dasharray="6 4" marker-end="url(#abierta)"/>')
    mx, my = x1 + (x2 - x1) * 0.55, y1 + (y2 - y1) * 0.55
    add(f'<rect x="{mx-30}" y="{my-10}" width="60" height="15" fill="#fff"/>')
    texto(mx, my + 2, est, size=11, style='font-style="italic"')

# «extend»: Solicitar Amistad extiende Buscar Usuarios (desde el resultado de la búsqueda)
ox, oy, _, _ = CASOS["CU0005"]
dx, dy, _, _ = CASOS["CU0018"]
add(f'<path d="M{ox+RX-20},{oy-RY+6} C{ox+RX+55},{oy-20} {dx+RX+55},{dy+20} {dx+RX},{dy+2}" fill="none" '
    f'stroke="{TINTA}" stroke-width="1.1" stroke-dasharray="6 4" marker-end="url(#abierta)"/>')
texto(ox + RX + 40, (oy + dy) / 2 + 4, "«extend»", size=11, anchor="start", style='font-style="italic"')

# Casos de uso
for cod, (cx, cy, nom, impl) in CASOS.items():
    fondo, borde, ancho = (IMPL_FONDO, IMPL_BORDE, 2.4) if impl else ("#fff", TINTA, 1.4)
    add(f'<ellipse cx="{cx}" cy="{cy}" rx="{RX}" ry="{RY}" fill="{fondo}" stroke="{borde}" stroke-width="{ancho}"/>')
    texto(cx, cy - 3, cod, size=11.5, weight="bold", color=IMPL_BORDE if impl else "#475569")
    texto(cx, cy + 13, nom, size=13)

for nombre, (x, y) in ACTORES.items():
    actor(nombre, x, y)

# Leyenda
ly = H - 78
add(f'<rect x="300" y="{ly}" width="1080" height="58" rx="4" fill="#fff" stroke="#cbd5e1"/>')
add(f'<ellipse cx="350" cy="{ly+29}" rx="34" ry="14" fill="{IMPL_FONDO}" stroke="{IMPL_BORDE}" stroke-width="2.4"/>')
texto(395, ly + 34, "Implementado en esta versión (CU0001, CU0006 y CU0010)", size=13, anchor="start")
add(f'<ellipse cx="860" cy="{ly+29}" rx="34" ry="14" fill="#fff" stroke="{TINTA}" stroke-width="1.4"/>')
texto(905, ly + 34, "No implementado en esta versión", size=13, anchor="start")
add(f'<line x1="1140" y1="{ly+29}" x2="1185" y2="{ly+29}" stroke="{TINTA}" stroke-width="1.3" marker-end="url(#hueca)"/>')
texto(1195, ly + 34, "Generalización", size=13, anchor="start")

add("</svg>")
SALIDA.parent.mkdir(parents=True, exist_ok=True)
SALIDA.write_text("\n".join(out), encoding="utf-8")
print("OK  ", SALIDA.relative_to(RAIZ))
