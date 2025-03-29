from flask import Blueprint, request, jsonify
from subprocess import run, CalledProcessError
import os
import csv
import sys
from datetime import datetime
import psycopg2
from config.db_config import db_config 

TSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dados_patentes_corrigidos.tsv")

# Função para conectar ao PostgreSQL
def conectar():
    return psycopg2.connect(**db_config)

# Função para executar o scraper
def executar_scraper(termo):
    try:
        print(f"🔍 Buscando patentes para: {termo}")
        python_executable = sys.executable
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "buscar_patentes.py"))
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"❌ ERRO: O arquivo {script_path} não foi encontrado!")
        run([python_executable, script_path, termo], check=True)
        print("✅ Scraper concluído!")
    except CalledProcessError as e:
        print(f"❌ Erro ao executar scraper: {e}")

def converter_data(data_str):
    """ Converte data do formato 'DD/MM/YYYY' para 'YYYY-MM-DD' """
    try:
        return datetime.strptime(data_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return None

def ler_arquivo_tsv():
    print(f"📌 Verificando existência do arquivo: {TSV_FILE}")

    if not os.path.exists(TSV_FILE):
        print(f"❌ Arquivo {TSV_FILE} NÃO encontrado!")
        return []
    
    patentes = []
    with open(TSV_FILE, "r", encoding="utf-8-sig") as file:
        reader = csv.reader(file, delimiter="\t")
        dados_patente = {}

        for row in reader:
            if len(row) < 2:
                continue

            chave, valor = row[0].strip(), row[1].strip()

            if "(21) Nº do Pedido:" in chave:
                if dados_patente:
                    patentes.append(dados_patente)
                dados_patente = {"numero": valor}

            elif "(22) Data do Depósito:" in chave:
                dados_patente["data_deposito"] = converter_data(valor)

            elif "(43) Data da Publicação:" in chave:
                dados_patente["data_publicacao"] = converter_data(valor)

            elif "(47) Data da Concessão:" in chave:
                dados_patente["data_concessao"] = converter_data(valor)

            elif "(51) Classificação IPC:" in chave:
                dados_patente["classificacao_ipc"] = valor[:255]  # Limita a 255 caracteres

            elif "(52) Classificação CPC:" in chave:
                dados_patente["classificacao_cpc"] = valor[:255]  # Limita a 255 caracteres

            elif "(54) Título:" in chave:
                dados_patente["titulo"] = valor

            elif "(57) Resumo:" in chave:
                dados_patente["resumo"] = valor

            elif "(71) Nome do Depositante:" in chave:
                dados_patente["depositante"] = valor

            elif "(72) Nome do Inventor:" in chave:
                dados_patente["inventor"] = valor

        if dados_patente:
            patentes.append(dados_patente)

    print(f"✅ Total de patentes carregadas: {len(patentes)}")
    return patentes

# Criando o blueprint para as rotas
patentes_bp = Blueprint('patentes', __name__)

@patentes_bp.route("/buscar", methods=["POST"])
def buscar_patentes():
    data = request.get_json()
    if not data or "termo" not in data:
        return jsonify({"error": "Nenhum termo de busca fornecido!"}), 400

    termo = data["termo"]
    executar_scraper(termo)  # Executa a busca
    patentes = ler_arquivo_tsv()  # Obtém os dados extraídos

    return jsonify(patentes)

# 📌 Rota para salvar as patentes no banco de dados
@patentes_bp.route("/salvar", methods=["POST"])
def salvar_patentes():
    data = request.get_json()
    palavra_chave = data.get("palavra_chave")

    if not palavra_chave:
        return jsonify({"error": "Palavra-chave não fornecida!"}), 400

    patentes = ler_arquivo_tsv()
    if not patentes:
        return jsonify({"error": "Nenhum dado para salvar!"}), 400

    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        # 1️⃣ Inserir a busca
        cursor.execute("INSERT INTO buscas (palavra_chave) VALUES (%s)", (palavra_chave,))
        id_busca = cursor.lastrowid  # Pega o ID gerado

        # 2️⃣ Inserir patentes vinculadas
        sql = """
            INSERT IGNORE INTO patentes
            (numero, data_deposito, data_publicacao, data_concessao, classificacao_ipc, classificacao_cpc,
             titulo, resumo, depositante, inventor, id_busca)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        for p in patentes:
            cursor.execute(sql, (
                p["numero"], p["data_deposito"], p["data_publicacao"], p["data_concessao"],
                p["classificacao_ipc"], p["classificacao_cpc"], p["titulo"], p["resumo"],
                p["depositante"], p["inventor"], id_busca
            ))

        connection.commit()
        cursor.close()
        connection.close()

        os.remove(TSV_FILE)

        return jsonify({"message": "✅ Dados salvos com sucesso!", "id_busca": id_busca})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
