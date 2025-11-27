import os
from dotenv import load_dotenv

from strands import Agent
from strands.models.ollama import OllamaModel
from strands_tools import calculator  # tool de cálculo pronta

# Carrega variáveis do .env
load_dotenv()

LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "llama3")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434")


# Configura o modelo do Ollama para o Strands
ollama_model = OllamaModel(
    host=LLM_BASE_URL,
    model_id=LLM_MODEL_NAME,
)

# Cria o agente com:
# - modelo do Ollama
# - tool de cálculo
# - system_prompt orientando o uso da tool
agent = Agent(
    model=ollama_model,
    tools=[calculator],
    system_prompt=(
        "Você é um assistente útil. "
        "Quando a pergunta do usuário envolver operações matemáticas "
        "(somar, subtrair, multiplicar, dividir, raiz, potência, etc.), "
        "use SEMPRE a tool 'calculator' para obter o resultado exato. "
        "Para outras perguntas de conhecimento geral, responda normalmente, "
        "sem usar a tool."
    ),
)


def run_agent(user_message: str) -> str:
    """
    Função auxiliar que envia a mensagem do usuário para o agente
    e retorna a resposta como string.
    """
    response = agent(user_message)
    # o Agent normalmente retorna um objeto do tipo Message/str; garantimos string:
    return str(response)
