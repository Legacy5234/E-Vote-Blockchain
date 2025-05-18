import time
import json
import hashlib

class Blockchain:
    difficulty = 4  # Number of leading zeros required for valid hash

    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = {
            'index': 0,
            'timestamp': time.time(),
            'votes': [],
            'previous_hash': '0',
            'nonce': 0
        }
        genesis_block['hash'] = self.compute_hash(genesis_block)
        self.chain.append(genesis_block)

    def compute_hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, block):
        block['nonce'] = 0
        computed_hash = self.compute_hash(block)
        while not computed_hash.startswith('0' * self.difficulty):
            block['nonce'] += 1
            computed_hash = self.compute_hash(block)
        return computed_hash

    def add_block(self, votes):
        previous_block = self.chain[-1]
        new_block = {
            'index': previous_block['index'] + 1,
            'timestamp': time.time(),
            'votes': votes,
            'previous_hash': previous_block['hash'],
            'nonce': 0
        }
        new_block['hash'] = self.proof_of_work(new_block)
        self.chain.append(new_block)
