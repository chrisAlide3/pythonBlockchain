blockchain = []


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None

    return blockchain[-1]


def enter_amount():
    return float(input('Enter the amount to be tranfered: '))


def add_transaction(transaction_value, last_transaction=[1.0]):
    """Adds a new value to the blockchain
    Arguments:
        :transaction_value: the amount to be added
        :last_transaction: the last blockchain value
    """
    if last_transaction == None:
        last_transaction = [1]

    blockchain.append([last_transaction, transaction_value])


def user_choice():
    return input("Your choice: ")


def display_choices():
    print("Please choose")
    print("1: Enter new transaction")
    print("2: Output blocks")
    print("h: Manipulate the chain")
    print("v: Verify blockchain")
    print("x: Exit")


def print_blockchain_elements():
    if len(blockchain) < 1:
        print("This blockchain is empty!")
    else:
        for block in blockchain:
            print("Outputting block")
            print(block)
        else:
            print("-" * 30)


def verify_chain():
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break

    # block_index = 0
    # is_valid = True
    # for block in blockchain:
    #     if block_index == 0:
    #         block_index += 1
    #         continue
    #     elif block[0] == blockchain[block_index - 1]:
    #         is_valid = True
    #     else:
    #         is_valid = False
    #         break
    #     block_index += 1

    return is_valid


waiting_for_input = True
while waiting_for_input:
    display_choices()
    selected_choice = user_choice()
    if selected_choice == '1':
        add_transaction(enter_amount(), get_last_blockchain_value())

    elif selected_choice == '2':
        print_blockchain_elements()

    elif selected_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]

    elif selected_choice == 'v':
        print("Chain Valid: " + str(verify_chain()))
        print_blockchain_elements()

    elif selected_choice == 'x':
        waiting_for_input = False

    else:
        print("Invalid choice! Try again")

    if not verify_chain():
        print("Invalid blockchain!!")
        print_blockchain_elements()
        break
else:
    print("User has quitted!")

print("Done!")
