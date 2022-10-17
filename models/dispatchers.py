from abc import ABC, abstractmethod
from typing import List

from events import Event
from models.request import Request
from timer import Timer


class BufferingDispatcher(ABC):
  """TODO"""

  timer: Timer

  def __init__(self) -> None:
    self.timer = Timer()

  @abstractmethod
  def buffer(self) -> List[Event]:
    pass


class SelectingDispatcher(ABC):
  """TODO"""

  timer: Timer

  def __init__(self) -> None:
    self.timer = Timer()

  @abstractmethod
  def process(self, request: Request) -> Event:
    pass
