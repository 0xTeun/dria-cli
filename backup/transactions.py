from langchain.tools import tool
from context import SessionContext
from ape import Contract

context = SessionContext()

@tool
def get_balance(address: str = None):
    """Get ETH balance of an address (defaults to active wallet)"""
    address = address or context.active_account.address
    return context.chain_manager.provider.get_balance(address)

@tool
def send_eth(to_address: str, amount: str):
    """Send ETH to another address"""
    if not context.active_account:
        return "Error: No wallet loaded. Use load_wallet first."
    
    try:
        receipt = context.active_account.transfer(to_address, amount)
        return f"Transaction successful: {receipt.txn_hash}"
    except Exception as e:
        return f"Transaction failed: {str(e)}"