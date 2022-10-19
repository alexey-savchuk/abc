from typing import List, Tuple, TypeVar


T = TypeVar('T')

class CyclicQueue:

  data: List[T]
  capacity: int

  def __init__(self, capacity: int) -> None:
    if capacity <= 0:
      raise ValueError

    self.data = []
    self.capacity = capacity

  def _rotate(self, n: int):
    n = n % self.capacity
    self.data = self.data[-n:] + self.data[:-n]

  def _is_full(self) -> bool:
    return len(self.data) == self.capacity

  def push_with_displace(self, x: T) -> Tuple[bool, T]:
    """TODO"""

    displaced = None

    if self._is_full():
      self._rotate(-1)
      displaced = self.data.pop()

    self.data.append(x)

    return (displaced != None, displaced)

  def push(self, x: T) -> None:
    self.push_with_displace(x)

  def pop(self) -> None:
    return self.data.pop(0)

  def pick(self, filter) -> List[T]:
    lst = [x for x in self.data if filter(x)]
    self.data = [x for x in self.data if not filter(x)]

    return lst

  def __len__(self) -> int:
    return len(self.data)

  def __str__(self) -> str:
    return str(self.data)