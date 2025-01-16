class Transactions():
    def __init__(self,):
        self.transaction_pool = []
        self.block_transactions = []

    def new_transaction(self, transaction):
        self.transaction_pool.append(transaction)

    def make_merkle(self, block_transactions):
        return