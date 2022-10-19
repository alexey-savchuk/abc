from abc import ABC, abstractmethod

from events import Event
from models.bid import Bid
from timer import Timer


class BufferingDispatcher(ABC):
  """TODO"""

  timer: Timer

  def __init__(self) -> None:
    super().__init__()

    self.timer = Timer()

  @abstractmethod
  def buffer(self, bid: Bid) -> Event:
    pass


class SelectingDispatcher(ABC):
  """TODO"""

  timer: Timer

  def __init__(self) -> None:
    super().__init__()

    self.timer = Timer()

  @abstractmethod
  def process(self, bid: Bid) -> Event:
    pass
