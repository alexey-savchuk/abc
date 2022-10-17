import logging
from model import Supervisor
from models.dispatchers.selecting_dispatcher import SelectingDispatcher
from models.units.generating_unit import *
from models.dispatchers.buffering_dispatcher import *
from models.units.processing_unit import ProcessingUnit


logging.basicConfig(filename='abc.log', filemode='w', level=logging.DEBUG)

def func():

  generating_units = [GeneratingUnit() for i in range(0, 10)]
  processing_units = [ProcessingUnit() for i in range(0, 10)]
  selecting_dispatcher = SelectingDispatcher(processing_units)

  sv = Supervisor(generating_units, None, selecting_dispatcher)

  sv.do_work()

if __name__ == "__main__":
  func()
