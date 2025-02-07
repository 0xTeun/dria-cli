from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from ape import networks
from agent import create_dria_agent
from tools.tools_manager import ToolManager

class DriaTerminal:
    def __init__(self):
        self.session = PromptSession()
        # self.connection = activate_chain("ethereum", "mainnet")
        # chain_str = networks.provider.connection_id
        # self.network, self.chain, *_ = chain_str.split(':', 2)
        self.tools = ToolManager("tools")
        self.agent = create_dria_agent(self.tools) 

    def get_prompt(self):
        """Generate the IPython-style prompt"""
        # network = self.network_info or "not-connected"
        # account = self.account.address[:6] + "..." + self.account.address[-3:] if self.account else "no-wallet"
        return HTML(f'[<blue>PLACE_HOLDER</blue>][<green>WALLET_PLACEHOLDER</green>] >> ')

    def run(self):
        """Run the terminal interface"""
        print("Welcome to Smol DRIA Terminal. Start typing commands in natural language.")
        
        while True:
            try:
                user_input = self.session.prompt(self.get_prompt())
                
                if user_input.lower() in ['exit', 'quit']:
                    break

                response = self.agent.generate_response(user_input)
                print("LLM Response:")
                print(response)
                print("Code Execution")
                results = self.tools.execute_llm_response(response)
                print(results)
                print("test in here")
                
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            except Exception as e:
                print(f"Error: {str(e)}")