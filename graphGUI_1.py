import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import tkinter as tk


class testgraph(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, controller)
        label = tk.Label(self, text = "Graph Page", font = LARGE_FONT)
        label.pack(pady = 10, padx = 10)

        button1 = ttk.Button(self, text = "Back to Home",\
                             command = lambda: controller.show_frame(StartPage))
        button1.pack()

        f = Figure(figsize = (5,5), dpi = 100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side = tk.BOTTOM, fill = t.BOTH, expand = True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

testgraph(tk.Frame)