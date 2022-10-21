import math
import random


class RandomGenerator:

  frequency: float

  def __init__(self, frequency: float) -> None:
    """TODO"""

    if frequency <= 0:
      raise ValueError

    self.frequency = frequency

  def __call__(self) -> float:
    """TODO"""

    r = random.random()
    return -1 / (self.frequency * math.log(r))
