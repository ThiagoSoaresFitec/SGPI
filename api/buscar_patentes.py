import os
import sys
import shutil
import time
import csv
import subprocess
import shutil  
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


if len(sys.argv) > 1:
    termo_pesquisa = sys.argv[1]
else:
    print("❌ Nenhum termo de pesquisa recebido!")
    sys.exit(1)  

print(f"🔍 Pesquisando por: {termo_pesquisa}")

options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.headless = False  

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 30)

base_dir = os.path.dirname(os.path.abspath(__file__))
html_patentes_dir = "html_patentes"

html_patentes_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html_patentes")

if os.path.exists(html_patentes_dir):
    for filename in os.listdir(html_patentes_dir):
        file_path = os.path.join(html_patentes_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path) 
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  
        except Exception as e:
            print(f"❌ Erro ao excluir {file_path}: {e}")
else:
    os.makedirs(html_patentes_dir)

print(f"📂 Diretório '{html_patentes_dir}' pronto para uso!")

# 🔍 1️⃣ Acessar a página inicial
driver.get("https://busca.inpi.gov.br/pePI/")
print("✅ Página inicial acessada!")

# 🔑 2️⃣ Acessar a página de login
driver.get("https://busca.inpi.gov.br/pePI/servlet/LoginController?action=login")
print("🔑 Página de login acessada!")

# 🔍 3️⃣ Acessar a página de pesquisa
driver.get("https://busca.inpi.gov.br/pePI/jsp/patentes/PatenteSearchBasico.jsp")
print("🔍 Página de pesquisa acessada!")

try:
    campo_pesquisa = wait.until(EC.presence_of_element_located((By.NAME, "ExpressaoPesquisa")))
    campo_pesquisa.send_keys(termo_pesquisa)  
    print(f"✍️ Campo de pesquisa preenchido com: {termo_pesquisa}")

    select = wait.until(EC.presence_of_element_located((By.NAME, "FormaPesquisa")))
    select.send_keys("todas as palavras")
    print("📌 Tipo de busca selecionado!")

    botao_pesquisa = wait.until(EC.element_to_be_clickable((By.NAME, "botao")))
    botao_pesquisa.click()
    print("▶️ Botão de pesquisa clicado!")

    time.sleep(5)

    patentes = []
    for tr in driver.find_elements(By.XPATH, "//tr[@bgcolor='#E0E0E0' or @bgcolor='white']"):
        cols = tr.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 3:
            numero_patente = cols[0].text.strip()
            titulo = cols[2].text.strip()

            link_element = cols[0].find_element(By.TAG_NAME, "a")
            link = link_element.get_attribute("href") if link_element else None

            if link:
                patentes.append({"numero_patente": numero_patente, "titulo": titulo, "link": link})

    print(f"📄 {len(patentes)} patentes encontradas!")

    for index, patente in enumerate(patentes, start=1):
        driver.get(patente["link"])
        time.sleep(10)  

        print(f"🔎 Extraindo detalhes de {patente['numero_patente']}")

        html_pagina = driver.page_source
        filename = os.path.join(html_patentes_dir, f"{patente['numero_patente']}.html")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(html_pagina)

        print(f"✅ Página salva: {filename}")

except Exception as e:
    print(f"❌ Erro: {e}")

finally:
    driver.quit()

print("⏳ Executando extração de dados...")
script_dir = os.path.dirname(os.path.abspath(__file__)) 
extrair_dados_path = os.path.join(script_dir, "extrair_dados.py")  
subprocess.run([sys.executable, extrair_dados_path])