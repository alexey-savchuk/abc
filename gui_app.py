import dearpygui.dearpygui as dpg
dpg.create_context()


class Data:
    devices: int
    sources: int
    way: str


def button_callback(sender, app_data, user_data):
    print(f"devices is: {Data.devices}")
    print(f"sources is: {Data.sources}")
    print(f"way is: {Data.way}")


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


def set_way_callback(sender, app_data):
    Data.way = app_data
    print(Data.way)


def do_some():
    print("some")

def add_row():
    global rows
    with dpg.table_row(parent="Suffer"):
        for i in range(0, columns):
            dpg.add_text(f"row{rows} column{i}", tag=f"cell_{rows}{i}")
            dpg.bind_item_handler_registry(f"cell_{rows}{i}", f"cell_handler_{rows}{i}")
    rows += 1


def create_table(colcount=3, rowcount=0):
    global columns
    global rows
    columns = colcount
    rows = 0
    with dpg.table(parent="lmao", header_row=True, policy=dpg.mvTable_SizingStretchProp,
                   borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True,
                   tag="Suffer", row_background=True, scrollY=True):
        for i in range(0, colcount):
            dpg.add_table_column(tag=f"col_{i}", label=f"column {i}")


with dpg.window(label="Primary", tag="Primary Window"):
    with dpg.tab_bar(label="tabs"):
        with dpg.tab(label="data"):
            dpg.add_text("Choice")
            dpg.add_input_text(label="num of sources",
                               callback=save_sources_num_button_callback,
                               default_value="0")
            dpg.add_input_text(label="num of devices",
                               callback=save_devices_num_button_callback,
                               default_value="0")

            dpg.add_text("Slider")
            dpg.add_slider_int(label="num of sources",
                               callback=save_sources_num_button_callback,
                               min_value=1,
                               max_value=10)
            dpg.add_slider_int(label="num of devices",
                               callback=save_devices_num_button_callback,
                               min_value=1,
                               max_value=10)

            dpg.add_text("ways")
            dpg.add_radio_button(label="Ways",
                                 items=["step", "auto"],
                                 callback=set_way_callback)
        with dpg.tab(label="actions"):
            dpg.add_button(label="Show data",
                           callback=button_callback)
            dpg.add_button(label="Some",
                           callback=do_some)

        with dpg.tab(label="plot"):
            dpg.add_simple_plot(label="Simpleplot1", default_value=(0.3, 0.9, 0.5, 0.3), height=300)
            dpg.add_simple_plot(label="Simpleplot2", default_value=(0.3, 0.9, 2.5, 8.9), overlay="Overlaying",
                                height=180,
                                histogram=True)

        with dpg.tab(label="logger", tag="lmao"):
            dpg.add_text("Step by step mode")
            dpg.add_spacer()
            dpg.add_button(tag="add_row_button", label="add row", callback=add_row)
            create_table()


dpg.create_viewport(title='Custom Title', width=400, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()