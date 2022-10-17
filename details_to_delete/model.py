import logging
from typing import Iterable, List

from events import Event, GeneratingEvent
from model_types import ModelTime

from models.buffers.buffer import Buffer

from models.dispatchers.buffering_dispatcher import BufferingDispatcher
from models.dispatchers.selecting_dispatcher import SelectingDispatcher

from models.units.generating_unit import GeneratingUnit
from models.units.processing_unit import ProcessingUnit


class Supervisor:

  generating_units: List[GeneratingUnit]

  buffering_dispatcher: BufferingDispatcher
  selecting_dispatcher: SelectingDispatcher

  events: List[Event]
  current_time: ModelTime = 0

  def __init__(
    self,
    generating_units: List[GeneratingUnit],
    buffering_dispatcher: BufferingDispatcher,
    selecting_dispatcher: SelectingDispatcher,
  ) -> None:

    self.generating_units = generating_units

    self.buffering_dispatcher = buffering_dispatcher
    self.selecting_dispatcher = selecting_dispatcher

    self.events = []

  def _add_new_event(self, event: Event) -> None:
    self.events.append(event)

  def _add_new_events(self, events: Iterable[Event]) -> None:
    self.events.extend(events)

  def _get_next_event(self) -> Event:
    return self.events.pop(0)

  def _preserve_order(self) -> None:
    self.events.sort(key=lambda event: event.time)

  def do_work(self) -> None:

    events = [unit.generate() for unit in self.generating_units]

    self._add_new_events(events)
    self._preserve_order()

    self.loop()

  def loop(self) -> None:
    while len(self.events) != 0:

      event = self._get_next_event()
      self.current_time = event.time
      logging.info(f"processing event = {event}")

      # new_events = event.handler()

      new_events = []
      if isinstance(event, GeneratingEvent):
        new_events.append(self.selecting_dispatcher.do_work(self.current_time))

      self._add_new_events(new_events)

      self._preserve_order()
