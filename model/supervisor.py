from dataclasses import dataclass
import logging
import math
import statistics
from typing import Iterable, List, Tuple


from model.event import Event, EventTag
from model.bid import Bid
from model.buffer import Buffer
from model.dispatchers import ProcessingDispatcher, SelectingDispatcher
from model.units import GeneratingUnit, ProcessingUnit
from model.step_record import StepRecorder
from model.timer import Timer


class Supervisor:

    def __init__(self,
                 num_sources: int,
                 num_devices: int,
                 buffer_capacity: int,
                 generation_freq: float,
                 min_proc_time: float,
                 max_proc_time: float,
                 num_total_bids: int) -> None:

        self.events: List[Event] = []
        self.timer: Timer = Timer()

        self.num_generating_units = num_sources
        self.num_processing_units = num_devices

        self.num_total_bids = num_total_bids
        self.current_num_bids = 0

        self.generating_units = [GeneratingUnit(i + 1, generation_freq) for i in range(num_sources)]
        self.processing_units = [ProcessingUnit(i + 1, min_proc_time, max_proc_time) for i in range(num_devices)]

        self.memory_buffer = Buffer(buffer_capacity)

        self.processing_dispatcher = ProcessingDispatcher(self.processing_units, self.memory_buffer)
        self.selecting_dispatcher = SelectingDispatcher(self.processing_units, self.memory_buffer)

    # Steo mode utils
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

    # Step mode actions
    def _start_modeling(self) -> None:
        self.current_num_bids = 0
        time = self.timer.get_current_time()
        tag = EventTag.START
        new_event = Event(time, tag)
        self._add_new_event(new_event)

    def _trigger_all_generating_units(self) -> None:
        new_events = []

        for unit in self.generating_units:
            if self.current_num_bids == self.num_total_bids:
                break

            event = unit.generate()
            new_events.append(event)

            self.current_num_bids += 1

        self._add_new_events(new_events)

    def _trigger_generating_unit(self, unit_id: int) -> None:

        for unit in self.generating_units:
            if self.current_num_bids == self.num_total_bids:
                break

            if unit.unit_id == unit_id:
                new_event = unit.generate()

                self.current_num_bids += 1

                self._add_new_event(new_event)
                break

    def _trigger_processing_unit(self, unit_id: int) -> None:
        for unit in self.processing_units:
            if unit.unit_id == unit_id:
                unit.make_free()

    def _trigger_processing_dispatcher(self, bid: Bid) -> None:
        new_event = self.processing_dispatcher.process(bid)

        if new_event:
            self._add_new_event(new_event)

    def _trigger_selecting_dispatcher(self) -> None:
        new_event = self.selecting_dispatcher.select()
        if new_event:
            self._add_new_event(new_event)

    def _update_statistics(self, bid: Bid) -> None:
        current_time = self.timer.get_current_time()
        logging.info(f"{current_time:.2f}: update statistics - {bid}")

    def _end_modeling(self) -> None:
        print("THE END")

    # Step mode
    def start_step_mode(self):
        self._start_modeling()

    def end_step_mode(self):
        time = self.timer.get_current_time()
        tag = EventTag.END
        new_event = Event(time, tag)
        self._add_new_event(new_event)

    def step(self) -> Tuple:
        if not self.events:
            self.end_step_mode()

        current_event = self._get_next_event()

        current_time = current_event.time
        self.timer.set_current_time(current_time)

        current_bid = current_event.data

        StepRecorder.current_time = current_time
        StepRecorder.event_type = current_event.tag.name
        StepRecorder.current_bid = current_bid
        StepRecorder.pushed_bid = None
        StepRecorder.poped_bid = None
        StepRecorder.refused_bid = None

        logging.info(f"{current_time:.2f}: processing {current_event}")
        logging.info(f"{current_time:.2f}: current buffer {[str(bid) for bid in self.memory_buffer]}")

        match current_event.tag:
            case EventTag.START:
                self._trigger_all_generating_units()

            case EventTag.GENERATE:
                self._trigger_generating_unit(current_bid.generating_unit_id)
                self._trigger_processing_dispatcher(current_bid)
                # self._trigger_selecting_dispatcher()

            case EventTag.PROCESS:
                self._trigger_processing_unit(current_bid.processing_unit_id)
                self._update_statistics(current_bid)
                self._trigger_selecting_dispatcher()

            case EventTag.END:
                self._end_modeling()

            case _:
                raise ValueError("Supervisor met unknown event tag")

        logging.info(f"END: current = {self.current_num_bids}, total = {self.num_total_bids}")

    def get_event_info(self) -> Tuple:
        return (StepRecorder.current_time,
                StepRecorder.event_type,
                StepRecorder.current_bid)

    def get_buffer_info(self) -> Tuple:
        return (self.memory_buffer,
                StepRecorder.pushed_bid,
                StepRecorder.poped_bid,
                StepRecorder.refused_bid)

    # Auto mode utils
    def _get_next_approx(self, p_prev: float, N_prev: int) -> float:

        # { unit_id: bids_in_system }
        stats = {i + 1: [] for i in range(self.num_generating_units)}

        self.start_step_mode()

        i = 0
        while True:
            is_done = True
            self.step()
            _, event_type, bid = self.get_event_info()

            if event_type == EventTag.GENERATE.name:
                unit_id = bid.generating_unit_id
                stats[unit_id].append(bid)
                i += 1

            for _, bids in stats.items():
                if not bids:
                    is_done = False

            if is_done and i > N_prev:
                break

        while True:
            is_done = True
            self.step()

            for bids in stats.values():
                for bid in bids:
                    if not bid.processing_unit_id and not bid.is_refused:
                        is_done = False

            if is_done:
                break

        self.end_step_mode()
        self.step()

        probabilities = {i + 1: 0 for i in range(self.num_generating_units)}

        for unit_id, bids in stats.items():

            total_num = len(bids)
            num_refused = 0

            for bid in bids:

                if bid.is_refused:
                    num_refused += 1

            probabilities[unit_id] = num_refused / total_num

        for i, x in probabilities.items():
            print(f"{i}: {x:.2f}")

        p_next = max(probabilities.values(), key=lambda p: math.fabs(p_prev - p))

        return p_next

    def _get_proper_num_bids(self) -> int:

        t_a = 1.643
        d = 0.1

        p_prev = 2
        print(f"p_prev = {p_prev}")
        N_prev = 100
        print(f"N_prev = {N_prev}")

        p_next = self._get_next_approx(p_prev, N_prev)
        print(f"p_next = {p_next}")
        N_next = (math.pow(t_a, 2) * (1 - p_next)) / (p_next * math.pow(d, 2))
        print(f"N_next = {N_next}")

        while math.fabs(p_next - p_prev) > 0.1:

            p_prev = p_next
            print(f"p_prev = {p_prev}")
            p_next = self._get_next_approx(p_next, N_next)

            N_prev = N_next
            print(f"N_prev = {N_prev}")
            N_next = (math.pow(t_a, 2) * (1 - p_next)) / (p_next * math.pow(d))
            print(f"N_next = {N_next}")

        return N_next

    # Auto mode
    def start_auto_mode(self):

        map = {i + 1: [] for i in range(self.num_generating_units)}
        num_refused = 0
        num_processed = 0

        print(self._get_proper_num_bids())

        # self.start_step_mode()

        # bids = []
        # for i in range(10000):
        #     self.step()

        #     _, event_type, bid = self.get_event_info()

        #     if event_type == EventTag.GENERATE.name:
        #         bids.append(bid)

        # self.end_step_mode()

        # for bid in bids:
            # print(bid)

        return "Done"
