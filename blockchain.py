import hashlib
import time
import json

TOTAL_SUPPLY = 550_889_899_559_000
GENESIS_ADDRESS = 'genesis_wallet'

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'nonce': self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.balances = {GENESIS_ADDRESS: TOTAL_SUPPLY}

    def create_genesis_block(self):
        genesis_transaction = {
            'from': None,
            'to': GENESIS_ADDRESS,
            'amount': TOTAL_SUPPLY
        }
        return Block(0, '0', time.time(), [genesis_transaction], nonce=0)

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, from_addr, to_addr, amount):
        if from_addr and self.balances.get(from_addr, 0) < amount:
            raise Exception("Insufficient balance")
        self.pending_transactions.append({
            'from': from_addr,
            'to': to_addr,
            'amount': amount
        })

    def mine_block(self, miner_address, difficulty=4):
        self.add_transaction(None, miner_address, 1)  # reward
        block = Block(
            index=len(self.chain),
            previous_hash=self.get_latest_block().hash,
            timestamp=time.time(),
            transactions=self.pending_transactions
        )

        while block.hash[:difficulty] != '0' * difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()

        self.chain.append(block)
        self.update_balances(block.transactions)
        self.pending_transactions = []

    def update_balances(self, transactions):
        for tx in transactions:
            from_addr = tx['from']
            to_addr = tx['to']
            amount = tx['amount']

            if from_addr:
                self.balances[from_addr] -= amount
            self.balances[to_addr] = self.balances.get(to_addr, 0) + amount

    def get_balance(self, address):
        return self.balances.get(address, 0)

if __name__ == "__main__":
    blockchain = Blockchain()
    print("Genesis block created.")
    print("Genesis balance:", blockchain.get_balance(GENESIS_ADDRESS))
