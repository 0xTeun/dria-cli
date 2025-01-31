import click
from langchain.agents import initialize_agent, AgentType
from langchain.chains.conversation.memory import ConversationBufferMemory
# from tools.blockchain_tools import get_current_block, send_eth_transfer

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

def create_agent():
    model = OllamaLLM(model="hf.co/DevQuasar/Dria-Agent-a-3B:Q5_K_M")
    pass