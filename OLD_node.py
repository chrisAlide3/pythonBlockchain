# Package to generate unique ID's
from uuid import uuid4

from blockchain import Blockchain
from utility.verification import Verification
from wallet import Wallet

class Node(Blockchain):

    def __init__(self):
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)


    def listen_for_input(self):
        # Displaying user interface
        if self.wallet.public_key == None:
            print("No wallet detected! Please create or load the wallet!")
        else:
            print('Welcome {}! Your current balance is: {:6.2f} coins'.format(self.wallet.public_key, self.blockchain.get_balance(self.wallet.public_key)))
        
        waiting_for_input = True
        while waiting_for_input:
            print("Please choose")
            print("1: Enter new transaction")
            print("2: Mine block")
            print("3: Output blocks")
            print("4: Show Balance of participant")
            print("5: Check transactions validity")
            print("6: Create wallet")
            print("7: Load wallet")
            print("8: Save keys")
            print("v: Verify blockchain")
            print("x: Exit")

            selected_choice = self.user_choice()

            if selected_choice == '1':
                tx_data = self.get_transaction_values()
                # unpacking the returned tuple
                recipient, amount = tx_data
                # if add_transaction(recipient, amount=amount):
                signature = self.wallet.sign_transaction(self.wallet.public_key, recipient, amount)
                if self.blockchain.add_transaction(recipient, self.wallet.public_key, signature, amount):
                    print('Transaction completed succesfully!')
                else:
                    print("Insufficient funds or no wallet for this transaction!")

                self.press_enter_to_continue()

            elif selected_choice == '2':
                if self.blockchain.mine_block():
                    print("Block mined succesfully!")
                else:
                    print("Error mining block! No wallet?")
                self.press_enter_to_continue()

            elif selected_choice == '3':
                self.print_blockchain_elements()
                self.press_enter_to_continue()

            elif selected_choice == '4':
                participant = input("Enter name for balance: ")
                print("The balance of {} is: {:6.2f} coins".format(
                    participant, self.blockchain.get_balance(participant)))
                print("-" * 30)
                self.press_enter_to_continue()

            elif selected_choice == '5':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print("All transactions are valid!")
                else:
                    print("Some transactions are not valid!")

            elif selected_choice == '6':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)

            elif selected_choice == '7':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)

            elif selected_choice == '8':
                self.wallet.save_keys()

            elif selected_choice == 'v':
                self.print_blockchain_elements()
                print("Chain Valid: " + str(Verification.verify_chain(self.blockchain.chain))) #blockchain.chain will trigger the getter function in the blockchain class
                self.press_enter_to_continue()

            elif selected_choice == 'x':
                waiting_for_input = False

            else:
                print("Invalid choice! Try again")

            if not Verification.verify_chain(self.blockchain.chain): #blockchain.chain will trigger the getter function in the blockchain class
                self.print_blockchain_elements()
                print("Invalid blockchain!!")
                self.press_enter_to_continue()
                break
            # Formats 6 empty spaces before the balance with 2 decimal floats
            print("{} your actual balance is: {:6.2f} coins".format(
                self.wallet.public_key, self.blockchain.get_balance(self.wallet.public_key)))
        else:
            print("User has quitted!")

        print("Done!")


    def user_choice(self):
        return input("Your choice: ")

    
    def press_enter_to_continue(self):
        input("---- Press ENTER to continue ----")


    def print_blockchain_elements(self):
        for block in self.blockchain.chain: #blockchain.chain will trigger the getter function in the blockchain class
            print("Outputting block")
            print(block)
        else:
            print("-" * 30)

    def get_transaction_values(self):
        tx_recipient = input('Please enter the receipient of the transaction: ')
        tx_amount = float(input('Please enter the amount to be sent: '))
        # Returns a tuple
        return (tx_recipient, tx_amount)


# Only run the app when it is called directly. Avoids the code to run if imported into other Python apps
if __name__ == '__main__':
    # We instanciate the new node from the Node class
    # Then run the function 'listen_for_input
    node = Node()
    node.listen_for_input()
