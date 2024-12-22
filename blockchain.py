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
