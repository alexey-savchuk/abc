import math
from typing import Dict, Iterable

import dearpygui.dearpygui as dpg
from numpy import int16

from app_tags import *
from app_settings import *
from model.auto_mode import StatsRecord

from model.bid import Bid
from model.supervisor import Supervisor


def _save_settings():

    Settings.num_sources = dpg.get_value(item=SETTINGS_NUM_SOURCES)
    Settings.num_devices = dpg.get_value(item=SETTINGS_NUM_DEVICES)
    Settings.buffer_capacity = dpg.get_value(item=SETTINGS_BUFFER_CAPACITY)
    Settings.generation_freq = dpg.get_value(item=SETTINGS_GENERATION_FREQ)
    Settings.min_processing_time = dpg.get_value(item=SETTINGS_MIN_PROCESSING_TIME)
    Settings.max_processing_time = dpg.get_value(item=SETTINGS_MAX_PROCESSING_TIME)
    Settings.max_bids = dpg.get_value(item=SETTINGS_MAX_BIDS)

    if Settings.min_processing_time > Settings.max_processing_time:
        raise ValueError("Invalid input: min. proc. time > max. proc. time")


def _get_supervisor() -> Supervisor:

    supervisor = Supervisor(num_sources=Settings.num_sources,
                            num_devices=Settings.num_devices,
                            buffer_capacity=Settings.buffer_capacity,
                            generation_freq=Settings.generation_freq,
                            min_proc_time=Settings.min_processing_time,
                            max_proc_time=Settings.max_processing_time,
                            num_total_bids=Settings.max_bids)

    return supervisor


num_events = 0
supervisor = None


def _draw_event_calendar_content_block() -> None:

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


def _draw_memory_buffer(bids: Iterable[Bid], pushed: Bid, poped: Bid, refused: Bid) -> None:

    dpg.delete_item(item=MEMORY_BUFFER, children_only=True)

    dpg.set_value(item="pushed_bid", value=pushed)
    dpg.set_value(item="poped_bid", value=poped)
    dpg.set_value(item="refused_bid", value=refused)

    dpg.add_table_column(label="position", parent=MEMORY_BUFFER)
    dpg.add_table_column(label="bid", parent=MEMORY_BUFFER)

    i = 1
    for bid in bids:
        with dpg.table_row(parent=MEMORY_BUFFER):
            dpg.add_text(i)
            dpg.add_text(bid)

        i += 1


def _draw_memory_buffer_content_block() -> None:

    dpg.delete_item(item=MEMORY_BUFFER_CONTENT_BLOCK, children_only=True)

    with dpg.group(parent=MEMORY_BUFFER_CONTENT_BLOCK, horizontal=True):
        dpg.add_text("pushed:")
        dpg.add_text(None, tag="pushed_bid")

    with dpg.group(parent=MEMORY_BUFFER_CONTENT_BLOCK, horizontal=True):
        dpg.add_text("poped:")
        dpg.add_text(None, tag="poped_bid")

    with dpg.group(parent=MEMORY_BUFFER_CONTENT_BLOCK, horizontal=True):
        dpg.add_text("refused:")
        dpg.add_text(None, tag="refused_bid")

    with dpg.table(tag=MEMORY_BUFFER, parent=MEMORY_BUFFER_CONTENT_BLOCK,
                   header_row=True, policy=dpg.mvTable_SizingStretchProp,
                   borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True,
                   row_background=True, scrollY=True, no_host_extendX=True):
        dpg.add_table_column(label="position", parent=MEMORY_BUFFER)
        dpg.add_table_column(label="bid", parent=MEMORY_BUFFER)


