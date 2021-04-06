import tkinter as tk
from tkinter import *

from tkinter import filedialog, simpledialog, scrolledtext
import json, csv
import matplotlib
from datetime import datetime
from dv import *#multiparser as mparser

from IPython.utils.tests.test_wildcard import obj_t

from dv.multiparser import MultiParser

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

def option_x_selected(*args):
    print(variable_axes_x.get())
    x_entry_field.delete(0, END)  # OPTIONS_X[1])
    x_entry_field.insert(0, variable_axes_x.get())

def option_y_selected(*args):
    print(variable_axes_y.get())

    y_entry_field.delete(0, END)
    y_entry_field.insert(0, variable_axes_y.get())


def option_xy_changed():
    menux = inp_x["menu"]
    menuy = inp_y["menu"]
    OPTIONS_X = list(objContainer.getobj("mpobject").get_parseobject().find_possible_keynames_all().keys())#.append("Neb")#self.entry.get())
    OPTIONS_Y = list(objContainer.getobj("mpobject").get_parseobject().find_possible_keynames_all().keys())#.append("Neb")#self.entry.get())#OPTIONS_X[:]
    menux.delete(0, "end")
    menuy.delete(0, "end")
    for string in OPTIONS_X:
        menux.add_command(label=string,command=lambda value=string: variable_axes_x.set(value))
        menuy.add_command(label=string,command=lambda value=string: variable_axes_y.set(value))

    print(OPTIONS_X)
    #global variable_axes_x, variable_axes_y
    variable_axes_x.set(OPTIONS_X[1])
    variable_axes_y.set(OPTIONS_Y[-1])

    x_entry_field.delete(0,END)#OPTIONS_X[1])
    x_entry_field.insert(0,OPTIONS_X[1])

    y_entry_field.delete(0,END)
    y_entry_field.insert(0,OPTIONS_Y[-1])

def ShowChoice():
    print("You selected: " + str(myVar.get()))

class myVars:
    def __init__(self):
        self.objekte = {}

    def getobj(self,whichobjname):
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
        toolbar = NavigationToolbar2Tk(self.c1, masterframe,
                                       pack_toolbar=False)  # matplotlib navigation toolbar; "pack_toolbar = False" necessary for .grid() geometry manager
        res = toolbar.grid(column=0, row=1, sticky=tk.W)
        toolbar.update()

    def plotxy(self, x, y):
        self.axes.scatter(x, y)
        self.c1.draw()

    def clearplot(self):
        self.axes.cla()  # clear axes
        self.c1.draw()

#        b2.config(background = "blue",foreground = "white") # use .config for single or multiple assignments
#        b2["background"]="blue"                             # use [" "] = ... for single assignments

class ReadData:

    def __init__(self):
        self.index = 0                               # index of function call (currently unused)

    def myscatjson(self):
        #filename = '../data/eq_data_1_day_m1.json'  # anpassen an lokalen Pfad erforderlich
        filename = filedialog.askopenfilename(filetypes=[("json files", "*.json")],
                                              title="Welche JSON-Datei soll geplottet werden? Sach schon")
        with open(filename) as f:
            all_eq_data = json.load(f)
        all_eq_dicts = all_eq_data['features']
        mags, plas, lons, lats = [], [], [], []
        for eq_dict in all_eq_dicts:
            mag = eq_dict['properties']['mag']
            pla = eq_dict['properties']['place']
            lon = eq_dict['geometry']['coordinates'][0]
            lat = eq_dict['geometry']['coordinates'][1]
            mags.append(mag)
            plas.append(pla)
            lons.append(lon)
            lats.append(lat)
        return mags, lats

    def myscatcsv(self):
        filename = filedialog.askopenfilename(filetypes=[("Weather-File","DWD_TXK_MN004.csv"),("json files", "*.csv")],
                                              title="Welche CSV-Datei soll geplottet werden? Sach schon")
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            line_count = 0
            x = []
            y2 = []
            y3 = []

            for row in csv_reader:
                #        print("row:",row)
                if line_count == 0:
                    y3_lab = row[3]  # Read column title
                else:
                    date = datetime.strptime(row[2], "%Y%m%d")
                    x.append(date)
                    y3.append(float(row[3]))
                line_count += 1
            return x,y3
        
    def final_read_csv(self):
        # selected in DropDown x=Year Spalte[2], y=TWH Spalte[3]
        # x-werte = csvreader.getvalues(col=2)
        # y-werte = csvreader.getvalues(col=3)
        filename="C:/Users/Nebil/Desktop/DataScientist/PycharmProjects/pythonProject1/DWD_TXK_MN004.csv"
        #filename = objContainer.getobj("selectedFile")
        with open(filename) as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            next(reader)
            spalte2 = []
            spalte3 = []
            for row in reader:
                #spalt2 = datetime.strptime(row[2], "%Y%m%d")
                spalte2.append(row[2])
                spalte3.append(float(row[3]))
        print("X-Y-Werte",spalte2, spalte3)
        return spalte2,spalte3

