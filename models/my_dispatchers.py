from random import random
from typing import List

from events import Event, EventTag
from models.dispatchers import SelectingDispatcher
from models.request import Request, Response


class MySelectingDispatcher(SelectingDispatcher):

  def __init__(self) -> None:
    super().__init__()

  def process(self, request: Request) -> Event:
    response = Response(0)
    event = Event(
      time=self.timer.get_current_time() + random() * 60,
      tag=EventTag.PROCESS,
      data=response)

    return event

