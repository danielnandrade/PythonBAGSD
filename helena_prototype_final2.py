import tkinter as tk
from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from dv.multiparser import MultiParser
import tkinter.scrolledtext as st

#TODO EXPORT
import pandas as pd
import numpy as np
import random  # XXX only for testing
import matplotlib.figure
import matplotlib.patches

class ApplicationWindow(tk.Frame):
    """ Class ApplicationWindow: In this class, the whole system of the window (GUI) is created. Moreover """
    plot_dropdown_dic = {'Test plot': 'testplot',
                             'Data scatter plot': 'data_scatterplot',
                             'Pie chart': 'piechart',
                             'Histogram': 'histogram',
                             'Bar chart': 'barchart',
                             'Mean and Std dev': 'mean_xy',
                             'Earth overlay': 'earth_overlay',
                             'Cosine wave': 'cosinewave',
                             'Stem and leaf plot': 'stemandleafplot',
                             'Pie chart Ordered': 'piechart_ordered',
                             'Bar chart Ordered': 'barchart_ordered',
                             'Bar Horizontal': 'barchart_horizontal',
                             'Bar Horizontal Ordered': 'barchart_horizontal_ordered',
                             'Lollipop': 'lollypop',
                             'Lollipop Ordered': 'lollypop_ordered',

    }
    plot_dropdown_color = {'Red' : 'red','Blue':'blue','Yellow':'yellow'
                         }

    def __init__(self,  *args, **kwargs):
        """ Constructor function: Creation of the object with a specific values."""
        super().__init__(*args, **kwargs)
        self.createwidgets()     # initiates the createwidgets method.
        # self.readData = ReadData()
        self.myVar = tk.StringVar()

    def createwidgets(self):
        self.x_entry_var = StringVar()
        self.y_entry_var = StringVar()
        self.plot_entry_var = StringVar()
        self.variable_plot = StringVar()
        self.color_entry_var = StringVar()

        """ Types of Variable (the most important ones):
        - options_x/y_axis or options_plotting: Possible options for the x/y-axis or for the plotting method at the
            beginning. Afterwards (in option_xy_changed), it will be replaced by the menux/y. The possible x- and y-axes
            will be inserted into menux/y.
        - variable_x/y: What one selects in the GUI to become the x- and y-axis (with the help of x/y_entry_var).
        - inp_x/y_axis or inp_plot: OptionMenu for the possible options, options_x/y_axis is inserted into the
            OptionMenu.
        - x/y_entry_var: StringVar. You can use this kind of variable for the later usage of the get and set methods. 
            With this, you can save it as an axis and scan the values in there for the later plotting. This is a tkinter
            method.
        - x/y_entry_field: Entry-field in which you can either write down what axes you want or in which you can save
            which axis you did in fact choose. This is later needed for the further usage into the saving of which
            x-axis oder y-axis you want. For this, you use the x/y_entry_var and the getter- and setter-method.
        - result_x/y: shows the entries of a chosen x/y-value. """

        """ Creation of the buttonframe. In it, the open/close, filename, the summary and the tabs will be included. """
        self.buttonframe = tk.Frame(self.master)
        self.buttonframe.grid(row=0, column=0, rowspan=2, sticky="nsew")       #

        self.open_f = tk.Button(self.buttonframe, text="Open File", command=self.selectfile, activeforeground="red")
        # # Open button, selected method: selectfile (see below)
        self.open_f.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.label_f = tk.Label(self.buttonframe, text="Filename: ...", fg="green")
        # # Label of the file, until later (in select file), the filename gets the name of the path.
        self.label_f.grid(row=0, column=1, columnspan=7)
        self.button_close = tk.Button(self.buttonframe, text="Close", command=root.destroy, activeforeground="red")
        self.button_close.grid(row=0, column=8, sticky=tk.N + tk.S + tk.E + tk.W)

        self.empty = tk.Label(self.buttonframe, text="\n").grid(row=1, column=5)  # empty line

        """Summary-Window: Here, the chosen x/y-axis and the graph-style and analysis are shown."""
        self.lbl_summary = tk.Label(self.buttonframe, text="Summary", font=("default", 16)).grid(row=2, column=0)
        self.x_summary = tk.Label(self.buttonframe, text="x-axis:", font=("default", 16)).grid(row=2, column=1)
        self.x_summary_inp = tk.Label(self.buttonframe, fg="blue", textvariable=self.x_entry_var, foreground="blue")
        self.x_summary_inp.grid(row=2, column=2)
        self.y_summary = tk.Label(self.buttonframe, text="y-axis:", font=("default", 16)).grid(row=2, column=3)
        self.y_summary_inp = tk.Label(self.buttonframe, fg="blue", textvariable=self.y_entry_var)
        self.y_summary_inp.grid(row=2, column=4)
        self.plot_summary = tk.Label(self.buttonframe, text="plot:", font=("default", 16)).grid(row=2, column=5)
        self.plot_summary_inp = tk.Label(self.buttonframe, fg="blue", textvariable=self.plot_entry_var)
        self.plot_summary_inp.grid(row=2, column=6)
        self.analysis_summary = tk.Label(self.buttonframe, text="colour:", font=("default", 16)).grid(row=2, column=7)
        self.analysis_summary_inp = tk.Label(self.buttonframe, fg="blue", textvariable=self.color_entry_var)
        self.analysis_summary_inp.grid(row=2, column=8)

        self.empty = tk.Label(self.buttonframe, text="").grid(row=3, column=5)  # empty line

        """ Creation of the Tabs. First step: Creation of the tabsframe INTO the buttonframe. You need the ttk method
        and the Notebook, in which the tabs are inserted into."""
        self.tabsframe = tk.LabelFrame(self.buttonframe, text="Choose your settings:", font=("default", 20))
        self.tabsframe.grid(row=4, column=0, columnspan=9, sticky=tk.N + tk.S + tk.E + tk.W)
        self.tf = ttk.Notebook(self.tabsframe)     # notebook-widget creates the possible tabs
        self.tab1 = ttk.Frame(self.tf)
        self.tab2 = ttk.Frame(self.tf)
        self.tab3 = ttk.Frame(self.tf)
        self.tab4 = ttk.Frame(self.tf)
        self.tf.add(self.tab1, state='disabled', text="Settings x-axis")    # adding a tab into the notebook
        self.tf.add(self.tab2, state='disabled', text="Settings y-axis")
        self.tf.add(self.tab3, state='disabled', text="Plotting options")
        self.tf.add(self.tab4, state='disabled', text="Plot Window")
        self.tf.grid(row=1, column=0)

        """ TAB1: Setting of the x-axis"""
        self.empty = tk.Label(self.tab1).grid(row=0, column=9)  # empty row

        self.infox = ttk.Label(self.tab1, text="Here, you can choose which values you want to choose for your x-axis")
        self.infox.grid(row=1, column=0, columnspan=3)

        self.empty = tk.Label(self.tab1).grid(row=2, column=9)     # empty row

        # # Creation of the option-menu for x. At the beginning empty, afterwards it is filled with the help
        # # of the function options_xy_changed and the menux/y.
        self.options_x_axis = [""]
        self.variable_x = StringVar(self.tab1)    # "presented" option in options-menu, get and set can be used here
        self.variable_x.set(self.options_x_axis[0])        # first step: variable_x is set as the first entry of the
        # # options_x_axis value
        self.variable_x.trace('w', self.option_x_selected)     # traces the overwritting of the variable_x with the
        # # function option_x_selected (see below), which one is pickedß

        self.lbl_x = tk.Label(self.tab1, text="Choose your\nx-axis")
        self.lbl_x.grid(row=3, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        # # Create the entry field for x and y of the OptionMenu, which can be changed. Important:You can either choose
        # # the axis manually or set it through the later function and thus through the OptionMenu-choosing
        # # (function: option_x/y_selected) """
        self.inp_x_axis = OptionMenu(self.tab1, self.variable_x, *self.options_x_axis)
        self.inp_x_axis.grid(row=3, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

        self.empty = tk.Label(self.tab1).grid(row=4, column=9)    # empty row

        self.lbl_datapath = tk.Label(self.tab1, text="Data path")
        self.lbl_datapath.grid(row=5, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.x_entry_field = tk.Entry(self.tab1, textvariable=self.x_entry_var)    # x_entry_var is inserted into the
        # # field; later, this can be updated from the selected x-axis (see options_x_selected)
        self.x_entry_field.grid(row=5, column=1)

        self.empty = tk.Label(self.tab1).grid(row=6, column=9)

        # # Here you can sniff into the data of the chosen axis, which in turn will be saved for later usage or
        # # shown in the result_x/y
        self.lbl_sniff_x = tk.Label(self.tab1, text="Want to sniff into the\nx-data?")   # possible: retrieve!
        self.lbl_sniff_x.grid(row=7, column=0)
        self.sniff_x = tk.Button(self.tab1, text="Sniff the x-data", command=self.retrieve_x_data,
                                 activeforeground="red")     # when clicked, it calls the retrieve_x_data
        self.sniff_x.grid(row=7, column=1)

        # # Here, there is a label which ist created, so that we can later see the results of the x and y entry.
        # # The text is changed later with the help of the retrieve_x and retrieve_x function, which gets the values
        # # from the multiparser function.
        #self.result_x = tk.Label(self.tab1, text="")      # text will be changed (function: retrieve_x_data)
        self.result_x = st.ScrolledText(self.tab1, width=50, height=6)
        self.result_x.grid(row=7, column=3)   #rowspan=2, columnspan=2

        self.empty = tk.Label(self.tab1).grid(row=8, column=9)    # empty row

        self.lbl_result_path_x = tk.Label(self.tab1, text="Path:").grid(row=9, column=1)
        self.lbl_result_path_x_entry = tk.Label(self.tab1, text="", justify=LEFT)     # entry will be later shown (function: retrieve_x_data)
        self.lbl_result_path_x_entry.grid(row=9, column=3, sticky=tk.W)
        self.lbl_result_number_x = tk.Label(self.tab1, text="Number of entries:").grid(row=10, column=1)
        self.lbl_result_number_x_entry = tk.Label(self.tab1, text="", justify=LEFT)   # entry will be later shown (function: retrieve_x_data)
        self.lbl_result_number_x_entry.grid(row=10, column=3, sticky=tk.W)

        """ TAB2: Settings y-axis """
        # # Same procedure as for the x-axis, see above.
        self.empty = tk.Label(self.tab2).grid(row=0, column=9)  # 0+1 row

        self.infoy = ttk.Label(self.tab2, text="Here, you can choose which values you want to choose for your y-axis")
        self.infoy.grid(row=1, column=0, columnspan=3)

        self.empty = tk.Label(self.tab2, text="").grid(row=2, column=9)

        self.options_y_axis = [""]
        self.variable_y = StringVar(self.tab2)
        self.variable_y.set(self.options_y_axis[0])
        self.variable_y.trace('w', self.option_y_selected)

        self.lbl_y = tk.Label(self.tab2, text="Choose your\ny-axis")
        self.lbl_y.grid(row=3, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.inp_y_axis = OptionMenu(self.tab2, self.variable_y, *self.options_y_axis)
        self.inp_y_axis.grid(row=3, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

        self.empty = tk.Label(self.tab2, text="").grid(row=4, column=9)

        self.lbl_datapath = tk.Label(self.tab2, text="Data path")
        self.lbl_datapath.grid(row=5, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        # self.y_entry_var = StringVar()
        self.y_entry_field = tk.Entry(self.tab2, textvariable=self.y_entry_var)   # eventually: text='empty'
        self.y_entry_field.grid(row=5, column=1)

        self.empty = tk.Label(self.tab2, text="").grid(row=6, column=9)

        self.lbl_sniff_y = tk.Label(self.tab2, text="Want to sniff into the\nx-data?")
        self.lbl_sniff_y.grid(row=7, column=0)
        self.sniff_y = tk.Button(self.tab2, text="Sniff the x-data", command=self.retrieve_y_data,
                                 activeforeground="red")  #
        self.sniff_y.grid(row=7, column=1)

        # self.result_y = tk.Label(self.tab2, text="")      # text will be changed (function: retrieve_x_data)
        self.result_y = st.ScrolledText(self.tab2, width=50, height=6)
        self.result_y.grid(row=7, column=3)

        self.empty = tk.Label(self.tab2).grid(row=8, column=9)

        self.lbl_result_path_y = tk.Label(self.tab2, text="Path:").grid(row=9, column=1)
        self.lbl_result_path_y_entry = tk.Label(self.tab2, text="", justify=LEFT)
        self.lbl_result_path_y_entry.grid(row=9, column=3, sticky=tk.W)
        self.lbl_result_number_y = tk.Label(self.tab2, text="Number of entries:").grid(row=10, column=1)
        self.lbl_result_number_y_entry = tk.Label(self.tab2, text="", justify=LEFT)
        self.lbl_result_number_y_entry.grid(row=10, column=3, sticky=tk.W)

        """ TAB3: Plot-Options """
        self.empty = tk.Label(self.tab3, text="").grid(row=0, column=9)  # empty row

        #+self.options_plotting = ["Scatter", "Line", "Sinus", "3D"] TODO: EXPORT !!

        self.options_plotting = list(self.plot_dropdown_dic.keys()) # TODO: EXPORT
        self.variable_plot = StringVar(self.tab3)     # see variable_x
        self.variable_plot.set(self.options_plotting[0])
        self.variable_plot.trace('w', self.option_plot_color_selected)
        # EVENTUELL HIER NOCH EIN TRACE HINZUFÜGEN, BRAUCHEN ABER EINE FUNKTION!

        self.lbl_graph = tk.Label(self.tab3, text="Choose your\nGraph-Style")
        self.lbl_graph.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        # same fot the OptionMenu with the plotting-methods
        self.inp_plot = OptionMenu(self.tab3, self.variable_plot, *self.options_plotting)
        self.inp_plot.grid(row=1, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

        self.lbl_plot_field = tk.Label(self.tab3, text="You choose to\nuse this plotting").grid(row=2, column=0)
        self.plot_entry_field = tk.Entry(self.tab3, textvariable=self.plot_entry_var)   # eventually: text='empty'
        self.plot_entry_field.grid(row=2, column=1)

        self.empty = tk.Label(self.tab3).grid(row=3, column=9)  # 0+1 row

        self.options_color = list(self.plot_dropdown_color.keys())
        self.variable_color = StringVar(self.tab3)
        self.variable_color.set(self.options_color[0])
        self.variable_color.trace('w', self.option_plot_color_selected)

        self.lbl_color = tk.Label(self.tab3, text="Which color do\nyou want")
        self.lbl_color.grid(row=4, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        # same fot zhe OptionMenu with the plotting-methods
        self.inp_color = OptionMenu(self.tab3, self.variable_color, *self.options_color)
        self.inp_color.grid(row=4, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

        self.lbl_color_field = tk.Label(self.tab3, text="You choose to\nuse this color").grid(row=5, column=0)
        self.color_entry_field = tk.Entry(self.tab3, textvariable=self.color_entry_var)   # eventually: text='empty'
        self.color_entry_field.grid(row=5, column=1)

        self.empty = tk.Label(self.tab3).grid(row=6, column=9)  # 0+1 row

        """ TAB4: Plot-Problem """
        self.plot_window = Plotwindow(self.tab4, (10, 8))         # inch
        # self.plot_window = Plotwindow(self.plotframe, (10, 8))  # inch

        self.plot_f = tk.Button(self.tab3, text="Plot", activeforeground="red", command=self.plot_window.plot)  # NOCH COMMAND HINEINSCHREIBEN
        self.plot_f.grid(row=7, column=0, rowspan=2, columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W)

        self.button_clear = tk.Button(self.tab4, text="Clear\nthe\nplot", command=self.clear)
        self.button_clear.grid(row=0, column=8, sticky=tk.N + tk.S + tk.E + tk.W)

    def selectfile(self):
        """ Function 'select file': With help of the tkinter askopenfilename, we save the name of the file as filename,
        so that we can use it later. """

        filename = filedialog.askopenfilename(filetypes=[("JSON-File", "*.json"), ("CSV-File", "*.csv")],
                                              title="Which data do you want plotted?")
        objContainer.setobj("selectedFile", filename)    # saves the filename into the objectContainer
        m = MultiParser(filename=filename)
        objContainer.setobj("mpobject", m)
        self.label_f.configure(text=filename)    # changes the label from "Filename ... to the filename (with path)
        self.option_xy_changed()       # executes the function option_xy_change (description see below)
        self.tf.tab(self.tab1, state='normal')     # activates the tabs
        self.tf.tab(self.tab2, state='normal')
        self.tf.tab(self.tab3, state='normal')
        self.tf.tab(self.tab4, state='normal')

    def option_xy_changed(self):
        """ Function 'option x-y-changed': Reads the data and finds possible key names for the axes. In particular,
         it uses the modul multiparser, the method find_possible_keynames_all.
         A new menu for x and y (menux/menuy) needs to be defined. If not, then only the first option of the
         options_x/y_axis will be shown. First, the data is inserted with multiparser into the options_x/y_axis,
         afterwards, the it is inserted into the menux/y. This is later insertes through the variable_x/y.set
         method. """

        menux = self.inp_x_axis["menu"]     # the menux is defined as the inp_x_axis (OptionMenu)
        menuy = self.inp_y_axis["menu"]     # same as for x
        # print(menux, type(menux))
        # # Next step: The list of options_x_axis and options_x_axis is changed into a list, in which the objContainer
        # # (filename of the opened file) is put into the get_parseobject().find_possible_keynames_all().keys()
        options_x_axis = list(objContainer.getobj(
            "mpobject").get_parseobject().find_possible_keynames_all().keys())
        options_y_axis = list(objContainer.getobj(
            "mpobject").get_parseobject().find_possible_keynames_all().keys())

        menux.delete(0, "end")
        menuy.delete(0, "end")

        # # add_command:
        # # label="string": the entries in options_x_axis are inserted into the menux/y.
        # # command=lambda (function): From Debug-Modus and with trying it explains that it is possible to change the
        # # OptionMenu. The values in the menu are the variable_x.set from the new options menu.
        for string in options_x_axis:
            menux.add_command(label=string, command=lambda value=string: self.variable_x.set(value))
            menuy.add_command(label=string, command=lambda value=string: self.variable_y.set(value))

        # print(options_x_axis, options_y_axis)
        self.variable_x.set(options_x_axis[1])     # "presented" x and y-values are shown
        self.variable_y.set(options_y_axis[-1])

    def option_x_selected(self, *args):
        """ Function option_x_selected (and below: option_y_selected): The CHOSEN option ('variable') of the OptionMenu
        which was selected will be inserted into x_entry_field and saved. """
        self.x_entry_field.delete(0, END)
        self.x_entry_field.insert(0, self.variable_x.get())    # in the x-entry field the picked values are shown and
        # # inserted into the position
        return self.variable_x.get()

    def option_y_selected(self, *args):
        """ See option_x_selected (above). """
        # # Same as for variable_x
        self.y_entry_field.delete(0, END)
        self.y_entry_field.insert(0, self.variable_y.get())
        return self.variable_y.get()

    def retrieve_x_data(self):
        """ Function retrieve_x_data: The values of the picked x-data (x_entry_var) are being scanned by the method
        multiparser (scan_values). Moreover, the results are shown into the result_x label field."""

        v1 = objContainer.getobj("mpobject").get_parseobject().find_possible_keypath(self.x_entry_var.get())
        # print(v1)
        retrieved_data = objContainer.getobj("mpobject").get_parseobject().scan_values('xvalues', v1)
        # Saving the x_entry_var into parseobject and scan the values of it (scan_values) and saves it into xvalues
        # # NOCH SCHAUEN: würde auch self.variable_y.get()) gehen?
        v2_text = str(retrieved_data)    #+ "\n" + str(v2)[87:165] + "\n..."
        if len(v2_text) <= 1000:
            pass
        else:
            v2_text = str(retrieved_data)[0:1000]
        # self.result_x.configure(text=v2_text)    # changes the text in result_x
        self.result_x.delete('1.0', END)
        self.result_x.insert(tk.INSERT, v2_text)

        v1 = str(v1)
        lengthx = str(len(retrieved_data))
        self.lbl_result_path_x_entry.configure(text=v1)
        self.lbl_result_number_x_entry.configure(text=lengthx)

        return retrieved_data

    def retrieve_y_data(self):
        """ See retrieve_x_data (above). """

        w1 = objContainer.getobj("mpobject").get_parseobject().find_possible_keypath(self.y_entry_var.get())
        w2 = objContainer.getobj("mpobject").get_parseobject().scan_values('yvalues', w1)
        w2_text = str(w2)
        # print(w)
        # self.result_y.configure(text=w2_text)    # changes the text in result_y
        if len(w2_text) <= 1000:
            pass
        else:
            w2_text = str(w2)[0:1000]
        # self.result_x.configure(text=v2_text)    # changes the text in result_x
        self.result_y.delete('1.0', END)
        self.result_y.insert(tk.INSERT, w2_text)

        w1 = str(w1)
        lengthy = str(len(w2))
        self.lbl_result_path_y_entry.configure(text=w1)
        self.lbl_result_number_y_entry.configure(text=lengthy)
        return w2

    def option_plot_color_selected(self, *args):
        """ See option_x_selected (above). """
        # # Same as for variable_x
        self.plot_entry_field.delete(0, END)
        self.plot_entry_field.insert(0, self.variable_plot.get())

        self.color_entry_field.delete(0, END)
        self.color_entry_field.insert(0, self.variable_color.get())

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

    # def plotxy(self, x, y):
    #     self.axes.scatter(x, y)
    #     self.c1.draw()

    def clearplot(self):
        self.axes.cla()  # clear axes
        self.c1.draw()

    def plot(self):  #selects plot to draw; gets called from plot button
        app.tf.select(app.tab4)

        '''
        to add new plot styles you have to do 3 things:
        1) write a plot method and add it after def plot(self)
        2) make an entry in plot_dropdown_dic (see there)
        3) add another elif case in def plot(self)
        '''
        plotstyle = app.plot_dropdown_dic[app.variable_plot.get()]
        if plotstyle =='testplot':
            self.testplot()
        elif plotstyle =='data_scatterplot':
            self.data_scatterplot()
        elif plotstyle =='mean_xy':
            self.mean_xy()
        elif plotstyle =='earth_overlay':
            self.earth_overlay()
        elif plotstyle =='piechart':
            self.piechart()
        elif plotstyle =='histogram':
            self.histogram()
        elif plotstyle =='barchart':
            self.barchart()
        elif plotstyle =='histogram':
            self.histogram()
        elif plotstyle == 'cosinewave':
            self.cosinewave()
        elif plotstyle == 'stemandleafplot':
            self.stemandleafplot()
        elif plotstyle == 'lollypop':
            self.lollypop()
        elif plotstyle == 'lollypop_ordered':
            self.lollypop_ordered()
        elif plotstyle == 'barchart_ordered':
            self.barchart_ordered()
        elif plotstyle == 'piechart_ordered':
            self.piechart_ordered()
        elif plotstyle == 'barchart_horizontal_ordered':
            self.barchart_horizontal_ordered()
        elif plotstyle == 'barchart_horizontal':
            self.barchart_horizontal()
    #just a test plot to test the drop down

    def testplot(self):
        x = range(1000)  # XXX plottable data to test
        y = []
        for i in range(1000):
            y.append(random.randint(0, 200))

        self.axes.scatter(x, y)
        self.c1.draw()

    def piechart(self):
        self.axes.remove()
        self.axes = self.figure.add_subplot(111)
        """A pie chart is a circle divided into sectors that each represent a proportion of the whole.
        It is often used to show proportion, where the sum of the sectors equal 100%."""


        xdata = app.retrieve_x_data()
        ydata = app.retrieve_y_data()

        x_label = str(app.option_x_selected())
        y_label = str(app.option_y_selected())

        self.axes.set_title(f"Piechart - {x_label} X {y_label}")
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
        self.axes.pie(xdata, autopct='%1.1f%%')
        self.axes.legend(ydata, loc="upper left")
        circle = matplotlib.patches.Circle((0, 0), 0.7, color='white')
        self.axes.add_artist(circle)
        self.axes.add_artist(circle)
        self.c1.draw()

    def piechart_ordered(self):
        self.axes.remove()
        self.axes = self.figure.add_subplot(111)
        """A pie chart is a circle divided into sectors that each represent a proportion of the whole.
        It is often used to show proportion, where the sum of the sectors equal 100%."""

        xdata = app.retrieve_x_data()
        ydata = app.retrieve_y_data()

        x_label = str(app.option_x_selected())
        y_label = str(app.option_y_selected())

        df = pd.DataFrame({'Yvalue': ydata, 'Xvalue': xdata})
        ordered_df = df.sort_values(by='Xvalue')

        self.axes.set_title(f"Piechart - {x_label} X {y_label}")
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
        self.axes.pie(ordered_df['Xvalue'], autopct='%1.1f%%')
        self.axes.legend(ordered_df['Yvalue'], loc="upper left")
        circle = matplotlib.patches.Circle((0, 0), 0.7, color='white')
        self.axes.add_artist(circle)
        self.axes.add_artist(circle)
        self.c1.draw()

    def histogram(self):
        self.axes.remove()
        self.axes = self.figure.add_subplot(111)
        """A histogram takes as input a numeric variable only.
        The variable is cut into several bins, and the number of observation per bin
        is represented by the height of the bar. It is possible to represent the
        distribution of several variable on the same axis using this technique."""

        xdata = app.retrieve_x_data()
        ydata = app.retrieve_y_data()

        x_label = str(app.option_x_selected())
        y_label = str(app.option_y_selected())

        self.axes.set_title(f"Histogram - {x_label} X {y_label}")
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
        chart_color_typ = app.plot_dropdown_color[app.variable_color.get()]
        # print(chart_color_typ)
        self.axes.hist(xdata,label=True, bins=len(ydata),edgecolor='black',color=chart_color_typ)
        self.c1.draw()

    def barchart(self):
        self.axes.remove()
        self.axes = self.figure.add_subplot(111)
        """A histogram takes as input a numeric variable only.
        The variable is cut into several bins, and the number of observation per bin
        is represented by the height of the bar. It is possible to represent the
        distribution of several variable on the same axis using this technique."""

        xdata = app.retrieve_x_data()
        ydata = app.retrieve_y_data()
        x_label = str(app.option_x_selected())
        y_label = str(app.option_y_selected())

        self.axes.set_title(f"Barchart - {x_label} X {y_label}")
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
        chart_color_typ = app.plot_dropdown_color[app.variable_color.get()]
        # print(chart_color_typ)
        self.axes.bar(ydata, xdata, width=0.8, bottom=None, align="center",color=chart_color_typ)
        self.axes.set_xticks(ydata)
        self.c1.draw()

    def barchart_ordered(self):
        self.axes.remove()
        self.axes = self.figure.add_subplot(111)
        """A histogram takes as input a numeric variable only.
        The variable is cut into several bins, and the number of observation per bin
        is represented by the height of the bar. It is possible to represent the
        distribution of several variable on the same axis using this technique."""

        xdata = app.retrieve_x_data()
        ydata = app.retrieve_y_data()

        x_label = str(app.option_x_selected())
        y_label = str(app.option_y_selected())

        df = pd.DataFrame({'Yvalue': ydata, 'Xvalue': xdata})
        ordered_df = df.sort_values(by='Xvalue')

        self.axes.set_title(f"Barchart - {x_label} X {y_label}")
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
        chart_color_typ = app.plot_dropdown_color[app.variable_color.get()]
        # print(chart_color_typ)
        self.axes.bar(ordered_df['Yvalue'], ordered_df['Xvalue'], width=0.8, bottom=None,
                      align="center",color=chart_color_typ)
        self.axes.set_xticks(ordered_df['Yvalue'])
        self.c1.draw()

    def barchart_horizontal(self):
        self.axes.remove()
        self.axes = self.figure.add_subplot(111)
        """A histogram takes as input a numeric variable only.
        The variable is cut into several bins, and the number of observation per bin
        is represented by the height of the bar. It is possible to represent the
        distribution of several variable on the same axis using this technique."""

        xdata = app.retrieve_x_data()
        ydata = app.retrieve_y_data()

        x_label = str(app.option_x_selected())
        y_label = str(app.option_y_selected())

        self.axes.set_title(f"Barchart - {x_label} X {y_label}")
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
        chart_color_typ = app.plot_dropdown_color[app.variable_color.get()]
        # print(chart_color_typ)
        self.axes.barh(ydata, xdata,color=chart_color_typ)
        self.c1.draw()


    def barchart_horizontal_ordered(self):
        self.axes.remove()
        self.axes = self.figure.add_subplot(111)
        """A histogram takes as input a numeric variable only.
        The variable is cut into several bins, and the number of observation per bin
        is represented by the height of the bar. It is possible to represent the
        distribution of several variable on the same axis using this technique."""

        xdata = app.retrieve_x_data()
        ydata = app.retrieve_y_data()

        x_label = str(app.option_x_selected())
        y_label = str(app.option_y_selected())

        df = pd.DataFrame({'Yvalue': ydata, 'Xvalue': xdata})
        ordered_df = df.sort_values(by='Xvalue')

        self.axes.set_title(f"Barchart - {x_label} X {y_label}")
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
        chart_color_typ = app.plot_dropdown_color[app.variable_color.get()]
        # print(chart_color_typ)
        self.axes.barh(ordered_df['Yvalue'],ordered_df['Xvalue'],color=chart_color_typ)
        self.c1.draw()

    def lollypop(self):
        self.axes.remove()
        self.axes = self.figure.add_subplot(111)
        """A histogram takes as input a numeric variable only.
        The variable is cut into several bins, and the number of observation per bin
        is represented by the height of the bar. It is possible to represent the
        distribution of several variable on the same axis using this technique."""

        xdata = app.retrieve_x_data()
        ydata = app.retrieve_y_data()

        x_label = str(app.option_x_selected())
        y_label = str(app.option_y_selected())

        self.axes.set_title(f"Lollypop - {x_label} X {y_label}")
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
        self.axes.stem(ydata,xdata)
        self.axes.set_ylim(0)
        self.c1.draw()

    def lollypop_ordered(self):
        self.axes.remove()
        self.axes = self.figure.add_subplot(111)
        """A histogram takes as input a numeric variable only.
        The variable is cut into several bins, and the number of observation per bin
        is represented by the height of the bar. It is possible to represent the
        distribution of several variable on the same axis using this technique."""


        xdata = app.retrieve_x_data()
        ydata = app.retrieve_y_data()

        x_label = str(app.option_x_selected())
        y_label = str(app.option_y_selected())

        df = pd.DataFrame({'Yvalue': ydata, 'Xvalue': xdata})
        ordered_df = df.sort_values(by='Xvalue')

        self.axes.set_title(f"Lollypop Ordered - {x_label} X {y_label}")
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
        self.axes.stem(ordered_df['Yvalue'],ordered_df['Xvalue'])
        self.axes.set_ylim(0)
        self.c1.draw()

    def data_scatterplot(self):
        #first iteration
        #plots data from last retrieved data set
        #convert to float or axes are not ordered!!!!


        xdata = app.retrieve_x_data()
        ydata = app.retrieve_y_data()
        x_label = str(app.option_x_selected())
        y_label = str(app.option_y_selected())
        xdata = list(map(float, xdata))
        ydata = list(map(float, ydata))
        # print('xdata from data_scatterplot:', xdata, 'type:', type(xdata))
        # print('ydata from data_scatterplot:', ydata, 'type:', type(ydata))
        #print('xlabel from data_scatterplot:', x_label, 'type:', type(x_label))
        #print('ylabel from data_scatterplot:', y_label, 'type:', type(y_label))
        #self.figure.ylabel(y_label)
        self.axes.set_title('A simple and fast scatter plot')
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
        self.axes.scatter(xdata, ydata)
        self.c1.draw()

    def cosinewave(self):
        x = np.arange(0, 20, 0.2)             # allows us to get x values for the data plot
        y = np.cos(x)                 # allows the amplitude of the cosine wave to be cosine of a variable like time
        # print('self:', self)
        self.axeshlines(y=0, color='r')
        self.axes.scatter(x, y)
        self.c1.draw()
        pass

    def stemandleafplot(self):
        # marks obtained by students in an examination
        y = [10, 11, 22, 24, 35, 37, 45, 47, 48, 58, 56, 59, 61, 71, 81, 92, 95]
        x = [1, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 6, 7, 8, 9, 9]  # corresponding stems
        # set the x axis and y axis limits
        self.axes.set_xlim([0, 10])
        self.axes.set_ylim([0, 100])

        y_line, x_line, baseline = self.axes.stem(x, y, '-.')
        #mpl.mplcursors.cursor()
        self.c1.draw()

    #analytics:

    def mean_xy(self):
        xdata = app.retrieve_x_data()
        ydata = app.retrieve_y_data()

        xdata = list(map(float, xdata))     # needed to order axes
        ydata = list(map(float, ydata))

        # print('xdata from mean_xy:', xdata, 'type:', type(xdata))
        # print('ydata from mean_xy:', ydata, 'type:', type(ydata))

        mean_x = float(np.mean(np.array(xdata)))
        mean_y = float(np.mean(np.array(ydata)))

        std_deviation_x = float(np.std(np.array(xdata)))
        std_deviation_y = float(np.std(np.array(ydata)))

        # ellipse_std_dev = matplotlib.patches.Ellipse((mean_x, mean_y), (100), (100), angle=0)
        ellipse_std_dev = matplotlib.patches.Ellipse((mean_x, mean_y),
                                                     width=(std_deviation_x*2),
                                                     height=(std_deviation_y*2),
                                                     angle=0)
        ellipse_std_dev.set_fill(0)
        ellipse_std_dev.set_color('red')
        self.axes.add_artist(ellipse_std_dev)

        self.axes.hlines(mean_y, min(xdata), max(xdata), color='red')
        self.axes.vlines(mean_x, min(ydata), max(ydata), color='red')
        self.axes.scatter(mean_x, mean_y, color='red')

        mean_x = round(mean_x, 2)
        mean_y = round(mean_y, 2)
        std_deviation_x = round(std_deviation_x, 2)
        std_deviation_y = round(std_deviation_y, 2)

        mean_text = 'X = ' + str(mean_x) + ' +- ' + str(std_deviation_x) + '\n' + 'Y = ' + str(mean_y) + ' +- ' + str(std_deviation_y)
        self.axes.annotate(mean_text, (mean_x, mean_y), color='red')

        self.c1.draw()

    #additional plots:

    def earth_overlay(self):
        #TODO: *scling and use another file with no imprint
        overlay = plt.imread('pngkit_world-map-outline-png_1243196.png')
        self.axes.imshow(overlay, aspect='auto')
        self.c1.draw()

print("__name__:", __name__)

if __name__ == "__main__":

    root = tk.Tk()
    root.title("What do you want to plot?")
    app = ApplicationWindow(master=root)

    objContainer = myVars()
    # print("meineObjekte=", objContainer.getAllNames())
    app.mainloop()
