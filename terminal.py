from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from ape import networks
from agent import create_dria_agent
from tools.chain import activate_chain
from utils import extract_and_execute_code

class DriaTerminal:
    def __init__(self):
        self.session = PromptSession()
        self.connection = activate_chain("ethereum", "mainnet")
        self.network_info = self.connection.network_choice
        self.agent = create_dria_agent() 

    def get_prompt(self):
        """Generate the IPython-style prompt"""
        network = self.network_info or "not-connected"
        # account = self.account.address[:6] + "..." + self.account.address[-3:] if self.account else "no-wallet"
        return HTML(f'[<blue>{network}</blue>][<green>WALLET_PLACEHOLDER</green>] >> ')

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
                results = extract_and_execute_code(response)
                print(results)

                
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            except Exception as e:
                print(f"Error: {str(e)}")

        # Cleanup on exit
        if networks.active_provider:
            networks.active_provider.disconnect()