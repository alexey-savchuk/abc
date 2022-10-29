from pickletools import read_unicodestring4, read_unicodestring8
from typing import Generic, List, Tuple, TypeVar


T = TypeVar('T')

class CyclicQueue(Generic[T]):

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError

        self.data: List[T] = []
        self.capacity: int = capacity

    def _rotate(self, n: int):
        n = n % self.capacity
        self.data = self.data[-n:] + self.data[:-n]

    def push_with_displace(self, x: T) -> T | None:

        displaced = None

        if len(self.data) == self.capacity:
            displaced = self.data.pop()

        self.data.append(x)

        return displaced

        # cap = 5 
        # [ 1 (1), 2 (2), 4 (4), 5 (5), _ ]

        # cap = 5 
        # [ 1 (1), 2 (2), 3 (3) 4 (4), 5(5)]
        # [ 1 (1), 2 (2), _, <-4 (4), <-5(5), _new_place_ ]

    def is_full(self):
        return len(self.data) == self.capacity

    def push(self, x: T) -> None:
        self.data.append(x)

    def pop(self, index: int = 0) -> T:
        return self.data.pop(index)

    def __len__(self) -> int:
        return len(self.data)

    def __str__(self) -> str:
        return str(self.data)

    def __iter__(self):
        return iter(self.data)

    def __next__(self):
        return next(self.data)

    def make_empty(self):
        self.data = []
