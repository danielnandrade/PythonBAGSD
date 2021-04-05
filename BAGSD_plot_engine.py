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
        -self.options_plotting = ["Scatter", "Line", "3D", "..."] #fill this list with  def give_plottable_styles(self):


'''

#imports:

import matplotlib as plt


import BAGSD_plot_styles as stl


def test_execution():
    #simple testing method to test stuff in  that module
    pass

style = ''
xvalues = []
yvalues = []

#class BAGSD_plotter(*args,**kwargs):
class BAGSD_plotter:
    #organizes and executes all the plotting
    #handles and creates subplots to send back to the ui

    def __init__(self,*args,**kwargs):#,xvalues=None,yvalues=None,style=None):
        print(kwargs)
        self.style = style
        self.xvalues = xvalues
        self.yvalues = yvalues
        #what shit has the constructor to initialize??




    def call_style(self):
        pickedstyle = stl.style(xvalues,yvalues)
        print(pickedstyle)
        return pickedstyle
        #just chooses plotting styles from BAGSD_plot_styleso


    def pipe_plot_data(self):
        #gives plot data to called plot style
        pass

    def give_plottable_styles(self):
        print('list aof callable styles')
        #listOfStyles = {"2D": 2, "3D: 3, "Pie":1 ....}
        #give back needed parameters???
        pass



if __name__ == '__main__':
    test_execution()