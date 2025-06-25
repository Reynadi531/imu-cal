import dearpygui.dearpygui as dpg
import loader.sensor_formatter as sensor_formatter
import loader.serial_loader as serial_loader
import threading
import calibration.cal_gyroscope as cal_gyro
import time

reading = False
read_thread = None 
recordContinously = False

def _read_Gyroscope_data_thread():
    global reading
    while reading:
        xyzgyro = sensor_formatter.read_sensor_data()['gyroscope']
        dpg.set_value("gyro_x_value", f"{xyzgyro['x']:.2f}")
        dpg.set_value("gyro_y_value", f"{xyzgyro['y']:.2f}")
        dpg.set_value("gyro_z_value", f"{xyzgyro['z']:.2f}")

def cb_start_reading():
    global reading, read_thread
    if read_thread and read_thread.is_alive():
        dpg.set_value("gyro_status_text", "Status: Already Reading")
        return
    if not serial_loader.get_serial_instance().is_open:
        dpg.set_value("gyro_status_text", "Status: Serial Port Not Open")
        return
    if not reading:
        reading = True
        dpg.set_value("gyro_status_text", "Status: Reading...")
        read_thread = threading.Thread(target=_read_Gyroscope_data_thread, daemon=True)
        read_thread.start()

def cb_stop_reading():
    global reading
    reading = False
    if read_thread and read_thread.is_alive():
        read_thread.join(timeout=1)
    sensor_formatter.stop_sensor_reading()
    dpg.set_value("gyro_status_text", "Status: Not Reading")

def cb_read_once_gyro_data():
    gyro_data = sensor_formatter.read_once_gyroscope()
    dpg.set_value("gyro_x_value", f"{gyro_data['x']:.2f}")
    dpg.set_value("gyro_y_value", f"{gyro_data['y']:.2f}")
    dpg.set_value("gyro_z_value", f"{gyro_data['z']:.2f}")

def cb_record_once_gyro_data():
    gyro_data = sensor_formatter.read_once_gyroscope()
    dpg.set_value("gyro_x_value_cal", f"{gyro_data['x']:.2f}")
    dpg.set_value("gyro_y_value_cal", f"{gyro_data['y']:.2f}")
    dpg.set_value("gyro_z_value_cal", f"{gyro_data['z']:.2f}")
    cal_gyro.add_record(gyro_data['x'], gyro_data['y'], gyro_data['z'])
    dpg.set_value("recorded_data_count_gyro", f"Recorded Data: {cal_gyro.count_records()}")

def cb_get_offset():
    offset = cal_gyro.get_offset()
    if offset:
        dpg.set_value("offset_value_input", f"{offset[0]:.2f}, {offset[1]:.2f}, {offset[2]:.2f}")
    else:
        dpg.set_value("offset_value_input", "No records available")

def cb_record_continuously_gyro_data():
    global recordContinously
    count = dpg.get_value("calibration_record_count_gyro")
    print(f"Count: {count}")
    recordContinously = not recordContinously
    for _ in range(count):
        if not recordContinously:
            break
        gyro_data = sensor_formatter.read_once_gyroscope()
        dpg.set_value("gyro_x_value_cal", f"{gyro_data['x']:.2f}")
        dpg.set_value("gyro_y_value_cal", f"{gyro_data['y']:.2f}")
        dpg.set_value("gyro_z_value_cal", f"{gyro_data['z']:.2f}")
        cal_gyro.add_record(gyro_data['x'], gyro_data['y'], gyro_data['z'])
        dpg.set_value("recorded_data_count_gyro", f"Recorded Data: {cal_gyro.count_records()}")
        time.sleep(0.3)

def create_gyroscope_tab():
    with dpg.tab(label="Gyroscope", tag="Gyroscope_tab"):
        with dpg.collapsing_header(label="Gyroscope Data", default_open=True):
            with dpg.group(horizontal=True):
                dpg.add_text("Gyroscope Data:")
                dpg.add_button(label="Read Once", tag="read_once_gyro_data_button", callback=cb_read_once_gyro_data)
                dpg.add_button(label="Start Read", tag="read_gyro_data_button", callback=cb_start_reading)
                dpg.add_button(label="Stop Read", tag="stop_read_gyro_data_button", callback=cb_stop_reading)
                dpg.add_text("Status: Not Reading", tag="gyro_status_text")
            with dpg.collapsing_header(label="Gyroscope Data", default_open=True):
                with dpg.table(tag="gyro_data_table", header_row=True, height=200, width=400):
                    dpg.add_table_column(label="X")
                    dpg.add_table_column(label="Y")
                    dpg.add_table_column(label="Z")
                    with dpg.table_row():
                        dpg.add_text("0.0", tag="gyro_x_value")
                        dpg.add_text("0.0", tag="gyro_y_value")
                        dpg.add_text("0.0", tag="gyro_z_value")
        with dpg.collapsing_header(label="Calibration", default_open=True):
            with dpg.group():
                dpg.add_text("Calibration Data:")
                dpg.add_button(label="Record Once", tag="record_once_gyro_data_button", callback=cb_record_once_gyro_data)
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Record Continuously", tag="record_continuously_gyro_data_button", callback=cb_record_continuously_gyro_data)
                    dpg.add_input_int(label="Number of Records", default_value=100, min_value=1, max_value=1000, tag="calibration_record_count_gyro", width=100)
            with dpg.table(tag="gyro_data_table_cal", header_row=True, height=50, width=400):
                dpg.add_table_column(label="X")
                dpg.add_table_column(label="Y")
                dpg.add_table_column(label="Z")
                with dpg.table_row():
                    dpg.add_text("0.0", tag="gyro_x_value_cal")
                    dpg.add_text("0.0", tag="gyro_y_value_cal")
                    dpg.add_text("0.0", tag="gyro_z_value_cal")
            with dpg.group(horizontal=True):
                dpg.add_text("Recorded Data: 0", tag="recorded_data_count_gyro")
                dpg.add_button(label="Get Offsets", tag="get_offsets_button", callback=cb_get_offset)
            with dpg.group(horizontal=True):
                dpg.add_text("Offeset value: ", tag="offset_value_text")
                dpg.add_input_text(readonly=True, tag="offset_value_input", width=400, default_value="0.0, 0.0, 0.0")