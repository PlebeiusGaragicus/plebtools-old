class ChainState:
    block_height: int = None
    latest_block_hash: str = None
    block_time: int = None
    nBits: int = None
    difficulty: float = None

    spot_price: float = None


# initialized to the Genesis block
# TODO put links to bitcoin code on github with line numbers
class GenesisBlock(ChainState):
    def __init__(self):
        self.block_height: int = 0
        self.latest_block_hash: str = '000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f'
        self.block_time: int = 1231006505
        self.nBits: int = 0x1d00ffff
        self.difficulty: float = 1.0

        self.spot_price: float = 0.0
