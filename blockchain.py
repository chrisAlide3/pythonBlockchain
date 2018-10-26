MINING_REWARD = 10

genesis_block = {'previous_hash': '',
                 'index': 0,
                 'transactions': []}
blockchain = [genesis_block]
open_transactions = []
owner = 'Chris'
# participant = set(['Chris'])
# we can define a set with {} like dictionaries without assigning key pairs. Python will know it's a set
# sets don't allow duplicates. If a duplicate is added it just will be ignored, it doesn't throw an error
participants = {'Chris'}


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None

    return blockchain[-1]


def get_transaction_values():
    tx_recipient = input('Please enter the receipient of the transaction: ')
    tx_amount = float(input('Please enter the amount to be sent: '))
    # Returns a tuple
    return (tx_recipient, tx_amount)

def verify_transaction(transaction):
    balance = get_balance(transaction['sender'])
    if balance < transaction['amount']:
        return False, transaction['amount'], balance
    else:
        return True, transaction['amount'], balance

def add_transaction(recipient, sender=owner, amount=1.0):
    """Adds transactions to the open_transactions dictionary
    Arguments:
        :sender: the sender of the transaction
        :recipient: the receiver of the transactio
        :amount: the value of the transaction (default 1.0)
    """
    transaction = {'sender': sender, 'recipient': recipient, 'amount': amount}
    
    success, tx_amount, balance = verify_transaction(transaction)
    if success:
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True, tx_amount, balance
    else:
        return False, tx_amount, balance


def mine_block():
    # index [-1] accesses the last block of the chain
    last_block = blockchain[-1]

    hashed_block = hash_block(last_block)

    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }

    open_transactions.append(reward_transaction)

    block = {'previous_hash': hashed_block,
             'index': len(blockchain),
             'transactions': open_transactions}

    blockchain.append(block)
    return True


def user_choice():
    return input("Your choice: ")


def display_choices():
    print("Please choose")
    print("1: Enter new transaction")
    print("2: Output blocks")
    print("3: Mine block")
    print("4: Show participants of the network")
    print("5: Show Balance of participant")
    print("h: Manipulate the chain")
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


def get_balance(participant):
    sent_amount = 0
    # Sent amounts in Blockchain
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    # Sent amounts in open Transactions
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    for tx in tx_sender:
        if len(tx) > 0:
            idx = 0
            while idx < len(tx):
                sent_amount += tx[idx]
                idx += 1

    received_amount = 0
    # Received amounts in Blockchain
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    for tx in tx_recipient:
        if len(tx) > 0:
            idx = 0
            while idx < len(tx):
                received_amount += tx[idx]
                idx += 1

    return received_amount - sent_amount

    # balance = 0
    # for block_idx in range(len(blockchain)):
    #     for tx_idx in range(len(blockchain[block_idx]['transactions'])):
    #         if blockchain[block_idx]['transactions'][tx_idx]['sender'] == participant:
    #             balance = balance - blockchain[block_idx]['transactions'][tx_idx]['amount']
    #         if blockchain[block_idx]['transactions'][tx_idx]['recipient'] == participant:
    #             balance = balance + blockchain[block_idx]['transactions'][tx_idx]['amount']
    # return balance


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])

    # Example using comprehesion lists
    # THIS RETURNS a LIST: hashed_block = str([last_block[key] for key in last_block])
    # To return a string with separation use the join method
    # hashed_block = '-'.join([str(last_block[key]) for key in last_block])

    ## Example using normal For loop ##
    # hashed_block = ''
    # for key in last_block:
    #     value = last_block[key]
    #     hashed_block = hashed_block + str(value)
    # # The block is defined as a dictionary
    # print(hashed_block)


def verify_chain():
    # With enumerate we change the list to a Tuple so we can unpack it with idx-value pairs
    for (index, block) in enumerate(blockchain):
        if index < 1:
            continue
        if block['previous_hash'] != hash_block(blockchain[index-1]):
            return False
    return True

    ### Example with normal for loop ################
    # is_valid = True

    # for el_idx in range(len(blockchain)):
    #     if el_idx < 1:
    #         continue
    #     else:
    #         previous_block = blockchain[el_idx-1]
    #         hash_previous_block = hash_block(previous_block)
    #         if blockchain[el_idx]['previous_hash'] == hash_previous_block:
    #             is_valid = True
    #         else:
    #             is_valid = False
    #             break
    # return is_valid


waiting_for_input = True
while waiting_for_input:
    display_choices()
    selected_choice = user_choice()

    if selected_choice == '1':
        tx_data = get_transaction_values()
        # unpacking the returned tuple
        recipient, amount = tx_data
        # if add_transaction(recipient, amount=amount):
        success, tx_transaction, balance = add_transaction(recipient, amount=amount)
        if success:
            print('Transaction completed succesfully!')
        else:
            print("Your balance of " + str(balance) + " is to low for this transaction of " + str(tx_transaction) + " coins!")

        press_enter_to_continue()

    elif selected_choice == '2':
        print_blockchain_elements()
        press_enter_to_continue()

    elif selected_choice == '3':
        if mine_block():
            open_transactions = []
            print("Block mined succesfully!")
        else:
            print("Error mining block! Try again")
        press_enter_to_continue()

    elif selected_choice == '4':
        print(participants)
        press_enter_to_continue()

    elif selected_choice == '5':
        participant = input("Enter name for balance: ")
        print(participant + " your balance is: ")
        print(get_balance(participant))
        print("-" * 30)
        press_enter_to_continue()

    elif selected_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {'previous_hash': '',
                             'index': 0,
                             'transactions': [{'sender': 'Marc', 'recipient': 'Chris', 'amount': 100.0}]}

    elif selected_choice == 'v':
        print_blockchain_elements()
        print("Chain Valid: " + str(verify_chain()))
        press_enter_to_continue()

    elif selected_choice == 'x':
        waiting_for_input = False

    else:
        print("Invalid choice! Try again")

    if not verify_chain():
        print_blockchain_elements()
        print("Invalid blockchain!!")
        press_enter_to_continue()
        break
else:
    print("User has quitted!")

print("Done!")
