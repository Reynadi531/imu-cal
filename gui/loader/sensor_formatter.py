import serial
import loader.serial_loader as serial_loader

serial_instance: serial.Serial = serial_loader.get_serial_instance()

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

accelerometer_data = {
    'x': 0.0,
    'y': 0.0,
    'z': 0.0
}

gyroscope_data = {
    'x': 0.0,
    'y': 0.0,
    'z': 0.0
}

def read_once_gyroscope():
    global gyroscope_data
    global serial_instance
    if serial_instance.is_open:
        try:
            serial_instance.write("gd\n".encode('utf-8'))
            data = serial_instance.readline().decode('utf-8').strip()
            gyro_data = data.split(',')
            print(gyro_data)
            gyroscope_data['x'] = float(gyro_data[0])
            gyroscope_data['y'] = float(gyro_data[1])
            gyroscope_data['z'] = float(gyro_data[2])
            return gyroscope_data
        except Exception as e:
            print(f"Error reading gyroscope data: {e}")
            return gyroscope_data
    else:
        print("Serial port is not open.")
        return gyroscope_data

def read_once_accelerometer(): 
    global accelerometer_data
    global serial_instance
    if serial_instance.is_open:
        try:
            serial_instance.write("ad\n".encode('utf-8'))
            data = serial_instance.readline().decode('utf-8').strip()
            accel_data = data.split(',')
            print(accel_data)
            accelerometer_data['x'] = float(accel_data[0])
            accelerometer_data['y'] = float(accel_data[1])
            accelerometer_data['z'] = float(accel_data[2])
            return accelerometer_data
        except Exception as e:
            print(f"Error reading accelerometer data: {e}")
            return accelerometer_data
    else:
        print("Serial port is not open.")
        return accelerometer_data

def read_sensor_data() -> dict:
    if serial_instance.is_open:
        try:
            serial_instance.write("c\n".encode('utf-8'))
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

def stop_sensor_reading():
    global serial_instance
    if serial_instance.is_open:
        try:
            serial_instance.write("s\n".encode('utf-8'))
            print("Sensor reading stopped.")
        except Exception as e:
            print(f"Error stopping sensor reading: {e}")
    else:
        print("Serial port is not open.")