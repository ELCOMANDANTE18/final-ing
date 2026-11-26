import os

from app import create_app, db

app = create_app()

# Crea las tablas si no existen (create_all no toca las que ya están).
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Seguridad: antes corría con debug=True en host='0.0.0.0'. El depurador de
    # Werkzeug permite ejecutar código desde el navegador, y en 0.0.0.0 queda
    # expuesto a cualquiera de la red. Ahora escucha solo en esta máquina y el
    # modo debug se activa a propósito con FLASK_DEBUG=1.
    debug = os.getenv('FLASK_DEBUG', '0') == '1'
    app.run(host='127.0.0.1', port=5000, debug=debug)
