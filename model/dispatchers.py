import logging
from typing import List

from model.event import Event
from model.bid import Bid
from model.buffer import Buffer
from model.units import ProcessingUnit
from model.step_record import StepRecorder
from model.timer import Timer


target_id = None

class ProcessingDispatcher:

    def __init__(self, processing_units: List[ProcessingUnit], buffer: Buffer) -> None:

        self.timer = Timer()

        self.processing_units = processing_units
        self.buffer = buffer

    def _has_free_unit(self) -> bool:
        for unit in self.processing_units:
            if unit.is_free():
                return True

        return False

    def _buffer(self, bid: Bid) -> None:
        refused_bid = self.buffer.push_with_displace(bid)

        if refused_bid:
            refused_bid.is_refused = True

        StepRecorder.pushed_bid = bid
        StepRecorder.refused_bid = refused_bid

        logging.debug(f"Buffering {bid}")
        logging.debug(f"Refused {refused_bid}")


    def _process(self, bid: Bid) -> Event:

        bid.selection_time = self.timer.get_current_time()

        for unit in self.processing_units:
            if unit.is_free():
                event = unit.process(bid)
                return event

    def process(self, bid: Bid) -> Event | None:

        global target_id

        if not self._has_free_unit():
            self._buffer(bid)
            return

        target_id = bid.generating_unit_id
        event = self._process(bid)
        return event


class SelectingDispatcher:

    def __init__(self, processing_units: List[ProcessingUnit], buffer: Buffer) -> None:

        self.timer: Timer = Timer()

        self.processing_units: List[ProcessingUnit] = processing_units
        self.buffer: Buffer = buffer

    def _get_new_bid(self) -> Bid:
        global target_id

        new_bid = None

        for index, bid in enumerate(self.buffer):
            if bid.generating_unit_id == target_id:
                new_bid = self.buffer.queue.pop(index)
                logging.debug(f"poped: idx={index}, {bid}")
                break

        if new_bid:
            return new_bid

        self._init_new_package()
        logging.debug("Init new package")

        for index, bid in enumerate(self.buffer):
            if bid.generating_unit_id == target_id:
                new_bid = self.buffer.queue.pop(index)
                logging.debug(f"poped: idx={index}, {bid}")
                break

        return new_bid

    def _init_new_package(self) -> None:
        global target_id

        ids = [bid.generating_unit_id for bid in self.buffer]
        if ids:
            target_id = min(ids)

    def _process(self, bid: Bid) -> Event:

        bid.selection_time = self.timer.get_current_time()

        for unit in self.processing_units:
            if unit.is_free():
                event = unit.process(bid)
                return event

    def select(self) -> Event:
        event = None

        bid = self._get_new_bid()
        if bid:
            event = self._process(bid)

        StepRecorder.poped_bid = bid

        logging.debug(f"select: {bid}")

        return event
