HASH     = 1                            # 10**0
KILOHASH = 1_000                        # 10**3
MEGAHASH = 1_000_000                    # 10**6
GIGAHASH = 1_000_000_000                # 10**9
TERAHASH = 1_000_000_000_000            # 10**12
PETAHASH = 1_000_000_000_000_000        # 10**15
EXAHASH  = 1_000_000_000_000_000_000    # 10**18

# number of satoshi in one bitcoin
ONE_HUNDRED_MILLION = 100_000_000       # 10**8

# 6 blocks per hour, for 24 hours - assuming a perfect cadence of 10 minutes per block
EXPECTED_BLOCKS_PER_DAY = 144           # 24 * 6

# https://github.com/bitcoin/bitcoin/blob/0.21/src/chainparams.cpp#L69
SUBSIDY_HALVING_INTERVAL = 210_000

# https://github.com/bitcoin/bitcoin/blob/8e7eeb5971444c0c93e9a89bbdcc3a51a19e09e9/src/chainparams.cpp#L84
POW_TARGET_SPACING = 2016 # AKA BLOCKS PER 'EPOCH'
