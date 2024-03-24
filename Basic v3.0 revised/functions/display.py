import tkinter
import tkinter.messagebox
import pandas

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

def display_df(dataframe, data):
    _data = data
    dataframe.config(state="normal")
    dataframe.delete(1.0, tkinter.END)
    dataframe.insert(tkinter.END, _data.to_string())
    dataframe.config(state="disable")

def plot(window, fig, plot1, data):
    plot1.clear()

    plot1.plot(data.index, data["Adj Close_x"].astype(float), label = "Stock A")
    plot1.plot(data.index, data["Adj Close_y"].astype(float), label = "Stock B")
    plot1.plot(data.index, data["Mean"].astype(float), label = "Mean")
    
    plot1.legend()
    
    canvas = FigureCanvasTkAgg(fig, master = window)   
    canvas.draw()
  
    toolbar = NavigationToolbar2Tk(canvas, window) 
    toolbar.update()
    toolbar.pack()

    widget = canvas.get_tk_widget()
    widget.pack()
    return widget, toolbar