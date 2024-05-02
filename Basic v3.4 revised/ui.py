import tkinter
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import functions
from functions import plotting, BT_fit, data
import GUI_window

import functions
import sys
external_file = [
    "functions"
]
for f in external_file:
    sys.path.append(f)

_start = ""
_end = ""
stockA = ""
stockB = ""
tk_window = ""

def main():
    global tk_window
    
    def enter():
        global _start
        global _end
        global stockA
        global stockB
        _start, _end, stockA, stockB = GUI_window.get_input()
        data_, decision_log_ = data.price_trend(stockA, stockB, _start, _end)
        GUI_window.T_display_display_df(data_, 4)
        GUI_window.T_display_display_df(decision_log_, 5)
        GUI_window.T_display_plot(tk_window, stockA, stockB, data_, decision_log_)
        
        
    def confirm_to_quit():
        if tkinter.messagebox.askokcancel('Warning', 'Quit?'):
            tk_window.quit()
    
    tk_window = GUI_window.create_GUIwindow()
    
    button2 = tkinter.Button(tk_window, text='Quit', command=confirm_to_quit)
    button2.pack()
    button3 = tkinter.Button(tk_window, text='Enter', command=enter)
    button3.pack()
    tk_window.mainloop()
    
main()