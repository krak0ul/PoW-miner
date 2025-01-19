from hashlib import sha256


def SHA256(text): 
    return sha256(text.encode("utf-8")).hexdigest()


def mine_time(timestamp, new_timestamp):
    return new_timestamp - timestamp


def avg_mine_time(block_times):
    return sum(block_times) / len(block_times)
