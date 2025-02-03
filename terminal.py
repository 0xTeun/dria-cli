from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from ape import networks, accounts, chain
# from agent import create_dria_agent

class DriaTerminal:
    def __init__(self):
        self.session = PromptSession()
    
    def run(self):
        """Run the terminal interface"""
        print("Welcome to Smol DRIA Terminal. Start typing commands in natural language.")
        
        while True:
            try:
                user_input = self.session.prompt(self.get_prompt())
                
                if user_input.lower() in ['exit', 'quit']:
                    break

                response = self.agent.run(user_input)
                
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            except Exception as e:
                print(f"Error: {str(e)}")