def plotdatajson():
#    b2.invoke()             # b2 ausfuehren
#    b2.flash()              # kurzes Blinken von b2 (nur sichtbar, wenn activeforeground != bg)
    x, y = datrd.myscatjson()
    plot_w.plotxy(x, y)

def plotdatacsv():
    x, y = datrd.myscatcsv()
    plot_w.plotxy(x, y)

def clear():
    plot_w.clearplot()

def selectfile():
    filename = filedialog.askopenfilename(filetypes=[("JSON-File", "*.json"), ("json files", "*.json")],
                                          title="Welche CSV-Datei soll geplottet werden? Sach schon")
    objContainer.setobj("selectedFile",filename)
    #r.config(state="normal")
    m = MultiParser(filename=filename)
    objContainer.setobj("mpobject", m)
    lbl_filename.configure(text=filename)
    option_xy_changed()

def retrieve_x_data():
    print(x_entry_var.get())
    v = objContainer.getobj("mpobject").get_parseobject().find_possible_keypath(x_entry_var.get())
    v2=objContainer.getobj("mpobject").get_parseobject().scan_values('xvalues',v)
    print(v, type(END))
    length="1"
    if isinstance(v2, dict) or isinstance(v2,list):
        length = str(len(v2))
        if len(str(v2)) > 1000:
            print(v2)
            v2 = str(v2)[0:500] + "\n.........\n"


    lbl_result_key_x['text'] = "Pfad:"+v + "\nAnzahl:"+length
    lbl_result_x.configure(state='normal')
    lbl_result_x.delete("1.0", END)
    lbl_result_x.insert("end", str(v2))
    lbl_result_x.configure(state='disabled')

def retrieve_y_data():
    print("looking data for key:",y_entry_var.get())
    v=list(objContainer.getobj("mpobject").get_parseobject().scan_values('yvalues',y_entry_var.get()))
    print(v)
    #lbl_result_x.configure(text=v)

def plot_final_read_csv():
    x, y = datrd.final_read_csv()
    plot_w.plotxy(x, y)

def plot_static2():
    t = list(range(1, 100))  # obj.scan_values("lonx","$.features[*].geometry.coordinates[0]")
    tt = [x1 ** 2 for x1 in t]  # obj.scan_values("laty","$.features[*].geometry.coordinates[1]")
    #mag = [x2 ** 3 for x2 in lonx]  # obj.scan_values("mag","$.features[*].properties.mag")

    plot_w.axes.set_ylim(0, 800)
    plot_w.axes.set_xlabel("Quadrat- und Kubik-Kurve")
    plot_w.axes.xaxis.grid(True, which="minor")
    plot_w.axes.yaxis.tick_right()
    plot_w.axes.plot(t, tt, "-r", label = "Squared")
    plot_w.c1.draw()

def plot_static3():
    t = list(range(1, 100))  # obj.scan_values("lonx","$.features[*].geometry.coordinates[0]")
    tt = [x1 ** 3 for x1 in t]  # obj.scan_values("laty","$.features[*].geometry.coordinates[1]")
    #mag = [x2 ** 3 for x2 in lonx]  # obj.scan_values("mag","$.features[*].properties.mag")

    plot_w.axes.set_ylim(0, 800)
    plot_w.axes.set_xlabel("Quadrat- und Kubik-Kurve")
    plot_w.axes.xaxis.grid(True, which="minor")
    plot_w.axes.yaxis.tick_right()
    plot_w.axes.plot(t, tt, "-r", label = "Squared")
    plot_w.c1.draw()

print("__name__:", __name__)

