import hashlib  # For hashing
import json

def hash_string_256(string):
    # the Hexdigest function at the end returns a hex value to sha256
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
    # json.dumps stringifies the block dictionary in json format
    # We need to add sort_keys=True to make sure the dictionary is always in the same order
        # encode just encodes it as UTF-8

    #We need to convert the block object to dictionary. JSON doesn't support Python Object type
    hashable_block = block.__dict__.copy()
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())

    # Example creating a string from lists using JOIN. The symbol in front is the delimiter to use
    # return '-'.join([str(block[key]) for key in block])

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

