'''
Commenting:
* plot styles are based on matplotlib


TODO:



'''

#imports:

import matplotlib as plt


def test_execution():
    #simple testing method to test stuff in  that module

    pass


def testplot(x,y):
    finished_plot = scatter(x, y)
    return finished_plot






def scatter_2D():
    #simple 2d scatter
    pass

def lineplot_2D():
    #simple line plot
    pass

def plot_static2(p):
    t = list(range(1, 100))  # obj.scan_values("lonx","$.features[*].geometry.coordinates[0]")
    tt = [x1 ** 2 for x1 in t]  # obj.scan_values("laty","$.features[*].geometry.coordinates[1]")
    #mag = [x2 ** 3 for x2 in lonx]  # obj.scan_values("mag","$.features[*].properties.mag")

    plot_w.axes.set_ylim(0, 800)
    plot_w.axes.set_xlabel("Quadrat- und Kubik-Kurve")
    plot_w.axes.xaxis.grid(True, which="minor")
    plot_w.axes.yaxis.tick_right()
    plot_w.axes.plot(t, tt, "-r", label = "Squared")
    plot_w.c1.draw()

def plot_daniel(xvalues, yvalues, xlabel, ylabel):
    pass





if __name__ == '__main__':
    test_execution()