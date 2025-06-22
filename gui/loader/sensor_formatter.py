import serial
import loader.serial_loader as serial_loader

serial_instance: serial = serial_loader.get_serial_instance()

def read_accelerometer_data():
    if serial_instance.is_open:
        try:
            data = serial_instance.readline().decode('utf-8').strip()
            data = data.split(';')[0]
            x, y, z = map(float, data.split(','))
            return {'x': x, 'y': y, 'z': z}
        except Exception as e:
            print(f"Error reading accelerometer data: {e}")
            return None
    else:
        print("Serial port is not open.")
        return None