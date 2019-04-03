import matplotlib as mpl
import numpy as np
import tkinter as tk
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg

def draw_figure(canvas, figure, loc=(0,0)):

    figure_canvas_agg = FigureCanvasAgg(figure)
    figure_canvas_agg.draw()
    figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
    figure_w, figure_h = int(figure_w), int(figure_h)
    photo = tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)

    canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)

    tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

    return photo

w, h = 300, 200
window = tk.Tk()
window.title("A figure in a canvas")
canvas = tk.Canvas(window, width=w, height=h)
canvas.pack()

X = np.linspace(0, 2 * np.pi, 50)
Y = np.sin(X)

fig = mpl.figure.Figure(figsize=(2, 1))
ax = fig.add_axes([0, 0, 1, 1])
ax.plot(X, Y)

fig_x, fig_y = 10, 10
fig_photo = draw_figure(canvas, fig,loc=(fig_x, fig_y))
fig_w, fig_h = fig_photo.width(), fig_photo.height()

canvas.create_line(200, 50, fig_x + fig_w / 2, fig_y + fig_h / 2)
canvas.create_text(200, 50, text="Zero-crossing", anchor="s")

tk.mainloop()