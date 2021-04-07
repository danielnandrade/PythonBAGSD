

############################new
import pandas as pd
############################new

    plot_dropdown_dic = {'Test plot' : 'testplot',
                         'Data scatter plot': 'data_scatterplot',
                         'Pie chart': 'piechart',
                         'Pie chart Ordered': 'piechart_ordered',
                         'Histogram': 'histogram',
                         'Bar chart': 'barchart',
                         'Bar chart Ordered': 'barchart_ordered',
                         'Bar Horizontal': 'barchart_horizontal',
                         'Bar Horizontal Ordered': 'barchart_horizontal_ordered',
                         'Lollipop': 'lollypop',
                         'Lollipop Ordered': 'lollypop_ordered',
                         'analytics: mean': 'mean_xy',
                         'Earth overlay': 'earth_overlay',
                         'Cosine wave': 'cosinewave',
                         'Stem and leaf plot': 'stemandleafplot'
                         }
    plot_dropdown_color = {'Red' : 'red','Blue':'blue','Yellow':'yellow'
                         }


############################new
        self.options_color = list(self.plot_dropdown_color.keys())
        self.variable_color = StringVar(self.buttonframe)
        self.variable_color.set(self.options_color[0])
        self.lbl3 = tk.Label(self.buttonframe, text="Choose your\nColor")
        self.lbl3.grid(row=4, column=4, sticky=tk.N + tk.S + tk.E + tk.W)
        self.inp_plot = OptionMenu(self.buttonframe, self.variable_color, *self.options_color)
        self.inp_plot.grid(row=4, column=5, sticky=tk.N + tk.S + tk.E + tk.W)
############################new


########################change
    def plot(self):  #selects plot to draw; gets called from plot button
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

    ########################change



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
        print(chart_color_typ)
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
        print(chart_color_typ)
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
        print(chart_color_typ)
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
        print(chart_color_typ)
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
        print(chart_color_typ)
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
        #draw crossing lines
        #use numpy mean

        #let lines cross?
        #return labels on which data set the mean is based
        pass

    def standard_dev(self,xdata=None,ydata=None):

        #use numpy standard dev

        #plot oval
        # return labels on which data set the standev is based
        pass


if __name__ == "__main__":
    """ 1st: Creation of the root-window (with title) and in the root-window the button-frame (which options we have 
    to plot it, see below) and the plot-frame (frame in which we plot) at the end. """
    root = tk.Tk()
    root.title("What do you want to plot?")
    app = ApplicationWindow(master=root)
    objContainer = myVars()
    print("meineObjekte=", objContainer.getAllNames())
    app.mainloop()uto