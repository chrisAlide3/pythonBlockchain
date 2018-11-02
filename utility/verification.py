"""Provides verification helper methods"""

from utility.hash_utils import hash_string_256, hash_block
from wallet import Wallet

class Verification:
    # staticmethod is used for functions who don't need to access any other attribute or method in the same class
    # !! Note the first argument 'self' HAS to be ommited !!
    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        guess = (str([tx.to_ordered_dict() for tx in transactions]) +
                str(last_hash + str(proof))).encode()
        guess_hash = hash_string_256(guess)
        # Returns true or false! not the guess_hash!!
        return guess_hash[0:2] == '00'


    # classmethod is used for funtions who don't need access to any attributes in the class
    # but need access to other methods in that class
    # !! The 'self' argument has to be replaced with 'cls' argument
    @classmethod
    def verify_chain(cls, blockchain):
        # With enumerate we change the list to a Tuple so we can unpack it with idx-value pairs
        for (index, block) in enumerate(blockchain):
            if index < 1:
                continue
            if block.previous_hash != hash_block(blockchain[index-1]):
                print("Previous hash is invalid!")
                return False
            # We remove the last transaction with the range operator [:-1]. It's the mining reward
            # When we mine we don't include it in the proof of work
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print("Proof of work is invalid")
                return False
        return True


    @staticmethod
    def verify_transaction(transaction, get_balance, check_funds=True):
        if check_funds:
            balance_sender = get_balance()
            return balance_sender >= transaction.amount and Wallet.verify_transaction_signature(transaction)
        else:
            return Wallet.verify_transaction_signature(transaction)


    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        # The all keyword checks if returned list of ALL booleans are True
        # If its the case it returns True, if not it returns False
        # Here we verify each transactions from open_transactions and run the
        # verify_transaction function, which returns True or False
        return all([cls.verify_transaction(tx, get_balance, False) for tx in open_transactions])
