from dataclasses import dataclass
import dearpygui.dearpygui as dpg

from app_tags import *
from model import Supervisor
from models.buffer import Buffer
from models.dispatchers import BufferingDispatcher, SelectingDispatcher
from models.units import GeneratingUnit, ProcessingUnit


class Settings:
    num_sources: int
    num_devices: int
    buffer_capacity: int


def _save_settings():
    Settings.num_sources = dpg.get_value(item=SETTINGS_NUM_SOURCES)
    Settings.num_devices = dpg.get_value(item=SETTINGS_NUM_DEVICES)
    Settings.buffer_capacity = dpg.get_value(item=SETTINGS_BUFFER_CAPACITY)


def _get_supervisor() -> Supervisor:

    generating_units = [GeneratingUnit(i + 1) for i in range(Settings.num_sources)]
    processing_units = [ProcessingUnit(i + 1) for i in range(Settings.num_devices)]

    buffer = Buffer(Settings.buffer_capacity)

    buffering_dispatcher = BufferingDispatcher(buffer)
    selecting_dispatcher = SelectingDispatcher(processing_units, buffer)

    supervisor = Supervisor(generating_units, processing_units,
                            buffering_dispatcher, selecting_dispatcher)

    return supervisor


num_events = 0
supervisor = None


def _create_event_calendar_content_block() -> None:

    global num_events
    num_events = 0

    dpg.delete_item(item=EVENT_CALENDAR_CONTENT_BLOCK, children_only=True)

    with dpg.table(tag=EVENT_CALENDAR, parent=EVENT_CALENDAR_CONTENT_BLOCK,
                   header_row=True, policy=dpg.mvTable_SizingStretchProp,
                   borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True,
                   row_background=True, scrollY=True, no_host_extendX=True):

        dpg.add_table_column(label="model time")
        dpg.add_table_column(label="event type")
        dpg.add_table_column(label="current bid")


def _create_memory_buffer_content_block() -> None:

    dpg.delete_item(item=MEMORY_BUFFER_CONTENT_BLOCK, children_only=True)

    # with dpg.table(tag="refused_table", parent=MEMORY_BUFFER_CONTENT_BLOCK,
    #                header_row=True, policy=dpg.mvTable_SizingStretchProp,
    #                borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True,
    #                row_background=True, scrollY=True, no_host_extendX=True):
    #     dpg.add_table_column(label="refused bid")

    #     with dpg.table_row(tag="refused_bid"):
    #         dpg.add_text("")

    # dpg.add_separator(parent=MEMORY_BUFFER_CONTENT_BLOCK)

    with dpg.table(tag=MEMORY_BUFFER, parent=MEMORY_BUFFER_CONTENT_BLOCK,
                   header_row=True, policy=dpg.mvTable_SizingStretchProp,
                   borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True,
                   row_background=True, scrollY=True, no_host_extendX=True):

        dpg.add_table_column(label="position")
        dpg.add_table_column(label="bid")

        for i in range(Settings.buffer_capacity):
            with dpg.table_row(tag=f"mem_{i}"):
                dpg.add_text(i + 1)
                dpg.add_text("")


def start_step_mode(sender, app_data) -> None:

    _save_settings()
    _create_event_calendar_content_block()
    _create_memory_buffer_content_block()

    global supervisor
    supervisor = _get_supervisor()
    supervisor.start_step_mode()

    dpg.configure_item(item=EVENT_CALENDAR_WINDOW, show=True)
    dpg.configure_item(item=MEMORY_BUFFER_WINDOW, show=True)


def add_row(sender, app_data) -> None:

    global num_events
    global supervisor

    time, event, bid, buffer = supervisor.step()

    if num_events == 0:
        with dpg.table_row(tag="row_1", parent=EVENT_CALENDAR):

            dpg.add_text(f"{time:.2f}")
            dpg.add_text(event)
            dpg.add_text(bid)
    else:
        with dpg.table_row(tag=f"row_{num_events + 1}", before=f"row_{num_events}"):

            dpg.add_text(f"{time:.2f}")
            dpg.add_text(event)
            dpg.add_text(bid)

    print(buffer)

    num_events += 1









































def start_auto_mode(sender, app_data) -> None:

    dpg.delete_item(item="auto_mode_data", children_only=True)
    dpg.configure_item(item="auto_mode_window", show=True)