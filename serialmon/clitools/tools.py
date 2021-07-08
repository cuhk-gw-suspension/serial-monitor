import click

from serialmon.utils.adaptUSBport import get_serial_device
from serialmon.utils.log import print_serial_info

@click.group()
def cli():
    pass

@cli.command()
def listport():
    """list all ports not with description 'n/a'."""
    try:
        click.echo("Path\t\t\tDescription")
        for p in get_serial_device():
            click.echo("%s\t\t%s" % (p.name, p.description))
    except IOError as e:
        click.echo(e)

@cli.command()
@click.option('-p', type=click.Path(), help='port path to the serial device')
@click.option('-baud', help='baud rate of the serial communication')
@click.option('-timeout', default=1, required=False, help='timeout of the connection')
def read(port, baud, timeout):
    """Read and print information from a serial port indefinitely."""
    print_serial_info(port, baud, timeout)

@cli.command()
def gui():
    """open gui with live plots of serial data (if data)"""
    from serialmon.monitor import main

    main()
