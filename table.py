from typing import List
import dearpygui.dearpygui as dpg


dpg.create_context()


class MyRow:

    def __init__(self, cells: List[int | str]) -> None:
      self.cells = cells

    def put_cell(self, cell: int | str) -> None:
      self.cells.append(cell)

    def get_all_cells(self) -> List[int | str]:
      return self.cells

    def __str__(self) -> str:
        return str(self.cells)


def do_action(sender, app_data, user_data):

  x = 0

  print(user_data)

  for row in user_data:
    for cell in row.get_all_cells():
      dpg.set_value(cell, f"some-text-{x}")
      x += 1

  # for row in user_data:
    # dpg.set_value(row, "new text")


with dpg.window(label="Main Window", tag="main-window", width=500, height=500):

  lst = []

  with dpg.table(header_row=False):
    # use add_table_column to add columns to the table,
    # table columns use child slot 0
    dpg.add_table_column()
    dpg.add_table_column()
    dpg.add_table_column()

    # add_table_next_column will jump to the next row
    # once it reaches the end of the columns
    # table next column use slot 1
    for i in range(0, 4):

        with dpg.table_row():

            my_row = MyRow([])

            for j in range(0, 3):
                text = dpg.add_text(f"Row{i} Column{j}")
                print(text, dpg.get_value(text))
                my_row.put_cell(text)

            print(my_row)
            lst.append(my_row)

  dpg.add_button(label="Do action", tag="action-button", user_data=lst, callback=do_action)


dpg.create_viewport(title='Custom Title', width=600, height=200)

dpg.setup_dearpygui()
dpg.show_viewport()

dpg.set_primary_window(window="main-window", value=True)

dpg.start_dearpygui()
dpg.destroy_context()
