import sys, os, time
from datetime import datetime
from hashlib import sha256
import randomname, random

from block import Block

# prefix_zeros is our equivalent of a target
PREFIX_ZEROS = 5            # The more leading zeros the harder the mining
MAX_BLOCK_SIZE = 4          # number of transactions in a block
BLOCK_TIME_TARGET = 60      # target time between each block

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
    # print(f"old timestamp: {timestamp}")
    # print(f"new timestamp: {new_timestamp}")
    mine_time = new_timestamp - timestamp
    return mine_time


def avg_block_time(block_times, block_time_target):
    return block_times.sum() / block_times.len()

def compute_difficulty(block_times, block_time_target, prefix_zeros):
    average_time = block_times.sum() / block_times.len()

    if 0 < (block_time_target - average_time) <= 3:
        prefix_zeros += 1

    if 0 > (block_time_target - average_time) >= 3:
        prefix_zeros -= 1


def main():
    block_number = 0
    previous_hash = 0
    timestamp = int(time.time())

    while True:
        # Generate random transactions
        transaction_list = gen_transactions(MAX_BLOCK_SIZE)

        # create new block and mine it
        new_block = Block(previous_hash,sha256(repr(transaction_list).encode("ascii")).hexdigest(), PREFIX_ZEROS, transaction_list)
        previous_hash = new_block.mine(PREFIX_ZEROS)

        print(f"Mined block {block_number}")
        print(repr(new_block))
        new_block.transactions()

        # add blocks to the array
        block_chain.append(new_block)
        block_number += 1


        # compute mine time
        new_timestamp = new_block.timestamp
        block_time = mine_time(timestamp, new_timestamp)
        print(f"time to mine: {block_time}\n")
        block_times.append(block_time)
        
        timestamp = new_timestamp
        print("------------------------------------------------")


if __name__ == '__main__':
    main()