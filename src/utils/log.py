import serial
import time
import os
import traceback
from adaptUSBport import get_nano_port



def log_serial_info(
        elapsed_time,
        file_path,
        port_path=None,
        baud=1_000_000,
        timeout=1):
    '''
    Log serial data for an given time from Arduino and export to a csv.

    Parameters
    ------------
    elapsed_time: float or int
                elapsed time for reading the serial print, in seconds.
    file_path: string
                path to file storing serial readings.
    port_path: string, optional
                path to the Arduino port, default to nano 33 ble port path.
    baud: int, optional
                baud rate of the serial communication.
    timeout: int, optional
                timeout for reading the serial print, in seconds.

    '''
    if port_path is None:
        port_path = get_nano_port()

    if not os.path.exists(port_path):
        raise IOError("Could not find the specified Arduino port")

    dir_path, *_ = os.path.split(file_path)

    if not os.path.exists(dir_path) and dir_path is not None:
        os.makedirs(dir_path)

    try:
        mycsv = open(file_path, 'w')
    except IOError:
        print("failed to open file")
        traceback.print_exc()
    except:
        print(repr(Exception))
        traceback.print_exc()

    if timeout is None:
        raise Exception('timeout must be specified.')

    print('starting trial, ETA: %.2f seconds'%elapsed_time)

    start = time.perf_counter()
    with serial.Serial(port_path, baud, timeout=timeout) as ser:
        while (time.perf_counter() - start < elapsed_time):
            line = ser.readlines()
            mycsv.write(line.decode('UTF-8'))
    mycsv.close()
    print("data logged successfully.")



def print_serial_info(port_path=None, baud=1_000_000, timeout=1):
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
    if port_path is None:
        port_path = get_nano_port()

    if timeout is None:
        raise Exception('timeout must be specified.')

    with serial.Serial(port_path, baud, timeout=timeout) as ser:
        while True:
            line = ser.readline()
            if "\n" not in line:
                line = line + "\n"
            print(line.decode('UTF-8'), end="")
