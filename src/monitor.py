from utils.plotter import array2d_animate
from utils.adaptUSBport import get_serial_port
from matplotlib.figure import Figure
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

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
        self.master.geometry("800x500")
        self.master.configure(background="grey")
        self.pack()

        self.create_graphs()
        self.create_widgets()
        self.refresh_portlist()

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

    def _setbaud(self, baud):
        self.current_baud = baud
        print("set baud to", self.current_baud)

    def _setport(self, port):
        self.current_port = port
        print("set port to", self.current_port)
        print("selected device: ",
              self.current_port.device,
              " | ",
              self.current_port.description)
        self.ax.set_title("Serial Data: " + self.current_port.name)

    def refresh_portlist(self):
        print("\nrefreshing serial ports...")
        self.portmenu.delete(0, self.portmenu.index(tk.END))
        try:
            self.portlist = get_serial_port()
            for p in self.portlist:
                self.portmenu.add_command(label= p.name + " | " + p.description,
                                          command=lambda x=p.device: self._setport(x))
        except IOError as e:
            self.portmenu.add_separator()
            self.portmenu.add_command(label="empty", command=None)
            self.ax.set_title("Serial Data:" + str(e), size=16)
            print(e)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
