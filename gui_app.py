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

        with dpg.tab(label="logger"):
            pass


dpg.create_viewport(title='Custom Title', width=400, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()