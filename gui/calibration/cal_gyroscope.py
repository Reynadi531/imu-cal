import numpy as np
import pandas as pd

record = pd.DataFrame(columns=['x', 'y', 'z'])

def add_record(x, y, z):
    global record
    new_record = [x, y, z]
    record.loc[len(record)] = new_record 

def count_records():
    global record
    return len(record)

def get_records():
    global record
    if record.empty:
        print("No records available.")
        return None
    return record.copy()

def getMinMax():
    global record
    if record.empty:
        print("No records available.")
        return None

    gyro_x = record['x'].values
    gyro_y = record['y'].values
    gyro_z = record['z'].values

    min_x = np.min(gyro_x)
    max_x = np.max(gyro_x)
    min_y = np.min(gyro_y)
    max_y = np.max(gyro_y)
    min_z = np.min(gyro_z)
    max_z = np.max(gyro_z)
    
    return min_x, max_x, min_y, max_y, min_z, max_z

def get_offset():
    global record
    if record.empty:
        print("No records available.")
        return None

    min_x, max_x, min_y, max_y, min_z, max_z = getMinMax()
    
    offset_x = (max_x + min_x) / 2
    offset_y = (max_y + min_y) / 2
    offset_z = (max_z + min_z) / 2 

    return offset_x, offset_y, offset_z
