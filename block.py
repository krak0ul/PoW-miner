import time

class Block():
    def __init__(self, version, previous_hash, merkle_root, timestamp, prefix_zeros, nonce):
        self.version = version
        self.previous_hash = previous_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp or int(time.time())
        self.prefix_zeros = prefix_zeros
        self.nonce = nonce