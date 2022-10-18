from dataclasses import dataclass
from enum import Enum, auto

from models.bid import Bid


class EventTag(Enum):
  """TODO"""

  START = auto()
  SELECT = auto()
  BUFFER = auto()
  PROCESS = auto()
  GENERATE = auto()
  EMPTY = auto()
  REFUSE = auto()


@dataclass
class Event:
  """TODO"""

  time: float
  tag: EventTag
  data: Bid | None = None

  def __str__(self) -> str:
    return "Event[{:.2f}, {:s}, {:s}]".format(self.time, str(self.tag.name), str(self.data))
