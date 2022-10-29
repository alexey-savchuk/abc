from model.bid import Bid
from utils.cyclic_queue import CyclicQueue


class Buffer:

    def __init__(self, capacity: int) -> None:
        super().__init__()

        self.queue: CyclicQueue[Bid] = CyclicQueue(capacity)

    def push_with_displace(self, bid: Bid) -> Bid | None:
        #return self.queue.push_with_displace(bid)
        refused_bid = None
        if self.queue.is_full():
            list = [bid.generation_time for bid in self.queue]
            if list:
                max_time = max(list)
                for id, bid in enumerate(self.queue):
                    if bid.generation_time == max_time:
                        refused_bid = self.pop(id) # pop_with_shift
                        break

        self.queue.push(bid)
        return refused_bid

    def push(self, bid: Bid) -> None:
        self.push_with_displace(bid)

    def pop(self, index: int = 0) -> Bid:
        return self.queue.pop(index)

    def __iter__(self):
        return iter(self.queue)

    def __next__(self):
        return next(self.queue)

    def make_empty(self):
        self.queue.make_empty()

