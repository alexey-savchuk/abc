import random
from events import Event, GeneratingEvent
from model_types import ModelTime
from models.dispatchers.buffering_dispatcher import BufferingDispatcher


class GeneratingUnit:

  previous_time: ModelTime = 0

  def generate(self) -> Event:

    K = 60
    self.previous_time += random.random() * K

    event = GeneratingEvent(time=self.previous_time, handler=lambda: [])
    return event
