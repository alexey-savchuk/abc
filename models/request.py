from dataclasses import dataclass


@dataclass
class Request:

  unit_id: int


@dataclass
class Response:

  unit_id: int