def start_step_mode(sender, app_data) -> None:

    try:
        _save_settings()
    except ValueError as err:
        dpg.set_value(item=ERROR_MESSAGE, value=err)
        dpg.configure_item(item=ERROR_WINDOW, show=True)
        return
    except Exception:
        dpg.set_value(item=ERROR_MESSAGE, value=ERROR_DEFAULT_MESSAGE)
        dpg.configure_item(item=ERROR_WINDOW, show=True)
        return

    _draw_event_calendar_content_block()
    _draw_memory_buffer_content_block()

    global supervisor
    supervisor = _get_supervisor()
    supervisor.start_step_mode()

    dpg.configure_item(item=STEP_BUTTON, enabled=True)
    dpg.configure_item(item=STOP_BUTTON, enabled=True)

    dpg.configure_item(item=EVENT_CALENDAR_WINDOW, show=True)
    dpg.configure_item(item=MEMORY_BUFFER_WINDOW, show=True)


def step_action(sender, app_data) -> None:

    global num_events
    global supervisor

    supervisor.step()
    time, event, bid = supervisor.get_event_info()

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

    buffer, pushed, poped, refused = supervisor.get_buffer_info()
    _draw_memory_buffer(buffer, pushed, poped, refused)

    num_events += 1

def stop_action(sender, app_data) -> None:

    global num_events
    global supervisor

    supervisor.end_step_mode()
    supervisor.step()
    time, event, bid = supervisor.get_event_info()

    with dpg.table_row(tag=f"row_{num_events + 1}", before=f"row_{num_events}"):
        dpg.add_text(f"{time:.2f}")
        dpg.add_text(event)
        dpg.add_text(bid)

    dpg.configure_item(item=STEP_BUTTON, enabled=False)
    dpg.configure_item(item=STOP_BUTTON, enabled=False)


def _draw_summary_table_content_block() -> None:

    dpg.delete_item(item=SUMMARY_TABLE_CONTENT_BLOCK, children_only=True)

    with dpg.table(tag=SUMMARY_TABLE, parent=SUMMARY_TABLE_CONTENT_BLOCK,
                   header_row=True, policy=dpg.mvTable_SizingStretchProp,
                   borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True,
                   row_background=True, scrollY=True, no_host_extendX=True):
        dpg.add_table_column(label="source", parent=SUMMARY_TABLE)
        dpg.add_table_column(label="num. bids", parent=SUMMARY_TABLE)
        dpg.add_table_column(label="P", parent=SUMMARY_TABLE)
        dpg.add_table_column(label="E[WT]", parent=SUMMARY_TABLE)
        dpg.add_table_column(label="E[PT]", parent=SUMMARY_TABLE)
        dpg.add_table_column(label="E[TT]", parent=SUMMARY_TABLE)
        dpg.add_table_column(label="V[WT]", parent=SUMMARY_TABLE)
        dpg.add_table_column(label="V[PT]", parent=SUMMARY_TABLE)

