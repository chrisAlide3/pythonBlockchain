# JSONIFY helper to convert responses to JSON
# REQUEST helper to manage JSON arguments
# SEND_FROM_DIRECTORY allows to display an HTML page (Arguments: directory, file_name)
from flask import Flask, jsonify, request, send_from_directory
#flask-cors allows clients from other servers to access this server
from flask_cors import CORS 

from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
# enables other clients to access our app
CORS(app)

@app.route('/', methods=['GET'])
def get_node_ui():
    return send_from_directory('ui', 'node.html')

@app.route('/network', methods=['GET'])
def get_network_ui():
    return send_from_directory('ui', 'network.html')


@app.route('/wallet', methods=['POST'])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port) #node_id for developpment only. Remove for production
        response = {
            'message': 'Wallet created and saved!',
            'private_key': wallet.private_key,
            'public_key': wallet.public_key,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Error saving wallet!'
        }
        return jsonify(response), 500


@app.route('/wallet', methods=['GET'])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port) #node_id for developpment only. Remove for production
        response = {
            'message': 'Wallet loaded',
            'private_key': wallet.private_key,
            'public_key': wallet.public_key,
            'funds': blockchain.get_balance()
        }

        return jsonify(response), 201
    else:
        response = {
            'message': 'Error loading wallet'
        }
        return jsonify(response), 500


@app.route('/balance', methods=['GET'])
def get_balance():
    balance = blockchain.get_balance()
    if balance == None:
        response = {
            'message': 'No balance to show. Please load a wallet' 
        }
        return jsonify(response), 401
    else:
        response = {
            'public_key': wallet.public_key,
            'funds': balance
        }
        return jsonify(response), 201

@app.route('/mine', methods=['POST'])
def mine_block():
    block = blockchain.mine_block()
    if block != None:
        #converting block to dictionary
        dict_block = block.__dict__.copy()
        #converting transactions in block to dictionary
        dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]

        response = {
            'message': 'Block mined succesfully!',
            'block': dict_block,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Mining block failed!',
            'wallet_setup': wallet.public_key != None,
        }
        return jsonify(response), 500


@app.route('/transaction', methods=['POST'])
def add_transaction():
    #Send error and abort if no wallet loaded
    if wallet.public_key == None:
        response = {
            'message': 'No wallet loaded!'
        }
        return jsonify(response), 400

    values = request.get_json()
    #Error if no arguments submitted
    if not values:
        response = {
            'message': 'No data submitted'
        }
        return jsonify(response), 400
    #Error if expected fields are not submitted
    required_fields = ['recipient', 'amount']
    if not all(field in values for field in required_fields):
        response = {
            'message': 'Some expected data are missing'
        }
        return jsonify(response), 400

    recipient = values['recipient']
    amount = values['amount']
    signature = wallet.sign_transaction(wallet.public_key, recipient, amount)
    tx = blockchain.add_transaction(recipient, wallet.public_key, signature, amount)
    if tx != None:
        tx = tx.__dict__
        response = {
            'message': 'Transaction added successfully',
            'transaction': tx,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Error adding transaction'
        }
        return jsonify(response), 500


@app.route('/broadcast-transaction', methods=['POST'])
def broadcast_transaction():
    values = request.get_json()
    if not values:
        response = {
            'message': 'No values found!'
        }
        return jsonify(response), 400

    required_fields = ['sender', 'recipient', 'amount', 'signature']
    if not all(key in values for key in required_fields):
        response = {
            'message': 'Missing attributes!'
        }
        return jsonify(response), 400
    else:
        tx = blockchain.add_transaction(values['recipient'], values['sender'], values['signature'], values['amount'], is_receiving=True)
        if tx != None:
                tx = tx.__dict__
                response = {
                    'message': 'Transaction added successfully',
                    'transaction': tx,
                }
                return jsonify(response), 201
        else:
            response = {
                'message': 'Error adding transaction'
            }
            return jsonify(response), 500


@app.route('/broadcast-block', methods=['POST'])
def broadcast_block():
    values = request.get_json()
    if not values:
        response = {
            'message': 'No values found!'
        }
        return jsonify(response), 400

    if 'block' not in values:
        response = {
            'message': 'No block found!'
        }
        return jsonify(response), 400
    else:
        block = values['block']
        # check if received block is the next block in our local blockchain
        if block['index'] == blockchain.chain[-1].index + 1:
            if blockchain.add_block(block):
                response = {
                    'message': 'Block added to blockchain'
                }
                return jsonify(response), 201
            else:
                response = {
                    'message': 'Block not added'
                }
                return jsonify(response), 400

        # handling if block higher than last block + 1
        elif block['index'] > blockchain.chain[-1]:
            pass
        # handling when block is lower in the chain than our chain
        else:
            response = {
                'message': 'Blockchain seems to be shorter. Block not added'
            }
            return jsonify(response), 409 #sended data invalid



@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = blockchain.chain
    #converting block object to dictionary for JSON
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    #converting transaction object to dictionary for each block for JSON
    for dict_block in dict_chain:
        dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]

    return jsonify(dict_chain), 200


@app.route('/transactions', methods=['GET'])
def get_open_transactions():
    open_transactions = blockchain.get_open_transactions()
    dict_transactions = [tx.__dict__ for tx in open_transactions]
    return jsonify(dict_transactions), 201


@app.route('/node', methods=['POST'])
def add_node():
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data attached'
        }
        return jsonify(response), 400

    if 'node' not in values:
        response = {
            'message': 'Expected node is empty'
        }
        return jsonify(response), 400
    else:
        blockchain.add_peer_node(values['node'])
        response = {
            'message': 'Node added to peer',
            'peer_nodes': blockchain.get_peer_nodes()
        }
        return jsonify(response), 201


#we pass the argument in the path with <attribute_name>
#than take it as argument in the function itself
@app.route('/node/<node_url>', methods=['DELETE'])
def remove_node(node_url):
    if node_url == None or node_url == '':
        response = {
            'message': 'Expected node is empty'
        }
        return jsonify(response), 400
    else:
        blockchain.remove_peer_node(node_url)
        response = {
            'message': 'Node removed from peer',
            'peer_nodes': blockchain.get_peer_nodes()
        }
        return jsonify(response), 201


@app.route('/nodes', methods=['GET'])
def get_nodes():
    nodes = blockchain.get_peer_nodes()
    response = {
        'message': 'Nodes loaded',
        'nodes': nodes
    }
    return jsonify(response), 200


if __name__ == '__main__':
    #For Developpment. To be removed in production
    #We can pass the port argument when calling the application
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5000)
    args = parser.parse_args()
    port = args.port

    wallet = Wallet(port)
    blockchain = Blockchain(wallet.public_key, port)

    app.run(host='0.0.0.0', port=port)


