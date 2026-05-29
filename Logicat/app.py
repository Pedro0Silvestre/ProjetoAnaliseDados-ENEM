from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
import ast
import re  
import json



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def boas_vindas(request: Request):
    return templates.TemplateResponse(request, "boas_vindas.html")

@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "home.html")

@app.get("/graficos", response_class=HTMLResponse)
async def ver_graficos(request: Request):
    conexao = sqlite3.connect("Logicat.db")
    cursor = conexao.cursor()
    
    # Substituído 'ano' por 'year' e 'assunto' por 'tema' conforme as colunas reais da sua tabela
    cursor.execute("SELECT year, COUNT(*) FROM question WHERE year IS NOT NULL GROUP BY year ORDER BY year ASC")
    dados_anos = cursor.fetchall()
    
    cursor.execute("SELECT tema, COUNT(*) FROM question WHERE tema IS NOT NULL GROUP BY tema")
    dados_eixos = cursor.fetchall()
    
    cursor.execute("SELECT dificuldade, COUNT(*) FROM question WHERE dificuldade IS NOT NULL GROUP BY dificuldade")
    dados_dificuldade = cursor.fetchall()
    
    conexao.close()
    
    anos_labels = [str(row[0]) for row in dados_anos]
    anos_valores = [row[1] for row in dados_anos]
    
    labels_eixos = [row[0] for row in dados_eixos]
    valores_eixos = [row[1] for row in dados_eixos]
    
    labels_dificuldade = [row[0] for row in dados_dificuldade]
    valores_dificuldade = [row[1] for row in dados_dificuldade]
    
    return templates.TemplateResponse(
        request, 
        "graficos.html", 
        {
            "anos": anos_labels,
            "anos_valores": anos_valores,
            "labels_eixos": labels_eixos, 
            "valores_eixos": valores_eixos,
            "labels_dificuldade": labels_dificuldade, 
            "valores_dificuldade": valores_dificuldade
        }
    )

# 4. ROTA DE ANÁLISES (Listagem de questões por ano corrigida)
@app.get("/analises", response_class=HTMLResponse)
async def ver_analises(request: Request, ano: str = None):
    conexao = sqlite3.connect("Logicat.db")
    cursor = conexao.cursor()
    
    # Busca os anos para montar os botões superiores
    cursor.execute("SELECT DISTINCT year FROM question WHERE year IS NOT NULL ORDER BY year DESC")
    todos_anos = [str(row[0]) for row in cursor.fetchall()]
    
    questoes = []
    if ano:
        try:
            # Forçamos a conversão para inteiro para bater com a tipagem do banco
            ano_inteiro = int(ano)
            
            # Buscamos index, title e tema usando o valor tipado corretamente
            cursor.execute("SELECT [index], title, tema FROM question WHERE year = ?", (ano_inteiro,))
            dados = cursor.fetchall()
            
            questoes = [{"id": row[0], "title": row[1], "tema": row[2]} for row in dados]
        except ValueError:
            # Caso venha algo inválido na URL, evita que o servidor quebre
            questoes = []
        
    conexao.close()
    
    return templates.TemplateResponse(
        request, 
        "analises.html", 
        {
            "todos_anos": todos_anos,
            "questoes": questoes,
            "ano_selecionado": ano
        }
    )

# 5. ROTA DA QUESTÃO INDIVIDUAL (Versão Corrigida com Regex para não cortar o Enunciado)
@app.get("/questao/{ano}/{questao_id}", response_class=HTMLResponse)
async def ver_questao_individual(request: Request, ano: int, questao_id: int):
    conexao = sqlite3.connect("Logicat.db")
    cursor = conexao.cursor()
    
    cursor.execute(
        "SELECT title, year, context, alternatives, correctAlternative FROM question WHERE [index] = ? AND year = ?", 
        (questao_id, ano)
    )
    resultado = cursor.fetchone()
    conexao.close()
    
    if not resultado:
        return HTMLResponse(content=f"Questão não encontrada.", status_code=404)
        
    contexto_bruto = resultado[2] if resultado[2] else ""
    imagem_url = None
    
    # Captura o padrão Markdown de imagem: ![qualquer_coisa](url_da_imagem)
    padrao_imagem = r"!\[.*?\]\((.*?)\)"
    
    if contexto_bruto:
        match = re.search(padrao_imagem, contexto_bruto)
        if match:
            imagem_url = match.group(1)  # Extrai apenas a URL que está dentro dos parênteses
            contexto_bruto = re.sub(padrao_imagem, "", contexto_bruto)  # Remove APENAS a tag da imagem, mantendo todo o resto do texto intacto

    raw_alternativas = resultado[3]
    lista_alternativas = []
    
    if raw_alternativas:
        try:
            lista_alternativas = ast.literal_eval(raw_alternativas)
        except Exception:
            if isinstance(raw_alternativas, str) and "\n" in raw_alternativas:
                lista_alternativas = [alt.strip() for alt in raw_alternativas.split("\n") if alt.strip()]
            else:
                lista_alternativas = [{"letter": "X", "text": raw_alternativas, "isCorrect": False}]
                
    questao_dados = {
        "title": resultado[0],
        "year": resultado[1],
        "context": contexto_bruto,
        "imagem": imagem_url,
        "alternatives": lista_alternativas,
        "correct": resultado[4]
    }
    
    return templates.TemplateResponse(request, "exibir_questao.html", {"questao": questao_dados})