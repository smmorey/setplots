
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 

from __future__ import absolute_import
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt


from clawpack.geoclaw import topotools
from six.moves import range


#--------------------------
def setplot(plotdata=None):
#--------------------------
    
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """ 


    from clawpack.visclaw import colormaps, geoplot
    from numpy import linspace
    import math

    if plotdata is None:
        from clawpack.visclaw.data import ClawPlotData
        plotdata = ClawPlotData()


    plotdata.clearfigures()  # clear any old figures,axes,items data

    def speed(current_data):
        from numpy import ma, where, sqrt, log10
        drytol = 1e-3
        q = current_data.q
        h=q[0,:,:]
        hu=q[1,:,:]
        hv=q[2,:,:]
        u = where(h>0.0, hu/h, 0.)
        v = where(h>0.0, hv/h, 0.) 
        speed = sqrt(u**2 +v**2)
        return speed

    def stress(current_data):
        from numpy import ma, where, sqrt, log10
        q = current_data.q
        h=q[0,:,:]
        hu=q[1,:,:]
        hv=q[2,:,:]
        u = where(h>0.0, hu/h, 0.)
        v = where(h>0.0, hv/h, 0.)
        speed = np.sqrt(u**2 +v**2) #Speed calc, same as above
        n = 0.06 #Manning's n
        g = 9.8 #gravity 
        cf = where(h>0.0, (g*n**2)/(h**(1./3)), 0.) #calculate friction coefficient, DONT FORGET THE FUCKING PERIOD YOU IDIOT (mike)
        stress = 1000*cf*(speed**2)
        return stress




#####----------------------------------------- 
    # Gorge  depth
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='Gorgetesting_depth', figno=21)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Depth')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [95.0,95.45]
    plotaxes.ylimits = [29.5,30.0]

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = geoplot.depth #variable to plot
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 300
    plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]
    plotitem.amr_patchedges_show = [0] 

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    #plotitem.pcolor_cmap = geoplot.blank
    plotitem.pcolor_cmap = geoplot.bw_colormap
    plotitem.pcolor_cmin = 2000.0
    plotitem.pcolor_cmax = 6000.0
    #plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]

    #plotaxes.afteraxes = addgauges
#####----------------------------------------- 
    # Gorge  speed
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='Gorgetesting_speed', figno=22)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Speed')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [95.0,95.45]
    plotaxes.ylimits = [29.5,30.0]

    # speed
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = speed
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 80
    plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]
    plotitem.amr_patchedges_show = [0] 

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    #plotitem.pcolor_cmap = geoplot.blank
    plotitem.pcolor_cmap = geoplot.bw_colormap
    plotitem.pcolor_cmin = 2000.0
    plotitem.pcolor_cmax = 6000.0
    #plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]

    #plotaxes.afteraxes = addgauges

#####----------------------------------------- 
    # Gorge  stress
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='Gorgetesting_stress', figno=23)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Stress')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [95.0,95.45]
    plotaxes.ylimits = [29.5,30.0]

    # stress
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = stress
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 30000  #make this reasonable max stress
    plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]
    plotitem.amr_patchedges_show = [0] 

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    #plotitem.pcolor_cmap = geoplot.blank
    plotitem.pcolor_cmap = geoplot.bw_colormap
    plotitem.pcolor_cmin = 2000.0
    plotitem.pcolor_cmax = 6000.0
    #plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]





    


#-----------------------------------------
    
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    #plotdata.print_framenos = np.arange(0,5,1)       # list of frames to print
    #plotdata.print_framenos = [1,2,3,4,5]       #frame is a timestep, so this is the way
    #plotdata.print_gaugenos = [1,2,3,4]          # list of gauges to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = False                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = False                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?
    plotdata.parallel = True                 # make multiple frame png's at once

    return plotdata

