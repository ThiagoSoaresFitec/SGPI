from flask import Flask
from flask_cors import CORS
from routes.patentes_routes import patentes_bp
from routes.user_routes import usuario_bp, inicializar
from routes.auth_routes import auth_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Registrando o blueprint com as rotas de patentes
app.register_blueprint(patentes_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(auth_bp)

inicializar()
if __name__ == "__main__":
    app.run(debug=True, port=5000)
