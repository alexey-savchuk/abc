import logging
from typing import Iterable, List, Tuple
from event import Event, EventTag
from models.bid import Bid
from models.buffer import Buffer

from models.dispatchers import BufferingDispatcher, SelectingDispatcher
from models.units import GeneratingUnit, ProcessingUnit
from step_record import StepRecorder
from timer import Timer


class Supervisor:

    def __init__(
        self,
        generating_units: List[GeneratingUnit],
        processing_units: List[ProcessingUnit],
        buffer: Buffer,
        buffering_dispatcher: BufferingDispatcher,
        selecting_dispatcher: SelectingDispatcher
    ) -> None:

        self.events: List[Event] = []
        self.timer: Timer = Timer()

        self.generating_units: List[GeneratingUnit] = generating_units
        self.processing_units: List[ProcessingUnit] = processing_units
        self.buffer: Buffer = buffer
        self.buffering_dispatcher: BufferingDispatcher = buffering_dispatcher
        self.selecting_dispatcher: SelectingDispatcher = selecting_dispatcher

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
        new_events = [unit.generate() for unit in self.generating_units if unit.unit_id == unit_id]
        self._add_new_events(new_events)

    def _trigger_processing_unit(self, unit_id: int) -> None:
        for unit in self.processing_units:
            if unit.unit_id == unit_id:
                unit.change_state()

    def _trigger_buffering_dispatcher(self, bid: Bid) -> None:
        self.buffering_dispatcher.buffer(bid)

    def _trigger_selecting_dispatcher(self) -> None:
        new_event = self.selecting_dispatcher.select()
        if new_event:
            self._add_new_event(new_event)

    def _update_statistics(self, bid: Bid) -> None:
        current_time = self.timer.get_current_time()
        logging.info(f"{current_time:.2f}: update statistics - {bid}")

    def _end_modeling(self) -> None:
        self.events = []

    def start_step_mode(self):
        self._start_modeling()

    def end(self):
        time = self.timer.current_time
        tag = EventTag.END
        new_event = Event(time, tag)
        self._add_new_event(new_event)

    def step(self) -> Tuple:
        StepRecorder.pushed = None
        StepRecorder.poped = None
        StepRecorder.refused = None

        current_event = self._get_next_event()
        current_time = current_event.time

        self.timer.set_current_time(current_time)

        current_bid = current_event.data

        logging.info(f"{current_time:.2f}: processing {current_event}")
        logging.info(f"{current_time:.2f}: buffer - {self.buffering_dispatcher.memory.queue.data}")

        match current_event.tag:

            case EventTag.START:
                self._trigger_all_generating_units()

            case EventTag.GENERATE:
                self._trigger_generating_unit(current_bid.generating_unit_id)
                self._trigger_buffering_dispatcher(current_bid)
                self._trigger_selecting_dispatcher()

            case EventTag.PROCESS:
                self._trigger_processing_unit(current_bid.processing_unit_id)
                self._update_statistics(current_bid)
                self._trigger_selecting_dispatcher()

            case EventTag.END:
                self._end_modeling()

            case _:
                raise ValueError("Supervisor met unknown event tag")

        return current_time, current_event.tag.name, current_bid, self.buffer, StepRecorder.pushed, StepRecorder.poped, StepRecorder.refused
