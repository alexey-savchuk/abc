import logging
from typing import Iterable, List
from events import Event, EventTag
from models.bid import Bid

from models.dispatchers import BufferingDispatcher, SelectingDispatcher
from models.units import GeneratingUnit, ProcessingUnit
from timer import Timer


class Supervisor:

  generating_units: List[GeneratingUnit]
  processing_units: List[ProcessingUnit]

  buffering_dispatcher: BufferingDispatcher
  selecting_dispatcher: SelectingDispatcher

  events: List[Event]
  timer: Timer

  def __init__(self,
      generating_units: List[GeneratingUnit],
      processing_units: List[ProcessingUnit],
      buffering_dispatcher: BufferingDispatcher,
      selecting_dispatcher: SelectingDispatcher) -> None:

    self.generating_units = generating_units
    self.processing_units = processing_units
    self.buffering_dispatcher = buffering_dispatcher
    self.selecting_dispatcher = selecting_dispatcher

    self.events = []
    self.timer = Timer()

  # Utils
  def _add_new_event(self, event: Event) -> None:
    self.events.append(event)
    self._preserve_order()

  def _add_new_events(self, events: Iterable[Event]) -> None:
    self.events.extend(events)
    self._preserve_order()

  def _get_next_event(self) -> Event:
    return self.events.pop(0)

  def _preserve_order(self) -> None:
    self.events.sort(key=lambda event: event.time)

  # Actions
  def _start_modeling(self) -> None:
    time = 0
    tag = EventTag.START
    new_event = Event(time, tag)
    self._add_new_event(new_event)

  def _trigger_all_generating_units(self) -> None:
    new_events = [unit.generate() for unit in self.generating_units]
    self._add_new_events(new_events)

  def _trigger_generating_unit(self, unit_id: int) -> None:
    units = [unit for unit in self.generating_units if unit.unit_id == unit_id]
    new_events = [unit.generate() for unit in units]
    self._add_new_events(new_events)

  def _process_bid(self, bid: Bid) -> None:
    new_event = self.selecting_dispatcher.process(bid)
    self._add_new_event(new_event)

  def _update_statistics(self, bid: Bid) -> None:
    logging.info(f"Statistics: {bid}")

  def _trigger_selecting_dispatcher(self) -> None:
    time = self.timer.get_current_time()
    tag = EventTag.SELECT
    new_event = Event(time, tag)
    self._add_new_event(new_event)

  def _trigger_buffering_dispatcher(self, bid: Bid) -> None:
    new_event = self.buffering_dispatcher.buffer(bid)
    self._add_new_event(new_event)

  # Start modeling
  def start(self) -> None:
    self._start_modeling()

    while len(self.events) != 0:

      current_event = self._get_next_event()
      self.timer.set_current_time(current_event.time)

      logging.info(f"Processing event = {current_event}")

      match current_event.tag:
        case EventTag.START:
          self._trigger_all_generating_units()

        case EventTag.GENERATE:
          bid = current_event.data
          self._process_bid(bid)
          self._trigger_generating_unit(bid.generating_unit_id)

        case EventTag.BUFFER:
          bid = current_event.data
          self._trigger_buffering_dispatcher(bid)

        case EventTag.PROCESS:
          bid = current_event.data

          self._update_statistics(bid)
          # self._trigger_selecting_dispatcher()

        case EventTag.EMPTY:
          pass

        case EventTag.REFUSE:
          pass

        case _:
          raise ValueError("Supervisor met unknown event tag")

  def start_step_mode(self):
    self._start_modeling()

  def step(self) -> None:
    current_event = self._get_next_event()
    self.timer.set_current_time(current_event.time)

    logging.info(f"Processing event = {current_event}")
    logging.info(f"Selecting dispatcher list: {self.selecting_dispatcher.bids_to_process}")
    logging.info(f"Selecting dispatcher list: {self.selecting_dispatcher.buffer.queue}")


    match current_event.tag:
      case EventTag.START:
        self._trigger_all_generating_units()

      case EventTag.SELECT:
        pass

      case EventTag.GENERATE:
        bid = current_event.data
        self._process_bid(bid)
        self._trigger_generating_unit(bid.generating_unit_id)

      case EventTag.BUFFER:
        bid = current_event.data
        self._trigger_buffering_dispatcher(bid)

      case EventTag.PROCESS:
        bid = current_event.data

        self._update_statistics(bid)
        # self._trigger_selecting_dispatcher()

      case EventTag.EMPTY:
        pass

      case EventTag.REFUSE:
        pass

      case _:
        raise ValueError("Supervisor met unknown event tag")
