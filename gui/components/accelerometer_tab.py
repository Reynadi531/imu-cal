import dearpygui.dearpygui as dpg
import loader.sensor_formatter as sensor_formatter
import threading
import time # For simulating sensor reading delay

reading = False
read_thread = None # To hold the reference to the reading thread

def _read_accelerometer_data_thread():
    global reading
    while reading:
        xyzAccel = sensor_formatter.read_accelerometer_data()
        dpg.set_value("accel_x_value", f"{xyzAccel['x']:.2f}")
        dpg.set_value("accel_y_value", f"{xyzAccel['y']:.2f}")
        dpg.set_value("accel_z_value", f"{xyzAccel['z']:.2f}")
        # time.sleep(0.1) 

def cb_start_reading():
    global reading, read_thread
    if not reading:
        reading = True
        dpg.set_value("accel_status_text", "Status: Reading...")
        read_thread = threading.Thread(target=_read_accelerometer_data_thread, daemon=True)
        read_thread.start()

def cb_stop_reading():
    global reading
    reading = False
    if read_thread and read_thread.is_alive():
        read_thread.join(timeout=1)
    dpg.set_value("accel_status_text", "Status: Not Reading")
    dpg.set_value("accel_x_value", "0.0")
    dpg.set_value("accel_y_value", "0.0")
    dpg.set_value("accel_z_value", "0.0")

def create_accelerometer_tab():
    with dpg.tab(label="Accelerometer", tag="accelerometer_tab"):
        with dpg.group(horizontal=True):
            dpg.add_text("Accelerometer Data:")
            dpg.add_button(label="Start Read", tag="read_accel_data_button", callback=cb_start_reading)
            dpg.add_button(label="Stop Read", tag="stop_read_accel_data_button", callback=cb_stop_reading)
        dpg.add_text("Status: Not Reading", tag="accel_status_text")
        with dpg.table(tag="accel_data_table", header_row=True, height=200, width=400):
            dpg.add_table_column(label="X")
            dpg.add_table_column(label="Y")
            dpg.add_table_column(label="Z")
            with dpg.table_row():
                dpg.add_text("0.0", tag="accel_x_value")
                dpg.add_text("0.0", tag="accel_y_value")
                dpg.add_text("0.0", tag="accel_z_value")
        