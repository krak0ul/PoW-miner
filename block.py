import time
from hashlib import sha256

class Block():
    def __init__(self, previous_hash, merkle_root, prefix_zeros, transaction_list, timestamp=0, nonce=0, version = 42):
        self.version = version
        self.previous_hash = previous_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp #or int(time.time())
        self.prefix_zeros = prefix_zeros
        self.nonce = nonce
        self.transaction_list = transaction_list

    def __repr__(self):
        return f"version: {self.version} \nPrevious hash: {self.previous_hash} \nMerkle root: {self.merkle_root} \
                s\nTimestamp: {self.timestamp}\nPrefix zeros: {self.prefix_zeros} \nNonce: {self.nonce}\n"
    
    def info(self):
        return "Timestamp: {self.timestamp}\nPrefix zeros: {self.prefix_zeros} \nNonce: {self.nonce}\n"
    
    def SHA256(self, text): 
        return sha256(text.encode("ascii")).hexdigest()

    def mine(self, prefix_zeros):
        self.nonce = 0

        # iterate nonce while the first characters of block_hash != PREFIX_ZEROS
        while True:
            block_hash = self.SHA256(repr(self))
            
            if( block_hash[:prefix_zeros] == '0'*prefix_zeros ):
                # print(block_hash[:prefix_zeros])
                # print('0'*prefix_zeros)
                self.timestamp = time.time()
                return block_hash
            self.nonce += 1
    