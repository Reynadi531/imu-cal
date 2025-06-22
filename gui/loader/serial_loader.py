import serial
import serial.tools
import serial.tools.list_ports
import yaml
import os

config = {
    'serial': {
        'port': None,
        'baudrate': None,
        'timeout': None 
    }
}

if not os.path.exists(os.path.join(os.path.dirname(__file__), '../config.yaml')):
    open(os.path.join(os.path.dirname(__file__), '../config.yaml'), 'w')

with open(os.path.join(os.path.dirname(__file__), '../config.yaml'), 'r') as file:
    config = yaml.safe_load(file)

ser = serial.Serial()

def connect_serial():
    with open(os.path.join(os.path.dirname(__file__), '../config.yaml'), 'r') as file:
        config = yaml.safe_load(file)

    try:
        ser.port = config['serial']['port']
        ser.baudrate = config['serial']['baudrate']
        ser.timeout = config['serial']['timeout']
        ser.open()
        print(f"Connected to {ser.port} at {ser.baudrate} baud.")
    except serial.SerialException as e:
        print(f"Error connecting to serial port: {e}")
    
    return ser.is_open

    
def disconnect_serial():
    ser.close()
    if not ser.is_open:
        print("Serial port disconnected successfully.")

def get_serial_instance():
    return ser

def set_serial_config(port=None, baudrate=None, timeout=None):
    if port is not None:
        ser.port = port
    if baudrate is not None:
        ser.baudrate = baudrate
    if timeout is not None:
        ser.timeout = timeout
    
    config['serial']['port'] = ser.port
    config['serial']['baudrate'] = ser.baudrate
    config['serial']['timeout'] = ser.timeout
    with open(os.path.join(os.path.dirname(__file__), '../config.yaml'), 'w') as file:
        yaml.safe_dump(config, file)

    print(f"Serial configuration set to: {ser.port}, {ser.baudrate}, {ser.timeout}")

def get_connection_status():
    return ser.is_open

def get_listed_serial_ports():
    ports = serial.tools.list_ports.comports()
    port_list = [port.device for port in ports]
    return port_list
