import time
from utils import SHA256


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
                {self.timestamp}{self.target}{self.nonce}\n"
    
    def info(self):
        print(f"version: {self.version} \nPrevious hash: {self.previous_hash} \nMerkle root: {self.merkle_root} \
                \nTimestamp: {self.timestamp}\nTarget: {self.get_long_target()} {hex(self.target)} \nNonce: {self.nonce}\n")

    def transactions(self):
        print("Transaction list:")
        for i in self.transaction_list:
            print(f"From {i[0]}\tto {i[1]}\tAmmount: {i[2]} MxCoin")

    def all_info(self):
        return self.__repr__(self) 


    def get_long_target(self):
        exponent = (self.target >> 24) & 0xFF
        significand = self.target & 0xFFFFFF

        # Calculate the long target
        long_target = significand * (2 ** (8 * (exponent - 3)))      # substract 3 to exponent because significand represents the first 3 bytes of target
        return long_target


    def mine(self):
        self.nonce = 0

        # iterate nonce while  block_hash is bigger than the target
        while True:
            block_hash = int(SHA256(repr(self)), 16)   # hash as hex int type, not string
            
            if (block_hash <= self.get_long_target() ):
                self.timestamp = time.time()
                return block_hash
            self.nonce += 1
    