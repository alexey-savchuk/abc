from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class EventTag(Enum):
  """TODO"""

  START = auto()
  SELECT = auto()
  BUFFER = auto()
  PROCESS = auto()
  GENERATE = auto()
  EMPTY = auto()


@dataclass
class Event:
  """TODO"""

  time: float
  tag: EventTag
  data: Any = None

  def __str__(self) -> str:
    return f"Event[time={self.time}, tag={self.tag.name}, data={self.data}]"
