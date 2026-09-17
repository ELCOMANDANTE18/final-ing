import os

from app import create_app
from app.extensions import db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        os.makedirs(os.path.join(app.instance_path), exist_ok=True)
        db.create_all()
    app.run(debug=True, port=5000)
