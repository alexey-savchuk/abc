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
            stock_datax = []
            stock_datay2 = []
            stock_data1 = []
            stock_data2 = []
            stock_data3 = []
            stock_data4 = []
            stock_data5 = []
            for i in range(100):
                stock_datax.append(i)
                stock_datay2.append(0)
                stock_data1.append(400)
                stock_data2.append(275)
                stock_data3.append(150)
                stock_data4.append(500)
                stock_data5.append(600)

            with dpg.theme(tag="stock_theme1"):
                with dpg.theme_component(0):
                    dpg.add_theme_color(dpg.mvPlotCol_Line, (0, 0, 255), category=dpg.mvThemeCat_Plots)
                    dpg.add_theme_color(dpg.mvPlotCol_Fill, (0, 0, 255, 64), category=dpg.mvThemeCat_Plots)

            with dpg.theme(tag="stock_theme2"):
                with dpg.theme_component(0):
                    dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 0, 0), category=dpg.mvThemeCat_Plots)
                    dpg.add_theme_color(dpg.mvPlotCol_Fill, (255, 0, 0, 64), category=dpg.mvThemeCat_Plots)

            with dpg.theme(tag="stock_theme3"):
                with dpg.theme_component(0):
                    dpg.add_theme_color(dpg.mvPlotCol_Line, (0, 255, 0), category=dpg.mvThemeCat_Plots)
                    dpg.add_theme_color(dpg.mvPlotCol_Fill, (0, 255, 0, 64), category=dpg.mvThemeCat_Plots)

            with dpg.theme(tag="stock_theme4"):
                with dpg.theme_component(0):
                    dpg.add_theme_color(dpg.mvPlotCol_Fill, (255, 255, 100, 64), category=dpg.mvThemeCat_Plots)

            with dpg.plot(label="Stock Prices", height=400, width=-1):
                dpg.add_plot_legend()
                xaxis = dpg.add_plot_axis(dpg.mvXAxis, label="Days")
                with dpg.plot_axis(dpg.mvYAxis, label="Price"):
                    dpg.add_line_series(stock_datax, stock_data1, label="Stock 1")
                    dpg.bind_item_theme(dpg.last_item(), "stock_theme1")
                    dpg.add_line_series(stock_datax, stock_data2, label="Stock 2")
                    dpg.bind_item_theme(dpg.last_item(), "stock_theme2")
                    dpg.add_line_series(stock_datax, stock_data3, label="Stock 3")
                    dpg.bind_item_theme(dpg.last_item(), "stock_theme3")
                    dpg.add_shade_series(stock_datax, stock_data1, label="Stock 1")
                    dpg.bind_item_theme(dpg.last_item(), "stock_theme1")
                    dpg.add_shade_series(stock_datax, stock_data2, label="Stock 2")
                    dpg.bind_item_theme(dpg.last_item(), "stock_theme2")
                    dpg.add_shade_series(stock_datax, stock_data3, label="Stock 3", y2=stock_datay2)
                    dpg.bind_item_theme(dpg.last_item(), "stock_theme3")
                    dpg.add_shade_series(stock_datax, stock_data5, y2=stock_data4, label="Shade between lines")
                    dpg.bind_item_theme(dpg.last_item(), "stock_theme4")
                    dpg.fit_axis_data(dpg.top_container_stack())
                dpg.fit_axis_data(xaxis)

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