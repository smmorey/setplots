
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

    # def erodibilityratio(current_data): # ratio of impelling forces (dimensionless shear stress T) to resisting forces (critical shear stress Tc)
    #     from numpy import ma, where, sqrt, log10
    #     q=current_data.q
    #             h=q[0,:,:]
    #     hu=q[1,:,:]
    #     hv=q[2,:,:]
    #     u = where(h>0.0, hu/h, 0.)
    #     v = where(h>0.0, hv/h, 0.)
    #     speed = sqrt(u**2 +v**2) #Speed calc, same as above
    #     n = 0.06 #Manning's n
    #     g = 9.8 #gravity 

    # def dsp(current_data): # dsp = depth slope product
    #     from numpy import ma, where, sqrt, log10
    #     q = current_data.q
    #     h=q[0,:,:]
    #     g = 9.8 # gravity
    #     dsp = 1000*g*h*0.02 # using a bulk channel gradient of 0.02-- will need to figure out how to make a localized measurement of this
    #     return dsp

    # def froude(current_data):
    #     from numpy import ma, where, sqrt, log10
    #     drytol = 1e-3
    #     q = current_data.q
    #     h=q[0,:,:]
    #     hu=q[1,:,:]
    #     hv=q[2,:,:]
    #     u = where(h>0.0, hu/h, 0.)
    #     v = where(h>0.0, hv/h, 0.)
    #     g = 9.8 
    #     speed = np.sqrt(u**2 +v**2)
    #     froude = speed/((g*h)**(1.2))
    #     return froude
    

    # def blocksize(current_data):
    #     from numpy import ma, where, sqrt, log10
    #     q = current_data.q
    #     h=q[0,:,:]
    #     hu=q[1,:,:]
    #     hv=q[2,:,:]
    #     u = where(h>0.0, hu/h, 0.)
    #     v = where(h>0.0, hv/h, 0.)
    #     speed = np.sqrt(u**2 +v**2) #Speed calc, same as above
    #     n = 0.04 #Manning's n
    #     g = 9.8 #gravity idiot
    #     cf = where(h>0.0, (g*n**2)/(h**(1./3)), 0.) 
    #     stress = 1000*cf*(speed**2)
    #     tc = 0.15*((0.02)**(1./4)) #need to choose a slope here, sooooo 0.02
    #     blocksize = stress/(tc*g*1700)
    #     return blocksize




#####----------------------------------------- 
    # Lake (depth)
    #-----------------------------------------
#    
    plotfigure = plotdata.new_plotfigure(name='lake_depth', figno=1)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Depth')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [93.0, 95.6]
    plotaxes.ylimits = [28.0,30.0]

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = geoplot.depth #variable to plot
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 200
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
    # Lake (speed)
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='lake_speed', figno=2)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Speed')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [93,94.96]
    plotaxes.ylimits = [28.96,29.77]

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
    # Lake (stress)
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='lake_stress', figno=3)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Stress')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [93,94.96]
    plotaxes.ylimits = [28.96,29.77]
    # stress
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = stress
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 2500  #make this reasonable max stress
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








#####----------------------------------------- 
    # Outburst (depth)
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='Outburst_depth', figno=11)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Depth')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [94.8,95.2]
    plotaxes.ylimits = [29.5,29.9]

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
    # Outburst (speed)
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='Outburst_speed', figno=12)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Speed')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [94.8,95.2]
    plotaxes.ylimits = [29.5,29.9]

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
    # Outburst (stress)
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='Outburst_stress', figno=13)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Stress')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [94.8,95.2]
    plotaxes.ylimits = [29.5,29.9]
    # stress
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = stress
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 40000  #make this reasonable max stress
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
    # Gorge  depth
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='Gorgetesting_depth', figno=21)
    plotfigure.show = True
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
    plotfigure.show = True
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
    plotitem.pcolor_cmax = 60
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
    plotfigure.show = True
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
    plotitem.pcolor_cmax = 10000  #make this reasonable max stress
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







