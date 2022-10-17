from abc import ABC
from typing import Callable
from model_types import ModelTime

class Event(ABC):

  time: ModelTime
  handler: Callable

  def __init__(self, time: ModelTime, handler: Callable) -> None:
    self.time = time
    self.handler = handler


class GeneratingEvent(Event):

  def __init__(self, time: ModelTime, handler: Callable):
    super().__init__(time, handler)

  def __str__(self) -> str:
    return "GeneratingEvent[time = {:10.5f}, handler = {}]".format(self.time, self.handler)


class ProcessingEvent(Event):

  def __init__(self, time: ModelTime, handler: Callable):
    super().__init__(time, handler)

  def __str__(self) -> str:
    return "ProcessingEvent[time = {:10.5f}, handler = {}]".format(self.time, self.handler)


class BufferingEvent(Event):

  def __init__(self, time: ModelTime):
    super(time, None)


class SuspendEvent(Event):

  def __init__(self, time: ModelTime, handler: Callable):
    super().__init__(time, handler)

  def __str__(self) -> str:
    return "SuspendEvent[time = {:10.5f}, handler = {}]".format(self.time, self.handler)
