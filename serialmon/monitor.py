from .utils.plotter import array2d_animate
from .utils.adaptUSBport import get_serial_device
from matplotlib.figure import Figure
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import serial
from ast import literal_eval
import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Real Time Serial Data Plot")
        self.master.geometry("600x500")
        self.master.configure(background="grey")
        self.pack()

        self.current_port = None
        self.current_baud = None
        self.MAX_DATA_LENGTH = 50000

        self.create_graphs()  # create a figure to hold graphs
        self.create_widgets()  # create gui widgets
        self.refresh_portlist()  # refresh serial port info and choose first port to listen
        self.plot_graphs()  # plot curves on the graph indefintely

    def create_graphs(self):
        style.use("seaborn-bright")
        self.fig = Figure((6.5, 5), dpi=100)
        self.fig.set_tight_layout("tight")
        self.ax = self.fig.add_subplot(111)
        self._graph_title = "Serial Data: No port selected."

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        # canvas.get_tk_widget().place(x=10, y=30, width=600, height=400)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.Y, expand=True)
        # canvas.get_tk_widget().grid(row=0, column=2, sticky=tk.N)
        self.canvas.draw()

        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()

    def create_widgets(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        self.portmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Port', menu=self.portmenu)

        self.baudlist = [9600, 14400, 19200, 57600, 115200, 1000000, 2000000]
        baudmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Baud', menu=baudmenu)
        for baud in self.baudlist:
            baudmenu.add_command(label=baud, command=lambda x=baud: self._setbaud(x))
        self.current_baud = self.baudlist[-2]

        menubar.add_command(label="Refresh", command=self.refresh_portlist)

    def refresh_portlist(self):
        print("\nrefreshing serial ports...")
        self.portmenu.delete(0, self.portmenu.index(tk.END))
        try:
            self.portlist = get_serial_device()
            for p in self.portlist:
                self.portmenu.add_command(label=p.name + " | " + p.description,
                                          command=lambda x=p: self._setport(x))
            self._setport(self.portlist[0])

        except IOError as e:
            self.portmenu.add_separator()
            self.portmenu.add_command(label="empty", command=None)
            self._graph_title = "Serial Data:" + str(e)
            print(repr(e))

    def plot_graphs(self):
        """
        plot curves in the figure if _data_holder contains data.
        update interval = 1000ms
        """
        try:
            self.ax.cla()

            artists = self.ax.plot(self._data_holder)
            self.ax.legend(artists, self.curve_label)
            self.ax.set_title(self._graph_title)
            self.ax.set_xlabel("sample")
            self.canvas.draw()
        except (AttributeError, ValueError):
            pass

        self.master.after(1000, self.plot_graphs)

    def _update_serial_config(self):
        """configure serial readline setting and clear data holded by the
        program.
        """
        self.ser = serial.Serial(self.current_port.device, self.current_baud, timeout=1)
        self.ser.reset_input_buffer()
        print("serial updated")
        self._data_holder = None
        print("cleared data")
        self._read_serial()

    def _setbaud(self, baud):
        self.current_baud = baud
        print("set baud to", self.current_baud)
        self._update_serial_config()

    def _setport(self, port):
        self.current_port = port
        print("selected device: ",
              self.current_port.device,
              " | ",
              self.current_port.description)
        self._graph_title = "Serial Data: " + self.current_port.name
        self._update_serial_config()

    def _read_serial(self):
        """try to read incoming serial print and store it in self._data_holder.
        """
        try:
            line = self.ser.readline().decode("utf-8")
            line = literal_eval(line)
            if type(line) is tuple:
                _temp = np.array(line, dtype=np.float64)
                self.curve_label = ["column%d" % i for i in range(len(_temp))]

            elif type(line) is dict:
                _temp = np.fromiter(line.items(), count=len(line))
                self.curve_label = np.fromiter(line.keys(), count=len(line))
            print(_temp)

            # limiting array size of the _data_holder
            if self._data_holder is None:
                self._data_holder = np.reshape(_temp, (1, len(_temp)))
            elif len(self._data_holder) < self.MAX_DATA_LENGTH:
                self._data_holder = np.vstack((self._data_holder, _temp))
            else:
                self._data_holder = np.vstack((self._data_holder[1:], _temp))

            self.master.after(0, self._read_serial)
        except Exception:
            print("waiting data", end='\r')
            self.master.after(1000, self._read_serial)


def app():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    app()
