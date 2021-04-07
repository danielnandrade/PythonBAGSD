import tkinter as tk
from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
# import json
# import csv
# import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# from datetime import datetime
# from dv import *
from dv.multiparser import multiParser
import tkinter.scrolledtext as st
# from IPython.utils.tests.test_wildcard import obj_t

# matplotlib.use('TkAgg')


class ApplicationWindow(tk.Frame):
    """ Class ApplicationWindow: In this class, the whole system of the window (GUI) is created. Moreover """

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
        self.analysis_entry_var = StringVar()

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
        self.label_f = tk.Label(self.buttonframe, text="Filename: ...", fg="red")
        # # Label of the file, until later (in select file), the filename gets the name of the path.
        self.label_f.grid(row=0, column=1, columnspan=7)
        self.button_close = tk.Button(self.buttonframe, text="Close", command=root.destroy, activeforeground="red")
        self.button_close.grid(row=0, column=8, sticky=tk.N + tk.S + tk.E + tk.W)

        self.empty = tk.Label(self.buttonframe, text="\n").grid(row=1, column=5)  # empty line

        """Summary-Window: Here, the chosen x/y-axis and the graph-style and analysis are shown."""
        self.lbl_summary = tk.Label(self.buttonframe, text="Summary", font=("default", 16)).grid(row=2, column=0)
        self.x_summary = tk.Label(self.buttonframe, text="x-axis:", font=("default", 16)).grid(row=2, column=1)
        self.x_summary_inp = tk.Label(self.buttonframe, state='disabled', textvariable=self.x_entry_var)
        self.x_summary_inp.grid(row=2, column=2)
        self.y_summary = tk.Label(self.buttonframe, text="y-axis:", font=("default", 16)).grid(row=2, column=3)
        self.y_summary_inp = tk.Label(self.buttonframe, state='disabled', textvariable=self.y_entry_var)
        self.y_summary_inp.grid(row=2, column=4)
        self.plot_summary = tk.Label(self.buttonframe, text="plot:", font=("default", 16)).grid(row=2, column=5)
        self.plot_summary_inp = tk.Label(self.buttonframe, state='disabled', textvariable=self.plot_entry_var)
        self.plot_summary_inp.grid(row=2, column=6)
        self.analysis_summary = tk.Label(self.buttonframe, text="analysis:", font=("default", 16)).grid(row=2, column=7)
        self.analysis_summary_inp = tk.Label(self.buttonframe, state='disabled', textvariable=self.analysis_entry_var)
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
        self.lbl_result_path_x_entry = tk.Label(self.tab1, text="")     # entry will be later shown (function: retrieve_x_data)
        self.lbl_result_path_x_entry.grid(row=9, column=3)
        self.lbl_result_number_x = tk.Label(self.tab1, text="Number of entries:").grid(row=10, column=1)
        self.lbl_result_number_x_entry = tk.Label(self.tab1, text="")   # entry will be later shown (function: retrieve_x_data)
        self.lbl_result_number_x_entry.grid(row=10, column=3)

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
        self.lbl_result_path_y_entry = tk.Label(self.tab2, text="")
        self.lbl_result_path_y_entry.grid(row=9, column=3)
        self.lbl_result_number_y = tk.Label(self.tab2, text="Number of entries:").grid(row=10, column=1)
        self.lbl_result_number_y_entry = tk.Label(self.tab2, text="")
        self.lbl_result_number_y_entry.grid(row=10, column=3)

        """ TAB3: Plot-Options """
        self.empty = tk.Label(self.tab3, text="").grid(row=0, column=9)  # empty row

        self.options_plotting = ["Scatter", "Line", "Sinus", "3D"]
        self.variable_plot = StringVar(self.tab3)     # see variable_x
        self.variable_plot.set(self.options_plotting[0])
        # EVENTUELL HIER NOCH EIN TRACE HINZUFÜGEN, BRAUCHEN ABER EINE FUNKTION!

        self.lbl_graph = tk.Label(self.tab3, text="Choose your\nGraph-Style")
        self.lbl_graph.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        # same fot the OptionMenu with the plotting-methods
        self.inp_plot = OptionMenu(self.tab3, self.variable_plot, *self.options_plotting)
        self.inp_plot.grid(row=1, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

        self.plot_entry_field = tk.Entry(self.tab3, textvariable=self.plot_entry_var)   # eventually: text='empty'
        self.plot_entry_field.grid(row=2, column=1)

        self.empty = tk.Label(self.tab3).grid(row=3, column=9)  # 0+1 row

        self.options_analysis = ["Medium", "Deviation"]
        self.variable_analysis = StringVar(self.tab3)
        self.variable_analysis.set(self.options_analysis[0])
        # EVENTUELL HIER NOCH EIN TRACE HINZUFÜGEN, BRAUCHEN ABER EINE FUNKTION!

        self.lbl_analysis = tk.Label(self.tab3, text="Choose what you\nwant to analyse")
        self.lbl_analysis.grid(row=4, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        # same fot zhe OptionMenu with the plotting-methods
        self.inp_analysis = OptionMenu(self.tab3, self.variable_analysis, *self.options_analysis)
        self.inp_analysis.grid(row=4, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

        self.analysis_entry_field = tk.Entry(self.tab3, textvariable=self.analysis_entry_var)   # eventually: text='empty'
        self.analysis_entry_field.grid(row=5, column=1)

        self.empty = tk.Label(self.tab3).grid(row=6, column=9)  # 0+1 row

        self.plot_f = tk.Button(self.tab3, text="Plot", activeforeground="red")  # NOCH COMMAND HINEINSCHREIBEN
        self.plot_f.grid(row=7, column=0, rowspan=2, columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W)

        """ TAB4: Plot-Window """
        self.plot_window = Plotwindow(self.tab4, (10, 8))         # inch
        # self.plot_window = Plotwindow(self.plotframe, (10, 8))  # inch

        self.button_clear = tk.Button(self.tab4, text="Clear\nthe\nplot", command=self.clear)
        self.button_clear.grid(row=0, column=8, sticky=tk.N + tk.S + tk.E + tk.W)

    def selectfile(self):
        """ Function 'select file': With help of the tkinter askopenfilename, we save the name of the file as filename,
        so that we can use it later. """

        filename = filedialog.askopenfilename(filetypes=[("JSON-File", "*.json"), ("CSV-File", "*.csv")],
                                              title="Which data do you want plotted?")
        objContainer.setobj("selectedFile", filename)    # saves the filename into the objectContainer
        m = multiParser(filename=filename)
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

    def option_y_selected(self, *args):
        """ See option_x_selected (above). """
        # # Same as for variable_x
        self.y_entry_field.delete(0, END)
        self.y_entry_field.insert(0, self.variable_y.get())

    def retrieve_x_data(self):
        """ Function retrieve_x_data: The values of the picked x-data (x_entry_var) are being scanned by the method
        multiparser (scan_values). Moreover, the results are shown into the result_x label field."""

        v1 = objContainer.getobj("mpobject").get_parseobject().find_possible_keypath(self.x_entry_var.get())
        # print(v1)
        v2 = objContainer.getobj("mpobject").get_parseobject().scan_values('xvalues', v1)
        # Saving the x_entry_var into parseobject and scan the values of it (scan_values) and saves it into xvalues
        # # NOCH SCHAUEN: würde auch self.variable_y.get()) gehen?
        v2_text = str(v2)    #+ "\n" + str(v2)[87:165] + "\n..."
        if len(v2_text) <= 1000:
            pass
        else:
            v2_text = str(v2)[0:1000]
        # self.result_x.configure(text=v2_text)    # changes the text in result_x
        self.result_x.delete('1.0', END)
        self.result_x.insert(tk.INSERT, v2_text)

        v1 = str(v1)
        lengthx = str(len(v2))
        self.lbl_result_path_x_entry.configure(text=v1)
        self.lbl_result_number_x_entry.configure(text=lengthx)

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
    # print("meineObjekte=", objContainer.getAllNames())
    app.mainloop()
