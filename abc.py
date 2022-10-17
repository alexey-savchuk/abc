import logging
from model import Supervisor
from models.my_dispatchers import MySelectingDispatcher
from models.my_units import MyGeneratingUnit


logging.basicConfig(filename='abc.log', filemode='w', level=logging.DEBUG)

if __name__ == "__main__":

  generating_units = [MyGeneratingUnit(id=i) for i in range(1, 11)]
  selecting_dispatcher = MySelectingDispatcher()

  sv = Supervisor(generating_units, selecting_dispatcher)

  sv.start()
