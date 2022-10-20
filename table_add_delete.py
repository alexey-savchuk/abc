import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.set_global_font_scale(1.4)
dpg.create_viewport(title='Coolest table', width=1280, height=720)


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
    with dpg.table(parent="main", header_row=True, policy=dpg.mvTable_SizingStretchProp,
                   borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True,
                   tag="Suffer", row_background=True, scrollY=True):
        for i in range(0, colcount):
            dpg.add_table_column(tag=f"col_{i}", label=f"column {i}")

with dpg.window(tag="main"):
    dpg.add_text("Step by step mode")
    dpg.add_spacer()
    dpg.add_button(tag="add_row_button", label="add row", callback=add_row)

    create_table()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()