from dataclasses import dataclass


@dataclass
class Bid:

  # Specified by generating unit
  generating_unit_id: int
  generation_time: float

  # Specified by processing unit
  processing_unit_id: int = None
  procession_time: float = None

  # Specified if bid was buffered
  buffered: bool = False
  beffering_time: float = None

  # Specified if bid was refused
  refused: bool = False
  refusion_time: float = None

  def __str__(self) -> str:

    return "Bid[{}, {}, {}, {}, {}, {}, {}, {}]".format(
      self.generating_unit_id, self.generation_time,
      self.processing_unit_id, self.procession_time,
      self.buffered, self.beffering_time,
      self.refused, self.refusion_time)
