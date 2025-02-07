from langchain_ollama.llms import OllamaLLM
from tools.tools_manager import ToolManager

from prompts.general import SYSTEM_PROMPT

class DriaAgent:
    def __init__(self, tools_manager: ToolManager):
        self.model = OllamaLLM(model="hf.co/DevQuasar/Dria-Agent-a-3B:Q5_K_M")
        self.tools = tools_manager
        self.system_prompt = SYSTEM_PROMPT.replace(
            "{{functions_schema}}", 
            tools_manager.get_tools_schema()
        )

    def generate_response(self, human_query: str):
        messages = [
            {"role" : "system", "content" : self.system_prompt},
            {"role" : "human", "content" : human_query}
        ]
        response = self.model.invoke(messages)
        return response

def create_dria_agent(tools_manager: ToolManager):
    return DriaAgent(tools_manager)