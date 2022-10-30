#!/bin/python3

import logging
import dearpygui.dearpygui as dpg
from app_actions import step_action, start_auto_mode, start_step_mode, stop_action


from app_tags import *


logging.basicConfig(filename='app.log', filemode='w', level=logging.DEBUG)


dpg.create_context()
dpg.set_global_font_scale(1.2)


with dpg.window(tag="primary-window"):

    dpg.add_text("GENERAL SETTINGS")

    dpg.add_separator()
    with dpg.group(horizontal=True):
        dpg.add_slider_int(tag=SETTINGS_NUM_SOURCES,
                          default_value=10,
                          min_value=1,
                          max_value=20,
                          format="sources = %d",
                          width=400, height=10)

        dpg.add_slider_int(tag=SETTINGS_NUM_DEVICES,
                          default_value=10,
                          min_value=1,
                          max_value=20,
                          format="devices = %d",
                          width=400, height=10)

        dpg.add_slider_int(tag=SETTINGS_BUFFER_CAPACITY,
                          default_value=10,
                          min_value=1,
                          max_value=20,
                          format="buffer size = %d",
                          width=400, height=10)


    dpg.add_separator()
    dpg.add_text("ADVANCED SETTINGS")
    dpg.add_spacer()
    dpg.add_separator()
    dpg.add_text("REQUEST")
    dpg.add_slider_float(tag=SETTINGS_GENERATION_FREQ,
                        default_value=0.1,
                        min_value=0.1,
                        max_value=10,
                        format="generation frequency = %.1f",
                        width=1215, height=10)
    dpg.add_separator()
    dpg.add_spacer()
    dpg.add_text("PROCESSING TIME")
    dpg.add_slider_float(tag=SETTINGS_MIN_PROCESSING_TIME,
                        default_value=20.0,
                        min_value=1.0,
                        max_value=100.0,
                        format="min = %.1f",
                        width=1215, height=10)
    dpg.add_slider_float(tag=SETTINGS_MAX_PROCESSING_TIME,
                        default_value=80.0,
                        min_value=1.0,
                        max_value=100.0,
                        format="max = %.1f",
                        width=1215, height=10)
    dpg.add_separator()
    dpg.add_spacer()
    dpg.add_text("REQUESTS !!!ONLY FOR STEP MODE!!!")
    dpg.add_slider_int(
                      tag=SETTINGS_MAX_BIDS,
                      default_value=100,
                      min_value=10,
                      max_value=1000,
                      format="max number = %d",
                        width=1215, height=10)
    dpg.add_separator()

    with dpg.window(label="Error", tag=ERROR_WINDOW, modal=True, show=False):
        dpg.add_text(ERROR_DEFAULT_MESSAGE, tag=ERROR_MESSAGE)


    dpg.add_spacer()
    with dpg.group(horizontal=True):
        dpg.add_button(label="start step mode", callback=start_step_mode)
        dpg.add_button(label="start auto mode", callback=start_auto_mode)

    with dpg.child_window(label="Event Calendar",
                    tag=EVENT_CALENDAR_WINDOW,
                    show=False,
                    width=1000, height=410,
                    pos=(0, 380)):

        with dpg.group(horizontal=True):
            dpg.add_button(label="step", tag=STEP_BUTTON, callback=step_action)
            dpg.add_button(label="stop", tag=STOP_BUTTON, callback=stop_action, show=False)

        dpg.add_spacer()
        dpg.add_group(tag=EVENT_CALENDAR_CONTENT_BLOCK)

    with dpg.child_window(label="Memory Buffer",
                    tag=MEMORY_BUFFER_WINDOW,
                    show=False,
                    width=1460 - 1000, height=410,
                    pos=(1000, 380)):

        dpg.add_group(tag=MEMORY_BUFFER_CONTENT_BLOCK)

    with dpg.child_window(label="Summary Table",
                    tag=SUMMARY_TABLE_WINDOW,
                    show=False,
                    width=740, height=410,
                    pos=(0, 380)):

        dpg.add_group(tag=SUMMARY_TABLE_CONTENT_BLOCK)

    with dpg.child_window(label="Device Usage",
                    tag=DEVICE_USAGE_TABLE_WINDOW,
                    show=False,
                    width=740, height=410,
                    pos=(740, 380)):

        dpg.add_group(tag=DEVICE_USAGE_TABLE_CONTENT_BLOCK)


with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (145, 93, 93), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (1, 255, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

    with dpg.theme_component(dpg.mvInputInt):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (145, 93, 93), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

dpg.bind_theme(global_theme)

dpg.set_primary_window(window="primary-window", value=True)

dpg.create_viewport(title='abc', width=1480, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()

dpg.start_dearpygui()
dpg.destroy_context()
