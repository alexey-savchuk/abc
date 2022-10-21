
import logging
from model import Supervisor
from models.buffer import Buffer
from models.dispatchers import BufferingDispatcher, SelectingDispatcher
from models.units import GeneratingUnit, ProcessingUnit


logging.basicConfig(filename='log/step.log', filemode='w', level=logging.DEBUG)


buffer = Buffer(3)
generating_units = [GeneratingUnit(unit_id=i) for i in range(1, 4)]
processing_units = [ProcessingUnit(unit_id=i) for i in range(1, 6)]
buffering_dispatcher = BufferingDispatcher(buffer)
selecting_dispatcher = SelectingDispatcher(processing_units, buffer)

sv = Supervisor(generating_units, processing_units, buffering_dispatcher, selecting_dispatcher)
sv.start_step_mode()


ENTER = ""
key_pressed = input("Press ENTER to start simulation")

while key_pressed == ENTER:
  sv.step()
  key_pressed = input("Press ENTER to continue or enter any character to abort")

  if key_pressed != ENTER:
    sv.end()
    sv.step()

print("Simulation aborted")
