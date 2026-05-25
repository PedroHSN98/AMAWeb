# Acessibilidade Auto

Script que avalia automaticamente a acessibilidade de sites usando amaweb UNIFESP.

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Certifique-se de ter o ChromeDriver instalado:
   - Faça download em: https://chromedriver.chromium.org/
   - Coloque na pasta do projeto ou adicione ao PATH

## Como usar

1. Adicione os URLs dos sites no arquivo `urls.txt` (um por linha):
```
www.example.com
outro-site.mt.gov.br
https://site-com-protocolo.com
```

2. Execute o script:
```bash
python amaweb.py
```

3. O resultado será salvo em `resultado.xlsx` com:
   - URL do site
   - Nota de acessibilidade

## Notas

- O script aceita URLs com ou sem `https://`
- Timeout padrão: 180 segundos por site
- A planilha é salva continuamente durante a execução