import functools
import hashlib  # For hashing
import json
import pickle  # binary JSON alternative

#External packages
## Python equivalent to axios in the front end app
import requests

# from utility is a folder. with the empty file __init__.py all the other files are bundled. 
# so we can import 'from folderName.fileName import className or functionName
from utility.hash_utils import hash_block
from utility.verification import Verification

from block import Block
from transaction import Transaction
from wallet import Wallet

MINING_REWARD = 10
# owner = set(['Chris'])
# we can define a set with {} like dictionaries without assigning key pairs. Python will know it's a set
# sets don't allow duplicates. If a duplicate is added it just will be ignored, it doesn't throw an error

# Will be passed from the node owner = 'Chris'

class Blockchain:
    def __init__(self, public_key, node_id): #node_id for developpment only. Remove for production
        # Our starting block
        genesis_block = Block(0, '', [], 100, 0)
        #Initialize our blockchain list
        self.chain = [genesis_block]
        # Note '__' double underscore in attribute name define them as private, they cannot be changed from outside this class
        self.__open_transactions = []
        #Initialising peer_node as empty set. A set doesn't keep duplicate values, but doesn't throw error. It just doesn't add the duplicate
        self.__peer_nodes = set()
        self.public_key = public_key
        self.node_id = node_id #node_id for developpment only. Remove for production
        self.resolve_conflicts = False
        self.load_data()


    @property #defines a getter for this attribute
    # The method name has to be the name of the attribute we want to make the getter. 
    # Python will automatically make it private. So in the getter function we need to refer it with '__' double underscore
    # From outside the getter function we can acces it with the normal attribute name
    def chain(self):
        return self.__chain[:]

    @chain.setter #defines setter method for this attribute. the name before the .setter has to be the attribute name
    # The method name has to be the name of the attribute we want to make the setter. 
    # Python will automatically make it private. So in the setter function we need to refer it with '__' double underscore
    # From outside the getter function we can acces it with the normal attribute name
    # The 2 arguments self and val are passed automatically by python
    def chain(self, val):
        self.__chain = val

    # Not needed anymore. We handle it with the getter function above
    # def get_chain(self):
    #     ## Note, with the range selector all [:] we return a copy of the chain, not the chain itself
    #     return self.__chain[:]


    def get_open_transactions(self):
        ## Note, with the range selector all [:] we return a copy of the open_transactions, not the transactions themselves
        return self.__open_transactions[:]


    def load_data(self):
        # Runtime Error handling with 'try' and 'except'
        try:
            # Load from PICKLE
            # Better implementation of special datatypes (eg. Ordered dicts)
            # Cannot display the file in readable form
            # Switch to JSON for this course so we can read the file
            # with open('blockchain.p', mode='rb') as f:
            #     global blockchain
            #     global open_transactions
            #     file_content = pickle.loads(f.read())
            #     blockchain = file_content['chain']
            #     open_transactions = file_content['otx']

            # Load from JSON
            with open('blockchain-{}.txt'.format(self.node_id), mode='r') as f: #node_id for developpment only. Remove for production
                text_content = f.readlines()
                # Loading blockchain
                # Range selector -1 to remove the line break
                blockchain = json.loads(text_content[0][:-1])
                # We need to alter the transaction in the block to add the ordereddic structure
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(
                        tx['sender'], tx['recipient'], tx['amount'], tx['signature']) for tx in block['transactions']]

                    updated_block = Block(
                        block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])

                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain #will trigger the setter method defined for the chain attribute
                # Loading transactions
                open_transactions = json.loads(text_content[1][:-1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(
                        tx['sender'], tx['recipient'], tx['amount'], tx['signature'])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
                # Loading peer nodes
                peer_nodes = json.loads(text_content[2])
                self.__peer_nodes = set(peer_nodes)
        except (IOError, IndexError):
            print('File not found')
        # except ValueError:
        #     print('Value Error!')
        # finally: #Always executes, if try succeed or Except errors handles. Used to cleanup
        #     print('Cleanup!')


    def save_data(self):
        try:
            # Using PICKLE
            # In this course we switch to JSON for readble file (see load_data)
            # with open('blockchain.p', mode='wb') as f:
            #     #In binary we cannot make a line break.
            #     #So we create a dictionary holding the x lists to save
            #     save_data = {
            #         'chain': blockchain,
            #         'otx': open_transactions
            #     }
            #     f.write(pickle.dumps(save_data))

            # Using JSON
            with open('blockchain-{}.txt'.format(self.node_id), mode='w') as f: #node_id for developpment only. Remove for production
                # Convert block objects to dictionary. JSON doesn't know Python objects
                saveable_chain = [block.__dict__ for block in
                                    [Block(block_el.index, block_el.previous_hash,
                                            [tx.__dict__ for tx in block_el.transactions],
                                            block_el.proof, block_el.timestamp)
                                        for block_el in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
                f.write('\n')
                f.write(json.dumps(list(self.__peer_nodes)))
        except IOError:
            print("Couldn't save data!")


    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        print(f"The proof number is: {proof}")
        return proof


    def get_last_blockchain_value(self):
        if len(self.__chain) < 1:
            return None

        return self.__chain[-1]


    def get_balance(self, sender=None):
        if sender == None:
            if self.public_key == None:
                return None
            participant = self.public_key
        else:
            participant = sender
        # Sent amounts in Blockchain
        tx_sender = [[tx.amount for tx in block.transactions  # block['transactions']
                    if tx.sender == participant] for block in self.__chain]
        # Sent amounts in open Transactions
        open_tx_sender = [tx.amount
                        for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)

        tx_recipient = [[tx.amount for tx in block.transactions  # ['transactions']
                        if tx.recipient == participant] for block in self.__chain]

        # Calculating amount with use of reducer and lambda function
        # Reduce function has to be imported from functools.1st argument is a function, 2nd is the Listname
        # 3rd optional is the start value. It returns the old value + new value of operation
        # Lambda is a temporary function. The fields after lambda are the arguments followed by ':' Then the function itself
        sent_amount = functools.reduce(lambda tx_sum, tx_amount: tx_sum + sum(
            tx_amount) if len(tx_amount) > 0 else tx_sum + 0, tx_sender, 0)
        received_amount = functools.reduce(lambda tx_sum, tx_amount: tx_sum + sum(
            tx_amount) if len(tx_amount) > 0 else tx_sum + 0, tx_recipient, 0)

        return received_amount - sent_amount

        # Calculating amount with use of For loop
        # sent_amount = 0
        # for tx in tx_sender:
        #     if len(tx) > 0:
        #         idx = 0
        #         while idx < len(tx):
        #             sent_amount += tx[idx]
        #             idx += 1

        # received_amount = 0
        # # Received amounts in Blockchain
        # tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
        # for tx in tx_recipient:
        #     if len(tx) > 0:
        #         idx = 0
        #         while idx < len(tx):
        #             received_amount += tx[idx]
        #             idx += 1

        # Other way to calculate the balance (My first solution I come up)
        # balance = 0
        # for block_idx in range(len(blockchain)):
        #     for tx_idx in range(len(blockchain[block_idx]['transactions'])):
        #         if blockchain[block_idx]['transactions'][tx_idx]['sender'] == participant:
        #             balance = balance - blockchain[block_idx]['transactions'][tx_idx]['amount']
        #         if blockchain[block_idx]['transactions'][tx_idx]['recipient'] == participant:
        #             balance = balance + blockchain[block_idx]['transactions'][tx_idx]['amount']
        # return balance


    def add_transaction(self, recipient, sender, signature, amount=1.0, is_receiving=False):
        """Adds transactions to the open_transactions dictionary
        Arguments:
            :sender: the sender of the transaction
            :recipient: the receiver of the transaction
            :signature: the signature of the transaction 
            :amount: the value of the transaction (default 1.0)
        """

        # As the order of Dictionaries can change we need to work with imported Ordereddics package
        # The order is important to us for the SHA256 hash algorithm
        # It's defined as a list of tuples
        # transaction = OrderedDict(
        #     [('sender', sender), ('recipient', recipient), ('amount', amount)])

        # prevent adding transaction when no wallet loaded
        # if self.public_key == None:
        #     return None

        transaction = Transaction(sender, recipient, amount, signature)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            #Broadcast transaction to all peer nodes as long it is NOT a received broadcast
            if not is_receiving:
                for node in self.__peer_nodes:
                    url = 'http://{}/broadcast-transaction'.format(node)
                    try:
                        response = requests.post(url, json={'sender': sender, 'recipient': recipient, 'amount': amount, 'signature': signature})
                        if response.status_code == 400 or response.status_code == 500:
                            print('Transaction declined. Need resolving')
                            return False
                    # continue with next peer node if connection error (node not online)
                    except requests.exceptions.ConnectionError:
                        continue
                        

            return transaction
        else:
            return None


    def mine_block(self):
        # prevent adding transaction when no wallet loaded
        if self.public_key == None:
            return None

        # index [-1] accesses the last block of the chain
        last_block = self.__chain[-1]

        hashed_block = hash_block(last_block)
        # We copy the list open_transaction with the ':' range selector to copy the whole list
        # In complex objects like lists,tuples,sets,dictionary just assigning a new value
        # with '=' just copies the reference. So if we change the copied list it will also be changed in the original
        copied_open_transactions = self.__open_transactions[:]

        # We calculate the proof number without the mining reward.
        # To validate the chain we need to remove the reward_transaction before validating it
        proof = self.proof_of_work()

        #verify each open_transactions signatures. if one signature doesn't verify correctly we abort the mining
        #this is done without the MINING transaction
        for tx in copied_open_transactions:
            if not Wallet.verify_transaction_signature(tx):
                return None

        reward_transaction = Transaction('MINING', self.public_key, MINING_REWARD, '')
        copied_open_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block,
                    copied_open_transactions, proof)
        
        self.__chain.append(block)
        
        #Empty open transaction files and save the datas
        self.__open_transactions = []
        self.save_data()
        #Broadcasting new block
        for node in self.__peer_nodes:
            url = 'http://{}/broadcast-block'.format(node)
            converted_block = block.__dict__.copy()
            converted_block['transactions'] = [tx.__dict__ for tx in converted_block['transactions']]
            try:
                response = requests.post(url, json={'block': converted_block})
                if response.status_code == 400 or response.status_code == 500:
                    print('Block declined!')
                # when broadcasting block to peers returns a 409 message then set reolve_conflicts. see node.py broadcast_block
                if response.status_code == 409:
                    self.resolve_conflicts = True

            except requests.exceptions.ConnectionError:
                continue

        
        return block


    def add_block(self, block):
        # converting the received dictionary transactions to transaction objects
        transactions = [Transaction(tx['sender'], tx['recipient'], tx['amount'], tx['signature']) for tx in block['transactions']]
        proof_is_valid = Verification.valid_proof(transactions[:-1], block['previous_hash'], block['proof'])
        hashes_match = hash_block(self.chain[-1]) == block['previous_hash']
        if not proof_is_valid or not hashes_match:
            return False

        converted_block = Block(block['index'], block['previous_hash'], transactions, block['proof'], block['timestamp'])
        self.__chain.append(converted_block)
        #Removing transaction from open_transaction if they are in the mined block
        stored_transactions = self.__open_transactions[:]
        for itx in block['transactions']:
            for opentx in stored_transactions:
                if opentx.sender == itx['sender'] and opentx.recipient == itx['recipient'] and opentx.amount == itx['amount'] and opentx.signature == itx['signature']:
                    try:
                        self.__open_transactions.remove(opentx)
                    except ValueError:
                        print('Item was alredy removed')
        
        self.save_data()
        return True


    def resolve(self):
        winner_chain = self.chain
        replace = False
        for node in self.__peer_nodes:
            url = 'http://{}/chain'.format(node)
            try:
                response = requests.get(url)
                node_chain = response.json()
                # node_chain.transactions = [Transaction(tx['sender'], tx['recipient'], tx['amount'], tx['signature']) for tx in node_chain.transactions]
                node_chain = [Block(block['index'], block['previous_hash'], [Transaction(tx['sender'], tx['recipient'], tx['amount'], tx['signature']) for tx in block['transactions']], block['proof'], block['timestamp']) for block in node_chain]
                if len(node_chain) > len(winner_chain) and Verification.verify_chain(node_chain):
                    replace = True
                    winner_chain = node_chain
            except requests.exceptions.ConnectionError:
                continue
        self.chain = winner_chain
        self.resolve_conflicts = False
        if replace:
            self.__open_transactions = []
        self.save_data()
        return replace

    def add_peer_node(self, node):
        """Adds new node to the peer_node_set
            Arguments:
                :node: the URL of the node that should be added
        """
        self.__peer_nodes.add(node)
        self.save_data()


    def remove_peer_node(self, node):
            """removes node from the peer_node_set
                Arguments:
                    :node: the URL of the node that should be removed
            """
            self.__peer_nodes.discard(node)
            self.save_data()


    def get_peer_nodes(self):
        #returns a copy of the peer_nodes
        return list(self.__peer_nodes)