#  TODO
# generate random transactions to fill transaction pool
# link transactions to wallets and validation based on available funds
# method to select n transactions from the pool based on max block size
# merkle tree algorithm

class Transactions():
    def __init__(self,):
        self.transaction_pool = []
        self.block_transactions = []

    def new_transaction(self, transaction):
        self.transaction_pool.append(transaction)

    def make_merkle(self, block_transactions):
        # TODO
        return