#####----------------------------------------- 
    # Gorge-Tuting depth
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='gorge_tuting_depth', figno=24)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Depth')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [95.25,95.5]
    plotaxes.ylimits = [29.25,29.7]

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
    # Gorge-Tuting speed
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='gorge_tuting_speed', figno=25)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Speed')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [95.25,95.5]
    plotaxes.ylimits = [29.25,29.7]

    # speed
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = speed
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 60
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
    # Gorge-Tuting stress
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='gorge_tuting_stress', figno=26)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Stress')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [95.25,95.5]
    plotaxes.ylimits = [29.25,29.7]

    # stress
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = stress
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 16000  #make this reasonable max stress
    plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]
    plotitem.amr_patchedges_show = [0] 

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    #plotitem.pcolor_cmap = geoplot.blank
    plotitem.pcolor_cmap = geoplot.bw_colormap
    plotitem.pcolor_cmin = 2000.0
    plotitem.pcolor_cmax = 5000.0
    #plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]

    #plotaxes.afteraxes = addgauges







#####----------------------------------------- 
    # Gorge-Tuting2 depth - arrives here at Frame 12, t = 1.08e04
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='Gorge-Tuting2_depth', figno=27)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Depth')
    plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [94.85,95.35]
    plotaxes.ylimits = [28.9,29.35]

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = geoplot.depth #variable to plot
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 250
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
    # Gorge-Tuting2 speed
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='Gorge-Tuting2_speed', figno=28)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Speed')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [94.85,95.35]
    plotaxes.ylimits = [28.9,29.35]

    # speed
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = speed
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 60
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
    # Gorge-Tuting2 stress
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='Gorge-Tuting2_stress', figno=29)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Stress')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [94.85,95.35]
    plotaxes.ylimits = [28.9,29.35]

    # stress
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = stress
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 16000  #make this reasonable max stress
    plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]
    plotitem.amr_patchedges_show = [0] 

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    #plotitem.pcolor_cmap = geoplot.blank
    plotitem.pcolor_cmap = geoplot.bw_colormap
    plotitem.pcolor_cmin = 2000.0
    plotitem.pcolor_cmax = 5000.0
    #plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]







#####----------------------------------------- 
    # Tuting-ish(depth) arrives here in Frame 16, t = 1.44e04
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='Tuting_depth', figno=30)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Depth')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [94.65,95.0]
    plotaxes.ylimits = [28.6,29.05]

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = geoplot.depth #variable to plot
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 250
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
    # Tuting-ish (speed)
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='Tuting_speed', figno=31)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Speed')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [94.65,95.0]
    plotaxes.ylimits = [28.6,29.05]

    # speed
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = speed
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 60
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
    # Tuting-ish (stress)
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='Tuting_stress', figno=32)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Stress')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [94.65,95.0]
    plotaxes.ylimits = [28.6,29.05]

    # stress
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = stress
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 234.0
    plotitem.pcolor_cmax = 61555.0  #make this reasonable max stress
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
    # Downstream 1 (depth) arrives here at Frame 26, t = 2.34e04
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='downstream1_depth', figno=33)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Depth')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [94.8,95.15]
    plotaxes.ylimits = [28.15,28.7]

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
    # Downstream 1 (speed)
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='downstream1_speed', figno=34)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Speed')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [94.8,95.15]
    plotaxes.ylimits = [28.15,28.7]

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
    # Downstream 1 (stress)
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='downstream1_stress', figno=35)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Stress')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [94.8,95.15]
    plotaxes.ylimits = [28.15,28.7]

    # stress
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = stress
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 10000  #make this reasonable max stress
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








#####----------------------------------------- 
    # Downstream 2 (depth) - arrives at Frame 36, t = 3.24e04
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='downstream2_depth', figno=36)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Depth')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [94.8,95.4]
    plotaxes.ylimits = [28.0,28.5]

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = geoplot.depth #variable to plot
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 150
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
    # Downstream 2 (speed) 
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='downstream2_speed', figno=37)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Speed')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [94.9,95.1]
    plotaxes.ylimits = [28.15,28.3]

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
    # Downstream 2 (stress)
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='downstream2_stress', figno=38)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,15]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Stress')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [94.9,95.1]
    plotaxes.ylimits = [28.15,28.3]

    # stress
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = stress
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 234.0
    plotitem.pcolor_cmax = 61555.0 #make this reasonable max stress
    plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]
    plotitem.amr_patchedges_show = [0] 

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    #plotitem.pcolor_cmap = geoplot.blank
    plotitem.pcolor_cmap = geoplot.bw_colormap
    plotitem.pcolor_cmin = 100.0
    plotitem.pcolor_cmax = 2000.0
    #plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]






#####----------------------------------------- 
    #  Backflow up the Siyom (depth) - arrives at Frame 35
    #-----------------------------------------

    plotfigure = plotdata.new_plotfigure(name='backflow_depth', figno=39)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,10]}
