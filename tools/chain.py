from langchain.tools import tool
from ape import networks
from context import SessionContext

context = SessionContext()

@tool
def switch_network(ecosystem_network: str):
    """Switch blockchain networks. Format: 'ecosystem:network'"""
    try:
        with networks.parse_network_choice(ecosystem_network) as provider:
            context.chain_manager = provider
            return f"Switched to {ecosystem_network} (Chain ID: {provider.chain_id})"
    except Exception as e:
        return f"Network error: {str(e)}"

@tool
def current_network_info():
    """Get detailed information about the current network"""
    if not context.chain_manager.network:
        return "Not connected to any network"
    
    return {
        "ecosystem": context.chain_manager.network.ecosystem.name,
        "network": context.chain_manager.network.name,
        "chain_id": context.chain_manager.chain_id,
        "gas_price": context.chain_manager.gas_price,
        "block_number": context.chain_manager.blocks.height
    }