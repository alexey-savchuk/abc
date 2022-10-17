from dataclasses import dataclass
from datetime import datetime

@dataclass
class Request:

  unit_id: int
  message: str
  generated_at: datetime
# buffered_at: datetime
  processed_at: datetime = None