#
    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Depth')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [94.6,95.1]
    plotaxes.ylimits = [28.00,28.35]

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = geoplot.depth #variable to plot
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 200.0
    plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]
    plotitem.amr_patchedges_show = [0] 

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    #plotitem.pcolor_cmap = geoplot.blank
    plotitem.pcolor_cmap = geoplot.bw_colormap
    plotitem.pcolor_cmin = 100.0
    plotitem.pcolor_cmax = 2000.0
    #plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]

#####----------------------------------------- 
    #  Backflow up the Siyom (speed)
    #-----------------------------------------

    plotfigure = plotdata.new_plotfigure(name='backflow_speed', figno=40)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,10]}
#
    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Speed')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [94.6,95.1]
    plotaxes.ylimits = [28.00,28.35]

    # speed
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = speed
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 60
    plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]
    plotitem.amr_patchedges_show = [0] 

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    #plotitem.pcolor_cmap = geoplot.blank
    plotitem.pcolor_cmap = geoplot.bw_colormap
    plotitem.pcolor_cmin = 100.0
    plotitem.pcolor_cmax = 2000.0
    #plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]

#####----------------------------------------- 
    #  Backflow up the Siyom (stress)
    #-----------------------------------------

    plotfigure = plotdata.new_plotfigure(name='backflow_stress', figno=41)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,10]}
#
    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Stress')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [94.6,95.1]
    plotaxes.ylimits = [28.00,28.35]

    # stress
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = stress
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 20000  #make this reasonable max stress
    plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]
    plotitem.amr_patchedges_show = [0] 

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    #plotitem.pcolor_cmap = geoplot.blank
    plotitem.pcolor_cmap = geoplot.bw_colormap
    plotitem.pcolor_cmin = 100.0
    plotitem.pcolor_cmax = 2000.0
    #plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]

    #plotaxes.afteraxes = addgauges

# #####----------------------------------------- 
#     #  Backflow up the Siyom (blocksize)
#     #-----------------------------------------

#     plotfigure = plotdata.new_plotfigure(name='blocksize_stress', figno=42)
#     plotfigure.show = False
#     plotfigure.kwargs = {'figsize':[15,10]}
# #
#     # Set up for axes in this figure:
#     plotaxes = plotfigure.new_plotaxes('Maximum grain size capable of being moved')
#     #plotaxes.title = 'Water Surface'
#     plotaxes.scaled = True
#     plotaxes.xlimits = [94.65,95.0]
#     plotaxes.ylimits = [28.15,28.35]

#     # stress
#     plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
#     #plotitem.plot_var = geoplot.surface
#     plotitem.plot_var = blocksize
#     plotitem.pcolor_cmap = geoplot.custom_river
#     plotitem.pcolor_cmin = 0.0
#     plotitem.pcolor_cmax = 32.8  #make this reasonable max stress
#     plotitem.add_colorbar = True    #turn off for making movies
#     plotitem.amr_celledges_show = [0]
#     plotitem.amr_patchedges_show = [0] 

#     # Land
#     plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
#     plotitem.plot_var = geoplot.land
#     #plotitem.pcolor_cmap = geoplot.blank
#     plotitem.pcolor_cmap = geoplot.bw_colormap
#     plotitem.pcolor_cmin = 100.0
#     plotitem.pcolor_cmax = 2000.0
#     #plotitem.add_colorbar = True    #turn off for making movies
#     plotitem.amr_celledges_show = [0]

#     #plotaxes.afteraxes = addgauges


#####----------------------------------------- 
    # Tuting zoom (depth) arrives here in Frame 16, t = 1.44e04
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='Tutingzoom_depth', figno=43)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,10]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Depth')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [94.8,94.95]
    plotaxes.ylimits = [28.93,29.07]

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = geoplot.depth #variable to plot
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 250
    plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]
    plotitem.amr_patchedges_show = [0] 

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    #plotitem.pcolor_cmap = geoplot.blank
    plotitem.pcolor_cmap = geoplot.bw_colormap
    plotitem.pcolor_cmin = 800.0
    plotitem.pcolor_cmax = 3000.0
    #plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]

    #plotaxes.afteraxes = addgauges

