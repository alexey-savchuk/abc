from dataclasses import dataclass


@dataclass
class Bid:

    # Specified by generating unit
    generating_unit_id: int
    generation_time: float

    # Specified by processing unit
    processing_unit_id: int = 0
    procession_time: float = 0

    # Specified if bid was buffered
    buffered: bool = False
    beffering_time: float = 0

    # Specified if bid was refused
    refused: bool = False
    refusion_time: float = 0

    def __str__(self) -> str:

        gunit = self.generating_unit_id
        gtime = self.generation_time
        punit = self.processing_unit_id
        ptime = self.procession_time
        bflag = self.buffered
        btime = self.beffering_time
        rflag = self.refused
        rtime = self.refusion_time

        return f"Bid[{gunit}, {gtime:.2f}, {punit}, {ptime:.2f}]" #, {bflag}, {btime:.2f}, {rflag}, {rtime:.2f}]"
