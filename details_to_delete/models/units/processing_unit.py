import random
from events import Event, ProcessingEvent
from model_types import ModelTime


class ProcessingUnit:

  previous_time: ModelTime

  def __init__(self) -> None:
    self.previous_time = 0
    self.busy = False

  def is_busy(self) -> bool:
    return self.busy

  def process(self, current_time: ModelTime) -> Event:

    self.busy = True

    K = 60
    self.previous_time = current_time
    self.previous_time += random.random() * K

    event = ProcessingEvent(time=self.previous_time, handler=lambda: [])
    return event
