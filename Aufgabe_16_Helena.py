import tkinter as tk
import matplotlib.pyplot as plt
import csv
import json
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.filedialog import askopenfilename
from tkinter import messagebox


class Plotwindow:
    def __init__(self, masterframe, size):   # size aus plt
        # (w, h) = size
        self.figure = plt.Figure(size)
        self.axes = self.figure.add_subplot(111)
        # create canvas as matplotlib drawing area
        self.canvas = FigureCanvasTkAgg(self.figure, master=masterframe)
        self.canvas.get_tk_widget().grid()  # Get reference to tk_widget

    def plotxy(self, x, y):
        self.axes.scatter(x, y,color = "red",marker = ".")
        self.canvas.draw()

    def clearplot(self):
        self.axes.cla()  # clear axes
        self.canvas.draw()


class ReadData:

    def __init__(self):
        self.index = 0  # index of function call

    def callback(self):
        global filename
        filename = askopenfilename(filetypes=[("json", "*.json"), ("csv", "*.csv"), ("All files", "*.*")])  # filetypes: Filter Dateitypen
        x = filename.split('.')
        if x[1] != 'csv' and x[1] != 'json':
            print("No Json- or CSV-File!")
            messagebox.showinfo("Alert", "No Json- or CSV-file!")
        else:
            p.config(state='normal')

    def myjson(self):
        with open(filename) as f:
            all_eq_data = json.load(f)
        all_eq_dicts = all_eq_data['features']
        mags, lons, lats = [], [], []
        for eq_dict in all_eq_dicts:
            mag = eq_dict['properties']['mag']
            lon = eq_dict['geometry']['coordinates'][0]
            lat = eq_dict['geometry']['coordinates'][1]
            mags.append(mag)
            lons.append(lon)
            lats.append(lat)
        return mags, lats

    def mycsv(self):
        with open(filename) as f:
            reader = csv.reader(f, delimiter=",")   # siehe in csv Datei
            headerrow = next(reader)
            x, y3 = [], []
            for row in reader:
                date = datetime.strptime(row[2], "%Y%m%d")
                x.append(date)
                y3.append(float(row[3]))
        return x, y3


def plotdata():
    if filename.split('.')[1] == 'json':
        x, y = datrd.myjson()     # datrd ist Variable der Instanziierung von ReadData()
        plot_w.plotxy(x, y)    # plot_w Instanz von Plotwindow()
    elif filename.split('.')[1] == 'csv':
        x, y = datrd.mycsv()
        plot_w.plotxy(x, y)


def clear():
    plot_w.clearplot()
    p.config(state='disabled')


print("__name__:", __name__)

if __name__ == "__main__":

    root = tk.Tk()

    root.title("MyPlot")

    mainframe = tk.Frame(root)    # Frame wird gesetzt: tk.Frame(root)
    mainframe.grid(row=2, column=0)

    datrd = ReadData()     # Instantiierung der Klasse ReadData

    plot_w = Plotwindow(mainframe, (8, 6))  # inch


    buttonframe = tk.Frame(root)    # Steht im root drinnen
    buttonframe.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)

    label = tk.Label(buttonframe, text="Please select your json or csv-file\nto work with or close the program.")
    label.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W)

    o = tk.Button(buttonframe, text='Open File', command=datrd.callback)  # command = enthält den auszuführenden Befehl
    o.grid(row=0, column=1, sticky=tk.N + tk.S)

    p = tk.Button(buttonframe, text="Plot", state='disabled', command=plotdata, activeforeground="red")  #
    p.grid(row=0, column=2, sticky=tk.N + tk.S)

    cl = tk.Button(buttonframe, text="Clear", command=clear)
    cl.grid(row=0, column=3, sticky=tk.N + tk.S)

    c = tk.Button(buttonframe, text="Close", command=root.destroy, activeforeground="red")
    c.grid(row=0, column=4, sticky=tk.N + tk.S + tk.W)

    root.mainloop()
