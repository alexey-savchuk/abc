import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.set_global_font_scale(1.4)
dpg.create_viewport(title='Coolest table', width=1280, height=720)

tag_r_id = 0
id_fd = 0
rws_cnt = 0
def add_row():
    global rows
    global tag_r_id
    global id_fd
    global rws_cnt

    rws_cnt += 1

    if rws_cnt > 9:
        delete_row(id_fd)
        id_fd += 1

    with dpg.table_row(parent="Suffer", tag=f"some_{tag_r_id}"):
        for i in range(0, columns):
            dpg.add_text(f"row{rows} column{i}", tag=f"cell_{rows}{i}")
            dpg.bind_item_handler_registry(f"cell_{rows}{i}", f"cell_handler_{rows}{i}")
    rows += 1
    tag_r_id += 1


def create_table(colcount=3, rowcount=8):
    global columns
    global rows

    columns = colcount
    rows = 0
    with dpg.table(parent="main", header_row=True, policy=dpg.mvTable_SizingStretchProp,
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
    dpg.add_button(tag="add_row_button", label="add row", callback=add_row)
    dpg.add_button(tag="delete_row_button", label="delete row", callback=delete_row)

    create_table()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()