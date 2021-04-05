import tkinter as tk
from tkinter import *
from tkinter import filedialog
# import json
# import csv
# import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# from datetime import datetime
# from dv import *
from dv.multiparser import multiParser
# from IPython.utils.tests.test_wildcard import obj_t

# matplotlib.use('TkAgg')


class ApplicationWindow(tk.Frame):
    """ Class ApplicationWindow: In this class, the whole system of the window is created. """
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.__st = tk.StringVar()
        self.createwidgets()     # initiates the createwidgets method.
        # self.readData = ReadData()
        self.myVar = tk.StringVar()

    def createwidgets(self):
        self.buttonframe = tk.Frame(self.master)
        self.buttonframe.grid(row=0, column=0, sticky=tk.W)
        self.plotframe = tk.Frame(self.master)
        self.plotframe.grid(row=1, column=0)

        """ 2nd: Creation of the button-frame with every button. """

        self.x_entry_var = StringVar()
        self.y_entry_var = StringVar()

        # First row:
        self.open_f = tk.Button(self.buttonframe, text="Open File", command=self.selectfile, activeforeground="red")  #
        self.open_f.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.label_f = tk.Label(self.buttonframe, text="Filename: ...", fg="red")
        self.label_f.grid(row=0, column=1, columnspan=6)
        # # HIER NOCH GUCKEN: NICHT BREITER ALS6?
        self.button_close = tk.Button(self.buttonframe, text="Close", command=root.destroy, activeforeground="red")
        self.button_close.grid(row=0, column=7, sticky=tk.N + tk.S + tk.E + tk.W)

        # Second row:
        self.options_x_axis = [""]
        self.options_y_axis = [""]
        self.options_plotting = ["Scatter", "Line", "3D", "..."]

        self.show_first_x = StringVar(self.buttonframe)
        self.show_first_x.set(self.options_x_axis[0])
        self.show_first_x.trace('w', self.option_x_selected)

        self.variable_axes_y = StringVar(self.buttonframe)
        self.variable_axes_y.set(self.options_y_axis[0])
        self.variable_axes_y.trace('w', self.option_y_selected)

        self.variable_plot = StringVar(self.buttonframe)
        self.variable_plot.set(self.options_plotting[0])

        self.lbl_x = tk.Label(self.buttonframe, text="Choose your\nx-axis")
        self.lbl_x.grid(row=3, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.inp_x_axis = OptionMenu(self.buttonframe, self.show_first_x, *self.options_x_axis)
        self.inp_x_axis.grid(row=3, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

        self.lbl_y = tk.Label(self.buttonframe, text="Choose your\ny-axis")
        self.lbl_y.grid(row=3, column=2, sticky=tk.N + tk.S + tk.E + tk.W)
        self.inp_y_axis = OptionMenu(self.buttonframe, self.variable_axes_y, *self.options_y_axis)
        self.inp_y_axis.grid(row=3, column=3, sticky=tk.N + tk.S + tk.E + tk.W)

        self.lbl3 = tk.Label(self.buttonframe, text="Choose your\nGraph-Style")
        self.lbl3.grid(row=3, column=4, sticky=tk.N + tk.S + tk.E + tk.W)
        self.inp_plot = OptionMenu(self.buttonframe, self.variable_plot, *self.options_plotting)
        self.inp_plot.grid(row=3, column=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.plot_f = tk.Button(self.buttonframe, text="Plot")  # activeforeground="red"NOCH COMMAND SCHREIBEN
        self.plot_f.grid(row=2, column=7, rowspan=4, sticky=tk.N + tk.S + tk.E + tk.W)

        # Third row:
        self.x_entry_field = tk.Entry(self.buttonframe, text='leer', textvariable=self.x_entry_var)
        self.x_entry_field.grid(row=4, column=1)

        self.y_entry_field = tk.Entry(self.buttonframe, text='leer', textvariable=self.y_entry_var)  # , textvariable=x_entry_var)
        self.y_entry_field.grid(row=4, column=3)

        # Fourth row:
        self.lbl4 = tk.Label(self.buttonframe, text="Want to retrieve into the\nx-data?")
        self.lbl4.grid(row=5, column=0)
        self.bdata_x = tk.Button(self.buttonframe, text="Retrieve x-data", command=self.retrieve_x_data,
                                 activeforeground="red")  #
        self.bdata_x.grid(row=5, column=1)

        self.lbl5 = tk.Label(self.buttonframe, text="Want to sniff into the\ny-data?")
        self.lbl5.grid(row=5, column=2)
        self.bdata_x = tk.Button(self.buttonframe, text="Retrieve y-data", command=self.retrieve_y_data,
                                 activeforeground="red")  #
        self.bdata_x.grid(row=5, column=3)

        # Fifth row:
        self.result_x = tk.Label(self.buttonframe, text="")
        self.result_x.grid(row=6, column=1)
        self.result_y = tk.Label(self.buttonframe, text="")
        self.result_y.grid(row=6, column=3)

        self.button_clear = tk.Button(self.buttonframe, text="Clear", command=self.clear)
        self.button_clear.grid(row=6, column=7, sticky=tk.N + tk.S + tk.E + tk.W)

        """ 3rd: Creation of the plot-window and frame. Here, we go to the class, which instantiate the plot-frame. """
        self.plot_window = Plotwindow(self.plotframe, (9, 6))  # inch

    def selectfile(self):
        """ Function 'select file': With help of the tkinter askopenfilename, we save the name of the file as filename,
        so that we can use it later. """
        filename = filedialog.askopenfilename(filetypes=[("JSON-File", "*.json"), ("CSV-File", "*.csv"),
                                                         ("json files", "*.json")],
                                              title="Which data do you want plotted?")
        objContainer.setobj("selectedFile", filename)    # HIER NOCH HINZUFÜGEN!
        m = multiParser(filename=filename)
        objContainer.setobj("mpobject", m)
        self.label_f.configure(text=filename)    # changes the label from "Filename ... to the filename (with path)
        self.option_xy_changed()       # executes the function option_xy_change (description see below)

    def option_xy_changed(self):
        """ Function 'option x-y-changed:  """
        menux = self.inp_x_axis["menu"]
        menuy = self.inp_y_axis["menu"]
        options_x_axis = list(objContainer.getobj(
            "mpobject").get_parseobject().find_possible_keynames_all().keys())
        # .append("Neb")#self.entry.get())
        options_y_axis = list(objContainer.getobj(
            "mpobject").get_parseobject().find_possible_keynames_all().keys())
        # .append("Neb")#self.entry.get())#OPTIONS_X[:]
        menux.delete(0, "end")
        menuy.delete(0, "end")
        for string in options_x_axis:
            menux.add_command(label=string, command=lambda value=string: self.show_first_x.set(value))
            menuy.add_command(label=string, command=lambda value=string: self.variable_axes_y.set(value))

        print(options_x_axis)
        # global variable_axes_x, variable_axes_y
        self.show_first_x.set(options_x_axis[1])
        self.variable_axes_y.set(options_y_axis[-1])

        self.x_entry_field.delete(0, END)  # OPTIONS_X[1])
        self.x_entry_field.insert(0, options_x_axis[1])

        self.y_entry_field.delete(0, END)
        self.y_entry_field.insert(0, options_y_axis[-1])

    def option_x_selected(self, *args):
        # print(self.show_first_x.get())
        self.x_entry_field.delete(0, END)  # OPTIONS_X[1])
        self.x_entry_field.insert(0, self.show_first_x.get())

    def option_y_selected(self, *args):
        # print(self.variable_axes_y.get())

        self.y_entry_field.delete(0, END)
        self.y_entry_field.insert(0, self.variable_axes_y.get())

    def retrieve_x_data(self):
        print("looking data for key:", self.x_entry_var.get())
        v = list(objContainer.getobj("mpobject").get_parseobject().scan_values('xvalues', self.x_entry_var.get()))
        v = str(v)[0:30] + "..."  # NOCH ANPASSEN?
        print(v)
        self.result_x.configure(text=v)

    def retrieve_y_data(self):
        print("looking data for key:", self.y_entry_var.get())
        w = list(objContainer.getobj("mpobject").get_parseobject().scan_values('yvalues', self.y_entry_var.get()))
        w = str(w)[0:30] + "..."
        print(w)
        self.result_y.configure(text=w)
        # lbl_result_x.configure(text=v)

    def clear(self):
        self.plot_window.clearplot()


class myVars:
    def __init__(self):
        self.objekte = {}

    def getobj(self, whichobjname):
        return self.objekte[whichobjname]

    def setobj(self, objname, obj):
        self.objekte[objname] = obj

    def getAllNames(self):
        return self.objekte.keys()


class Plotwindow:

    def __init__(self, masterframe, size):
        (w, h) = size
        self.figure = plt.Figure(size)
        self.axes = self.figure.add_subplot(111)
        # create canvas as matplotlib drawing area
        res = self.c1 = FigureCanvasTkAgg(self.figure, master=masterframe)
        self.c1.get_tk_widget().grid(column=0, row=0, columnspan=4)  # Get reference to tk_widget
        toolbar = NavigationToolbar2Tk(self.c1, masterframe, pack_toolbar=False)
        # matplotlib navigation toolbar; "pack_toolbar = False" necessary for .grid() geometry manager
        toolbar.grid(column=0, row=1, sticky=tk.W)
        toolbar.update()

    def plotxy(self, x, y):
        self.axes.scatter(x, y)
        self.c1.draw()

    def clearplot(self):
        self.axes.cla()  # clear axes
        self.c1.draw()


print("__name__:", __name__)

if __name__ == "__main__":
    """ 1st: Creation of the root-window (with title) and in the root-window the button-frame (which options we have 
    to plot it, see below) and the plot-frame (frame in which we plot) at the end. """
    root = tk.Tk()
    root.title("What do you want to plot?")
    app = ApplicationWindow(master=root)

    objContainer = myVars()
    print("meineObjekte=", objContainer.getAllNames())
    app.mainloop()