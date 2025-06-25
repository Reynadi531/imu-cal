import numpy as np
import pandas as pd

record = pd.DataFrame(columns=['x', 'y', 'z'])

def add_record(x, y, z):
    global record
    record.loc[len(record)] = [x, y, z] 

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

    accel_x = record['x'].values
    accel_y = record['y'].values
    accel_z = record['z'].values

    min_x = np.min(accel_x)
    max_x = np.max(accel_x)
    min_y = np.min(accel_y)
    max_y = np.max(accel_y)
    min_z = np.min(accel_z)
    max_z = np.max(accel_z)
    
    return min_x, max_x, min_y, max_y, min_z, max_z