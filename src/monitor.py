from utils.plotter import array2d_animate
from utils.adaptUSBport import get_serial_port
from matplotlib.figure import Figure
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import serial
from ast import literal_eval

import sys

if sys.version_info[0] < 3:
    import Tkinter as tk
else:
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

        self.create_graphs()
        self.create_widgets()
        self.refresh_portlist()
        self.plot_graphs()

    def create_graphs(self):
        style.use("seaborn-bright")
        self.fig = Figure((6.5, 5), dpi=100)
        self.fig.set_tight_layout("tight")
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Serial Data: No port selected.", size=16)
        self.ax.set_xlabel("sample")

        canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        # canvas.get_tk_widget().place(x=10, y=30, width=600, height=400)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.Y, expand=True)
        # canvas.get_tk_widget().grid(row=0, column=2, sticky=tk.N)
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()

    def create_widgets(self):
        # self.quit = tk.Button(self, text="QUIT", fg="red",
        #                       command=self.master.destroy)
        # self.quit.grid()

        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        self.portmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Port', menu=self.portmenu)

        self.baudlist = [9600, 14400, 19200, 57600, 115200, 1000000, 2000000]
        baudmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Baud', menu=baudmenu)
        for baud in self.baudlist:
            baudmenu.add_command(label=baud, command=lambda x=baud: self._setbaud(x))

        menubar.add_command(label="Refresh", command=self.refresh_portlist)

        # scrollbar = tk.Scrollbar(self)
        # self.listbox = tk.Listbox(self,
        #                           yscrollcommand=scrollbar.set)
        # scrollbar.config(command=self.listbox.yview)
        # self.listbox.grid(row=0, column=0)
        # scrollbar.grid(row=0, column=1, sticky=tk.N + tk.S)
        # self.listbox.bind("<<ListboxSelect>>", self.listbox_callback)
        #
        # refresh_button = tk.Button(self, text="refresh", fg="green",
        #                                 command=self.refresh_portlist)
        # refresh_button.grid(row=1, column=0)

    def refresh_portlist(self):
        print("\nrefreshing serial ports...")
        self.portmenu.delete(0, self.portmenu.index(tk.END))
        try:
            self.portlist = get_serial_port()
            for p in self.portlist:
                self.portmenu.add_command(label=p.name + " | " + p.description,
                                          command=lambda x=p.device: self._setport(x))
            self._setport(self.portlist[0])

        except IOError as e:
            self.portmenu.add_separator()
            self.portmenu.add_command(label="empty", command=None)
            self.ax.set_title("Serial Data:" + str(e), size=16)
            print(repr(e))

    def plot_graphs(self):
        try:
            self.ax.cla()
            for data in self._data_holder.T:
                self.ax.plot(data, label=self.curve_label)
                self.ax.legend()
        except AttributeError:
            pass
        self.master.after(1000, self.plot_graphs)

    def _update_serial_config(self):
        self.ser = serial.Serial(self.current_port, self.current_baud, timeout=1)
        self._data_holder = None
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
        self.ax.set_title("Serial Data: " + self.current_port.name)
        self._update_serial_config()

    def _read_serial(self):
        try:
            line = self.ser.readline().decode("utf-8")
            line = literal_eval(line)
            if type(line) is tuple:
                _temp = np.array(line, dtype=np.float64)
                self.curve_label = ["column%d"%i for i in range(len(_temp))]

            elif type(line) is dict:
                _temp = np.fromiter(line.items(), count=len(line))
                self.curve_label = np.fromiter(line.keys(), count=len(line))

            if self._data_holder is None:
                self._data_holder = _temp
            else:
                np.vstack((self._data_holder, _temp))

            self.master.after(0, self._read_serial)
        except Exception:
            self.master.after(1000, self._read_serial)




root = tk.Tk()
app = Application(master=root)
app.mainloop()
