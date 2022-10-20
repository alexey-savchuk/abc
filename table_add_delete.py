import random
from typing import Tuple
import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.set_global_font_scale(1.4)
dpg.create_viewport(title='abc', width=1280, height=720)

def outer_api_call() -> Tuple[int]:
    return (random.random(), random.random(), random.random())


NUM_ROWS = 10


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
    print(id)
    dpg.delete_item(f"some_{id}")






with dpg.window(tag="main"):
    dpg.add_text("Step by step mode")
    dpg.add_spacer()
    dpg.add_button(tag="add_row_button", label="step", callback=add_row)

    create_table()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()