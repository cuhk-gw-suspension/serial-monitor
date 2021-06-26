import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Real Time Serial Data Plot")
        self.master.geometry("700x500")
        self.master.configure(background="grey")

        self.pack()
        self.create_widgets()
        self.create_graphs()

    def create_widgets(self):
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.scrollbar = tk.Scrollbar(self)
        self.listbox = tk.Listbox(self,
                                  yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.pack(side=tk.LEFT)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.bind("<<ListboxSelect>>", self.listbox_callback)

    def create_graphs(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Serial Data: No port selected.")
        self.ax.set_xlabel("sample")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        # self.canvas.get_tk_widget().place(x=10, y=30, width=600, height=400)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.draw()

    def listbox_callback(self):
        pass


root = tk.Tk()
app = Application(master=root)
app.mainloop()
