############################# Module used
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

############################# Variable part

x_value = [15, 30, 45, 10, 30, 60, 80, 90, 100, 130, 14]
x_label = "X Label"
y_value = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
y_label = "Y Label"
title_value = "Variable Title"
graph_colors = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']

############################# Pie CHART

def piechart():

    """A pie chart is a circle divided into sectors that each represent a proportion of the whole.
    It is often used to show proportion, where the sum of the sectors equal 100%."""

    plt.title(title_value)
    plt.pie(x_value, labels=y_value, autopct='%1.1f%%')
    plt.tight_layout()
    plt.show()

############################# Histogram CHART

def histogramchart():

    """A histogram takes as input a numeric variable only.
    The variable is cut into several bins, and the number of observation per bin
    is represented by the height of the bar. It is possible to represent the
    distribution of several variable on the same axis using this technique."""

    plt.title(title_value)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.hist(x_value,bins=len(y_value),edgecolor='black')
    plt.tight_layout()
    plt.show()

############################# Barchart CHART

def barchart():

    """A barplot shows the relationship between a numeric and a categoric variable.
    Each entity of the categoric variable is represented as a bar. The size of the
    bar represents its numeric value.
    Barplot is sometimes described as a boring way to visualize information.
    However it is probably the most efficient way to show this kind of data.
    Ordering bars and providing good annotation are often necessary."""

    plt.title(title_value)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.bar(range(0,len(y_value)), x_value)
    plt.xticks(range(0,len(y_value)), y_value)
    plt.show()

############################# Scatter CHART

def scatterchart():

    y_value_int = [45, 10, 85, 70, 40, 10, 65, 45, 60, 100, 15]
    """A scatterplot displays the relationship between 2 numeric variables.
    For each data point, the value of its first variable is represented on
    the X axis, the second on the Y axis"""

    plt.title(title_value)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.plot(x_value, y_value_int, linestyle=None, marker='o')
    plt.show()


############################# Scatter_line CHART

def scatterchart_line():

    y_value_int = [45, 10, 85, 70, 40, 10, 65, 45, 60, 100, 15]

    """A scatterplot displays the relationship between 2 numeric variables.
    For each data point, the value of its first variable is represented on
    the X axis, the second on the Y axis"""

    plt.title(title_value)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.plot(x_value, y_value_int, linestyle='-', marker='o')
    plt.show()

#############################  Lollipop_scatter CHART

def lollipop_scatter():

    y_value_int = [45, 10, 85, 70, 40, 10, 65, 45, 60, 100, 15]

    """A lollipop plot is basically a barplot, where the bar is transformed
    in a line and a dot. It shows the relationship between a numeric and a
    categoric variable.
    However it is more appealing and convey as well the information.
    It is especially useful when you have several bars of the same height:
    it avoids to have a cluttered figure and a Moiré effect."""

    plt.title(title_value)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.stem(y_value_int,x_value)
    plt.ylim(0)
    plt.show()

#############################  Lollipop_ordered CHART

def lollipop_ordered():

    y_value_int = [45, 10, 85, 70, 40, 10, 65, 45, 60, 100, 15]

    """A lollipop plot is basically a barplot, where the bar is transformed
    in a line and a dot. It shows the relationship between a numeric and a
    categoric variable.
    However it is more appealing and convey as well the information.
    It is especially useful when you have several bars of the same height:
    it avoids to have a cluttered figure and a Moiré effect."""

    df = pd.DataFrame({'Yvalue':y_value,'Xvalue':x_value})
    ordered_df = df.sort_values(by='Xvalue')
    my_range = range(1,len(df.index)+1)

    plt.title(title_value)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.stem(ordered_df['Xvalue'])
    plt.xticks(my_range, ordered_df['Yvalue'])
    plt.ylim(0)
    plt.show()

#############################  Lollipop_ordered_horizontal CHART

def lollipop_ordered_horizontal():

    y_value_int = [45, 10, 85, 70, 40, 10, 65, 45, 60, 100, 15]

    """A lollipop plot is basically a barplot, where the bar is transformed
    in a line and a dot. It shows the relationship between a numeric and a
    categoric variable.
    However it is more appealing and convey as well the information.
    It is especially useful when you have several bars of the same height:
    it avoids to have a cluttered figure and a Moiré effect."""

    df = pd.DataFrame({'Yvalue':y_value,'Xvalue':x_value})
    ordered_df = df.sort_values(by='Xvalue')
    my_range = range(1,len(df.index)+1)

    plt.title(title_value)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.hlines(y=my_range, xmin=0, xmax=ordered_df['Xvalue'])
    plt.plot(ordered_df['Xvalue'], my_range)
    plt.yticks(my_range, ordered_df['Yvalue'])
    plt.show()


def main():
    piechart()
    histogramchart()
    barchart()
    scatterchart()
    scatterchart_line()
    lollipop_scatter()
    lollipop_ordered()
    lollipop_ordered_horizontal()

if __name__=="__main__":
    main()

