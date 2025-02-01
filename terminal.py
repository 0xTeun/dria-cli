from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from ape import networks, accounts, chain
# from .agent import create_dria_agent

class DriaTerminal:
    def __init__(self):
        self.session = PromptSession()
        self.agent = None # create_dria_agent()
        self.network = None
        self.ecosystem = None
        self.account = None
        self._connect_to_default_network()
    
    def _connect_to_default_network(self):
        """Connect to ethereum mainnet by default"""
        try:
            
            # Connect to ethereum mainnet using network choice format
            with networks.parse_network_choice("ethereum:mainnet:alchemy") as provider:
                self.network = provider.network.name
                self.ecosystem = provider.network.ecosystem.name
                
                # # Try to load first account if available
                # if accounts.aliases:
                #     self.account = accounts.load(accounts.aliases[0])
                
                # print(f"Connected to {self.network}")
                # if self.account:
                #     print(f"Using account: {self.account.address}")
                
        except Exception as e:
            print(f"Failed to connect to network: {str(e)}")
            self.ecosystem = "not-connected"
            self.network = "not-connected"
            self.account = None

    def switch_network(self, ecosystem: str, network: str = 'mainnet', provider: str = None):
        """Switch to a different blockchain network"""
        try:
            if networks.active_provider:
                networks.active_provider.disconnect()
            
            # If no provider specified, use network's default provider
            network_choice = f"{ecosystem}:{network}"
            if provider:
                network_choice += f":{provider}"
            
            with networks.parse_network_choice(network_choice) as provider:
                self.network = provider.network.name
                print(f"Switched to {self.network}")
                
        except Exception as e:
            print(f"Failed to switch network: {str(e)}")
            self.network = "not-connected"

    def get_prompt(self):
        """Generate the IPython-style prompt"""
        network = self.network or "not-connected"
        account = self.account.address[:6] + "..." + self.account.address[-3:] if self.account else "no-wallet"
        return HTML(f'[<blue>{self.ecosystem}:{network}</blue>][<green>{account}</green>] >> ')

    def _handle_network_command(self, command: str) -> bool:
        """Handle network switching commands"""
        parts = command.lower().split()
        
        # Handle basic network switch
        if len(parts) == 1 and parts[0] in networks.ecosystems:
            self.switch_network(parts[0])
            return True
            
        # Handle network with specific chain (e.g., "ethereum goerli")
        if len(parts) == 2 and parts[0] in networks.ecosystems:
            self.switch_network(parts[0], parts[1])
            return True
            
        # Handle network with specific provider (e.g., "ethereum mainnet custom_rpc")
        if len(parts) == 3 and parts[0] in networks.ecosystems:
            self.switch_network(parts[0], parts[1], parts[2])
            return True
            
        return False

    def run(self):
        """Run the terminal interface"""
        print("Welcome to Smol DRIA Terminal. Start typing commands in natural language.")
        print("Available networks:", ", ".join(networks.ecosystems))
        
        while True:
            try:
                user_input = self.session.prompt(self.get_prompt())
                
                if user_input.lower() in ['exit', 'quit']:
                    break
                
                # Check if it's a network switch command
                if not self._handle_network_command(user_input):
                    # If not, it would be handled by the agent (when implemented)
                    print("Command received:", user_input)
                    # response = self.agent.run(user_input)
                    # print(response)
                
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            except Exception as e:
                print(f"Error: {str(e)}")
        
        # Cleanup on exit
        if networks.active_provider:
            networks.active_provider.disconnect()