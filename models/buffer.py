from models.bid import Bid
from utils.cyclic_queue import CyclicQueue


class Buffer:

    def __init__(self, capacity: int) -> None:
        super().__init__()

        self.queue: CyclicQueue[Bid] = CyclicQueue(capacity)

    def push_with_displace(self, bid: Bid) -> Bid | None:
        return self.queue.push_with_displace(bid)

    def push(self, bid: Bid) -> None:
        self.push_with_displace(bid)

    def pop(self, index: int = 0) -> Bid:
        return self.queue.pop(index)

    def __iter__(self):
        return iter(self.queue)

    def __next__(self):
        return next(self.queue)
