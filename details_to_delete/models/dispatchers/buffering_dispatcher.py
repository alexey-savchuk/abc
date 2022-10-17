from abc import ABC, abstractmethod
from urllib.request import Request

from models.buffers.buffer import Buffer


class BufferingDispatcher:

  def __init__(self, buffer: Buffer) -> None:
    pass

  @abstractmethod
  def register(self, request: Request) -> None:
    pass
