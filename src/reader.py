import serial
import time
import os
import csv
from .adaptUSBport import get_nano_port

def log_serial_info(
        fieldnames,
        file_path="arduino_data.csv",
        port_path=get_nano_port(), 
        baud=1_000_000, 
        timeout=1):
    '''
    Read serial data for an given time from Arduino and export to a tsv.

    Parameters
    ------------
    port_path: string, optional
                path to the Arduino port, default to nano 33 ble port path.
    baud: int, optional
                baud rate of the serial communication.
    timeout: int, optional
                timeout for reading the serial print, in seconds.

    '''
    if not os.path.exists(port_path):
        raise IOError("Could not find the specified Arduino port")

    if timeout is None:
        raise Exception('timeout must be specified.')

    dir_path, filename = os.path.split(file_path)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with open(file_path, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    with serial.Serial(port_path, baud, timeout=timeout) as ser:
        while True:
            line = ser.readline().decode('UTF-8')
            if "\n" not in line:
                line = line + "\n"
            print(line, end="")

            with open(file_path, 'a') as csv_file:
                csv_file.write(line)



def print_serial_info(port_path=get_nano_port(), baud=1_000_000, timeout=1):
    '''
    Read serial data indefinitely from Arduino device.

    Parameters
    ------------
    port_path: string, optional
                path to the Arduino port, default to nano 33 ble.
    baud: int, optional
                baud rate of the serial communication.
    timeout: int, optional
                timeout for reading the serial print, in seconds.

    '''
    if timeout is None:
        raise Exception('timeout must be specified.')

    with serial.Serial(port_path, baud, timeout=timeout) as ser:
        while True:
            line = ser.readline()
            if "\n" not in line:
                line = line + "\n"
            print(line.decode('UTF-8'), end="")


