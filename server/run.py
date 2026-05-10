from flask import Flask
from flask_cors import CORS

from server.routes.auth import auth_bp
from server.routes.history import history_bp

app = Flask(__name__)
CORS(app)

def create_app():
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(history_bp, url_prefix="/history")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
