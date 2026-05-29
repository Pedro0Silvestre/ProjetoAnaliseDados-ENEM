import sqlite3
import pandas as pd
import requests
from io import StringIO

# 1. Defina a URL 'raw' do seu CSV no GitHub
url_github = "https://raw.githubusercontent.com/Pedro0Silvestre/ProjetoAnaliseDados-ENEM/refs/heads/main/questoes_analisada_2023_2012.csv"

print("Baixando os dados do GitHub...")
# 2. Faz o download do conteúdo do arquivo
response = requests.get(url_github)


if response.status_code == 200:
    # Transforma o texto baixado em um fluxo de dados que o Pandas consegue ler
    dados_csv = StringIO(response.text)
    
    # Carrega os dados em um DataFrame do Pandas
    df = pd.read_csv(dados_csv)
    
    print("Dados baixados com sucesso! Conectando ao SQLite...")
    
    # 3. Conecta ao banco SQLite (se o arquivo não existir, ele será criado na hora)
    conexao = sqlite3.connect("Logicat.db")
    
    # 4. Envia o DataFrame direto para o banco de dados
    # 'nome_da_tabela' é o nome que você quer dar para a tabela no banco
    # if_exists='replace' recria a tabela se ela já existir (bom para testes)
    # index=False evita que o índice do Pandas vire uma coluna no banco
    df.to_sql("question", conexao, if_exists="replace", index=False)
    
    # Fecha a conexão por boa prática
    conexao.close()
    
    print("Banco de dados SQLite criado e populado com sucesso!")
else:
    print(f"Erro ao baixar o arquivo. Status code: {response.status_code}")