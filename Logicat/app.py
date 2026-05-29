from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI()

# Configura o FastAPI para servir arquivos estáticos (CSS, imagens)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configura a pasta de templates HTML
templates = Jinja2Templates(directory="templates")

# 1. ROTA DE BOAS-VINDAS (Tela Inicial)
@app.get("/", response_class=HTMLResponse)
async def boas_vindas(request: Request):
    return templates.TemplateResponse(request, "boas_vindas.html")

# 2. ROTA DA HOME (Dashboard)
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "home.html")