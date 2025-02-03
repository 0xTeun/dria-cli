from langchain.tools import tool
from ape.api.providers import BlockAPI
from ape import chain, networks

@tool
def activate_chain(ecosystem:str, chain="mainnet")-> bool:
    """
    Activate the specified blockchain ecosystem and chain.

    Args:
        ecosystem (str): The name of the ecosystem to activate.
        chain (str, optional): The name of the chain to activate. 
                               Defaults to "mainnet".

    Returns:
        bool: True if the ecosystem and chain were activated successfully, 
              False otherwise.
    """
    try:
        with networks.parse_network_choice(f"{ecosystem}:f{chain}:alchemy") as provider:
            print(f"changed to {provider.name}")
            print(dir(provider))
            pass
        return True
    except Exception as e:
        print(e)
        return False

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