def _draw_summary_table(stats: Dict[int, StatsRecord]) -> None:

    dpg.delete_item(item=SUMMARY_TABLE, children_only=True)

    dpg.add_table_column(label="source", parent=SUMMARY_TABLE)
    dpg.add_table_column(label="num. bids", parent=SUMMARY_TABLE)
    dpg.add_table_column(label="P", parent=SUMMARY_TABLE)
    dpg.add_table_column(label="E[WT]", parent=SUMMARY_TABLE)
    dpg.add_table_column(label="E[PT]", parent=SUMMARY_TABLE)
    dpg.add_table_column(label="E[TT]", parent=SUMMARY_TABLE)
    dpg.add_table_column(label="V[WT]", parent=SUMMARY_TABLE)
    dpg.add_table_column(label="V[PT]", parent=SUMMARY_TABLE)

    for unit_id, record in stats.items():
        with dpg.table_row(parent=SUMMARY_TABLE):
            dpg.add_text(unit_id)
            dpg.add_text(record.num_total_bids)

            if record.probability != None:
                dpg.add_text(f"{record.probability:.5f}")
            else:
                dpg.add_text(record.probability)

            waiting_mean = None
            waiting_variance = None
            processing_mean = None
            processing_variance = None

            if record.num_total_bids:
                waiting_mean = record.sum_waiting_time / record.num_total_bids
                waiting_mean_sqr = record.sum_sqr_processing_time / record.num_total_bids
                waiting_variance = waiting_mean_sqr - math.pow(waiting_mean, 2)

                processing_mean = record.sum_processing_time / record.num_total_bids
                processing_mean_sqr = record.sum_sqr_processing_time / record.num_total_bids
                processing_variance = processing_mean_sqr - math.pow(processing_mean, 2)

            if waiting_mean != None:
                dpg.add_text(f"{waiting_mean:.2f}")
            else:
                dpg.add_text(waiting_mean)
            if processing_mean != None:
                dpg.add_text(f"{processing_mean:.2f}")
            else:
                dpg.add_text(processing_mean)
            if waiting_mean != None and processing_mean != None:
                dpg.add_text(f"{waiting_mean + processing_mean:.2f}")
            else:
                dpg.add_text(None)
            if waiting_variance != None:
                dpg.add_text(f"{waiting_variance:.2f}")
            else:
                dpg.add_text(waiting_variance)
            if processing_variance != None:
                dpg.add_text(f"{processing_variance:.2f}")
            else:
                dpg.add_text(processing_variance)

def _draw_device_usage_table_content_block() -> None:

    dpg.delete_item(item=DEVICE_USAGE_TABLE_CONTENT_BLOCK, children_only=True)

    with dpg.table(tag=DEVICE_USAGE_TABLE, parent=DEVICE_USAGE_TABLE_CONTENT_BLOCK,
                   header_row=True, policy=dpg.mvTable_SizingStretchProp,
                   borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True,
                   row_background=True, scrollY=True, no_host_extendX=True):
        dpg.add_table_column(label="device", parent=DEVICE_USAGE_TABLE)
        dpg.add_table_column(label="K", parent=DEVICE_USAGE_TABLE)

def _draw_device_usage_table(stats: Dict[int, float]) -> None:

    dpg.delete_item(item=DEVICE_USAGE_TABLE, children_only=True)

    dpg.add_table_column(label="device", parent=DEVICE_USAGE_TABLE)
    dpg.add_table_column(label="K", parent=DEVICE_USAGE_TABLE)

    for unit_id, K in stats.items():
        with dpg.table_row(parent=DEVICE_USAGE_TABLE):
            dpg.add_text(unit_id)
            dpg.add_text(K)

def start_auto_mode(sender, app_data) -> None:

    try:
        _save_settings()
    except ValueError as err:
        dpg.set_value(item=ERROR_MESSAGE, value=err)
        dpg.configure_item(item=ERROR_WINDOW, show=True)
        return
    except Exception:
        dpg.set_value(item=ERROR_MESSAGE, value=ERROR_DEFAULT_MESSAGE)
        dpg.configure_item(item=ERROR_WINDOW, show=True)
        return

    _draw_summary_table_content_block()
    _draw_device_usage_table_content_block()

    dpg.add_text("processing...", tag="dummy_text1", parent=SUMMARY_TABLE_CONTENT_BLOCK, before=SUMMARY_TABLE)
    dpg.add_text("processing...", tag="dummy_text2", parent=DEVICE_USAGE_TABLE_CONTENT_BLOCK, before=DEVICE_USAGE_TABLE)

    dpg.configure_item(item=SUMMARY_TABLE_WINDOW, show=True)
    dpg.configure_item(item=DEVICE_USAGE_TABLE_WINDOW, show=True)

    global supervisor
    supervisor = _get_supervisor()

    stats, device_stats = supervisor.start_auto_mode()

    dpg.delete_item(item="dummy_text1")
    dpg.delete_item(item="dummy_text2")
    _draw_summary_table(stats)
    _draw_device_usage_table(device_stats)

