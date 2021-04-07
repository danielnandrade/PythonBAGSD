import pandas as pd
import numpy as np
import random  # XXX only for testing
import matplotlib.figure
import matplotlib.patches
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class PlotEngine:
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
                         'Lollipop Ordered': 'lollypop_ordered'
                         }

    plot_dropdown_color = {'Red': 'red', 'Blue': 'blue', 'Yellow': 'yellow'}

    def __init__(self, plotframe):
        self.figure = plt.Figure((8, 8))
        self.axes = self.figure.add_subplot(111)
        # create canvas as matplotlib drawing area
        self.c1 = FigureCanvasTkAgg(self.figure, master=plotframe)
        self.c1.get_tk_widget().grid(column=0, row=0, columnspan=4)  # Get reference to tk_widget
        toolbar = NavigationToolbar2Tk(self.c1, plotframe, pack_toolbar=False)
        # matplotlib navigation toolbar; "pack_toolbar = False" necessary for .grid() geometry manager
        toolbar.grid(column=0, row=1)#, sticky=tk.W)
        toolbar.update()

    def get_plot_dropdown_dic_as_list(self):
        return list(self.plot_dropdown_dic.keys())

    def get_plot_dropdown_color_as_list(self):
        return list(self.plot_dropdown_color.keys())

    def set_plot_parameters(self, xvalues, yvalues, xlabel, ylabel, plotstyle, graphcolor="blue"):
        self.xvalues = xvalues
        self.yvalues = yvalues
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.plotstyle = plotstyle
        self.graphcolor = graphcolor

        plotstyle = self.plot_dropdown_dic[plotstyle]

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

    def clearplot(self):
        self.axes.cla()  # clear axes
        self.c1.draw()

    def data_scatterplot(self):
        # first iteration
        # plots data from last retrieved data set
        # convert to float or axes are not ordered!!!!
        self.axes.remove()
        self.axes = self.figure.add_subplot(111)

        self.xvalues = list(map(float, self.xvalues))
        self.yvalues = list(map(float, self.yvalues))
        # print('self.xvalues from data_scatterplot:', self.xvalues, 'type:', type(self.xvalues))
        # print('self.yvalues from data_scatterplot:', self.yvalues, 'type:', type(self.yvalues))
        # print('xlabel from data_scatterplot:', self.xlabel, 'type:', type(self.xlabel))
        # print('ylabel from data_scatterplot:', self.ylabel, 'type:', type(self.ylabel))
        # self.figure.ylabel(self.ylabel)
        self.axes.set_title(f"Fast scatter plot - {self.xlabel} X {self.ylabel}")  # yyy
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)
        self.axes.scatter(self.xvalues, self.yvalues)
        self.c1.draw()

    def piechart(self):
        self.axes.remove()
        self.axes = self.figure.add_subplot(111)
        """A pie chart is a circle divided into sectors that each represent a proportion of the whole.
        It is often used to show proportion, where the sum of the sectors equal 100%."""

        self.axes.set_title(f"Piechart - {self.xlabel} X {self.ylabel}")
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)
        self.axes.pie(self.xvalues, autopct='%1.1f%%')
        self.axes.legend(self.yvalues, loc="upper left")
        circle = matplotlib.patches.Circle((0, 0), 0.7, color='white')
        self.axes.add_artist(circle)
        self.axes.add_artist(circle)
        self.c1.draw()

    def piechart_ordered(self):
        self.axes.remove()
        self.axes = self.figure.add_subplot(111)
        """A pie chart is a circle divided into sectors that each represent a proportion of the whole.
        It is often used to show proportion, where the sum of the sectors equal 100%."""

        df = pd.DataFrame({'Yvalue': self.yvalues, 'Xvalue': self.xvalues})
        ordered_df = df.sort_values(by='Xvalue')

        self.axes.set_title(f"Piechart - {self.xlabel} X {self.ylabel}")
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)
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

        self.axes.set_title(f"Histogram - {self.xlabel} X {self.ylabel}")
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)
        chart_color_typ = self.graphcolor
        # print(chart_color_typ)
        self.axes.hist(self.xvalues, label=True, bins=len(self.yvalues), edgecolor='black', color=chart_color_typ)
        self.c1.draw()

    def barchart(self):
        self.axes.remove()
        self.axes = self.figure.add_subplot(111)
        """A histogram takes as input a numeric variable only.
        The variable is cut into several bins, and the number of observation per bin
        is represented by the height of the bar. It is possible to represent the
        distribution of several variable on the same axis using this technique."""

        self.axes.set_title(f"Barchart - {self.xlabel} X {self.ylabel}")
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)
        chart_color_typ = self.graphcolor
        # print(chart_color_typ)
        self.axes.bar(self.yvalues, self.xvalues, width=0.8, bottom=None, align="center", color=chart_color_typ)
        self.axes.set_xticks(self.yvalues)
        self.c1.draw()

    def barchart_ordered(self):
        self.axes.remove()
        self.axes = self.figure.add_subplot(111)
        """A histogram takes as input a numeric variable only.
        The variable is cut into several bins, and the number of observation per bin
        is represented by the height of the bar. It is possible to represent the
        distribution of several variable on the same axis using this technique."""

        df = pd.DataFrame({'Yvalue': self.yvalues, 'Xvalue': self.xvalues})
        ordered_df = df.sort_values(by='Xvalue')

        self.axes.set_title(f"Barchart - {self.xlabel} X {self.ylabel}")
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)
        chart_color_typ = self.graphcolor
        # print(chart_color_typ)
        self.axes.bar(ordered_df['Yvalue'], ordered_df['Xvalue'], width=0.8, bottom=None,
                      align="center", color=chart_color_typ)
        self.axes.set_xticks(ordered_df['Yvalue'])
        self.c1.draw()

    def barchart_horizontal(self):
        self.axes.remove()
        self.axes = self.figure.add_subplot(111)
        """A histogram takes as input a numeric variable only.
        The variable is cut into several bins, and the number of observation per bin
        is represented by the height of the bar. It is possible to represent the
        distribution of several variable on the same axis using this technique."""

        self.axes.set_title(f"Barchart - {self.xlabel} X {self.ylabel}")
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)
        chart_color_typ = self.graphcolor
        # print(chart_color_typ)
        self.axes.barh(self.yvalues, self.xvalues, color=chart_color_typ)
        self.c1.draw()

    def barchart_horizontal_ordered(self):
        self.axes.remove()
        self.axes = self.figure.add_subplot(111)
        """A histogram takes as input a numeric variable only.
        The variable is cut into several bins, and the number of observation per bin
        is represented by the height of the bar. It is possible to represent the
        distribution of several variable on the same axis using this technique."""

        df = pd.DataFrame({'Yvalue': self.yvalues, 'Xvalue': self.xvalues})
        ordered_df = df.sort_values(by='Xvalue')

        self.axes.set_title(f"Barchart - {self.xlabel} X {self.ylabel}")
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)
        chart_color_typ = self.graphcolor
        # print(chart_color_typ)
        self.axes.barh(ordered_df['Yvalue'], ordered_df['Xvalue'], color=chart_color_typ)
        self.c1.draw()

    def lollypop(self):
        self.axes.remove()
        self.axes = self.figure.add_subplot(111)
        """A histogram takes as input a numeric variable only.
        The variable is cut into several bins, and the number of observation per bin
        is represented by the height of the bar. It is possible to represent the
        distribution of several variable on the same axis using this technique."""

        self.axes.set_title(f"Lollypop - {self.xlabel} X {self.ylabel}")
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)
        self.axes.stem(self.yvalues, self.xvalues)
        self.axes.set_ylim(0)
        self.c1.draw()

    def lollypop_ordered(self):
        self.axes.remove()
        self.axes = self.figure.add_subplot(111)
        """A histogram takes as input a numeric variable only.
        The variable is cut into several bins, and the number of observation per bin
        is represented by the height of the bar. It is possible to represent the
        distribution of several variable on the same axis using this technique."""

        df = pd.DataFrame({'Yvalue': self.yvalues, 'Xvalue': self.xvalues})
        ordered_df = df.sort_values(by='Xvalue')

        self.axes.set_title(f"Lollypop Ordered - {self.xlabel} X {self.ylabel}")
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)
        self.axes.stem(ordered_df['Yvalue'], ordered_df['Xvalue'])
        self.axes.set_ylim(0)
        self.c1.draw()

    def cosinewave(self):           # YYY
        """This type of graphs depict periodic waves (wind/sound/light) that are generated from oscillations """
        self.xvalues = list(map(float, self.xvalues))

        # x = np.arange(0, 20, 0.2) # allows us to get x values for the data plot
        # y = np.cos(x) # allows the amplitude/height (the peak deviation of the function from zero)
        # of the cosine wave to be cosine of a variable like time

        x = np.array(self.xvalues)  # allows us to get x values for the data plot
        print(x, type(x))
        y = x*np.cos(x)  # allows the amplitude/height (the peak deviation of the function from zero)
        # of the cosine wave to be cosine of a variable like time
        print('self:', self)


        #self.axes.stem(mean_y, (self.xvalues == 0), color='red')
        #self.my_axeshlines(y=0, color='r')

        self.axes.plot(x, y)

        self.axes.set_title('Group E Project_Cosine_wave_plot')
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)

        self.c1.draw()

    def stemandleafplot(self):  # YYY
        # marks obtained by students in an examination
        self.xvalues = list(map(float, self.xvalues))
        self.yvalues = list(map(float, self.yvalues))

        #y = [10, 11, 22, 24, 35, 37, 45, 47, 48, 58, 56, 59, 61, 71, 81, 92, 95]
        #x = [1, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 6, 7, 8, 9, 9]  # corresponding stems


        # set the x axis and y axis limits
        self.axes.set_xlim([min(self.xvalues), max(self.xvalues)])
        self.axes.set_ylim([min(self.yvalues), max(self.yvalues)])
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)

        self.axes.stem(self.xvalues, self.yvalues, '-.')
        #y_line, x_line, baseline

        #mpl.mplcursors.cursor()
        self.c1.draw()

    #analytics:

    def mean_xy(self):
        self.xvalues = list(map(float, self.xvalues))     # needed to order axes
        self.yvalues = list(map(float, self.yvalues))

        # print('self.xvalues from mean_xy:', self.xvalues, 'type:', type(self.xvalues))
        # print('self.yvalues from mean_xy:', self.yvalues, 'type:', type(self.yvalues))

        mean_x = float(np.mean(np.array(self.xvalues)))
        mean_y = float(np.mean(np.array(self.yvalues)))

        std_deviation_x = float(np.std(np.array(self.xvalues)))
        std_deviation_y = float(np.std(np.array(self.yvalues)))

        # ellipse_std_dev = matplotlib.patches.Ellipse((mean_x, mean_y), (100), (100), angle=0)
        ellipse_std_dev = matplotlib.patches.Ellipse((mean_x, mean_y),
                                                     width=(std_deviation_x*2),
                                                     height=(std_deviation_y*2),
                                                     angle=0)
        ellipse_std_dev.set_fill(0)
        ellipse_std_dev.set_color('red')
        self.axes.add_artist(ellipse_std_dev)

        self.axes.hlines(mean_y, min(self.xvalues), max(self.xvalues), color='red')
        self.axes.vlines(mean_x, min(self.yvalues), max(self.yvalues), color='red')
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
        # overlay = self.plt.imread('pngkit_world-map-outline-png_1243196.png')
        # self.axes.imshow(overlay, aspect='auto')
        # self.c1.draw()
        pass
