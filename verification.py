from hash_utils import hash_string_256, hash_block

class Verification:

    def valid_proof(self, transactions, last_hash, proof):
        guess = (str([tx.to_ordered_dict() for tx in transactions]) +
                str(last_hash + str(proof))).encode()
        guess_hash = hash_string_256(guess)
        # Returns true or false! not the guess_hash!!
        return guess_hash[0:2] == '00'


    def verify_chain(self, blockchain):
        # With enumerate we change the list to a Tuple so we can unpack it with idx-value pairs
        for (index, block) in enumerate(blockchain):
            if index < 1:
                continue
            if block.previous_hash != hash_block(blockchain[index-1]):
                print("Previous hash is invalid!")
                return False
            # We remove the last transaction with the range operator [:-1]. It's the mining reward
            # When we mine we don't include it in the proof of work
            if not self.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print("Proof of work is invalid")
                return False
        return True


    def verify_transaction(self, transaction, get_balance):
        balance = get_balance(transaction.sender)
        if balance < transaction.amount:
            return False
        else:
            return True


    def verify_transactions(self, open_transactions, get_balance):
        # The all keyword checks if returned list of ALL booleans are True
        # If its the case it returns True, if not it returns False
        # Here we verify each transactions from open_transactions and run the
        # verify_transaction function, which returns True or False
        return all([self.verify_transaction(tx, get_balance) for tx in open_transactions])


