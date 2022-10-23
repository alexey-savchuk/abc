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
        self.timer.current_time = 0
        self.current_num_bids = 0
        time = self.timer.get_current_time()
        tag = EventTag.START
        new_event = Event(time, tag)
        self._add_new_event(new_event)

    def _trigger_all_generating_units(self) -> None:
        new_events = []

        for unit in self.generating_units:
            if self.current_num_bids > self.num_total_bids:
                break

            event = unit.generate()
            new_events.append(event)

            self.current_num_bids += 1

        self._add_new_events(new_events)

    def _trigger_generating_unit(self, unit_id: int) -> None:

        for unit in self.generating_units:
            if self.current_num_bids > self.num_total_bids:
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

    # Auto mode
    def start_auto_mode(self):

        stats = {i + 1: [] for i in range(self.num_generating_units)}
        probs = {i + 1: 1 for i in range(self.num_generating_units)}
        delta = {i + 1: 1 for i in range(self.num_generating_units)}

        times = {i + 1: [0, 0, 0] for i in range(self.num_generating_units)}

        N = 100

        cond = 1
        max_iteration = 200
        num_iteration = 0
        while cond > 0.1 and num_iteration < max_iteration:

            num_iteration += 1

            self.num_total_bids = N
            self.start_step_mode()
            self.step()

            _, event_type, bid = self.get_event_info()
            while event_type != EventTag.END.name:

                if event_type == EventTag.GENERATE.name:
                    unit_id = bid.generating_unit_id
                    stats[unit_id].append(bid)

                self.step()
                _, event_type, bid = self.get_event_info()


            # for id, bids in stats.items():
            #     print(id)
            #     for bid in bids:
            #         print(bid)

            for unit_id, bids in stats.items():
                num_total = len(bids)
                num_refused = 0

                for bid in bids:
                    if bid.is_refused:
                        num_refused += 1
                    else:
                        time_delta = bid.processing_time - bid.generation_time
                        times[unit_id][0] += 1
                        times[unit_id][1] += math.pow(time_delta, 2)
                        times[unit_id][2] += time_delta


                if num_total:
                    delta[unit_id] = math.fabs(probs[unit_id] - num_refused / num_total)
                    probs[unit_id] = num_refused / num_total

            max = 0
            id = 0
            for i, d in delta.items():
                if d > max and d != 1:
                    id = i
                    max = d

            if max > 0:
                N = (math.pow(1.643, 2) * (1 - probs[id])) / (probs[id] * 0.01)
            else:
                max = 1

            print("max = ", max)
            print("N = ", N)

            print("probs")
            for id, p in probs.items():
                print(id, p)

            print("delta")
            for id, p in delta.items():
                print(id, p)

            cond = max


        for unit_id, tim in times.items():
            mean1 = tim[1] / tim[0]
            mean2 = tim[2] / tim[0]

            variance = mean1 - mean2 * mean2

            print("id = ", unit_id, ", mean = ", mean2, ", var = ", variance)

        return "Done"
