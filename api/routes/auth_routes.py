import jwt
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
import psycopg2
from config.db_config import db_config

auth_bp = Blueprint('auth', __name__)

# Chave secreta para a assinatura do JWT
SECRET_KEY = "asdflkjqwoiuytrewq"  

def conectar():
    return psycopg2.connect(
        host=db_config["host"],
        database=db_config["database"],
        user=db_config["user"],
        password=db_config["password"],
        port=db_config["port"]
    )

# Função para criar token JWT
def criar_token(usuario_id):
    payload = {
        "id": usuario_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expiração em 1 hora
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Rota de login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"error": "Usuário e senha são obrigatórios!"}), 400

    try:
        connection = conectar()
        cursor = connection.cursor()

        # Verifique as credenciais do usuário no banco de dados
        cursor.execute("SELECT id, email, senha, perfil FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user and check_password_hash(user[2], senha):  # Verifique a senha com o hash
            # Gerar o token JWT
            payload = {
                "id": user[0],
                "email": user[1],
                "role": user[3],  # Inclui o perfil (role) no payload
                "exp": datetime.utcnow() + timedelta(hours=1)  # Token expira em 1 hora
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            return jsonify({
                "token": token,
                "role": user[3]  # Retorna a role ou perfil na resposta
            }), 200
        else:
            return jsonify({"error": "Credenciais inválidas!"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Decorador para proteger rotas com autenticação
# auth_routes.py

def token_required(f):
    def decorator(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"error": "Token de autenticação não fornecido!"}), 401

        try:
            # Verifica o token
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user_id = data["id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido!"}), 401

        return f(current_user_id, *args, **kwargs)

    # Adiciona um nome único para evitar sobrecarga de endpoint
    decorator.__name__ = f"{f.__name__}_protected"
    return decorator

