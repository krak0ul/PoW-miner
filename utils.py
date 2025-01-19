from hashlib import sha256
import randomname, random

def SHA256(text): 
    return sha256(text.encode("utf-8")).hexdigest()


def mine_time(block_chain):
    if len(block_chain) > 1:
        return block_chain[-1].get_timestamp() - block_chain[-2].get_timestamp()


def avg_mine_time(block_chain, difficulty_period):
    total_time = block_chain[-1].get_timestamp() - block_chain[-difficulty_period].get_timestamp()
    
    average = total_time / difficulty_period
    return average


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