from typing import List
from events import Event, SuspendEvent
from model_types import ModelTime
from models.units.processing_unit import ProcessingUnit


class SelectingDispatcher:

  units: List[ProcessingUnit]

  def __init__(self, units: List[ProcessingUnit]) -> None:
    self.units = units

  def do_work(self, current_time: ModelTime) -> Event:

    for unit in self.units:
      if not unit.is_busy():
        event = unit.process(current_time)
        return event

    event = SuspendEvent(time=999, handler=lambda: [])
    return event
