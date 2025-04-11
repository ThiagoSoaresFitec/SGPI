import jwt
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
import psycopg2
from config.db_config import db_config

auth_bp = Blueprint('auth', __name__)
SECRET_KEY = "asdflkjqwoiuytrewq"  # Chave secreta para assinar o token

def conectar():
    return psycopg2.connect(
        host=db_config["host"],
        database=db_config["database"],
        user=db_config["user"],
        password=db_config["password"],
        port=db_config["port"]
    )

# --------------------------
# ✅ Função para gerar token JWT
# --------------------------
def criar_token(usuario_id, email, perfil):
    payload = {
        "id": usuario_id,
        "email": email,
        "role": perfil,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# --------------------------
# ✅ Rota de login
# --------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"error": "Email e senha são obrigatórios!"}), 400

    try:
        connection = conectar()
        cursor = connection.cursor()

        cursor.execute("SELECT id, email, senha, perfil, nome FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if not user:
            return jsonify({"error": "Usuário não encontrado!"}), 404

        if not check_password_hash(user[2], senha):
            return jsonify({"error": "Senha incorreta!"}), 401

        token = criar_token(user[0], user[1], user[3])

        return jsonify({
            "token": token,
            "username": user[4],
            "id": user[0],
            "email": user[1],
            "role": user[3].capitalize()
        }), 200

    except Exception as e:
        return jsonify({"error": f"Erro no login: {e}"}), 500

# --------------------------
# ✅ Decorador para proteger rotas com token JWT
# --------------------------
def token_required(f):
    def decorator(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            parts = request.headers["Authorization"].split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]

        if not token:
            return jsonify({"error": "Token de autenticação não fornecido!"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user_id = data["id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido!"}), 401

        return f(current_user_id, *args, **kwargs)

    decorator.__name__ = f"{f.__name__}_protected"
    return decorator
