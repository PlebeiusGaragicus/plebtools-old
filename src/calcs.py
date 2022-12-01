from .constants import *

####################################
def block_subsity( height ) -> int:
    """
        This returns the coinbase reward in satoshi for a given block height

        see: https://github.com/bitcoin/bitcoin/blob/b71d37da2c8c8d2a9cef020731767a6929db54b4/src/validation.cpp#L1479-L1490
    """
    return (50 * ONE_HUNDRED_MILLION) >> (height // SUBSIDY_HALVING_INTERVAL)

#################################################
def blocks_until_halvening(block_height) -> int:
    """
        This tells you how many blocks until the next halvening
    """
    return ((block_height // SUBSIDY_HALVING_INTERVAL + 1) * SUBSIDY_HALVING_INTERVAL) - block_height


########################################
def fiat(sats, bitcoin_price) -> float:
    """
        Convert sats into fiat value at given price of bitcoin
    """
    return sats * (bitcoin_price / ONE_HUNDRED_MILLION)

#######################################
def btc(fiat, bitcoin_price) -> float:
    """
        Convert fiat into sats at given price of bitcoin
    """
    return int(ONE_HUNDRED_MILLION * (fiat / bitcoin_price))


###################################################
def hash_value(subsidy, fees, difficulty) -> float:
    """
        This will return the hash value
    """
    nh = get_hashrate_from_difficulty(difficulty)

    return (subsidy + fees) / nh

###########################
def hash_price() -> float:
    raise NotImplementedError
    return 0.0

########################################
def get_difficulty(bits: int) -> float:
    """
        This converts the 'bits' field in a bitcoin block to the 'difficulty' number
        reference: https://github.com/bitcoin/bitcoin/blob/8f3ab9a1b12a967cd9827675e9fce112e51d42d8/src/rpc/blockchain.cpp#L75-L95
    """

    shift = (bits >> 24) & 0xFF
    diff = 0x0000FFFF / (bits & 0x00FFFFFF)

    while shift < 29:
        diff *= 256.0
        shift += 1
    
    while shift > 29:
        diff /= 256.0
        shift -= 1

    return diff

###############################################################
def get_hashrate_from_difficulty( difficulty: float) -> float:
    """
        Returns estimated network terahashes for a given network difficulty
    """
    return (difficulty * 2 ** 32) / 600 / TERAHASH
