import sys, os, time
from datetime import datetime

from block import Block
from target import Target
from utils import SHA256, mine_time, gen_transactions

INITIAL_TARGET = 0x200f0000        # The smaller the target the harder the mining - simplified view
MAX_BLOCK_SIZE = 4          # number of transactions in a block
BLOCK_TIME_TARGET = 10      # target time between each block (seconds)
DIFFICULTY_PERIOD = 10      # target will be computed every DIFFICULTY_PERIOD blocks

block_chain = []


def main():
    # initialize target hash difficulty class
    target = Target(DIFFICULTY_PERIOD, INITIAL_TARGET)
    previous_hash = 0
    
    while True:
        # Generate random transactions
        transaction_list = gen_transactions(MAX_BLOCK_SIZE)

        # create new block and mine it
        new_block = Block(SHA256(repr(transaction_list)), target.target, transaction_list, previous_hash)
        previous_hash = new_block.mine()

        print(f"Mined block {len(block_chain)}")
        new_block.info()
        # new_block.transactions()

        # add blocks to the chain array
        block_chain.append(new_block)

        # compute mine time
        print(f"time to mine: {mine_time(block_chain)}")
        print("\n------------------------------------------------\n")

        # compute new target
        target.difficulty(block_chain, BLOCK_TIME_TARGET)
        


if __name__ == '__main__':
    main()