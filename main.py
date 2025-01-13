import sys, os, time
from datetime import datetime
from hashlib import sha256

# prefix_zeros is our equivalent of a target
PREFIX_ZEROS = '000'  # The more leading zeros the harder the mining

transaction_list = [
    ['Sender', 'Receiver', '20'],
    ['Patrice', 'Michelle', '300'],
    ['qvdchz', 'znof', '2']
]


def SHA256(text):
    return sha256(text.encode("ascii")).hexdigest()

# def match_target(block):
#     return

def mine(block_number, transaction_list, previous_hash, PREFIX_ZEROS):
    nonce = 0
    block_hash = SHA256(repr(transaction_list))

# while the first characters of block_hash != PREFIX_ zeros, iterate nonce
    while block_hash[:(len(PREFIX_ZEROS))] != PREFIX_ZEROS:
        nonce += 1
        block_hash = SHA256(f"{transaction_list}{nonce}")
        print(block_hash)
    print(block_hash)
    return 


def main():
    block_number = 0
    previous_hash = 0

    print(SHA256(repr(transaction_list)))

    while True:
        mine(block_number, transaction_list, previous_hash, PREFIX_ZEROS)
        block_number += 1
        print(f'Block number: {block_number}')
        break
    return

if __name__ == '__main__':
    main()