from typing import List, Tuple

from models.bid import Bid
from utils.cyclic_queue import CyclicQueue


class Buffer:

  queue: CyclicQueue[Bid]

  def __init__(self, capacity: int) -> None:
    super().__init__()

    self.queue = CyclicQueue(capacity)

  def pick_bids(self, unit_id: int) -> List[Bid]:
    lst = self.queue.pick(filter=lambda bid: bid.generating_unit_id == unit_id)
    return lst

  def add_bid_with_displace(self, bid: Bid) -> Tuple[bool, Bid]:
    return self.queue.push_with_displace(bid)

  def get_next_package(self) -> Tuple[int, List[Bid]]:

    ids = [bid.generating_unit_id for bid in self.queue.data]

    if ids:
      target_id = min(ids)
      return (target_id, self.pick_bids(target_id))

    return (None, [])
