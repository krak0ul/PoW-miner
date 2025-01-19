import sys, os, time
from datetime import datetime

from block import Block
from target import Target
from utils import SHA256, avg_mine_time, mine_time, gen_transactions

INITIAL_TARGET = 0x200f0000        # The more smaller the target the harder the mining - simplified view
MAX_BLOCK_SIZE = 4          # number of transactions in a block
BLOCK_TIME_TARGET = 10      # target time between each block (seconds)
DIFFICULTY_PERIOD = 10      # target will be computed every DIFFICULTY_PERIOD blocks

block_chain = []



def main():
    target = Target(DIFFICULTY_PERIOD, INITIAL_TARGET)
    old_timestamp = time.time()

    while True:
        # Generate random transactions
        transaction_list = gen_transactions(MAX_BLOCK_SIZE)

        # create new block and mine it
        new_block = Block(SHA256(repr(transaction_list)), target.target, transaction_list)
        previous_hash = new_block.mine()

        print(f"Mined block {len(block_chain)}")
        new_block.info()
        # new_block.transactions()

        # add blocks to the chain array
        block_chain.append(new_block)

        # compute mine time
        block_time = mine_time(block_chain)
        print(f"time to mine: {block_time}")
        print("\n------------------------------------------------\n")

        # compute new target
        if len(block_chain) % target.difficulty_period == 0:
            average_time = avg_mine_time(block_chain, DIFFICULTY_PERIOD)
            print("------------------------------------------------------")
            print("Computing new target")
            print(f"Average block time: {average_time}")
            print(f"old target: {hex(target.get_long_target())}")
            target.compute_difficulty(average_time, BLOCK_TIME_TARGET)
            print(f"new target: {hex(target.get_long_target())}")
            print("------------------------------------------------------")

        


if __name__ == '__main__':
    main()