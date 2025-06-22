import dearpygui.dearpygui as dpg
import loader.serial_loader as ser

config = {}

def refresh_serial_ports():
    port_list = ser.get_listed_serial_ports()
    dpg.configure_item("serial_port_dropdown", items=port_list, default_value=port_list[0] if port_list else "No Ports Available")

def dropdown_serial_ports():
    port_list = ser.get_listed_serial_ports()
    with dpg.group(horizontal=True):
        dpg.add_text("Available Ports:")
        dpg.add_combo(port_list, tag="serial_port_dropdown", width=200, default_value=port_list[0] if port_list else "No Ports Available", callback=lambda s, a: len(port_list) > 0 if ser.set_serial_config(port=a) else None)
        dpg.add_button(label="Refresh", tag="refresh_ports_button", callback=refresh_serial_ports)

def cb_connect_serial():
    port = dpg.get_value("serial_port_dropdown")
    baud_rate = dpg.get_value("baud_rate_input")
    timeout = dpg.get_value("timeout_input")
    print(port, baud_rate, timeout)
    if port == "No Ports Available" or not port:
        dpg.set_value("serial_status_text", "Status: No Ports Available")
        return

    ser.set_serial_config(port, baud_rate, timeout)
    if ser.connect_serial():
        dpg.set_value("serial_status_text", f"Status: Connected to {port} at {baud_rate} baud")
    else:
        dpg.set_value("serial_status_text", "Status: Connection Failed")

def cb_disconnect_serial():
    if ser.get_connection_status():
        ser.disconnect_serial()
        dpg.set_value("serial_status_text", "Status: Disconnected")
    else:
        dpg.set_value("serial_status_text", "Status: Nothing to be Disconnected")

def create_config_tab():
    with dpg.tab(label="Configuration", tag="config_tab"):
        dropdown_serial_ports() 

        with dpg.group(horizontal=True):
            dpg.add_text("Baud Rate:")
            dpg.add_input_int(tag="baud_rate_input", default_value=115200, width=100, callback=lambda s, a: ser.set_serial_config(baudrate=a))
        
        with dpg.group(horizontal=True):
            dpg.add_text("Timeout (s):")
            dpg.add_input_float(tag="timeout_input", default_value=1.0, width=100, callback=lambda s, a: ser.set_serial_config(timeout=a))
        
        with dpg.group(horizontal=True):
            dpg.add_button(label="Connect", tag="connect_serial_button", callback=cb_connect_serial)
            dpg.add_button(label="Disconnect", tag="disconnect_serial_button", callback=cb_disconnect_serial)
        dpg.add_text("Status: Not Connected", tag="serial_status_text")
        