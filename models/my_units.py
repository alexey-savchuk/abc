from typing import List
from events import Event, EventTag
from models.request import Request

from models.units import GeneratingUnit, ProcessingUnit
from utils.random import RandomGenerator


class MyGeneratingUnit(GeneratingUnit):
  """TODO"""

  id: int
  generator: RandomGenerator = RandomGenerator(0.01)

  def __init__(self, id: int) -> None:
    super().__init__()
    self.id = id

  def generate(self) -> Event:

    request = Request(unit_id=self.id)
    event = Event(
      self.timer.get_current_time() + self.generator(),
      tag=EventTag.GENERATE,
      data=request
    )

    return event


class MyProcessingUnit(ProcessingUnit):
  """TODO"""

  def __init__(self) -> None:
    pass

  def process(self) -> List[Event]:
    pass

