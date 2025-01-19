import random
from mnemonic import Mnemonic



class Wallet:
    # generate wallet seed phrase and derive private key
    def keygen(self, passphrase =""):
        mnemo = Mnemonic("english")
        self.words = mnemo.generate(strength=256)

        self.seed = mnemo.to_seed(self.words, passphrase)
        entropy = mnemo.to_entropy(self.words)
        
        return
    
my_wallet = Wallet()

my_wallet.keygen()

print(my_wallet.words)
