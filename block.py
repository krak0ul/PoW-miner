import time
from utils import SHA256, get_long_target


# TODO
# coinbase transactions

class Block():
    def __init__(self, merkle_root, target, transaction_list, previous_hash = 0, timestamp=0, nonce=0, version = 42):
        self.version = version
        self.previous_hash = previous_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.target = target        # 32 bit simplified compact form
        self.nonce = nonce
        self.transaction_list = transaction_list

    def __repr__(self):
        return f"{self.version}{self.previous_hash}{self.merkle_root}\
                {self.timestamp}{self.target}{self.nonce}{self.transaction_list}"
    
    def info(self):
        print(f"version: {self.version} \nPrevious hash: {self.previous_hash} \nMerkle root: {self.merkle_root} \
                \nTimestamp: {self.timestamp}\nTarget: {get_long_target(self.target)} {hex(self.target)} \nNonce: {self.nonce}\n")

    def transactions(self):
        print("Transaction list:")
        for i in self.transaction_list:
            print(f"From {i[0]}\tto {i[1]}\tAmmount: {i[2]} MxCoin")

    def all_info(self):
        return self.__repr__(self) 
    
    def get_timestamp(self):
        return self.timestamp


    def mine(self):
        self.nonce = 0

        # iterate nonce while  block_hash is bigger than the target
        while True:
            block_hash = int(SHA256(repr(self)), 16)   # hash as hex int type, not string
            
            if (block_hash <= get_long_target(self.target) ):
                self.timestamp = time.time()
                return block_hash
            self.nonce += 1
    