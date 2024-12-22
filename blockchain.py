import hashlib
import time


def hash(text):
    encoded_text = text.encode('utf-8')
    return hashlib.sha256(encoded_text).hexdigest()


class Block:
    def __init__(self, previous_hash, transactions):
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.transactions = transactions
        self.merkle_root = self.compute_merkle_root()
        self.hash = self.mine_block()

    def compute_merkle_root(self):

        if len(self.transactions) == 0:
            return hash("")

        hashes = [hash(tx) for tx in self.transactions]

        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1])

            new_hashes = []
            for i in range(0, len(hashes), 2):
                new_hashes.append(hash(hashes[i] + hashes[i + 1]))
            hashes = new_hashes

        return hashes[0]

    def mine_block(self):

        nonce = 0
        while True:
            block_hash = hash(self.previous_hash + str(self.timestamp) + self.merkle_root + str(nonce))
            if block_hash.startswith('0000'):  # Condition for valid hash
                return block_hash
            nonce += 1

class Blockchain: 
    def init(self): 
        self.chain = [] 
        self.create_genesis_block() 
 
    def create_genesis_block(self): 
        genesis_block = Block("0", ["Genesis Block"]) 
        self.chain.append(genesis_block) 
 
    def add_block(self, transactions): 
        previous_hash = self.chain[-1].hash 
        new_block = Block(previous_hash, transactions) 
        self.chain.append(new_block)


def validate_blockchain(blockchain): 
    for i in range(1, len(blockchain.chain)): 
        current = blockchain.chain[i] 
        previous = blockchain.chain[i - 1] 
 
        if current.previous_hash != previous.hash: 
            return False 
 
        if current.merkle_root != current.compute_merkle_root(): 
            return False 
 
        if not current.hash.startswith('0000'): 
            return False 
 
    return True 
 
def create_transaction(sender, receiver, amount): 
    return f"{sender} -> {receiver}: {amount}"


