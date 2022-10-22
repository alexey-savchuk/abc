from dataclasses import dataclass


@dataclass
class Config:

  generating_units_count: int = 0
  processing_units_count: int = 0
  buffer_capacity: int = 0

  generation_frequency: float = 0
