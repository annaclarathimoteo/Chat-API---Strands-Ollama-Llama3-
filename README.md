# 🧠 Chat Agent – Strands + Ollama (Llama 3.1)

Este projeto implementa uma API de Chat capaz de interagir com um agente de IA construído com **Strands Agents**, utilizando o **Ollama** como servidor local de modelos e o **Llama 3.1** como LLM principal.

O agente foi configurado para:

- 🧮 Detectar automaticamente quando uma pergunta exige **cálculo matemático** e acionar a tool `calculator`;
- 💬 Responder normalmente a perguntas de **conhecimento geral**;
- ✂️ Gerar respostas **diretas, objetivas e sem frases redundantes** (evita frases como “a resposta ao seu questionamento é…”);
- ⚙️ Processar chamadas via API, utilizando **FastAPI + Uvicorn**.

---

## 📌 Funcionalidades

### ✔️ 1. Chat inteligente com operação híbrida

O agente conversa naturalmente sobre qualquer tema, mas usa ferramentas quando necessário:

- Se a pergunta envolver operações matemáticas (somar, subtrair, multiplicar, dividir, raiz, potência etc.), ele usa **exclusivamente** a tool `calculator` e retorna **apenas o resultado numérico**.
- Para perguntas gerais, responde apenas com texto, de forma direta e objetiva.

### ✔️ 2. Tool de Cálculo Matemático

O agente identifica solicitações como:

- `"Quanto é 1234 * 5678?"`
- `"Qual a raiz quadrada de 144?"`
- `"Eleve 3 à potência 5."`

e resolve com alta precisão via `strands_tools.calculator`, retornando **somente o número** no campo `response`.

### ✔️ 3. Execução 100% local

- O **Ollama** executa o modelo **Llama 3.1** no seu computador.
- Não há dependência de APIs externas.

### ✔️ 4. API simples e robusta

Disponibiliza o endpoint:

- `POST /chat`

Que recebe:

```json
{ "message": "Qual é a capital da França?" }
E retorna:

json
Copiar código
{ "response": "A capital da França é Paris." }
Para perguntas de cálculo, o retorno será apenas o valor numérico, por exemplo:

json
Copiar código
{ "response": "7006652" }
🧱 Estrutura do Projeto
text
Copiar código
chat-agent-ollama/
│
├── agent.py              # Configuração do agente (Strands + Ollama + tool calculator)
├── main.py               # API FastAPI com rota /chat
│
├── schemas/
│   ├── __init__.py       # Exporta ChatRequest e ChatResponse
│   └── chat.py           # Pydantic models (request/response)
│
├── .env                  # Configurações do modelo (LLM_MODEL_NAME, LLM_BASE_URL)
├── requirements.txt      # Dependências do projeto
└── .venv/                # Ambiente virtual (não versionado)
⚙️ Instalação e Setup
1️⃣ Instalar o Ollama
Baixe e instale em:

👉 https://ollama.com

2️⃣ Baixar o modelo Llama 3.1
No terminal:

bash
Copiar código
ollama pull llama3.1
3️⃣ Criar ambiente virtual
bash
Copiar código
python3 -m venv .venv
source .venv/bin/activate  # Linux/MacOS
# No Windows: .venv\Scripts\activate
4️⃣ Instalar dependências
bash
Copiar código
pip install -r requirements.txt
As dependências principais incluem:

fastapi

uvicorn[standard]

python-dotenv

strands-agents

strands-agents-tools

ollama

5️⃣ Configurar o arquivo .env
Crie um arquivo .env na raiz do projeto:

env
Copiar código
LLM_MODEL_NAME=llama3.1
LLM_BASE_URL=http://localhost:11434
Obs.: O código define um padrão llama3 caso a variável não exista, mas o recomendado é configurar explicitamente llama3.1 no .env.

6️⃣ Rodar o servidor FastAPI
Com o ambiente virtual ativado:

bash
Copiar código
uvicorn main:app --reload
A documentação interativa (Swagger) ficará disponível em:

👉 http://127.0.0.1:8000/docs

🛰️ Endpoint da API
POST /chat
Request (JSON)

json
Copiar código
{
  "message": "Quanto é 1234 * 5678?"
}
Response (JSON) – pergunta de cálculo

json
Copiar código
{
  "response": "7006652"
}
O valor é produzido pela tool calculator, não pelo LLM, e retornado sem frases adicionais.

Response (JSON) – pergunta geral

json
Copiar código
{
  "response": "O Brasil foi oficialmente 'descoberto' por Pedro Álvares Cabral em 1500."
}
🤖 Funcionamento Interno do Agente
Arquivo: agent.py

Principais responsabilidades:

Carrega variáveis do .env com python-dotenv;

Configura o modelo Llama via OllamaModel:

python
Copiar código
ollama_model = OllamaModel(
    host=LLM_BASE_URL,
    model_id=LLM_MODEL_NAME,
)
Registra a tool de cálculo calculator;

Define um system_prompt que:

Obriga o uso da tool apenas quando a mensagem envolver operações matemáticas;

Determina que o agente responda de forma direta, objetiva e sem redundâncias;

Em perguntas de cálculo, orienta a retornar somente o resultado final.

Trecho principal:

python
Copiar código
agent = Agent(
    model=ollama_model,
    tools=[calculator],
    system_prompt=(
        "Responda sempre de forma direta, objetiva e sem frases redundantes. "
        "Não use construções como 'A resposta ao seu questionamento é' ou similares. "
        "Quando a mensagem envolver operações matemáticas "
        "(somar, subtrair, multiplicar, dividir, raiz, potência etc.), "
        "use exclusivamente a tool 'calculator' e retorne apenas o resultado final. "
        "Para perguntas gerais, responda normalmente."
    ),
)
A função run_agent garante que o endpoint sempre retorne apenas o texto puro da resposta:

python
Copiar código
def run_agent(user_message: str) -> str:
    response = agent(user_message)

    if isinstance(response, dict):
        return response.get("response", "").strip()

    return str(response).strip()
📄 Schemas (Pydantic)
Arquivo: schemas/chat.py

python
Copiar código
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        description="Mensagem enviada pelo usuário para o agente."
    )

class ChatResponse(BaseModel):
    response: str = Field(
        ...,
        description="Resposta gerada pelo agente de IA."
    )
O pacote schemas é exposto via schemas/__init__.py:

python
Copiar código
from .chat import ChatRequest, ChatResponse
🧭 Como Testar
Via Swagger (recomendado)
Inicie o servidor:

bash
Copiar código
uvicorn main:app --reload
Acesse:

👉 http://127.0.0.1:8000/docs

Use o endpoint POST /chat, informe um message e execute.

Via curl
bash
Copiar código
curl -X POST "http://127.0.0.1:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{ "message": "Quanto é 3^5?" }'
Resposta esperada:

json
Copiar código
{ "response": "243" }