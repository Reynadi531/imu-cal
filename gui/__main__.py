# Codename: Sydney
import dearpygui.dearpygui as dpg
import components.config_tab as config_tab
import components.accelerometer_tab as accelerometer_tab
import components.gyroscope_tab as gyroscope_tab

dpg.create_context()
dpg.create_viewport(title="IMU Calibration Tools", width=800, height=600)

with dpg.window(label="IMU Calibration Tools", tag="main_window"):
    with dpg.menu_bar():
        dpg.add_text("IMU Calibration Tools | Custom Made for GY-85 Sensor and Fall Detection Research 2025", tag="title_text")
    with dpg.tab_bar(tag="main_tab_bar"):
        config_tab.create_config_tab()
        accelerometer_tab.create_accelerometer_tab() 
        gyroscope_tab.create_gyroscope_tab()

dpg.set_primary_window("main_window", True)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()