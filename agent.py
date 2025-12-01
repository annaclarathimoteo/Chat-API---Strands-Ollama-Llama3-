import os
from dotenv import load_dotenv

from strands import Agent
from strands.models.ollama import OllamaModel
from strands_tools import calculator  # tool de cálculo pronta

load_dotenv()

LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "llama3")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434")

ollama_model = OllamaModel(
    host=LLM_BASE_URL,
    model_id=LLM_MODEL_NAME,
)

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

def run_agent(user_message: str) -> str:
    """
    Envia a mensagem do usuário para o agente e retorna apenas o texto da resposta.
    """
    response = agent(user_message)

    # Garante que o retorno seja apenas o conteúdo textual
    # sem objetos, dicts ou wrappers desnecessários
    if isinstance(response, dict):
        return response.get("response", "").strip()

    return str(response).strip()
