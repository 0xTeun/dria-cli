from ape.api.providers import BlockAPI

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
    from ape import networks
    from ape.exceptions import ProviderNotConnectedError
    try:
        # Check if there's an existing connection and disconnect
        if networks.connected:
            networks.active_provider.disconnect()
            print("Previous connection closed")
    except ProviderNotConnectedError:
        pass

    # Be more explicit with the network choice
    network_choice = f"{chain.lower()}:{network.lower()}"
    print(f"Attempting to connect to {network_choice}")
    
    # Check if ecosystem is available
    if chain not in networks.ecosystems:
        raise ValueError(f"Ecosystem {chain} not found. Available: {list(networks.ecosystems.keys())}")
    
    provider = networks.parse_network_choice(f"{chain}:{network}:node")
    try:
        provider.__enter__()
        print(f"Successfully connected to {provider.provider.network_choice}")
        return True
    except Exception as e:
        print(f"Connection error: {str(e)}")
        raise
    # try:
    # # Check if there's an existing connection and disconnect
    #     if networks.connected:
    #         networks.active_provider.disconnect()
    #         networks.provider.disconnect()
    #         # networks.provider.disconnect()
    #         print("Previous connection closed")
    # except ProviderNotConnectedError:
    #     # No existing connection, that's fine
    #     pass
    # # print(f"Is connected: {networks.provider.is_connected}")
    # # if not networks.provider.is_connected:
    # #     networks.provider.disconnect()
    
    # provider = networks.parse_network_choice(f"{chain}:{network}:node")
    # provider.__enter__()
    # # print(f"{provider.is_connected}: Connected to {provider.network_choice}")

    # return True


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