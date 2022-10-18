import logging
from events import Event, EventTag
from models.bid import Bid

from models.units import GeneratingUnit, ProcessingUnit
from utils.random import RandomGenerator


class MyGeneratingUnit(GeneratingUnit):
  """TODO"""

  generator: RandomGenerator = RandomGenerator(0.01)

  def __init__(self, unit_id: int) -> None:
    super().__init__(unit_id=unit_id)

  def generate(self) -> Event:

    time = self.timer.get_current_time() + self.generator()
    bid = Bid(generating_unit_id=self.unit_id, generation_time=time)

    event = Event(
      time,
      tag=EventTag.GENERATE,
      data=bid
    )

    logging.debug(f"Generating {event}")

    return event


class MyProcessingUnit(ProcessingUnit):
  """TODO"""

  generator: RandomGenerator = RandomGenerator(0.1)
  busy: bool = False

  def __init__(self, unit_id: int) -> None:
    super().__init__(unit_id)

  def process(self, bid: Bid) -> Event:
    time = self.timer.get_current_time() + self.generator()

    bid.processing_unit_id = self.unit_id
    bid.procession_time = time

    event = Event(
      time=time,
      tag=EventTag.PROCESS,
      data=bid)

    self.busy = True

    logging.debug(f"Processing {event}")

    return event

  def is_busy(self) -> bool:
    return self.busy

