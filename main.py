from fastapi import FastAPI
import uvicorn

from agent import run_agent
from schemas import ChatRequest, ChatResponse




app = FastAPI(
    title="Chat API - Strands + Ollama (Llama3)",
    version="1.0.0",
)



@app.post(
    "/chat",
    response_model=ChatResponse,
    summary="Endpoint de chat com o agente de IA",
    description=(
        "Recebe uma mensagem de texto do usuário no campo `message` "
        "e retorna a resposta gerada pelo agente de IA no campo `response`. "
        "O agente utiliza uma tool de cálculo matemático quando a pergunta "
        "exige operações numéricas e responde normalmente em perguntas de "
        "conhecimento geral."
    ),
)
async def chat(payload: ChatRequest):
    """
    Endpoint de chat:
    - recebe JSON: {"message": "..."}
    - retorna JSON: {"response": "..."}
    """
    answer = run_agent(payload.message)
    return ChatResponse(response=answer)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
