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

def plot(window, fig, plot1, stockA, stockB, data, decision_log):
    plot1.clear()

    plot1.plot(data.index, data[stockA].astype(float), label = stockA)
    plot1.plot(data.index, data[stockB].astype(float), label = stockB)
    plot1.plot(data.index, data["P_" + stockA].astype(float), label = "P_" + stockA)
    plot1.plot(data.index, data["P_" + stockB].astype(float), label = "P_" + stockB)
    plot1.plot(data.index, data["P_Mean"].astype(float), label = "Mean")
    
    for i in range(len(decision_log)):
        if i%4 == 0 or i%4 == 1:        # if i%2 == 0  [BY DEFAULT]
            plot1.axvline(decision_log.iloc[i,:].loc['Action Date'], color = "limegreen")
        else:
            plot1.axvline(decision_log.iloc[i,:].loc['Action Date'], color = "blue")
    
    plot1.legend()
    
    canvas = FigureCanvasTkAgg(fig, master = window)   
    canvas.draw()
  
    toolbar = NavigationToolbar2Tk(canvas, window) 
    toolbar.update()
    toolbar.pack()

    widget = canvas.get_tk_widget()
    widget.pack()
    return widget, toolbar