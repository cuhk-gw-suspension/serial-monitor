import click

from serialmon.utils.adaptUSBport import get_serial_device
from serialmon.utils.log import print_serial_info
from serialmon.monitor import app

@click.group()
def cli():
    pass

@cli.command()
def list():
    """list all ports not with description 'n/a'."""
    try:
        title = "Available serial ports:"
        click.echo(title)
        for i, p in enumerate(get_serial_device()):
            click.echo("%d: %s\t\t%s" % (i, p.device, p.description))
    except IOError as e:
        click.echo(e)

@cli.command()
@click.option('-p','--port',  help='port path to the serial device,\n \
                                    can be path string or number from serial list')
@click.option('-b', '--baud', type=int, help='baud rate of the serial communication')
@click.option('--timeout', default=1, required=False, help='timeout of the connection')
def read(port, baud, timeout):
    """Read and print information from a serial port indefinitely."""
    click.echo("start reading...")
    click.echo("Press ctrl C to escape.")
    try:
        port = int(port)
    except Exception:
        pass

    if type(port) is str:
        print_serial_info(port, baud, timeout)
    elif type(port) is int:
        p = get_serial_device()
        print_serial_info(p[port].device, baud, timeout)
    else:
        raise TypeError("wrong instruction of --port option.")

@cli.command()
def gui():
    """open gui with live plots of serial data (if data)"""
    app()

