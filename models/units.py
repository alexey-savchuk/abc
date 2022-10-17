from abc import ABC, abstractmethod
from typing import List, Tuple

from events import Event
from timer import Timer


class GeneratingUnit(ABC):
  """TODO"""

  timer: Timer

  def __init__(self) -> None:
    self.timer = Timer()

  @abstractmethod
  def generate(self) -> Event:
    pass

  def get_timer(self) -> Timer:
    return self.timer


class ProcessingUnit(ABC):
  """TODO"""

  timer: Timer

  def __init__(self) -> None:
    self.timer = Timer()

  @abstractmethod
  def process(self) -> List[Event]:
    pass
