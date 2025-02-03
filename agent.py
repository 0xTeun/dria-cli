from utils import extract_tool_docstrings, SYSTEM_PROMPT
from langchain_ollama.llms import OllamaLLM

class DriaAgent:
    def __init__(self):
        self.model = OllamaLLM(model="hf.co/DevQuasar/Dria-Agent-a-3B:Q5_K_M")
        self.system_prompt = SYSTEM_PROMPT.replace(
            "{{functions_schema}}", 
            extract_tool_docstrings("tools")
        )

    def generate_response(self, human_query: str):
        messages = [
            {"role" : "system", "content" : self.system_prompt},
            {"role" : "human", "content" : human_query}
        ]
        response = self.model.invoke(messages)
        return response

def create_dria_agent():
    return DriaAgent()