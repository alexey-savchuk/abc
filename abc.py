import logging
from model import Supervisor
from models.bid import Bid
from models.buffer import Buffer
from models.my_dispatchers import MyBufferingDispatcher, MySelectingDispatcher
from models.my_units import MyGeneratingUnit, MyProcessingUnit


logging.basicConfig(filename='log/abc.log', filemode='w', level=logging.DEBUG)

if __name__ == "__main__":

  buffer = Buffer(10)
  generating_units = [MyGeneratingUnit(unit_id=i) for i in range(1, 16)]
  processing_units = [MyProcessingUnit(unit_id=i) for i in range(1, 11)]
  buffering_dispatcher = MyBufferingDispatcher(buffer)
  selecting_dispatcher = MySelectingDispatcher(processing_units, buffer)

  sv = Supervisor(generating_units, processing_units, buffering_dispatcher, selecting_dispatcher)

  sv.start()
