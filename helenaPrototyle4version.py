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
    """ Class ApplicationWindow: In this class, the whole system of the window (GUI) is created. """

    def __init__(self,  *args, **kwargs):
        """ Constructor function: Creation of the object with a specific values."""
        super().__init__(*args, **kwargs)
        self.createwidgets()     # initiates the createwidgets method.
        # self.readData = ReadData()
        self.myVar = tk.StringVar()

    def createwidgets(self):
        """ Types of Variable:
        - options_x/y_axis or options_plotting: possible options for the x/y-axis or for the plotting method
        - variable_x/y: what one selects in the GUI to become the x and y-axis
        - inp_x/y_axis or inp_plot: OptionMenu for the possible options.
        - x/y_entry_field: Entry-field in which you can either write down what axes you want or in which you can save
            which axis you did in fact choose. This is later needed for the further usage into the saving of which
            x-axis oder y-axis you want. For this, you use
        - x/y_entry_var: is a StringVar which allows you later to get and set values for the x-axis and y-axis.
            This is a tkinter method.
        - result_x/y: """

        """ 1st: Creation of the root-window is below in the main-command and in the root-window the button-frame (which
        options we have to plot, see below) and the plot-frame (frame in which the plot is shown) at the end. """
        self.buttonframe = tk.Frame(self.master)
        self.buttonframe.grid(row=0, column=0, sticky=tk.W)
        self.plotframe = tk.Frame(self.master)
        self.plotframe.grid(row=1, column=0)

        """ 2nd: Creation of the button-frame with every button. """

        # First row:
        self.open_f = tk.Button(self.buttonframe, text="Open File", command=self.selectfile, activeforeground="red")
        # # Open button, selected method: selectfile (see below)
        self.open_f.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.label_f = tk.Label(self.buttonframe, text="Filename: ...", fg="red")
        # # Label of the file, until later (in select file), the filename gets the name of the path
        self.label_f.grid(row=0, column=1, columnspan=6)
        # # HIER NOCH GUCKEN: NICHT BREITER ALS 6?
        self.button_close = tk.Button(self.buttonframe, text="Close", command=root.destroy, activeforeground="red")
        self.button_close.grid(row=0, column=7, sticky=tk.N + tk.S + tk.E + tk.W)

        # Second row:
        # # First step: Creation of the different option-menus (empty at the beginning, later filled with the help
        # # of options_xy_changed
        self.options_x_axis = [""]
        self.options_y_axis = [""]
        self.options_plotting = ["", "Scatter", "Line", "Sinus", "3D"]

        self.variable_x = StringVar(self.buttonframe)   # "presented" option in options-menu, get and set nutzen möglich
        self.variable_x.set(self.options_x_axis[0])     # first step: variable_x is set as the first entry of the
        # # options_x_axis value
        self.variable_x.trace('w', self.option_x_selected)     # overwrites the variable_x with the trace and the
        # # function option_x_selected (see below), which one is picked

        self.variable_y = StringVar(self.buttonframe)     # same for y
        self.variable_y.set(self.options_y_axis[0])
        self.variable_y.trace('w', self.option_y_selected)

        self.variable_plot = StringVar(self.buttonframe)     # same for the plotting options
        self.variable_plot.set(self.options_plotting[0])

        self.lbl_x = tk.Label(self.buttonframe, text="Choose your\nx-axis")
        self.lbl_x.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        # # Creation of the OptionMenu, in which the "presented" is the show_first_x, and all the possible options or
        # # x-INPUTS are from the option_x_axis menu
        self.inp_x_axis = OptionMenu(self.buttonframe, self.variable_x, *self.options_x_axis)
        self.inp_x_axis.grid(row=1, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

        self.lbl_y = tk.Label(self.buttonframe, text="Choose your\ny-axis")
        self.lbl_y.grid(row=1, column=2, sticky=tk.N + tk.S + tk.E + tk.W)
        # same fot the OptionMenu with the y-axis
        self.inp_y_axis = OptionMenu(self.buttonframe, self.variable_y, *self.options_y_axis)
        self.inp_y_axis.grid(row=1, column=3, sticky=tk.N + tk.S + tk.E + tk.W)

        self.lbl_graph = tk.Label(self.buttonframe, text="Choose your\nGraph-Style")
        self.lbl_graph.grid(row=1, column=4, sticky=tk.N + tk.S + tk.E + tk.W)
        # same fot zhe OptionMenu with the plotting-methods
        self.inp_plot = OptionMenu(self.buttonframe, self.variable_plot, *self.options_plotting)
        self.inp_plot.grid(row=1, column=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.plot_f = tk.Button(self.buttonframe, text="Plot", activeforeground="red")  # NOCH COMMAND SCHREIBEN
        self.plot_f.grid(row=1, column=7, rowspan=3, sticky=tk.N + tk.S + tk.E + tk.W)

        """ Third row: """
        # # the x/y_entry_var is defined as a StringVar. You can use this kind of variable for the later usage of the
        # # get and set methods. With this, you can save it as an axis and scan the values in there for the later
        # # plotting.
        self.x_entry_var = StringVar()
        self.y_entry_var = StringVar()

        # # Create the entry field for x and y of the OptionMenu, which can be changed. Important: You can either choose
        # # the axis manually or set it through the later function and thus through the OptionMenu-choosing
        # # (function: option_x/y_selected) """
        self.x_entry_field = tk.Entry(self.buttonframe, textvariable=self.x_entry_var)   # eventually: text='empty'
        self.x_entry_field.grid(row=2, column=1)

        self.y_entry_field = tk.Entry(self.buttonframe, textvariable=self.y_entry_var)
        self.y_entry_field.grid(row=2, column=3)

        """ Fourth row: """
        # # Here you can sniff into the data of the chosen axis, which in turn will be saved for later usage or
        # # shown in the result_x/y
        self.lbl_sniff_x = tk.Label(self.buttonframe, text="Want to sniff into the\nx-data?")
        self.lbl_sniff_x.grid(row=3, column=0)
        self.sniff_x = tk.Button(self.buttonframe, text="Sniff the x-data", command=self.retrieve_x_data,
                                 activeforeground="red")  #
        self.sniff_x.grid(row=3, column=1)

        self.lbl_sniff_y = tk.Label(self.buttonframe, text="Want to sniff into the\ny-data?")
        self.lbl_sniff_y.grid(row=3, column=2)
        self.sniff_y = tk.Button(self.buttonframe, text="Sniff the y-data", command=self.retrieve_y_data,
                                 activeforeground="red")  #
        self.sniff_y.grid(row=3, column=3)

        # Fifth row:
        # # Here, there is a label which ist created, so that we can later see the results of the x and y entry.
        # # The text is changed later with the help of the retrieve_x and retrieve_x function, which gets the values
        # # from the multiparser function.
        self.result_x = tk.Label(self.buttonframe, text="")      # text will be changed (function: retrieve_x_data)
        self.result_x.grid(row=4, column=1)
        self.result_y = tk.Label(self.buttonframe, text="")      # text will be changed (function: retrieve_y_data)
        self.result_y.grid(row=4, column=3)

        self.button_clear = tk.Button(self.buttonframe, text="Clear", command=self.clear)
        self.button_clear.grid(row=4, column=7, sticky=tk.N + tk.S + tk.E + tk.W)

        """ 3rd: Creation of the plot-window and frame. Here, we go to the class, which instantiate the plot-frame. """
        self.plot_window = Plotwindow(self.plotframe, (10, 8))  # inch

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
        """ Function 'option x-y-changed': Reads the data and finds possible key names for the axes. In particular,
         it uses the modul multiparser, the method find_possible_keynames_all. """

        menux = self.inp_x_axis["menu"]     # the variable menu-x is defined as the inp_x_axis
        menuy = self.inp_y_axis["menu"]     # same as for x
        # # Next step: The list of options_x_axis and options_x_axis is changed into a list, in which the objContainer
        # # (filename of the opened file) is put into the get_parseobject().find_possible_keynames_all().keys()
        options_x_axis = list(objContainer.getobj(
            "mpobject").get_parseobject().find_possible_keynames_all().keys())
        options_y_axis = list(objContainer.getobj(
            "mpobject").get_parseobject().find_possible_keynames_all().keys())
        menux.delete(0, "end")
        menuy.delete(0, "end")

        # # Lambda-Function: In the menux the lambda-function is used: The values in the menu are the variable_x.set
        # # from the new options menu.
        for string in options_x_axis:
            menux.add_command(label=string, command=lambda value=string: self.variable_x.set(value))
            menuy.add_command(label=string, command=lambda value=string: self.variable_y.set(value))

        # print(options_x_axis, options_y_axis)
        self.variable_x.set(options_x_axis[1])     # "presented" x and y-values are shown
        self.variable_y.set(options_y_axis[-1])

        # self.x_entry_field.delete(0, END)  # in the x- and y-entry field the "presented" values are picked
        # self.x_entry_field.insert(0, self.variable_x)    # also possible: options_x_axis[1]
        #
        # self.y_entry_field.delete(0, END)
        # self.y_entry_field.insert(0, self.variable_y)

    def option_x_selected(self, *args):
        """ Function option_x_selected (and below: option_y_selected): The CHOSEN option ('variable') of the OptionMenu
        which was selected will be inserted into x_entry_field and saved. """
        self.x_entry_field.delete(0, END)
        self.x_entry_field.insert(0, self.variable_x.get())    # in the x- and y-entry field the picked values are shown

    def option_y_selected(self, *args):
        """ See option_x_selected (above). """
        # # Same as for variable_x
        self.y_entry_field.delete(0, END)
        self.y_entry_field.insert(0, self.variable_y.get())

    def retrieve_x_data(self):
        """ Function retrieve_x_data: The values of the picked x-data (x_entry_var) are being scanned by the method
        multiparser (scan_values). Moreover, the results are shown into the result_x label field."""
        # print("looking data for key:", self.x_entry_var.get())
        v = list(objContainer.getobj("mpobject").get_parseobject().scan_values('xvalues', self.x_entry_var.get()))
        # # NOCH SCHAUEN: würde auch self.variable_y.get()) gehen?
        v = str(v)[0:30] + "..."  # NOCH ANPASSEN?
        # print(v)
        self.result_x.configure(text=v)    # changes the text in result_x

    def retrieve_y_data(self):
        """ See retrieve_x_data (above). """
        # print("looking data for key:", self.y_entry_var.get())
        w = list(objContainer.getobj("mpobject").get_parseobject().scan_values('yvalues', self.y_entry_var.get()))
        w = str(w)[0:30] + "..."
        # print(w)
        self.result_y.configure(text=w)    # changes the text in result_y

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
        # (w, h) = size
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

    root = tk.Tk()
    root.title("What do you want to plot?")
    app = ApplicationWindow(master=root)

    objContainer = myVars()
    print("meineObjekte=", objContainer.getAllNames())
    app.mainloop()
