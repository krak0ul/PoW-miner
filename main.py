import sys, os, time
from datetime import datetime
from hashlib import sha256

from block import Block

# prefix_zeros is our equivalent of a target
PREFIX_ZEROS = 5  # The more leading zeros the harder the mining

MAX_BLOCK_SIZE = 2      # number of transactions in a block

transaction_list = [
    ['Sender', 'Receiver', '20'],
    ['Patrice', 'Michelle', '300'],
    ['qvdchz', 'znof', '2']
]

block_chain = []

def mine_time(timestamp, new_timestamp):
    # print(f"old timestamp: {timestamp}")
    # print(f"new timestamp: {new_timestamp}")
    mine_time = new_timestamp - timestamp
    print(f"time to mine: {mine_time}\n")
    return mine_time

def main():
    block_number = 0
    previous_hash = 0
    timestamp = time.time()

    while True:
        # create new block and mine it
        new_block = Block(previous_hash,sha256(repr(transaction_list).encode("ascii")).hexdigest(), PREFIX_ZEROS, transaction_list)
        previous_hash = new_block.mine(PREFIX_ZEROS)

        print(f"Mined block {block_number}")
        print(repr(new_block))

        # add blocks to the array
        block_chain.append(new_block)
        block_number += 1

        # compute mine time
        new_timestamp = new_block.timestamp
        mine_time(timestamp, new_timestamp)
        timestamp = new_timestamp


if __name__ == '__main__':
    main()