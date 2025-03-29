from flask import Blueprint, request, jsonify
import psycopg2
from werkzeug.security import generate_password_hash
from config.db_config import db_config
from .auth_routes import token_required  # Importando o decorador

usuario_bp = Blueprint('usuarios', __name__)

def conectar():
    return psycopg2.connect(
        host=db_config["host"],
        database=db_config["database"],
        user=db_config["user"],
        password=db_config["password"],
        port=db_config["port"]
    )

# Função para criar a tabela 'usuarios' se não existir
def criar_tabela_usuarios():
    try:
        connection = conectar()
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            perfil VARCHAR(50) CHECK (perfil IN ('administrador', 'pesquisador', 'engenheiro')) NOT NULL,
            senha VARCHAR(255) NOT NULL
        );
        """)

        connection.commit()
        cursor.close()
        connection.close()
        print("✅ Tabela de usuários criada com sucesso!")
    
    except Exception as e:
        print(f"❌ Erro ao criar tabela de usuários: {e}")

# Chama a função para criar a tabela de usuários na inicialização da aplicação
criar_tabela_usuarios()

# Rota para adicionar um novo usuário
@usuario_bp.route("/user", methods=["POST"])
@token_required  # Protege essa rota, só pode ser acessada com o token
def adicionar_usuario(current_user_id):
    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")
    perfil = data.get("perfil")
    senha = data.get("senha")

    if not nome or not email or not perfil or not senha:
        return jsonify({"error": "Todos os campos são obrigatórios!"}), 400

    if perfil not in ["administrador", "pesquisador", "engenheiro"]:
        return jsonify({"error": "Perfil inválido!"}), 400

    senha_hash = generate_password_hash(senha)

    try:
        connection = conectar()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO usuarios (nome, email, perfil, senha)
            VALUES (%s, %s, %s, %s)
        """, (nome, email, perfil, senha_hash))

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Usuário adicionado com sucesso!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Rota para listar todos os usuários
@usuario_bp.route("/user", methods=["GET"])
@token_required  # Protege essa rota, só pode ser acessada com o token
def listar_usuarios(current_user_id):
    try:
        connection = conectar()
        cursor = connection.cursor()

        cursor.execute("SELECT id, nome, email, perfil FROM usuarios")
        usuarios = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify([{"id": u[0], "nome": u[1], "email": u[2], "perfil": u[3]} for u in usuarios]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Rota para buscar um usuário específico
@usuario_bp.route("/user/<int:id>", methods=["GET"])
@token_required  # Protege essa rota, só pode ser acessada com o token
def buscar_usuario(current_user_id, id):
    try:
        connection = conectar()
        cursor = connection.cursor()

        cursor.execute("SELECT id, nome, email, perfil FROM usuarios WHERE id = %s", (id,))
        usuario = cursor.fetchone()

        cursor.close()
        connection.close()

        if usuario:
            return jsonify({"id": usuario[0], "nome": usuario[1], "email": usuario[2], "perfil": usuario[3]}), 200
        else:
            return jsonify({"error": "Usuário não encontrado!"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Rota para atualizar um usuário
@usuario_bp.route("/user/<int:id>", methods=["PUT"])
@token_required  # Protege essa rota, só pode ser acessada com o token
def atualizar_usuario(current_user_id, id):
    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")
    perfil = data.get("perfil")
    senha = data.get("senha")

    if not nome or not email or not perfil:
        return jsonify({"error": "Todos os campos são obrigatórios!"}), 400

    if perfil not in ["administrador", "pesquisador", "engenheiro"]:
        return jsonify({"error": "Perfil inválido!"}), 400

    senha_hash = generate_password_hash(senha) if senha else None

    try:
        connection = conectar()
        cursor = connection.cursor()

        if senha_hash:
            cursor.execute("""
                UPDATE usuarios
                SET nome = %s, email = %s, perfil = %s, senha = %s
                WHERE id = %s
            """, (nome, email, perfil, senha_hash, id))
        else:
            cursor.execute("""
                UPDATE usuarios
                SET nome = %s, email = %s, perfil = %s
                WHERE id = %s
            """, (nome, email, perfil, id))

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Usuário atualizado com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Rota para deletar um usuário
@usuario_bp.route("/user/<int:id>", methods=["DELETE"])
@token_required  # Protege essa rota, só pode ser acessada com o token
def deletar_usuario(current_user_id, id):
    try:
        connection = conectar()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Usuário deletado com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