if __name__ == "__main__":  # verhindert Start bei Import; ermöglicht Start bei Ausführung als Executable.
    root = tk.Tk()
    myVar = tk.StringVar()
    x_entry_var = StringVar()
    y_entry_var = StringVar()
    root.title("MyPlot")
    mainframe = tk.Frame(root)
    mainframe.grid(row=1, column=0)
    buttonframe = tk.Frame(root)
    buttonframe.grid(row=0, column=0, sticky=tk.W)
    datrd = ReadData()
    plot_w = Plotwindow(mainframe, (8, 6))  # inch
    lbl = tk.Label(buttonframe,text="myLabel for Plots")
    lbl.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
    b0 = tk.Button(buttonframe, text="File?", command=selectfile, activeforeground="red")  #
    b0.grid(row=1, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
    lbl_filename = tk.Label(buttonframe,text="Filename:...",fg="blue")
    lbl_filename.grid(row=0, column=1, columnspan=3)
    b_clear = tk.Button(buttonframe, text="Clear", command=clear)
    b_clear.grid(row=2, column=3, sticky=tk.N + tk.S + tk.E + tk.W)
    b_clear.config(activeforeground="red")
    b3 = tk.Button(buttonframe, text="Close", command=root.destroy, activeforeground="red")
    b3.grid(row=2, column=4, sticky=tk.N + tk.S + tk.E + tk.W)

    # c1 = FigureCanvasTkAgg(fig, master=root)  # matplotlib Zeichenflaeche
    # # print(c1)
    # # c1._tkcanvas.grid(row=0,column = 1,rowspan=20) #
    # c1.get_tk_widget().grid(row=0, column=1, rowspan=20)  #

    # auswaehlliste
    # Entity,Code,Year,Primary energy consumption (TWh)
    # ??? Hier die Liste aus dem CSV-Headern fuellen
    OPTIONS_X = ['']
    OPTIONS_Y = ["Entity", "Code", "Year", "Primary energy consumption (TWh)"]
    OPTIONS_PLOT = ["Scatter","Line","3D","..."]
    variable_axes_x = StringVar(buttonframe)
    variable_axes_x.set(OPTIONS_X[0])  # default value
    variable_axes_x.trace('w', option_x_selected)
    variable_axes_y = StringVar(buttonframe)
    variable_axes_y.set(OPTIONS_Y[0])  # default value
    variable_axes_y.trace('w', option_y_selected)
    variable_plot = StringVar(buttonframe)
    variable_plot.set(OPTIONS_PLOT[0])  # default value
    #variable_plot.trace('w', option_plot_changed)

    tk.Label(buttonframe,text="X-Achse").grid(row=3, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
    inp_x = OptionMenu(buttonframe, variable_axes_x, *OPTIONS_X)
    inp_x.grid(row=3, column=2, sticky=tk.N + tk.S + tk.E + tk.W)

    tk.Label(buttonframe, text="Y-Achse").grid(row=3, column=3, sticky=tk.N + tk.S + tk.E + tk.W)
    inp_y = OptionMenu(buttonframe, variable_axes_y, *OPTIONS_Y)
    inp_y.grid(row=3, column=4, sticky=tk.N + tk.S + tk.E + tk.W)

    # Plot-Type
    tk.Label(buttonframe, text="Graph-Style").grid(row=3, column=5, sticky=tk.N + tk.S + tk.E + tk.W)
    inp_plot = OptionMenu(buttonframe, variable_plot, *OPTIONS_PLOT)
    inp_plot.grid(row=3, column=6, sticky=tk.N + tk.S + tk.E + tk.W)

    b_plot = tk.Button(buttonframe, text="Plot", command=plot_final_read_csv, activeforeground="red")  #
    b_plot.grid(row=3, column=7, sticky=tk.N + tk.S + tk.E + tk.W)
    b_plot2 = tk.Button(buttonframe, text="Add to Plot2", command=plot_static2, activeforeground="red")  #
    b_plot2.grid(row=3, column=8, sticky=tk.N + tk.S + tk.E + tk.W)
    b_plot3 = tk.Button(buttonframe, text="Add to Plot3", command=plot_static3, activeforeground="red")  #
    b_plot3.grid(row=3, column=9, sticky=tk.N + tk.S + tk.E + tk.W)

    x_entry_field = tk.Entry(buttonframe, text='leer', textvariable=x_entry_var)
    x_entry_field.grid(row=4, column=2)
#    x_entry_field.insert(10, "XXXXX")

    y_entry_field = tk.Entry(buttonframe, text='leer')#, textvariable=x_entry_var)
    y_entry_field.grid(row=4, column=4)
#    x_entry_field.insert(10, "XXXXX")

    lbl_result_key_x = tk.Label(buttonframe, text="Testdaten X?")
    lbl_result_key_x.grid(row=5, column=1)
    bdata_x = tk.Button(buttonframe, text="retrieve...", command=retrieve_x_data, activeforeground="red")  #
    bdata_x.grid(row=5, column=2)

    # lbl_result_x = tk.Text(buttonframe, height=5, width=40)# relief=RIDGE, text = "whatever_you_do")# tk.Label(buttonframe, text="...data...")
    # #lbl_result_x.insert(tk.END,"your data here...")
    # scroll_bar = tk.Scrollbar(buttonframe, orient=VERTICAL, command=lbl_result_x.yview)
    # scroll_bar.grid(row=6, column=2,columnspan=1, sticky=NS,rowspan=2)
    # lbl_result_x.grid(row=6, column=1,sticky=W)
    # lbl_result_x.config(yscrollcommand=scroll_bar.set)#,font=('Arial', 8, 'bold', 'italic'))


    lbl_result_x = scrolledtext.ScrolledText(buttonframe,
                              wrap=tk.WORD,
                              width=40,
                              height=5,
                              font=("Times New Roman",
                                    10))
    lbl_result_x.grid(row=6, column=1, sticky=W)
    lbl_result_x.config(state=DISABLED)

    objContainer = myVars()
    print("meineObjekte=",objContainer.getAllNames())
    root.mainloop()



# das muss ausgelafert werden in CSVREADER_WIR !! TODO !!
# Entity,Code,Year,Primary energy consumption (TWh)
def getkeysfromcsv(filename):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
    headerrow = next(csv_reader)

    rlist = headerrow.split(",")
    print(rlist)
    return rlist

