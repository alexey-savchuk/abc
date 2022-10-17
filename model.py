import logging
from typing import Iterable, List
from events import Event, EventTag

from models.dispatchers import BufferingDispatcher, SelectingDispatcher
from models.units import GeneratingUnit
from timer import Timer


class Supervisor:

  generating_units: List[GeneratingUnit]

  buffering_dispatcher: BufferingDispatcher
  selecting_dispatcher: SelectingDispatcher

  events: List[Event]
  timer: Timer

  def __init__(self,
      generating_units: List[GeneratingUnit], selecting_dispatcher: SelectingDispatcher) -> None:

    self.generating_units = generating_units
    self.selecting_dispatcher = selecting_dispatcher

    self.events = []
    self.timer = Timer()

  def _add_new_event(self, event: Event) -> None:
    self.events.append(event)

  def _add_new_events(self, events: Iterable[Event]) -> None:
    self.events.extend(events)

  def _get_next_event(self) -> Event:
    return self.events.pop(0)

  def _preserve_order(self) -> None:
    self.events.sort(key=lambda event: event.time)

  def start(self) -> None:

    event = Event(0, EventTag.START)
    self._add_new_event(event)

    while len(self.events) != 0:

      current_event = self._get_next_event()
      new_events = []

      self.timer.set_current_time(current_event.time)

      logging.info(f"Processing event = {current_event}")

      match current_event.tag:
        case EventTag.START:
          for unit in self.generating_units:
            self._add_new_event(unit.generate())

        case EventTag.SELECT:
          print("SELECT")

        case EventTag.GENERATE:
          print("GENERATE")

          request = current_event.data
          event = self.selecting_dispatcher.process(request)

          self._add_new_event(event)

          for unit in self.generating_units:
            if unit.id == request.unit_id:
              self._add_new_event(unit.generate())

        case EventTag.BUFFER:
          print("BUFFER")

        case EventTag.PROCESS:
          logging.info(F"Processing finished")

        case EventTag.EMPTY:
          print("EMPTY")

        case _:
          raise ValueError

      self._add_new_events(new_events)
      self._preserve_order()
