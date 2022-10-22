import logging

from event import Event, EventTag
from models.bid import Bid
from timer import Timer
from utils.random import RandomGenerator


class GeneratingUnit:
    """TODO"""

    def __init__(self, unit_id: int) -> None:

        self.timer = Timer()
        self.generator = RandomGenerator(1)

        self.unit_id = unit_id

    def generate(self) -> Event:

        current_time = self.timer.get_current_time()
        time = current_time + self.generator()

        bid = Bid(generating_unit_id=self.unit_id, generation_time=time)

        event = Event(time, tag=EventTag.GENERATE, data=bid)

        logging.debug(f"{current_time:.2f}: unit {self.unit_id} generating {event}")

        return event


class ProcessingUnit:
    """TODO"""

    def __init__(self, unit_id: int) -> None:

        self.timer = Timer()
        self.generator = RandomGenerator(1)

        self.unit_id = unit_id
        self.free = True

    def is_free(self) -> bool:
        return self.free

    def change_state(self) -> None:
        self.free = not self.free

    def process(self, bid: Bid) -> Event:

        current_time = self.timer.get_current_time()
        time = current_time + self.generator()

        bid.processing_unit_id = self.unit_id
        bid.procession_time = time

        event = Event(time=time, tag=EventTag.PROCESS, data=bid)

        self.free = False

        logging.debug(f"{current_time:.2f}: unit {self.unit_id} generating {event}")

        return event
