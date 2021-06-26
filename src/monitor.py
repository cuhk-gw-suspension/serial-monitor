from utils.plotter import array2d_animate
from utils.adaptUSBport import get_serial_port
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.style import use
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Real Time Serial Data Plot")
        self.master.geometry("800x500")
        self.master.configure(background="grey")
        self.grid()

        self.create_graphs()
        self.create_widgets()
        self.refresh_portlist()

    def create_graphs(self):
        use("seaborn-bright")
        self.fig = Figure()
        # self.fig.tight_layout()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Serial Data: No port selected.", size=16)
        self.ax.set_xlabel("sample")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        # self.canvas.get_tk_widget().place(x=10, y=30, width=600, height=400)
        # self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.get_tk_widget().grid(row=0, column=2, sticky=tk.N + tk.S)
        self.canvas.draw()

    def create_widgets(self):
        # self.quit = tk.Button(self, text="QUIT", fg="red",
        #                       command=self.master.destroy)
        # self.quit.grid()

        self.scrollbar = tk.Scrollbar(self)
        self.listbox = tk.Listbox(self,
                                  yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.grid(row=0, column=0)
        self.scrollbar.grid(row=0, column=1, sticky=tk.N + tk.S)
        self.listbox.bind("<<ListboxSelect>>", self.listbox_callback)

        self.refresh_button = tk.Button(self, text="refresh", fg="green",
                                        command=self.refresh_portlist)
        self.refresh_button.grid(row=1, column=0)

    def listbox_callback(self, event):
        pass

    def refresh_portlist(self):
        self.listbox.delete(0, self.listbox.size())
        try:
            for p in get_serial_port():
                self.listbox.insert(tk.END, p.device + "|" + p.description)
        except IOError as e:
            self.ax.set_title("Serial Data:" + str(e), size=16)
            print(e)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
