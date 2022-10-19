import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=600, height=300)

class SavedData:
    devices: int
    sources: int

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

def save(sender, app_data):
    SavedData.devices = Data.devices
    SavedData.sources = Data.sources

    print(SavedData.devices, SavedData.sources)


def show(sender, app_data):
    print(SavedData.devices, SavedData.sources)




with dpg.window(label="Primary", tag="Primary Window"):

  dpg.add_text("Choice", tag="text1")
  dpg.add_input_text(label="num of sources",
                      callback=save_sources_num_button_callback,
                      default_value="0",
                      tag="option1")
  dpg.add_input_text(label="num of devices",
                      callback=save_devices_num_button_callback,
                      default_value="0",
                      tag="option2")
  dpg.add_button(label="save", callback=save, tag="balls_button1")
  dpg.add_button(label="show", callback=show, tag="balls_button2")



dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
