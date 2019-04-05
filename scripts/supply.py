import math
import datetime, time
import time
SECONDS_PER_BLOCK = 5
# This was chosen because it's an exponent of 2
# And it works out to about a year (1.3 years) if blocks are produced every 5 seconds as planned.
BLOCKS_PER_ERA = 2**23
# This was chosen because it puts the final issuance sometime in 2031
# If Ellipticoin hasn't caught on by then assume we've failed :/
NUMBER_OF_ERAS = 8
# This scales the currency so we end up with 21,000,000 EC at the end of the final Era to match Bitcoin's supply.
SCALE = 49
TOTAL_SUPPLY = 210000000000
# Expected launch date. I'm optimistic.
LAUNCH = datetime.datetime(2019, 9, 1, 0, 0)

def reward_at_era(era):
  return 2**(NUMBER_OF_ERAS - min(era, NUMBER_OF_ERAS)) * SCALE

def last_block_with_reward():
  total = 0
  for era in range(0, NUMBER_OF_ERAS):
    total += reward_at_era(era) * BLOCKS_PER_ERA
  return BLOCKS_PER_ERA * NUMBER_OF_ERAS + (TOTAL_SUPPLY - total) / SCALE

LAST_BLOCK_WITH_REWARD = last_block_with_reward()


def reward_at(block_number):
  reward = reward_at_era(reward_era(block_number))

  if (block_number > LAST_BLOCK_WITH_REWARD):
    return 0
  elif (block_number == LAST_BLOCK_WITH_REWARD - 1):
    return TOTAL_SUPPLY - (total_supply_at(block_number) + reward)
  else:
    return reward

def block_number_to_date(block_number):
  seconds = block_number * SECONDS_PER_BLOCK
  return (LAUNCH + datetime.timedelta(seconds=seconds)).strftime("%Y-%m-%d")

def reward_era(block_number):
  return min(int(block_number / BLOCKS_PER_ERA), NUMBER_OF_ERAS)

def total_supply_at(block_number):
  eras = int(block_number / BLOCKS_PER_ERA)
  total = 0
  for era in range(0, min(eras, NUMBER_OF_ERAS)):
    total += reward_at_era(era) * BLOCKS_PER_ERA
  if eras > NUMBER_OF_ERAS or eras * BLOCKS_PER_ERA != block_number:
    for block_number in range(min(eras, 8) * BLOCKS_PER_ERA, block_number):
      total += reward_at(block_number)
  return total


print "|Block Number|     Date    | Block Reward | Total Supply at end of period"
print "-------------------------------------------------------"

for block_number in range(0, (int(BLOCKS_PER_ERA * (NUMBER_OF_ERAS + 1.5))),
                          BLOCKS_PER_ERA / 2):
  date = block_number_to_date(block_number)
  reward = "varies" if reward_at(block_number) == 0 else reward_at(block_number)
  total_supply = total_supply_at(block_number)
  print("{:>12} | {} | {:>13} | {}".format(block_number, date, reward,
                                           total_supply))

# Output
# Values are in Ellipticoin Base Units (one onethousandth of an Ellipticoin)
# |Block Number|     Date    | Block Reward | Total Supply at end of period
# -------------------------------------------------------
#            0 | 2019-09-01 |         12544 | 0
#      4194304 | 2020-04-30 |         12544 | 52613349376
#      8388608 | 2020-12-29 |          6272 | 105226698752
#     12582912 | 2021-08-29 |          6272 | 131533373440
#     16777216 | 2022-04-28 |          3136 | 157840048128
#     20971520 | 2022-12-27 |          3136 | 170993385472
#     25165824 | 2023-08-27 |          1568 | 184146722816
#     29360128 | 2024-04-26 |          1568 | 190723391488
#     33554432 | 2024-12-24 |           784 | 197300060160
#     37748736 | 2025-08-24 |           784 | 200588394496
#     41943040 | 2026-04-24 |           392 | 203876728832
#     46137344 | 2026-12-22 |           392 | 205520896000
#     50331648 | 2027-08-22 |           196 | 207165063168
#     54525952 | 2028-04-21 |           196 | 207987146752
#     58720256 | 2028-12-20 |            98 | 208809230336
#     62914560 | 2029-08-19 |            98 | 209220272128
#     67108864 | 2030-04-19 |            49 | 209631313920
#     71303168 | 2030-12-18 |            49 | 209836834816
#     75497472 | 2031-08-18 |        varies | 210000000000
