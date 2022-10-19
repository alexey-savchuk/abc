from dearpygui.dearpygui import *


create_context()

i = 0

def handler(sender, data):
    print("Handler invoced")

    global text, i
    text = add_text(f"Some Text {i}", before="button-2", tag=f"some-text-{i}")
    i += 1


def empty_handler(sender, data):
    delete_item("some-text-1")


with window(label="Window 1", tag="window-1", width=520, height=677):
    add_button(label="Button 1", tag="button-1", callback=handler)
    add_button(label="Button 2", tag="button-2", callback=empty_handler)


create_viewport(title='My Application', width=400, height=600)
setup_dearpygui()

show_viewport()

set_primary_window("window-1", True)

start_dearpygui()
