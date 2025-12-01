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
