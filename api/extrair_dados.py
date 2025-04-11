import os
import csv
import re
from bs4 import BeautifulSoup

base_dir = os.path.dirname(os.path.abspath(__file__))

output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados_patentes_corrigidos.tsv")

html_patentes_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html_patentes")

with open(output_file, "w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile, delimiter="\t")  

    for index, filename in enumerate(sorted(os.listdir(html_patentes_dir))):
        filepath = os.path.join(html_patentes_dir, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
        except UnicodeDecodeError:
            with open(filepath, "r", encoding="ISO-8859-1") as file:
                soup = BeautifulSoup(file, "html.parser")

        tabelas = soup.find_all("table", {"width": "780px"})
        if len(tabelas) < 2:
            print(f"⚠️ Aviso: Nenhuma tabela válida encontrada em {filename}")
            continue

        tabela_dados = tabelas[1]  
        for row in tabela_dados.find_all("tr"):
            cols = row.find_all(["td", "th"])  
            cols = [re.sub(r"\s+", " ", col.text.strip()) for col in cols if col.text.strip()]
            if cols:  
                writer.writerow(cols)

        print(f"📄 Dados extraídos de {filename} e salvos no arquivo.")

print(f"✅ Extração concluída! Os dados foram salvos em '{output_file}'.")