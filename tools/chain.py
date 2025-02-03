from ape.api.providers import BlockAPI
from ape import chain, networks

def tool(func):
    """
    Custom tool decorator that preserves function metadata 
    and adds a marker for tool identification.
    """
    func.is_tool = True
    return func

@tool
def activate_chain(chain:str, network:str):
    """
    Activate the specified blockchain network. 
    Supported blockchains are Ethereum, Base, Arbitrum, and Optimism.
    Supported networks are mainnet and testnet.

    Args:
        chain (str): The name of the blockchain to activate.
        network (str, optional): The type of the chain to activate. 
    """
    try:
        with networks.parse_network_choice(f"{chain}:{network}:alchemy") as provider:
            print(f"Activated {provider.network_choice}")
            return provider
    except Exception as e:
        print(e)
        return None

@tool
def get_latest_block() -> dict:
    """
    Retrieve the latest block from the blockchain.

    Returns:
        dict: A dictionary containing the latest block and its details, 
              including number, hash, timestamp, gas used, and gas limit.
    """
    latest_block = chain.blocks.head
    return {
        "block" : latest_block,
        "details" : {
            "number": latest_block.number,
            "hash": str(latest_block.hash),
            "timestamp": latest_block.timestamp,
            "gas_used": latest_block.gas_used,
            "gas_limit": latest_block.gas_limit 
        }
    }

@tool
def get_block_by_number(number:int) -> BlockAPI:
    """
    Retrieve a block from the blockchain by its block number.

    Args:
        number (int): The block number to retrieve.

    Returns:
        BlockAPI: The block corresponding to the given number.
    """
    return chain.blocks[number]