from langchain.tools import tool
from ape import accounts
from context import SessionContext

context = SessionContext()

@tool
def load_wallet(alias: str):
    """Load a wallet by its alias from Ape's account manager"""
    try:
        context.active_account = accounts.load(alias)
        return f"Loaded wallet: {alias} ({context.active_account.address})"
    except accounts.AccountNotFound as e:
        return f"Wallet error: {str(e)}. Use list_wallets to see available options."

@tool
def list_wallets():
    """List all available wallets in Ape's account manager"""
    return "\n".join([f"{acc.alias}: {acc.address}" for acc in accounts])