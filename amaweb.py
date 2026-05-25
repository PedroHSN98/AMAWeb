from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from openpyxl import Workbook

import time
import math
import sys

# ============================================================
# CONFIGURAÇÕES
# ============================================================
jpeodl
ARQUIVO_URLS = "urls.txt"
ARQUIVO_RESULTADO = "resultado.xlsx"

TEMPO_TIMEOUT = 180  # (tempo maximo para aguardar a nota aparecer, em segundos. Se aparecer antes, o processo continua normalmente, vai para o próximo site)

# ============================================================
# LER URLS
# ============================================================

with open(ARQUIVO_URLS, "r", encoding="utf-8") as f:
    urls = [linha.strip() for linha in f if linha.strip()]

total_sites = len(urls)

# ============================================================
# CRIAR PLANILHA
# ============================================================

wb = Workbook()
ws = wb.active
ws.title = "Resultados"

# Cabeçalhos
ws.append(["URL", "Nota"])

# ============================================================
# CONFIGURAR CHROME HEADLESS
# ============================================================

options = Options()

options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--log-level=3")

driver = webdriver.Chrome(options=options)

# ============================================================
# FUNÇÃO BARRA DE PROGRESSO
# ============================================================

def mostrar_progresso(atual, total, media_segundos):
    porcentagem = atual / total

    largura_barra = 30

    preenchido = int(largura_barra * porcentagem)

    barra = "█" * preenchido + " " * (largura_barra - preenchido)

    restantes = total - atual

    tempo_restante = restantes * media_segundos

    minutos_restantes = tempo_restante / 60

    print("\n" + "=" * 60)
    print()

    print(
        f"Analisando: {math.floor(porcentagem * 100)}% "
        f"|{barra}| "
        f"[{atual}/{total}]"
    )

    print()

    print(
        f"Tempo estimado restante: "
        f"{minutos_restantes:.2f} minutos"
    )

    print()

    print(
        f"Média por site: "
        f"{media_segundos:.2f} segundos"
    )

    print()

    print("=" * 60)

# ============================================================
# PROCESSAR SITES
# ============================================================

inicio_total = time.time()

for i, site in enumerate(urls, start=1):

    inicio_site = time.time()

    # Corrige URL
    if not site.startswith("http"):
        url = f"https://amaweb.unifesp.br/avaliador/results/{site}"
    else:
        url = site

    try:
        driver.get(url)

        # Aguarda nota aparecer
        nota = WebDriverWait(driver, TEMPO_TIMEOUT).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".score-circle-value")
            )
        ).text.strip()

        # Limpeza do texto
        nota = nota.replace("Nota:", "").strip()

        # Caso venha vazio
        if not nota:
            nota = "Erro"

    except Exception:
        nota = "Erro"

    # Salva na planilha
    ws.append([site, nota])

    # Salva continuamente
    wb.save(ARQUIVO_RESULTADO)

    # ========================================================
    # ESTATÍSTICAS
    # ========================================================

    tempo_total = time.time() - inicio_total

    media_por_site = tempo_total / i

    # Limpa terminal
    sys.stdout.write("\033[H\033[J")

    # Exibe progresso formatado
    mostrar_progresso(
        atual=i,
        total=total_sites,
        media_segundos=media_por_site
    )

# ============================================================
# FINALIZAR
# ============================================================

driver.quit()

wb.save(ARQUIVO_RESULTADO)

print()
print("Análise finalizada.")
print(f"Planilha salva em: {ARQUIVO_RESULTADO}")