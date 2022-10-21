import logging
import random
import dearpygui.dearpygui as dpg
from model import Supervisor

from models.buffer import Buffer
from models.dispatchers import BufferingDispatcher, SelectingDispatcher
from models.units import GeneratingUnit, ProcessingUnit

logging.basicConfig(filename='log/step.log', filemode='w', level=logging.DEBUG)



def stop_action(sender, app_data):
  dpg.configure_item("modal_id", show=False)

num_row = 0

def step_action(sender, app_data, user_data):

    global num_row
    sv = user_data
    time, type, bid = sv.step()

    if num_row == 0:
        with dpg.table_row(tag="row_1", parent="calendar"):

            dpg.add_text(f"{time:.2f}")
            dpg.add_text(type)
            dpg.add_text(bid)
    else:
        with dpg.table_row(tag=f"row_{num_row + 1}", before=f"row_{num_row}"):

            dpg.add_text(f"{time:.2f}")
            dpg.add_text(type)
            dpg.add_text(bid)

    num_row += 1

    dpg.set_value(item="buffer", value="BUFFER: " + str([random.randint(0, 9) for i in range(0, 5)]))


dpg.create_context()


with dpg.window(label="Primary Window", tag="primary-window", width=500, height=500):


    dpg.add_button(label="Start Simulation")

    with dpg.popup(dpg.last_item(), mousebutton=dpg.mvMouseButton_Left, modal=True, tag="modal_id"):

        buffer = Buffer(3)
        generating_units = [GeneratingUnit(unit_id=i) for i in range(1, 4)]
        processing_units = [ProcessingUnit(unit_id=i) for i in range(1, 6)]
        buffering_dispatcher = BufferingDispatcher(buffer)
        selecting_dispatcher = SelectingDispatcher(processing_units, buffer)

        sv = Supervisor(generating_units, processing_units, buffering_dispatcher, selecting_dispatcher)
        sv.start_step_mode()

        dpg.add_button(label="stop", tag="stop-button", callback=stop_action)
        dpg.add_spacer()
        dpg.add_spacer()
        dpg.add_spacer()


        dpg.add_text("SIMULATION:")
        dpg.add_button(label="step", tag="step-button", callback=step_action, user_data=sv)
        dpg.add_text("BUFFER: [1, 2, 3, 4, 5]", tag="buffer")

        with dpg.table(parent="Step by Step", header_row=True, policy=dpg.mvTable_SizingStretchProp,
                        borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True,
                        tag="calendar", row_background=True, scrollY=True, no_host_extendX=True):

            dpg.add_table_column(label="Model Time")
            dpg.add_table_column(label="Event Type")
            dpg.add_table_column(label="Current Bid")





dpg.create_viewport(title='Custom Title', width=600, height=200)

dpg.setup_dearpygui()
dpg.show_viewport()

dpg.set_primary_window(window="primary-window", value=True)

dpg.start_dearpygui()
dpg.destroy_context()
