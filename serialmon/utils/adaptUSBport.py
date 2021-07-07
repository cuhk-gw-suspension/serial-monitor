import warnings
import serial
import serial.tools.list_ports

def get_nano_port():
    arduino_ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if 'BLE' in p.description
    ]

    if not arduino_ports:
        raise IOError("No Arduino Nano 33 BLE found")
    if len(arduino_ports) > 1:
        warnings.warn("Multiple Arduino Nano 33 BLE found - returning the first")

    return arduino_ports[0]

def get_serial_device():
    device = [p for p in serial.tools.list_ports.comports() if "n/a" not in p.description]

    if not device:
        raise IOError("No serial device found")

    return device

def get_serial_port():
    return [p.device for p in get_serial_device()]

if __name__ == "__main__":
    print(get_serial_port()[0])
    pass
