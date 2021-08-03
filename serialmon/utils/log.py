import serial
import time
import datetime
import os
import traceback
from .adaptUSBport import get_nano_port



def log_serial_info(
        serial_device,
        elapsed_time,
        file_path,
        ref_time=None,
        buffer_time=None):
    '''
    Log serial data for an given time from Arduino and export to a csv.

    Parameters
    ------------
    serial_device: Serial object
                object of serial.Serial
    elapsed_time: float or int
                elapsed time for reading the serial print, in seconds.
    file_path: string
                path to file storing serial readings.
    ref_time: float
                reference time returned by time.pref_counter() .
    buffer_time: int/float
                time to buffer, in sec.
                (buffer_time should not be too small since serial port takes
                time to establish)
    '''
    dir_path, *_ = os.path.split(file_path)

    if not os.path.exists(dir_path) and dir_path is not None and dir_path != "":
        os.makedirs(dir_path)

    try:
        mycsv = open(file_path, 'w')
    except IOError:
        print("failed to open file")
        traceback.print_exc()
    except Exception as e:
        print(repr(e))
        traceback.print_exc()

    count = 0; total_time = 0
    serial_device.flush()
    print('starting trial, ETA: %.2f seconds'%elapsed_time)
    for _ in range(2):
        serial_device.readline()

    if ref_time is not None and buffer_time is not None:
        while(time.perf_counter() - ref_time < buffer_time):
            time.sleep(1e-7)

    serial_device.reset_input_buffer()
    while(serial_device.in_waiting != 0):   # wait for reset buffer
        time.sleep(1e-8)

    start = time.perf_counter()             # time readline interval
    start_timer = time.perf_counter_ns()    # time log elapse time

    while (time.perf_counter() - start < elapsed_time):
        line = serial_device.readline()
        stop_timer = time.perf_counter_ns()
        tmp = (stop_timer - start_timer)*1e-3
        start_timer = stop_timer
        msg = line.decode("ascii")
        mycsv.write(msg)
        total_time += tmp
        count += 1

    mycsv.close()
    print("count:", count)
    print("mean interval:", total_time/count, "us")
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
        ser.flush()
        ser.readline()              # 0xff start byte
        time.sleep(1)
        while True:
            try:
                line = ser.readline().decode("ascii")
                print(line, end="")
            except KeyboardInterrupt:
                break

    print("\rClosed", port_path)


def print_int(port_path=None, baud=1_000_000, timeout=1):
    '''
    Read serial data indefinitely from Arduino device and interpert
    them as integer.

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
        ser.flush()
        ser.readline()              # 0xff start byte
        time.sleep(1)
        while True:
            try:
                line = ser.readline().strip()
                value = int.from_bytes(line, byteorder="big", signed=True)
                print(value)
            except KeyboardInterrupt:
                break

    print("\rClosed", port_path)
