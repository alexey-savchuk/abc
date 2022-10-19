from typing import List

from events import Event, EventTag
from models.bid import Bid
from models.buffer import Buffer
from models.dispatchers import BufferingDispatcher, SelectingDispatcher
from models.units import ProcessingUnit
from utils.random import RandomGenerator


class MyBufferingDispatcher(BufferingDispatcher):

  memory: Buffer

  def __init__(self, buffer: Buffer) -> None:
    super().__init__()
    self.memory = buffer

  def buffer(self, bid: Bid) -> Event:

    time = self.timer.get_current_time()
    bid.buffered = True
    bid.beffering_time = time

    is_refused, refused_bid = self.memory.add_bid_with_displace(bid)

    if is_refused:

      refused_bid.refused = True
      refused_bid.refusion_time = time

      return Event(time, EventTag.REFUSE, refused_bid)

    return Event(9999999999, EventTag.EMPTY)


class MySelectingDispatcher(SelectingDispatcher):

  processing_units: List[ProcessingUnit]
  buffer: Buffer

  generator: RandomGenerator = RandomGenerator(0.1)

  target_id: int
  bids_to_process: List[Bid]

  def __init__(self, processing_units: List[ProcessingUnit], buffer: Buffer) -> None:
    super().__init__()
    self.processing_units = processing_units
    self.buffer = buffer

    self.target_id = None
    self.bids_to_process = []

  def select(self) -> None:

    if self.target_id == None:
      self.target_id, self.bids_to_process = self.buffer.get_next_package()
      return

    self.bids_to_process += self.buffer.pick_bids(self.target_id)

    if len(self.bids_to_process) == 0:
      self.target_id, self.bids_to_process = self.buffer.get_next_package()


  def process(self, bid: Bid) -> Event:

    self.select()

    if self.target_id == None:
      self.target_id = bid.generating_unit_id

      for unit in self.processing_units:
        if not unit.is_busy():
          return unit.process(bid)

    if self.target_id == bid.generating_unit_id:
      self.bids_to_process.append(bid)
      return Event(self.timer.get_current_time(), EventTag.EMPTY)

    return Event(self.timer.get_current_time(), EventTag.BUFFER, data=bid)
