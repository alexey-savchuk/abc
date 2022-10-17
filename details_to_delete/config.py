from dataclasses import dataclass


@dataclass
class Config:

  generating_units_count: int
  processing_units_count: int
  buffer_capacity: int

  generation_frequency: float
