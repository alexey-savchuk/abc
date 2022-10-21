import logging
from typing import List, Tuple

from events import Event
from models.bid import Bid
from models.buffer import Buffer
from models.units import ProcessingUnit
from timer import Timer


class BufferingDispatcher:

    def __init__(self, buffer: Buffer) -> None:

        self.timer = Timer()

        self.memory = buffer

    def buffer(self, bid: Bid):

        time = self.timer.get_current_time()
        bid.buffered = True
        bid.beffering_time = time

        is_refused, refused_bid = self.memory.add_bid_with_displace(bid)

        logging.debug(f"Buffeting {bid}")

        if is_refused:
            refused_bid.refused = True
            refused_bid.refusion_time = time


class SelectingDispatcher:

    processing_units: List[ProcessingUnit]
    buffer: Buffer

    target_id: int
    bids_to_process: List[Bid]

    def __init__(self, processing_units: List[ProcessingUnit], buffer: Buffer) -> None:

        self.timer = Timer()

        self.processing_units = processing_units
        self.buffer = buffer

        self.target_id = None
        self.bids_to_process = []

    def _get_bids(self, unit_id: int) -> List[Bid]:
        return self.buffer.pick_bids(unit_id)

    def _get_next_package(self) -> Tuple[int, List[Bid]]:
        return self.buffer.get_next_package()

    def _process(self, bid: Bid) -> Event:

        for unit in self.processing_units:
            if unit.is_free():
                event = unit.process(bid)
                return event


    def select(self) -> Event:

        logging.debug(f"select: {self.target_id}, {self.bids_to_process}")

        if self.target_id:
            self.bids_to_process += self._get_bids(self.target_id)
        else:
            self.target_id, self.bids_to_process = self._get_next_package()

        if self.bids_to_process:
            bid = self.bids_to_process.pop(0)
            event = self._process(bid)
            return event
        else:
            self.target_id, self.bids_to_process = self._get_next_package()
