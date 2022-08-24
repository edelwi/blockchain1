# based on https://habr.com/ru/company/ruvds/blog/589371/
from hashlib import sha256
import json
from time import time
from typing import Optional, Any


class Block:
    def __init__(self, timestamp: Optional[float] = None, data: Optional[Any] = None):
        self.timestamp = timestamp or time()
        self.data = [] if data is None else data
        self.prev_hash = None
        self.nonce = 0
        self.hash = self.get_hash()

    def get_hash(self) -> str:
        block_hash = sha256()
        block_hash.update(str(self.prev_hash).encode("utf-8"))
        block_hash.update(str(self.timestamp).encode("utf-8"))
        block_hash.update(str(self.data).encode("utf-8"))
        block_hash.update(str(self.nonce).encode("utf-8"))
        return block_hash.hexdigest()

    def mine(self, difficulty: int) -> None:
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.get_hash()


class Blockchain:
    def __init__(self):
        self.chain = [Block(str(int(time())))]
        self.difficulty = 1
        self.block_time = 30000

    def get_last_block(self) -> Block:
        return self.chain[len(self.chain) - 1]

    def add_block(self, block: Block) -> None:
        block.prev_hash = self.get_last_block().hash
        block.hash = block.get_hash()
        block.mine(difficulty=self.difficulty)
        self.chain.append(block)
        self.difficulty += (-1, 1)[int(time()) - int(self.get_last_block().timestamp) < self.block_time]

    def is_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if any(
                    (
                            current_block.hash != current_block.get_hash(),
                            previous_block.hash != current_block.prev_hash,
                    )
            ):
                return False
        return True

    def __repr__(self) -> str:
        return json.dumps(
            [
                {
                    "data": item.data,
                    "timestamp": item.timestamp,
                    "nonce": item.nonce,
                    "hash": item.hash,
                    "previous_hash": item.prev_hash,
                }
                for item in self.chain
            ],
            indent=4,
        )


if __name__ == "__main__":
    bc = Blockchain()
    print(f"empty Blockchain: {bc}")
    block = Block(data="Vasya -> Pety: 10$")
    bc.add_block(block=block)
    block = Block(data="Vasya -> Olya: 12$")
    bc.add_block(block=block)
    block = Block(data="Pety <- Vasya: 10$")
    bc.add_block(block=block)
    block = Block(data={"from": "Petya", "to": "Vasya", "amount": 100})
    bc.add_block(block=block)
    print(f"after adding 4 block {bc}")
