import tkinter as tk
from tkinter import filedialog, simpledialog
import json
import matplotlib
#matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as myplt
fname = " "

class Plotwindow():
    def __init__(self, masterframe, size):
        (w, h) = size
        self.figure = myplt.Figure(size)
        self.axes = self.figure.add_subplot(111)
        # create canvas as matplotlib drawing area        
        self.canvas = FigureCanvasTkAgg(self.figure, master=masterframe)
        self.canvas.get_tk_widget().grid()  # Get reference to tk_widget

    #        print (self.canvas.get_tk_widget())
    def plotxy(self, x, y):
        self.axes.scatter(x, y)
        self.canvas.draw()

    def clearplot(self):
        self.axes.cla()  # clear axes /clf: clear figure
        self.canvas.draw()


class ReadData():

    def __init__(self):
        self.index = 0  # index of function call

    def myscat(self):
        with open(filename.get()) as f:
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


def plotdata():
    b3.invoke()
    b3.flash()
    x, y = datrd.myscat()
    plot_w.plotxy(x, y)

def get_data():
    filename.set(filedialog.askopenfilename(initialdir="/Users/Alfa/python", title="Open Data File:",
                 filetypes=(("json files", "*.json"), ("all files", "*.*"))))

def clear():
    plot_w.clearplot()


if __name__ == "__main__":  # verhindert Start bei Import; ermöglicht Start bei Ausführung als Executable.
    datrd = ReadData()
    root = tk.Tk()
    root.title("MyPlot")
    filename = tk.StringVar()
    filename.set(" ")
    mainframe = tk.Frame()
    plot_w = Plotwindow(mainframe, (8, 6))
    mainframe.grid(row=1, rowspan=8, column=0)
    buttonframe = tk.Frame()
    buttonframe.grid(row=0, column=0,sticky = tk.W)
    l1 = tk.Label(buttonframe, text="Daten plotten: ")  #
    l1.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
    b1 = tk.Button(buttonframe, text="Select", command=get_data)  #
    b1.grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
    b2 = tk.Button(buttonframe, text="Plot", command=plotdata)  #
    b2.grid(row=0, column=2, sticky=tk.N + tk.S + tk.E + tk.W)
    b3 = tk.Button(buttonframe, text="Clear", command=clear, activeforeground = "red")
    b3.grid(row=0, column=3, sticky=tk.N + tk.S + tk.E + tk.W)
    b4 = tk.Button(buttonframe, text="Close", command=root.destroy)
    b4.grid(row=0, column=4, sticky=tk.N + tk.S + tk.E + tk.W)
    root.mainloop()
