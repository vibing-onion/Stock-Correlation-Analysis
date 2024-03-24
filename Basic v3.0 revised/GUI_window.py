import tkinter
from tkinter import *
import sys

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import functions
from functions import display
sys.path.append("functions")

ele_list = []
fig_list = []
widget = ""
toolbar = ""

def get_input():
    # ele_list = [start_entry, end_entry, stockA_entry, stockB_entry]
    _start = str(ele_list[0].get())
    _end = str(ele_list[1].get())
    stockA = str(ele_list[2].get())
    stockB = str(ele_list[3].get())
    return _start, _end, stockA, stockB

def create_GUIwindow():
    global ele_list
    global fig_list
    
    window = tkinter.Tk()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")
    
    window.title("GUI board")
    
    start_entry = Entry()
    start_entry.pack()
    end_entry = Entry()
    end_entry.pack()
    stockA_entry = Entry()
    stockA_entry.pack()
    stockB_entry = Entry()
    stockB_entry.pack()
    dataframe = tkinter.Text(window)
    dataframe.config(state=DISABLED)
    dataframe.pack()
    
    ele_list = [start_entry, end_entry, stockA_entry, stockB_entry, dataframe]
    
    if len(fig_list) == 0:
        fig = Figure(figsize = (25, 5), dpi = 100)
        plot1 = fig.add_subplot(111)
        fig_list = [fig, plot1]
    
    return window

def T_display_display_df(data_):
    display.display_df(ele_list[4], data_)
    
def T_display_plot(window, data_):
    global fig_list
    global widget
    global toolbar
    if widget != "":
        widget.destroy()
    if toolbar != "":
        toolbar.destroy()
    widget, toolbar = display.plot(window, fig_list[0], fig_list[1], data_)