#####----------------------------------------- 
    # Tuting zoom (speed)
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='Tutingzoom_speed', figno=44)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,10]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Speed')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [94.8,94.95]
    plotaxes.ylimits = [28.93,29.07]

    # speed
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = speed
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 60
    plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]
    plotitem.amr_patchedges_show = [0] 

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    #plotitem.pcolor_cmap = geoplot.blank
    plotitem.pcolor_cmap = geoplot.bw_colormap
    plotitem.pcolor_cmin = 800.0
    plotitem.pcolor_cmax = 3000.0
    #plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]

    #plotaxes.afteraxes = addgauges

#####----------------------------------------- 
    # Tuting zoom (stress)
    #-----------------------------------------
#
    plotfigure = plotdata.new_plotfigure(name='Tutingzoom_stress', figno=45)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,10]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Stress')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [94.8,94.95]
    plotaxes.ylimits = [28.93,29.07]

    # stress
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = stress
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 0
    plotitem.pcolor_cmax = 30824.0  #make this reasonable max stress
    plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]
    plotitem.amr_patchedges_show = [0] 

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    #plotitem.pcolor_cmap = geoplot.blank
    plotitem.pcolor_cmap = geoplot.bw_colormap
    plotitem.pcolor_cmin = 800.0
    plotitem.pcolor_cmax = 3000.0
    #plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]


############# FOR MIKE #### --> Boulder Bar upstream of Tuting
# stress
    plotfigure = plotdata.new_plotfigure(name='BB_stress', figno=50)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':[15,10]}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Stress')
    #plotaxes.title = 'Water Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [94.9,94.921]
    plotaxes.ylimits = [29.04,29.056]

    # stress
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = stress
    plotitem.pcolor_cmap = geoplot.custom_river
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 30824.0  #make this reasonable max stress
    plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]
    plotitem.amr_patchedges_show = [0] 

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    #plotitem.pcolor_cmap = geoplot.blank
    plotitem.pcolor_cmap = geoplot.bw_colormap
    plotitem.pcolor_cmin = 450.0
    plotitem.pcolor_cmax = 800.0
    #plotitem.add_colorbar = True    #turn off for making movies
    plotitem.amr_celledges_show = [0]

# # block size
#     plotfigure = plotdata.new_plotfigure(name='BB_blocksize', figno=51)
#     plotfigure.show = False
#     plotfigure.kwargs = {'figsize':[15,10]}

#     # Set up for axes in this figure:
#     plotaxes = plotfigure.new_plotaxes('Grain Size capable of being moved')
#     #plotaxes.title = 'Water Surface'
#     plotaxes.scaled = True
#     plotaxes.xlimits = [94.9,94.921]
#     plotaxes.ylimits = [29.04,29.056]

#     # stress
#     plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
#     #plotitem.plot_var = geoplot.surface
#     plotitem.plot_var = blocksize
#     plotitem.pcolor_cmap = geoplot.custom_river
#     plotitem.pcolor_cmin = 0.0
#     plotitem.pcolor_cmax = 4.1  #make this reasonable max stress
#     plotitem.add_colorbar = True    #turn off for making movies
#     plotitem.amr_celledges_show = [0]
#     plotitem.amr_patchedges_show = [0] 

#     # Land
#     plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
#     plotitem.plot_var = geoplot.land
#     #plotitem.pcolor_cmap = geoplot.blank
#     plotitem.pcolor_cmap = geoplot.bw_colormap
#     plotitem.pcolor_cmin = 450.0
#     plotitem.pcolor_cmax = 800.0
#     #plotitem.add_colorbar = True    #turn off for making movies
#     plotitem.amr_celledges_show = [0]




#    #plotaxes.afteraxes = addgauges  
    #-----------------------------------------
    # Figures for gauges
    #-----------------------------------------
    #plotfigure = plotdata.new_plotfigure(name='Surface at gauges', figno=300, \
    #                type='each_gauge')
    #plotfigure.clf_each_gauge = False

    # Set up for axes in this figure:
    #plotaxes = plotfigure.new_plotaxes()
    #plotaxes.xlimits = 'auto'
    #plotaxes.ylimits = 'auto'
    #plotaxes.title = 'Surface'

    # Plot surface as blue curve:
    #plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    #plotitem.plot_var = 0
    #plotitem.plotstyle = 'b-'

    # Plot topo as green curve:
    #plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    #plotitem.show = False

    
    


#-----------------------------------------
    
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    #plotdata.print_framenos = np.arange(0,5,1)       # list of frames to print
    #plotdata.print_framenos = [9]       #frame is a timestep, so this is the way
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

