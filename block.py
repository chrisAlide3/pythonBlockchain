from time import time

#Importing Printable class, then pass it to Block class for inheritence
from printable import Printable

class Block(Printable):
    def __init__(self, index, previous_hash, transactions, proof, time=time()):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.proof = proof
        self.timestamp = time
