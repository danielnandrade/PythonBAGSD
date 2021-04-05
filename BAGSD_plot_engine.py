'''
Commenting:
* plotting engine to that is called everytime the UI wants to plot something
* what parameters get piped??:
    -2d,3d or nD??
    -label naming?
    -
    -...
    -(what analytics to show)

+ scale axes of plotted data

TODO:
    * write comment how to call BAGSD_plotter() from ui:
        -describe options/p parameters to give
        -...

'''

#imports:

import matplotlib as plt


import BAGSD_plot_styles as stl


def test_execution():
    #simple testing method to test stuff in  that module

    pass

class BAGSD_plotter(*args,**kwargs)
    #organizes and executes all the plotting
    #handles and creates subplots to send back to the ui
    def __init__(self):
        #what shit has the constructor to initialize??
        pass

    def call_style(self, style):
        stl.
        #just chooses plotting styles from BAGSD_plot_styleso
        pass

    def pipe_plot_data(self):
        #gives plot data to called plot style
        pass





if __name__ == '__main__':
    test_execution()