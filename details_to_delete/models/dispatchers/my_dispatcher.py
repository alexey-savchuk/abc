import logging

from models.buffers.buffer import Buffer
from models.requests.request import Request
import models.dispatchers.buffering_dispatcher as buffering_dispatcher

class MyDispatcher(buffering_dispatcher.BufferingDispatcher):

  def __init__(self, buffer: Buffer) -> None:
    super().__init__(Buffer)

  def register(self, request: Request) -> None:
    logging.info(f"registered request with unit_id={request.unit_id}, message={request.message}, generated_at={request.generated_at}")
