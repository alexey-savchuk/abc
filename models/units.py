from abc import ABC, abstractmethod
from typing import List

from events import Event
from models.bid import Bid
from timer import Timer


class GeneratingUnit(ABC):
  """TODO"""

  unit_id: int
  timer: Timer

  def __init__(self, unit_id: int) -> None:
    super().__init__()

    self.unit_id = unit_id
    self.timer = Timer()

  @abstractmethod
  def generate(self) -> Event:
    pass


class ProcessingUnit(ABC):
  """TODO"""

  unit_id: int
  timer: Timer

  def __init__(self, unit_id: int) -> None:
    super().__init__()

    self.unit_id = unit_id
    self.timer = Timer()

  @abstractmethod
  def process(self, bid: Bid) -> Event:
    pass
