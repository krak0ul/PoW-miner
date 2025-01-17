import sys, os, time
from datetime import datetime
from hashlib import sha256
import randomname, random

from block import Block

# prefix_zeros is our equivalent of a target
PREFIX_ZEROS = 5            # The more leading zeros the harder the mining
MAX_BLOCK_SIZE = 4          # number of transactions in a block
BLOCK_TIME_TARGET = 10      # target time between each block
DIFFICULTY_PERIOD = 10      # targe will be computed every DIFFICULTY_PERIOD blocks

block_chain = []
block_times = []


def gen_transactions(max_block_size):
    ''' Generate random transactions'''
    # Returns a list containing max_block_size transactions
    transaction_list = []
    for i in range(max_block_size):
        sender = randomname.get_name()
        recipient = randomname.get_name()
        ammount = random.randint(0, 10000)
    
        transaction = [sender, recipient, ammount]
        transaction_list.append(transaction)
    return transaction_list


def mine_time(timestamp, new_timestamp):
    return new_timestamp - timestamp


def avg_mine_time(block_times):
    return sum(block_times) / len(block_times)


def compute_difficulty(block_times, block_time_target, prefix_zeros):
    average_time = avg_mine_time(block_times)
    print(f"Avg time: {average_time}")
    ratio = block_time_target / average_time

    if ratio > 1.5 :
        ratio = 1.5
    # elif ratio 
    print(f"Ratio: {ratio}")
    return int(prefix_zeros * ratio)


def main():
    block_number = 0
    previous_hash = 0
    prefix_zeros = PREFIX_ZEROS
    timestamp = time.time()

    while True:
        # Generate random transactions
        transaction_list = gen_transactions(MAX_BLOCK_SIZE)

        # create new block and mine it
        new_block = Block(previous_hash, sha256(repr(transaction_list).encode("utf-8")).hexdigest(), prefix_zeros, transaction_list)
        previous_hash = new_block.mine()

        print(f"Mined block {block_number}")
        # print(repr(new_block))
        # new_block.transactions()

        # add blocks to the array
        block_chain.append(new_block)
        block_number += 1


        # compute mine time
        new_timestamp = new_block.timestamp
        block_time = mine_time(timestamp, new_timestamp)
        timestamp = new_timestamp
        print(f"time to mine: {block_time}\n")

        # compute difficulty
        block_times.append(block_time)
        if len(block_times) > DIFFICULTY_PERIOD:
            block_times.pop(0)

        if block_number % 10 == 0:
            prefix_zeros = compute_difficulty(block_times, BLOCK_TIME_TARGET, prefix_zeros)
            print("block times: " + repr(block_times))
            print(prefix_zeros)

        
        print("------------------------------------------------")


if __name__ == '__main__':
    main()