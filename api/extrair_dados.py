import os
import csv
import re
from bs4 import BeautifulSoup

# Definir diretórios e arquivos
base_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(base_dir, "dados_patentes_corrigidos.tsv")
html_patentes_dir = os.path.join(base_dir, "html_patentes")

# Verificar se o diretório de HTML existe
if not os.path.exists(html_patentes_dir):
    print(f"❌ Diretório {html_patentes_dir} não encontrado!")
    exit(1)

# Abrir arquivo de saída
with open(output_file, "w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile, delimiter="\t")  
    writer.writerow(["Campo", "Valor"])  # Cabeçalho para debug

    for filename in sorted(os.listdir(html_patentes_dir)):
        filepath = os.path.join(html_patentes_dir, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
        except UnicodeDecodeError:
            with open(filepath, "r", encoding="ISO-8859-1") as file:
                soup = BeautifulSoup(file, "html.parser")

        # Debug: imprimir parte do HTML para inspeção
        print(f"\n🔍 Processando arquivo: {filename}")
        print(f"🔹 Primeiros 500 caracteres do HTML:\n{soup.prettify()[:500]}\n")

        # Procurar todas as tabelas
        tabelas = soup.find_all("table")

        # Debug: Mostrar quantas tabelas foram encontradas
        print(f"📊 {len(tabelas)} tabelas encontradas!")

        if not tabelas:
            print(f"⚠️ Nenhuma tabela encontrada no arquivo {filename}")
            continue

        # Escolher a tabela correta (verificar manualmente o índice certo)
        tabela_dados = tabelas[1] if len(tabelas) > 1 else tabelas[0]

        for row in tabela_dados.find_all("tr"):
            cols = row.find_all(["td", "th"])  
            cols = [re.sub(r"\s+", " ", col.text.strip()) for col in cols if col.text.strip()]
            
            if cols:
                print(f"📌 Linha extraída: {cols}")  # Debug: imprimir linha
                writer.writerow(cols)

print(f"✅ Extração concluída! Os dados foram salvos em '{output_file}'.")
