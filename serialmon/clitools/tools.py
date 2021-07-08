import Click

from serialmon.utils.adaptUSBport import get_serial_device
from serialmon.utils.log import print_serial_info

@click.group()
def cli():
    pass

@cli.command()
def listport():
    """list all ports not with description 'n/a'."""
    Click.echo("Path\t\t\tDescription")
    for p in get_serial_device():
        Click.echo("%s\t\t%s" % (p.name, p.description))

@cli.command()
@click.option('-p', type=click.String, help='port path to the serial device')
@click.option('-baud', help='baud rate of the serial communication')
@click.option('-timeout', default=1, required=False, help='timeout of the connection')
def read(port, baud, timeout):
    """Read and print information from a serial port indefinitely."""
    print_serial_info(port, baud, timeout)
