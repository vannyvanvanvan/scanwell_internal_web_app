import hashlib as hash

def hash_string(input_string):
    byte_array = input_string.encode('utf-8')
    return hash.sha3_256(byte_array).hexdigest()
