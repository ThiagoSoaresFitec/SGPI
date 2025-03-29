from flask import Blueprint, request, jsonify
from db import get_db_connection

status_routes = Blueprint("status_routes", __name__)

@status_routes.route("/status/<int:patente_id>", methods=["POST"])
def add_status(patente_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO status_patente (patente_id, etapa, descricao) VALUES (%s, %s, %s)",
                   (patente_id, data["etapa"], data["descricao"]))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Status atualizado com sucesso!"}), 201

@status_routes.route("/status/<int:patente_id>", methods=["GET"])
def get_status(patente_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM status_patente WHERE patente_id = %s ORDER BY data_atualizacao DESC", (patente_id,))
    status = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(status)
