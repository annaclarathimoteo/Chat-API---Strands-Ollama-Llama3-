🧠 Chat Agent – Strands + Ollama (Llama 3.1)

Este projeto implementa uma API de Chat capaz de interagir com um Agente de IA construído com Strands Agents, utilizando Ollama como servidor local de modelos e o Llama 3.1 como LLM principal.

O agente é capaz de:

🧮 Detectar automaticamente quando uma pergunta exige cálculo matemático e acionar a calculator tool

💬 Responder normalmente a perguntas de conhecimento geral

⚙️ Processar chamadas via API, utilizando FastAPI + Uvicorn

Este repositório atende todos os requisitos do desafio técnico.

📌 Funcionalidades
✔️ 1. Chat inteligente com operação híbrida

O agente conversa naturalmente sobre qualquer tema, mas usa ferramentas quando necessário.

✔️ 2. Tool de Cálculo Matemático

O Agente identifica solicitações como:

"Quanto é 1234 * 5678?"
"Qual a raiz quadrada de 144?"
"Eleve 3 à potência 5."


E resolve com alta precisão via strands_tools.calculator.

✔️ 3. Execução 100% local

Ollama executa o Llama 3.1 no seu computador

Não há dependência de APIs externas

✔️ 4. API simples e robusta

Disponibiliza o endpoint:

POST /chat


Que recebe:

{ "message": "Qual é a capital da França?" }


E retorna:

{ "response": "A capital da França é Paris." }

🧱 Estrutura do Projeto
chat-agent-ollama/
│
├── agent.py              # Configuração do agente (Strands + Ollama + Tools)
├── main.py               # API FastAPI com rota /chat
│
├── schemas/
│   ├── __init__.py       # Exporta os schemas
│   └── chat.py           # Pydantic models (request/response)
│
├── .env                  # Configurações do modelo (LLM_MODEL_NAME, LLM_BASE_URL)
├── requirements.txt      # Dependências
└── .venv/                # Ambiente virtual

⚙️ Instalação e Setup
1️⃣ Instalar o Ollama

Baixe e instale via:
👉 https://ollama.com

2️⃣ Baixar o modelo Llama 3.1
ollama pull llama3.1

3️⃣ Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

4️⃣ Instalar dependências
pip install -r requirements.txt

5️⃣ Configurar o arquivo .env

Crie um .env na raiz:

LLM_MODEL_NAME=llama3.1
LLM_BASE_URL=http://localhost:11434

6️⃣ Rodar o servidor FastAPI
uvicorn main:app --reload


API disponível em:
👉 http://127.0.0.1:8000/docs

🛰️ Endpoint da API
POST /chat
Request (JSON)
{
  "message": "Quanto é 1234 * 5678?"
}

Response (JSON)
{
  "response": "7006652"
}


O valor será produzido via tool calculator, não pelo LLM.

🤖 Funcionamento Interno do Agente

O arquivo agent.py:

Carrega variáveis do .env

Configura o Llama 3.1 via OllamaModel

Registra a tool de cálculo

Define um system_prompt orientando o LLM a:

Usar a tool apenas quando a pergunta exigir cálculo

Responder normalmente sobre outros assuntos

Trecho principal:

agent = Agent(
    model=ollama_model,
    tools=[calculator],
    system_prompt=(
        "Você é um assistente útil. Quando a pergunta envolver cálculos, "
        "use SEMPRE a tool 'calculator'. Caso contrário, responda normalmente."
    ),
)

🧪 Exemplos de Uso
📘 Pergunta geral

Input:

{ "message": "Quem descobriu o Brasil?" }


Output:

{ "response": "O Brasil foi oficialmente 'descoberto' por Pedro Álvares Cabral em 1500." }


✔️ Não usa calculator
✔️ Responde via modelo LLM

🧮 Pergunta de cálculo

Input:

{ "message": "Calcule 250 * 32" }


Output:

{ "response": "8000" }


✔️ Usa calculator
✔️ Resultado exato

📄 Schemas (Pydantic)

schemas/chat.py

from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., description="Mensagem enviada pelo usuário.")

class ChatResponse(BaseModel):
    response: str = Field(..., description="Resposta gerada pelo agente de IA.")

🧭 Como Testar
Via Swagger

Abra:

👉 http://127.0.0.1:8000/docs

Via curl
curl -X POST "http://127.0.0.1:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{ "message": "Quanto é 3^5?" }'

