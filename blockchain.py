import functools
import hashlib  # For hashing
import json
import pickle  # binary JSON alternative
# from collections import OrderedDict  # to sort dictionaries

from hash_utils import hash_block
from block import Block
from transaction import Transaction
from verification import Verification

MINING_REWARD = 10
blockchain = []
open_transactions = []
owner = 'Chris'
# owner = set(['Chris'])
# we can define a set with {} like dictionaries without assigning key pairs. Python will know it's a set
# sets don't allow duplicates. If a duplicate is added it just will be ignored, it doesn't throw an error


def load_data():
    global blockchain
    global open_transactions

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
        with open('blockchain.txt', mode='r') as f:
            text_content = f.readlines()
            # Loading blockchain
            # Range selector -1 to remove the line break
            blockchain = json.loads(text_content[0][:-1])
            # We need to alter the transaction in the block to add the ordereddic structure
            updated_blockchain = []
            for block in blockchain:
                converted_tx = [Transaction(
                    tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]

                updated_block = Block(
                    block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])

                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            # Loading transactions
            open_transactions = json.loads(text_content[1])
            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = Transaction(
                    tx['sender'], tx['recipient'], tx['amount'])
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions
    except (IOError, IndexError):
        print('File not found')
        # Initialise Genesis block if blockchain doesn't exist
        genesis_block = Block(0, '', [], 100, 0)
        blockchain = [genesis_block]
        open_transactions = []

    # except ValueError:
    #     print('Value Error!')
    # finally: #Always executes, if try succeed or Except errors handles. Used to cleanup
    #     print('Cleanup!')


def save_data():
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
        with open('blockchain.txt', mode='w') as f:
            # Convert block objects to dictionary. JSON doesn't know Python objects
            saveable_chain = [block.__dict__ for block in
                                   [Block(block_el.index, block_el.previous_hash,
                                          [tx.__dict__ for tx in block_el.transactions],
                                          block_el.proof, block_el.timestamp)
                                    for block_el in blockchain]]
            f.write(json.dumps(saveable_chain))
            f.write('\n')
            saveable_tx = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(saveable_tx))
    except IOError:
        print("Couldn't save data!")


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None

    return blockchain[-1]


def get_transaction_values():
    tx_recipient = input('Please enter the receipient of the transaction: ')
    tx_amount = float(input('Please enter the amount to be sent: '))
    # Returns a tuple
    return (tx_recipient, tx_amount)


def proof_of_work(transactions):
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    verifier = Verification()
    while not verifier.valid_proof(transactions, last_hash, proof):
        proof += 1
    print(f"The proof number is: {proof}")
    return proof


def get_balance(participant):
    # Sent amounts in Blockchain
    tx_sender = [[tx.amount for tx in block.transactions  # block['transactions']
                  if tx.sender == participant] for block in blockchain]
    # Sent amounts in open Transactions
    open_tx_sender = [tx.amount
                      for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)

    tx_recipient = [[tx.amount for tx in block.transactions  # ['transactions']
                     if tx.recipient == participant] for block in blockchain]

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


def add_transaction(recipient, sender=owner, amount=1.0):
    """Adds transactions to the open_transactions dictionary
    Arguments:
        :sender: the sender of the transaction
        :recipient: the receiver of the transactio
        :amount: the value of the transaction (default 1.0)
    """

    # As the order of Dictionaries can change we need to work with imported Ordereddics package
    # The order is important to us for the SHA256 hash algorithm
    # It's defined as a list of tuples
    # transaction = OrderedDict(
    #     [('sender', sender), ('recipient', recipient), ('amount', amount)])

    transaction = Transaction(sender, recipient, amount)
    verifier = Verification()
    if verifier.verify_transaction(transaction, get_balance):
        open_transactions.append(transaction)
        save_data()
        return True
    else:
        return False


def mine_block():
    # index [-1] accesses the last block of the chain
    last_block = blockchain[-1]

    hashed_block = hash_block(last_block)
    # We copy the list open_transaction with the ':' range selector to copy the whole list
    # In complex objects like lists,tuples,sets,dictionary just assigning a new value
    # with '=' just copies the reference. So if we change the copied list it will also be changed in the original
    copied_open_transactions = open_transactions[:]

    # We calculate the proof number without the mining reward.
    # To validate the chain we need to remove the reward_transaction before validating it
    proof = proof_of_work(copied_open_transactions)

    reward_transaction = Transaction('MINING', owner, MINING_REWARD)

    copied_open_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block,
                  copied_open_transactions, proof)
    blockchain.append(block)
    return True


def user_choice():
    return input("Your choice: ")


def display_choices():
    print("Please choose")
    print("1: Enter new transaction")
    print("2: Output blocks")
    print("3: Mine block")
    print("4: Show Balance of participant")
    print("5: Check transactions validity")
    print("v: Verify blockchain")
    print("x: Exit")


def press_enter_to_continue():
    input("---- Press ENTER to continue ----")


def print_blockchain_elements():
    if len(blockchain) < 1:
        print("This blockchain is empty!")
    else:
        for block in blockchain:
            print("Outputting block")
            print(block)
        else:
            print("-" * 30)



# Loading the blockchain and open transactions
load_data()

# Displaying user interface
print('Welcome {}! Your current balance is: {} coins'.format(owner, get_balance(owner)))
waiting_for_input = True
while waiting_for_input:
    display_choices()
    selected_choice = user_choice()

    if selected_choice == '1':
        tx_data = get_transaction_values()
        # unpacking the returned tuple
        recipient, amount = tx_data
        # if add_transaction(recipient, amount=amount):
        if add_transaction(recipient, amount=amount):
            print('Transaction completed succesfully!')
        else:
            print("Insufficient funds for this transaction!")

        press_enter_to_continue()

    elif selected_choice == '2':
        print_blockchain_elements()
        press_enter_to_continue()

    elif selected_choice == '3':
        if mine_block():
            open_transactions = []
            save_data()
            print("Block mined succesfully!")
        else:
            print("Error mining block! Try again")
        press_enter_to_continue()

    elif selected_choice == '4':
        participant = input("Enter name for balance: ")
        print("The balance of {} is: {:6.2f} coins".format(
            participant, get_balance(participant)))
        print("-" * 30)
        press_enter_to_continue()

    elif selected_choice == '5':
        verifier = Verification()
        if verifier.verify_transactions(open_transactions, get_balance):
            print("All transactions are valid!")
        else:
            print("Some transactions are not valid!")

    elif selected_choice == 'v':
        verifier = Verification()
        print_blockchain_elements()
        print("Chain Valid: " + str(verifier.verify_chain(blockchain)))
        press_enter_to_continue()

    elif selected_choice == 'x':
        waiting_for_input = False

    else:
        print("Invalid choice! Try again")

    verifier = Verification()
    if not verifier.verify_chain(blockchain):
        print_blockchain_elements()
        print("Invalid blockchain!!")
        press_enter_to_continue()
        break
    # Formats 6 empty spaces before the balance with 2 decimal floats
    print("{} your actual balance is: {:6.2f} coins".format(
        owner, get_balance(owner)))
else:
    print("User has quitted!")

print("Done!")
