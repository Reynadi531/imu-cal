import serial
import loader.serial_loader as serial_loader

serial_instance: serial = serial_loader.get_serial_instance()

sensor = {
    'accelerometer': {
        'x': 0.0,
        'y': 0.0,
        'z': 0.0
    },
   'gyroscope': {
        'x': 0.0,
        'y': 0.0,
        'z': 0.0
    },
}

def read_sensor_data() -> dict:
    if serial_instance.is_open:
        try:
            data = serial_instance.readline().decode('utf-8').strip()
            data_parts = data.split(';')
            if len(data_parts) == 2:
                accel_data = data_parts[0].split(',')
                gyro_data = data_parts[1].split(',')
                sensor['accelerometer']['x'] = float(accel_data[0])
                sensor['accelerometer']['y'] = float(accel_data[1])
                sensor['accelerometer']['z'] = float(accel_data[2])
                sensor['gyroscope']['x'] = float(gyro_data[0])
                sensor['gyroscope']['y'] = float(gyro_data[1])
                sensor['gyroscope']['z'] = float(gyro_data[2])
                return sensor
            else:
                print("Invalid data format received.")
                return sensor
        except Exception as e:
            print(f"Error reading sensor data: {e}")
            return sensor
    else:
        print("Serial port is not open.")
        return sensor
