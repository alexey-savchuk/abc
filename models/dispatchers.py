import logging
from typing import List

from event import Event
from models.bid import Bid
from models.buffer import Buffer
from models.units import ProcessingUnit
from step_record import StepRecorder
from timer import Timer


class BufferingDispatcher:

    def __init__(self, buffer: Buffer) -> None:

        self.timer = Timer()
        self.memory = buffer

    def buffer(self, bid: Bid):

        time = self.timer.get_current_time()
        bid.buffered = True
        bid.beffering_time = time

        StepRecorder.pushed = bid
        refused_bid = self.memory.push_with_displace(bid)
        StepRecorder.refused = refused_bid

        logging.debug(f"Buffeting {bid}")

        if refused_bid:
            refused_bid.refused = True
            refused_bid.refusion_time = time

        logging.debug(f"Refused {refused_bid}")


class SelectingDispatcher:

    def __init__(self, processing_units: List[ProcessingUnit], buffer: Buffer) -> None:

        self.timer: Timer = Timer()

        self.processing_units: List[ProcessingUnit] = processing_units
        self.buffer: Buffer = buffer

        self.target_id: int = None

    def _get_new_bid(self) -> Bid:
        new_bid = None

        for index, bid in enumerate(self.buffer):
            if bid.generating_unit_id == self.target_id:
                new_bid = self.buffer.queue.pop(index)
                break

        if not new_bid:
            self._init_new_package()

        for index, bid in enumerate(self.buffer):
            if bid.generating_unit_id == self.target_id:
                new_bid = self.buffer.queue.pop(index)
                break

        return new_bid

    def _init_new_package(self) -> None:
        ids = [bid.generating_unit_id for bid in self.buffer]
        if ids:
            self.target_id = min(ids)

    def _process(self, bid: Bid) -> Event:

        for unit in self.processing_units:
            if unit.is_free():
                event = unit.process(bid)
                return event

    def _has_free_unit(self) -> bool:
        for unit in self.processing_units:
            if unit.is_free():
                return True

        return False


    def select(self) -> Event | None:
        event = None

        if not self._has_free_unit():
            return None

        bid = self._get_new_bid()
        StepRecorder.poped = bid
        if bid:
            event = self._process(bid)

        logging.debug(f"select: target id = {self.target_id}")

        return event
