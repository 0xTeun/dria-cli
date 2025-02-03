from utils import extract_tool_docstrings, SYSTEM_PROMPT
# from tools.blockchain_tools import get_current_block, send_eth_transfer

from langchain_ollama.llms import OllamaLLM

def setup_model():
    model = OllamaLLM(model="hf.co/DevQuasar/Dria-Agent-a-3B:Q5_K_M")

    system_prompt = SYSTEM_PROMPT.replace("{{functions_schema}}", extract_tool_docstrings("tools"))
    # prompt = ChatPromptTemplate.from_template(system_prompt)
    human_query = "Can you get me the latest block number of arbitrum mainnet?"
    messages = [
        {"role" : "system", "content" : system_prompt},
        {"role" : "human", "content" : human_query}
    ]

    response = model.invoke(messages)
    return response


if __name__=="__main__":
    print(setup_model())