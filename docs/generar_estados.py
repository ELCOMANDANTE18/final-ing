#!/usr/bin/env python3
"""Genera la lámina de diagramas de estados de Diseño con la forma del
`Diagrama_de_Estado.pdf` del grupo (estados de PlantUML: caja redondeada gris
con el nombre arriba, estado inicial negro y final con doble círculo).

Salida (SVG y PNG): "3. Diseño/5_Diagramas de Estado/Diagramas de Estado.svg" y ".png"

Dos diagramas, los dos de cosas que existen en el código actual:
  - Invitación (CU0010): el campo `status` de la tabla `invitations`.
  - Sesión del usuario en el frontend (CU0001): el token en `localStorage`,
    `AuthGuard` y `TokenInterceptor`.
La explicación de cada transición está en
"3. Diseño/5_Diagramas de Estado/estados.md". **Los nombres de este script y
los del texto tienen que coincidir.**

Uso: python3 docs/generar_estados.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generar_despliegue_subsistemas import (  # noqa: E402
    F_ETIQUETA, RELLENO, TINTA, Lienzo, a_png,
)

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "3. Diseño" / "5_Diagramas de Estado" / "Diagramas de Estado.svg"

W_EST, H_EST = 140, 50   # tamaño de un estado


def estado(L, cx, y, nombre):
    """Estado: caja redondeada con el nombre y una línea debajo (estilo PlantUML)."""
    x = cx - W_EST / 2
    L.out.append(
        f'<rect x="{x}" y="{y}" width="{W_EST}" height="{H_EST}" rx="12.5" fill="{RELLENO}" '
        f'stroke="{TINTA}" stroke-width="0.6"/>'
        f'<line x1="{x}" y1="{y + 26}" x2="{x + W_EST}" y2="{y + 26}" stroke="{TINTA}" stroke-width="0.6"/>')
    L.texto(cx, y + 18, nombre, 14)


def inicial(L, cx, cy):
    L.out.append(f'<circle cx="{cx}" cy="{cy}" r="10" fill="#222"/>')


def final(L, cx, cy):
    L.out.append(f'<circle cx="{cx}" cy="{cy}" r="11" fill="none" stroke="#222" stroke-width="1.2"/>'
                 f'<circle cx="{cx}" cy="{cy}" r="6" fill="#222"/>')


def titulo(L, cx, y, s):
    L.texto(cx, y, s, 18)


def invitacion(L, ox):
    cx = ox + 290
    titulo(L, cx, 75, "Invitación")
    inicial(L, cx, 110)
    estado(L, cx, 175, "Pendiente")
    L.flecha([(cx, 120), (cx, 175)], ["create(email, inviter_id)", "[email válido, sesión iniciada]"],
             (cx + 10, 140))

    ie, ifa = ox + 120, ox + 460            # centros de Enviada y Fallida
    estado(L, ie, 345, "Enviada")
    estado(L, ifa, 345, "Fallida")
    L.flecha([(cx - 40, 225), (ie + 20, 345)], ["correo aceptado por el servidor",
                                                 "/ update_status('enviada')"], (cx - 92, 262), ancla="end")
    L.flecha([(cx + 40, 225), (ifa - 20, 345)], ["el servidor rechaza o no responde",
                                                 "/ update_status('fallida')"], (cx + 92, 262))

    for c in (ie, ifa):
        L.flecha([(c, 395), (c, 449)])
        final(L, c, 460)

    L.nota(ox + 40, 500, 500, [
        "Enviada y Fallida son finales: no hay transición entre ellas ni vuelta",
        "a Pendiente. Reintentar crea una invitación nueva (la fallida queda",
        "como registro). Un rebote posterior del correo no cambia el estado.",
    ])


def sesion(L, ox):
    cx = ox + 330                         # centro de la columna izquierda
    titulo(L, cx + 90, 75, "Sesión del usuario (frontend)")
    inicial(L, cx, 110)
    estado(L, cx, 175, "Sin sesión")
    L.flecha([(cx, 120), (cx, 175)], ["abre la aplicación", "[sin access_token]"], (cx + 10, 140))

    # Bucle sobre Sin sesión: AuthGuard
    xl = cx - W_EST / 2
    L.flecha([(xl, 190), (xl - 40, 190), (xl - 40, 212), (xl, 212)],
             ["pide /welcome o /invite", "/ AuthGuard redirige a /login"], (xl - 48, 195), ancla="end")

    estado(L, cx, 375, "Sesión iniciada")
    L.flecha([(cx - 35, 225), (cx - 35, 375)], ["login() responde 200", "/ guarda access_token",
                                                 "y nombre en localStorage"], (cx - 43, 285), ancla="end")
    L.flecha([(cx + 15, 375), (cx + 15, 225)], ["logout()", "(Cerrar sesión)"], (cx + 23, 330))

    tx = cx + 290                         # centro de Token vencido
    estado(L, tx, 375, "Token vencido")
    L.flecha([(cx + W_EST / 2, 400), (tx - W_EST / 2, 400)], ["pasan 15 minutos"], (cx + 145, 392),
             ancla="middle")
    L.flecha([(tx, 375), (tx, 200), (cx + W_EST / 2, 200)],
             ["una petición responde 401", "/ TokenInterceptor: logout()", "y navega a /login"],
             (tx - 8, 260), ancla="end")

    L.nota(ox + 180, 500, 470, [
        "AuthGuard solo mira si hay un token guardado (isAuthenticated()),",
        "no si venció: con el token vencido deja abrir las pantallas hasta",
        "la primera petición al backend, que responde 401.",
    ])


def main():
    L = Lienzo(1300, 600)
    L.texto(20, 32, "Diagramas de Estado", 19, negrita=True, ancla="start")
    invitacion(L, 0)
    sesion(L, 600)
    DESTINO.write_text(L.svg(), encoding="utf-8")
    print(f"OK   {DESTINO.relative_to(RAIZ)}")
    a_png(DESTINO)


if __name__ == "__main__":
    main()
