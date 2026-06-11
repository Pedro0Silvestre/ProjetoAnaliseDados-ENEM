# ENEM Logicat

Este projeto é um MVP (Mínimo Produto Viável) projetado para extrair, tratar, categorizar e distribuir questões de Matemática do ENEM. Utilizando técnicas de Engenharia de Dados com **Pandas** e **Inteligência Artificial**, o sistema transforma dados brutos de uma API pública numa base estruturada, categorizada por nível de dificuldade e dividida em grandes temas e subassuntos específicos, servindo como uma plataforma completa de preparação e análise de desempenho para o estudante.

---

## 🛠️ Arquitetura do Projeto

O ecossistema do projeto foi desenhado seguindo a separação de responsabilidades (Frontend, Backend, Data Pipeline e Banco de Dados):

* **Frontend:** Interface limpa, interativa e responsiva construída com **HTML5, CSS3 e JavaScript (Vanilla)**. Permite a filtragem dinâmica de questões e renderização de gráficos analíticos em tempo real.
* **Backend:** Uma API moderna construída com **FastAPI** (Python) responsável por expor os endpoints de consumo das questões e o fornecimento de métricas consolidadas de forma rápida e assíncrona.
* **Banco de Dados:** **SQLite**, garantindo uma solução leve, relacional e de alta velocidade para leitura de dados operacionais e persistência de histórico de submissões.

---

## ⚙️ Novas Funcionalidades Core

O sistema expandiu o seu escopo inicial de visualização para se tornar uma ferramenta ativa de estudo, contendo duas grandes frentes:

### 1. Resolução de Questões em Tempo Real
* **Fluxo do Estudante:** O utilizador pode selecionar questões por assunto ou dificuldade e respondê-las diretamente pela interface.
* **Feedback Instantâneo:** Validação imediata do gabarito (Certo/Errado) por meio do JavaScript consumindo a API do backend.
* **Persistência de Desempenho:** Cada resposta enviada é gravada no banco de dados SQLite (armazenando o ID do utilizador, ID da questão, se acertou/errou e o timestamp), gerando a massa de dados necessária para alimentar o painel analítico.

### 2. Dashboard de Análise Histórica & Evolutiva
Uma camada analítica OLAP integrada que consolida os dados das provas e o histórico do utilizador ao longo dos anos para gerar inteligência de estudo:
* **Análise por Prova:** Visão detalhada do desempenho do estudante em edições específicas do ENEM (ex: ENEM 2024 vs ENEM 2025).
* **Visão Geral de Dificuldade:** Gráficos que mapeiam a distribuição de acertos e erros divididos por Fácil, Médio e Difícil, permitindo identificar onde o estudante está a perder mais pontos.
* **Mapeamento de Subassuntos (Evolutivo):** Gráficos de linha e barras que demonstram o desempenho e a frequência dos subassuntos ao longo das edições históricas do exame, sinalizando os temas mais recorrentes e as principais fraquezas do aluno.

---

## 📊 Pipeline de Dados (ETL)

O coração do projeto está na ingestão, enriquecimento e monitorização dos dados, divididos nas seguintes etapas:

1.  **Extração (Extract):** Os dados brutos foram consumidos diretamente da API pública do ENEM.
2.  **Tratamento (Transform com Pandas):** Utilizando a biblioteca **Pandas**, os dados textuais e metadados das questões foram limpos, padronizados e salvos inicialmente em formato **CSV**.
3.  **Enriquecimento com IA:** Uma Inteligência Artificial analisou o comando e o padrão de resolução de cada questão para inferir e injetar automaticamente três novas colunas na base de dados: `dificuldade`, `tema` e `subassunto`.
4.  **Carga (Load):** O arquivo final tratado foi migrado do DataFrame Pandas para tabelas estruturadas no banco de dados operacional **SQLite** (tabelas de questões, utilizadores e logs de respostas).

---

## 🧠 Matriz de Classificação de Dificuldade (Regras de Negócio)

A IA foi calibrada para classificar cada questão em **estritamente uma** das três categorias abaixo:

* **Fácil:** Questões que exigem apenas leitura direta de gráficos/tabelas, operações matemáticas básicas (soma, subtração, multiplicação, divisão) ou aplicação direta de fórmulas muito simples (como média aritmética simples).
* **Média:** Questões que exigem interpretação em mais de uma etapa, conversão de unidades de medida (ex: $m^3$ para litros), resolução de equações do 1º ou 2º grau, ou conceitos de geometria espacial/plana básica.
* **Difícil:** Questões complexas que envolvem análise combinatória avançada, probabilidade condicional, funções logarítmicas ou exponenciais, ou que exijam múltiplos passos de modelagem algébrica abstrata onde o aluno tradicionalmente enfrenta maior taxa de erro.

---

## 📑 Taxonomia de Conteúdos (Temas e Subassuntos)

A base de dados foi mapeada e segmentada exatamente na seguinte árvore de conteúdos da matriz do ENEM:

### 1. Matemática Básica
* **Subassuntos:** Razão e Proporção | Regra de Três | Porcentagem | Escala | Operações com Frações | Potenciação/Radiciação

### 2. Estatística e Probabilidade
* **Subassuntos:** Média (Aritmética/Ponderada) | Mediana | Moda | Análise de Gráficos/Tabelas | Probabilidade Simples e Condicional

### 3. Geometria Plana
* **Subassuntos:** Áreas de Figuras Planas (Quadrados, Retângulos, Triângulos, Círculos) | Teorema de Pitágoras | Semelhança de Triângulos | Área de Trapézio

### 4. Geometria Espacial
* **Subassuntos:** Volume e Área de Prismas, Cilindros, Cones, Pirâmides e Esferas | Projeção Ortogonal | Unidades de Medida e Vazão

### 5. Álgebra e Funções
* **Subassuntos:** Equações e Funções de 1º e 2º Grau | Funções Exponenciais e Logarítmicas | Progressão Aritmética (PA) e Geométrica (PG)

### 6. Combinatória e Trigonometria
* **Subassuntos:** Princípio Fundamental da Contagem (PFC) | Permutação | Arranjo | Combinação | Razões Trigonométricas no Triângulo Retângulo

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
* Python 3.10+ instalado.
* Navegador web moderno.

### 1. Configurando o Backend (FastAPI)
Navegue até a pasta do backend, instale as dependências essenciais e inicie o servidor:
```bash
pip install fastapi uvicorn pandas
uvicorn main:app --reload
