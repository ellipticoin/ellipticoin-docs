import datetime
import time

# All monetary values are in Ellipticoin Base Units (one onethousandth of an Ellipticoin)

YEARS_PER_ERA = 2
NUMBER_OF_ERAS = 7
SECONDS_PER_BLOCK = 5
SECONDS_IN_A_YEAR = datetime.timedelta(days=365).total_seconds()
BLOCKS_PER_ERA = int(YEARS_PER_ERA * SECONDS_IN_A_YEAR)/ SECONDS_PER_BLOCK
LOG_BASE = 2
SCALE = 10000
LAUNCH_DATE = datetime.datetime(2019, 9, 1, 0, 0)


def reward_era(block_number):
    return block_number / BLOCKS_PER_ERA

def reward_at_era(era):
    return LOG_BASE**(NUMBER_OF_ERAS - era - 1) * SCALE

def block_number_to_date(block_number):
    seconds = block_number * SECONDS_PER_BLOCK
    date = LAUNCH_DATE + datetime.timedelta(seconds=seconds)
    return date.strftime("%Y-%m-%d")

def total_supply_at(block_number):
    total = 0
    for era in range(0, reward_era(block_number)):
        total += reward_at_era(era) * BLOCKS_PER_ERA
    return total

print(BLOCKS_PER_ERA)
print "|Block Number|     Date    | Block Reward | Total Supply at end of period"
print "-------------------------------------------------------"

for block_number in range(0, (int(BLOCKS_PER_ERA * NUMBER_OF_ERAS)),
                          BLOCKS_PER_ERA):
    date = block_number_to_date(block_number)
    reward = reward_at_era(reward_era(block_number))
    total_supply = total_supply_at(block_number)
    print("{:>12} | {} | {:>13} | {}".format(block_number, date, reward,
                                             total_supply))

# Output
# |Block Number|     Date    | Block Reward | Total Supply at end of period
# -------------------------------------------------------
#            0 | 2019-09-01 |        640000 | 0
#     12614400 | 2021-08-31 |        320000 | 8073216000000
#     25228800 | 2023-08-31 |        160000 | 12109824000000
#     37843200 | 2025-08-30 |         80000 | 14128128000000
#     50457600 | 2027-08-30 |         40000 | 15137280000000
#     63072000 | 2029-08-29 |         20000 | 15641856000000
#     75686400 | 2031-08-29 |         10000 | 15894144000000
