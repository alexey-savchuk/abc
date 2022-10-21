import random
from typing import Tuple
import dearpygui.dearpygui as dpg

class Data:
    devices: int = 0
    sources: int = 0
    buffer: int = 0
    way: str = "step"

    _devices_saved: int
    _sources_saved: int
    _buffer_saved: int
    _way_saved: str

    @staticmethod
    def save():
        Data._devices_saved = Data.devices
        Data._sources_saved = Data.sources
        Data._buffer_saved = Data.buffer
        Data._way_saved = Data.way


    @staticmethod
    def show():
        print(f"{Data._devices_saved} - {Data._sources_saved} - {Data._buffer_saved} - {Data._way_saved} ")

# костыль
Data.save()

def save_devices_num_button_callback(sender, app_data):
    try:
        Data.devices = int(app_data)
    except ValueError:
        print("NOT VALID")


def save_sources_num_button_callback(sender, app_data):
    try:
        Data.sources = int(app_data)
    except ValueError:
        print("NOT VALID")

def save_buffer_num_button_callback(sender, app_data):
    try:
        Data.buffer = int(app_data)
    except ValueError:
        print("NOT VALID")

def set_way_callback(sender, app_data):
    Data.way = app_data
    print(Data.way)

def outer_api_call() -> Tuple[int]:
    return (random.random(), random.random(), random.random())


NUM_ROWS = 20


tag_r_id = 0
id_fd = 0
rws_cnt = 0
def add_row():
    global rows
    global tag_r_id
    global id_fd
    global rws_cnt

    rws_cnt += 1

    if rws_cnt > NUM_ROWS:
        delete_row(id_fd)
        id_fd += 1

    with dpg.table_row(parent="Suffer", tag=f"some_{tag_r_id}"):

        for i in range(0, columns):
            value = random.random()
            dpg.add_text(f"data = {value:.2f}")

    rows += 1
    tag_r_id += 1


def create_table(colcount=3, rowcount=NUM_ROWS):
    global columns
    global rows

    columns = colcount
    rows = 0
    with dpg.table(parent="Step by Step", header_row=True, policy=dpg.mvTable_SizingStretchProp,
                   borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True,
                   tag="Suffer", row_background=True, scrollY=True, no_host_extendX=True):
        for i in range(0, colcount):
            dpg.add_table_column(tag=f"col_{i}", label=f"column {i}")

        for i in range(rowcount):
            add_row()

def delete_row(id):
    dpg.delete_item(f"some_{id}")

dpg.create_context()
dpg.set_global_font_scale(1.4)
dpg.create_viewport(title='Custom Title', width=600, height=720)

with dpg.window(label="Example Window", tag="Primary Window"):
    dpg.add_input_text(label="sources",
                       callback=save_sources_num_button_callback,
                       default_value="0",
                       width=200)
    dpg.add_input_text(label="devices",
                       callback=save_devices_num_button_callback,
                       default_value="0",
                       width=200)
    dpg.add_input_text(label="buffer",
                       callback=save_buffer_num_button_callback,
                       default_value="0",
                       width=200)

    dpg.add_text("ways")
    dpg.add_radio_button(label="Ways",
                         items=["step", "auto"],
                         callback=set_way_callback)
    dpg.add_text("Commands")
    dpg.add_button(label="Show currnet data",
                   callback=Data.show)
    dpg.add_button(label="Save data",
                   callback=Data.save)

    dpg.add_spacer()
    dpg.add_button(label="Start model")
    with dpg.popup(dpg.last_item(), modal=True, mousebutton=dpg.mvMouseButton_Left, tag="main",
                   no_move=True, min_size=[600,690]):
        dpg.add_text("Step by step mode")
        dpg.add_spacer()
        dpg.add_button(tag="add_row_button", label="step", callback=add_row)

        create_table()



dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()