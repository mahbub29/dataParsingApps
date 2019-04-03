import matplotlib as mpl
import numpy as np
import tkinter as tk
import  matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg

def draw_figure(canvas, figure, loc=(0,0)):

    figure_canvas_agg = FigureCanvasAgg(figure)
    figure_canvas_agg.draw()
    figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
    figure_w, figure_h = int(figure_w), int(figure_h)
    photo = tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)

    canvas.create_image(loc[0] + figure_w / 2, loc[1] + figure_h / 2, image=photo)

    tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

    return photo

