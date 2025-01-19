import sys, os, time
from datetime import datetime
import randomname, random

from block import Block
from target import Target
from utils import SHA256, avg_mine_time, mine_time

INITIAL_TARGET = 0x200f0000        # The more smaller the target the harder the mining - simplified view
MAX_BLOCK_SIZE = 4          # number of transactions in a block
BLOCK_TIME_TARGET = 10      # target time between each block (seconds)
DIFFICULTY_PERIOD = 10      # target will be computed every DIFFICULTY_PERIOD blocks

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



def main():
    block_number = 0
    target = Target(INITIAL_TARGET)
    old_timestamp = time.time()

    while True:
        # Generate random transactions
        transaction_list = gen_transactions(MAX_BLOCK_SIZE)

        # create new block and mine it
        new_block = Block(SHA256(repr(transaction_list)), target.target, transaction_list)
        previous_hash = new_block.mine()

        print(f"Mined block {block_number}")
        new_block.info()
        # new_block.transactions()

        # add blocks to the chain array
        block_chain.append(new_block)
        block_number += 1


        # compute mine time
        block_time = mine_time(old_timestamp, new_block.timestamp)
        old_timestamp = new_block.timestamp
        print(f"time to mine: {block_time}\n")

        # compute difficulty
        block_times.append(block_time)                  # handle list of previous block times
        if len(block_times) > DIFFICULTY_PERIOD:
            block_times.pop(0)

        if block_number % DIFFICULTY_PERIOD == 0:          # compute new target
            average_time = avg_mine_time(block_times)
            print("------------------------------------------------------")
            print("Computing new target")
            print(f"Average block time: {average_time}")
            print(f"old target: {hex(target.get_long_target())}")
            target.compute_difficulty(average_time, BLOCK_TIME_TARGET)
            print(f"new target: {hex(target.get_long_target())}")
            print("------------------------------------------------------")

        
        print("------------------------------------------------")


if __name__ == '__main__':
    main()