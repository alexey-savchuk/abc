from typing import Any


class Buffer:

  def __init__(self, capacity: int) -> None:
    if capacity < 1:
      raise ValueError

    self.size = 0
    self.capacity = capacity
    self.data = [None] * capacity

  def enqueue(self, x: Any) -> None:

    idx = self.size % self.capacity
    self.data[idx] = x
    self.size += 1
    self.size %= self.capacity

  def dequeue(self) -> Any:
    return self.data.pop

  def __iter__(self):
    return iter(self.data)

  def __next__(self):
    return next(self.data)
