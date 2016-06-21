
"""
future feature list
V3.4
add image stacking?
"""

##############Written by BMiles#########################

import gc
import os
import cPickle as pickle
import tkFileDialog
import Tkinter
import csv
import ioCSV
import cluster_solving


import numpy as np
from numpy import array, linspace
from scipy import stats
import scipy.io as scio


# Enthought library imports
from traits.api import HasTraits, Instance, Str, Button, Bool, Enum, Float
from traitsui.api import View, Item, UItem, HGroup, VGroup, Group, RangeEditor

from pyface.api import FileDialog, OK
from enable.api import ComponentEditor, Component


# Chaco imports
from chaco.api import ArrayPlotData, ColorBar, GridPlotContainer, \
    Greens, Blues, Reds, Greys, gray, jet, autumn, bone, cool, copper, flag, yarg, hot, hsv, LinearMapper, Plot, GridDataSource,DataRange2D,\
        ImageData, DataRange1D
from chaco.tools.api import LineInspector, PanTool, ZoomTool
from chaco.plot_graphics_context import PlotGraphicsContext

from chaco.tools.image_inspector_tool import ImageInspectorTool, \
	     ImageInspectorOverlay


class ImagePlot(HasTraits):
    """UI Contols and Variables"""
    #MainTabsVariables
    plot = Instance(GridPlotContainer)
    LineScans = Instance(GridPlotContainer)
    zstack = Instance(GridPlotContainer)
    colocPlot = Instance(GridPlotContainer)
    notes = Str

    #ChangeFile
    load_button = Button("Load")
    reload_button = Button("Reload")
    nextfile = Button("Next")
    prevfile = Button("Prev")
    next1_button = Button("Next")
    prev1_button = Button("Prev")
    next2_button = Button("Next")
    prev2_button = Button("Prev")
    next3_button = Button("Next")
    prev3_button = Button("Prev")
    next4_button = Button("Next")
    prev4_button = Button("Prev")
    load1_button =Button("Load 1")
    load2_button =Button("Load 2")
    load3_button =Button("Load 3")
    load4_button =Button("Load 4")
    all_next_button = Button("All Next")
    all_prev_button = Button("All Prev")
    save_all_colloc = Button("Save all")
    coloc = Button("Plot Coloc Data")
    track_all = Bool("Require find in all files")
    #@variables
    loaded = False
    value = Str
    directory = Str
    filename = Str
    path = Str
    path1 = Str
    path2 = Str
    path3 = Str
    path4 = Str
    ###########

    #SaveImage
    save_plots_button = Button("Save Multi Plot")
    save_MainPlot_button = Button("Save Main Plot")
    save_folder_image = Button("Save Main Plot All Folder")
    justMainplot = Bool(False,desc = "Exclude line scans from save")
    save_coloc_button = Button("Save Coloc Image")

    #CatchSetBounds
    catch_bounds = Button("Catch Bounds")
    catch_mainplot_bounds = Button("Catch Line Plot Bounds")
    scale_set = Button("Set Scale")
    reset = Button("Reset")
    scale = Button("Scale")
    #@variables
    xLo = Float()
    xHi = Float()
    yLo = Float()
    yHi = Float()
    ##############

    #Alter plots
    title1 = Str
    title2 = Str
    title3 = Str
    title4 = Str
    titleColoc = Str
    flatten1 = Button("Flatten")
    flatten2 = Button("Flatten")
    flatten3 = Button("Flatten")
    flatten4 = Button("Flatten")
    flatten5 = Button("Flatten")
    colormap = Button("ApplyColorMap")
    #@variables
    auto_view = Bool(True, desc = "Auto View Area")
    presmooth = Bool(True, desc = "pre-treat X and Y")
    safesmooth = Bool(False, desc = "pre-treat X and Y based on user set values (buggy)")
    autocolor = Bool(True, desc = "auto apply user set bounds to colormaps")
    autoColoc = Bool(False, desc = "auto plot coloc data between plots 1 and 2")
    square2 = Enum("px","dist")
    plotUnit = Enum("px","dist")
    F_floor = Str("2500")
    ##############

    #zstack
    startZstack = Button('Z Stack')
    #ClusterFinding
    readline = Button("LineScan")
    output = Bool(False, desc = "if true output the linescan to .txt of the same name on \"linescan\"")
    find_clusters = Button("Find Clusters")
    dbscanner = Button("Re-DBScan")
    histogram = Button("Plot Histogram")
    collect_max = Button("Collect Maxima")
    clear_collect = Button("Clear Collection")
    write_collect = Button("Write Collection")
    plot_collection = Button("Plot Collection")
    track_particle_over_files = Button("Track Particles")
    dot_size = Float(6)
    #@variables
    imagefloor = Float(0.001, format='%.3f')
    mapsize = Float(4, format='%.1f')
    eps = Float(13, format='%.1f')
    minnumparticles = Float(4, format='%.1f')
    maxima_out = Str
    ill_power = Float(format='%.3f')
    ref_power = Float(format='%.3f')
    binrange = Float(20.0, format='%.1f')
    dictOfMaxima = {'name':[], 'file': [], 'data':[]}
    dictOfParticles = {}
    dictOfPairs = {}
    areaArray={}
    trackDistance = Str("15")
    pull_local_value = Bool(True, desc = "pull local value if no neighbour is found")
    boxHW = Str("8")
    ###############

    #AverageMainplot
    average_box = Button("Average View Area")
    average_box_value = Float(format='%.1f')

    #Special
    genfilelist = Button("List Files")
    out_to_mat = Button("To .mat")
    special = Button("Custom")

    """MainWindowVARIABLES"""
    #ReadLineVariables
    norm = Enum(True, False)
    xscanline = 0.0
    yscanline = 0.0
    xline  = Str(xscanline)
    yline  = Str(yscanline)
    fast_Low = Float(format='%.1f')
    fast_High = Float(format='%.1f')
    slow_Low = Float(format='%.1f')
    slow_High = Float(format='%.1f')
    slow_Diff = Float(format='%.1f')
    fast_Diff = Float(format='%.1f')
    line_up = Button(label = 'Line Up')
    line_down = Button(label = 'Line Down')
    line_left = Button(label = 'Line Left')
    line_right = Button(label = 'Line Right')


    """Data Variables"""
    #PlotOptions
    plta = Enum("R", "Phase", "R0","R/R0","Fluor", "X", "Y")
    pltb = Enum("R", "Phase", "R0","R/R0","Fluor", "X", "Y")
    pltc = Enum("R", "Phase", "R0","R/R0","Fluor", "X", "Y")
    pltd = Enum("R", "Phase", "R0","R/R0","Fluor", "X", "Y")
    plte = Enum("R", "Phase", "R0","R/R0","Fluor", "X", "Y")
    pltf = Enum("R", "Phase", "R0","R/R0","Fluor", "X", "Y")
    compare_to = Enum("R", "Phase", "R0","R/R0","Fluor", "X", "Y")
    pltaLow = Float(format='%.1f', label = "lo")
    pltaHi = Float(1.0,format='%.1f', label = "hi")
    pltbLow = Float(format='%.1f',label = "lo")
    pltbHi = Float(1.0,format='%.1f', label = "hi")
    pltcLow = Float(format='%.1f',label = "lo")
    pltcHi = Float(1.0,format='%.1f', label = "hi")
    pltdLow = Float(format='%.1f',label = "lo")
    pltdHi = Float(1.0,format='%.1f', label = "hi")
    plteLow = Float(format='%.1f', label = "lo")
    plteHi = Float(format='%.1f', label = "hi")
    apply1 = Button(label = 'Apply')
    apply2 = Button(label = 'Apply')
    apply3 = Button(label = 'Apply')
    apply4 = Button(label = 'Apply')
    apply5 = Button(label = 'Apply')
    apply1_ck = Bool(False)
    apply2_ck = Bool(False)
    apply3_ck = Bool(False)
    apply4_ck = Bool(False)
    apply5_ck = Bool(False)
    #DataDictionaries
    plotA = {"plot": plta, "data" : "", "shape" : "", "range" : np.zeros((2,2)), "path" : ""}
    plotB = {"plot": pltb, "data" : "", "shape" : "", "range" : np.zeros((2,2)), "path" : ""}
    plotC = {"plot": pltc, "data" : "", "shape" : "", "range" : np.zeros((2,2)), "path" : ""}
    plotD = {"plot": pltd, "data" : "", "shape" : "", "range" : np.zeros((2,2)), "path" : ""}
    plotE = {"plot": plte, "data" : "", "shape" : "", "range" : np.zeros((2,2)), "path" : ""}

    axistype_Enum = Enum("px", "dist")
    color_Dict = {"Greys" : Greys, "Gray" : gray, "Green": Greens, "Blues": Blues, "Red" : Reds, "Jet" : jet, "Autumn" : autumn, "Bone" : bone, "Cool" : cool, "Copper" : copper, "Flag" : flag, "Yarg" : yarg, "Hot" : hot, "HSV" : hsv }
    color_Enum1 = Enum(color_Dict.keys())
    color_Enum2 = Enum(color_Dict.keys())
    color_Enum3 = Enum(color_Dict.keys())
    color_Enum4 = Enum(color_Dict.keys())
    color_Enum5 = Enum(color_Dict.keys())
    """MISC Variables"""
    #wildcards
    wildcardsPNG  = [("PNG Files", "*.png"),("All files", "*.*")]
    wildcardsMAT = [("MAT Files", "*.mat"),("All files", "*.*")]
    wildcardsCSV = [("CSV Files", "*.csv"),("All files", "*.*")]
    wildcardsLOAD = [("Zis Files", "*.zis"),("All files", "*.*")]

    """Groups and Views"""
    collect_max_vars = Group(
        HGroup(
            UItem('collect_max'),
            UItem('clear_collect'),
            ),
        HGroup(
            UItem('write_collect'),
            UItem('plot_collection'),
        ),
        HGroup(
        UItem('track_particle_over_files'),
        Item('track_all'),
        ),
        HGroup(
        Item('boxHW'),
        Item('trackDistance'),
        ),
        HGroup(
        Item(name="compare_to", style = 'simple',show_label = False),
        Item('pull_local_value'),
        Item("dot_size"),
        ),
        show_border=True)
    average_box_vars = Group(
        HGroup(
            UItem('average_box'),
            Item('average_box_value', label = 'Average :'),
        ),show_border=True)
    histo_vars = Group(
        HGroup(
        Item('binrange'),
        UItem('histogram'),
        ),
        HGroup(
            Item('ill_power'),
            Item('ref_power'),
        ),
        Item('maxima_out'),show_border=True, label = "Histo")
    cluster_vars = Group(
        HGroup(
            Item('imagefloor'),
            Item('mapsize'),
        ),
        HGroup(
            Item('minnumparticles', label = "Min peak/cluster"),
            Item('eps'),
        ),
        HGroup(
        UItem('find_clusters'),
        UItem('dbscanner'),),
        collect_max_vars,
        average_box_vars,
        label = "Clustering", show_border=True)

    pltavars = Group(
                    HGroup(
                    Item(name="plta", style = 'simple',show_label = False),
                    Item(name = "color_Enum1", style = 'simple',show_label=False),
                    UItem('flatten1'),
                    ),
                    Item("path1", show_label = False),
                    Item("title1"),
                    HGroup(
                    Item(name='pltaLow'),
                    Item(name='pltaHi'),
                    Item(name = 'apply1_ck',show_label = False),
                    UItem(name='apply1'),
                    ),
                    HGroup(
                        UItem("prev1_button"),
                        UItem("load1_button"),
                        UItem("next1_button"),
                    ),
                    show_border=True)
    pltbvars = Group(
                    HGroup(
                    Item(name="pltb", style = 'simple',show_label = False),
                    Item(name = "color_Enum2", style = 'simple',show_label=False),
                    UItem('flatten2'),
                    ),
                    Item("path2", show_label = False),
                    Item("title2"),
                    HGroup(
                    Item(name='pltbLow'),
                    Item(name='pltbHi'),
                    Item(name = 'apply2_ck',show_label = False),
                    UItem(name='apply2'),
                    ),
                    HGroup(
                        UItem("prev2_button"),
                        UItem("load2_button"),
                        UItem("next2_button"),
                    ),
                    show_border=True)
    pltcvars = Group(
                    HGroup(
                    Item(name="pltc", style = 'simple',show_label = False),
                    Item(name = "color_Enum3", style = 'simple',show_label=False),
                    UItem('flatten3'),
                    ),
                    Item("path3", show_label = False),
                    Item("title3"),
                    HGroup(
                    Item(name='pltcLow'),
                    Item(name='pltcHi'),
                    Item(name = 'apply3_ck',show_label = False),
                    UItem(name='apply3'),
                    ),
                    HGroup(
                        UItem("prev3_button"),
                        UItem("load3_button"),
                        UItem("next3_button"),
                    ),
                    show_border=True)
    pltdvars = Group(
                    HGroup(
                    Item(name="pltd", style = 'simple', show_label = False),
                    Item(name = "color_Enum4", style = 'simple',show_label=False),
                    UItem('flatten4'),
                    ),
                    Item("path4", show_label = False),
                    Item("title4"),
                    HGroup(
                    Item(name='pltdLow'),
                    Item(name='pltdHi'),
                    Item(name = 'apply4_ck',show_label = False),
                    UItem(name='apply4'),
                    ),
                    HGroup(
                        UItem("prev4_button"),
                        UItem("load4_button"),
                        UItem("next4_button"),
                    ),
                    show_border=True)

    fastlinevars = Group(
        Item('fast_Low'),
        Item('fast_High'),
        Item('fast_Diff'),show_border=True)
    slowlinevars = Group(
        Item('slow_Low'),
        Item('slow_High'),
        Item('slow_Diff'),show_border=True)
    lineplot_vars = Group(
        UItem('catch_mainplot_bounds'),
        HGroup(
            fastlinevars,
            slowlinevars,
        ), label = "Line Bounds", show_border=True)
    readline_vars = Group(
        HGroup(
                Item('xline'),
                Item('yline'),
                UItem('readline'),
                Item('output', show_label = False),
            ),
            UItem('line_up'),
            HGroup(
            UItem('line_left'),
            UItem('line_right'),
            ),
            UItem('line_down'),

        label = "Read Line", show_border=True)

    constant_group = Group(VGroup(
            HGroup(
                Item(name="plte", style = 'simple',show_label=False),
                Item(name="color_Enum5", style = 'simple', label = 'Map:'),
                Item(name="norm", style = 'simple', label = 'Norm:'),
            ),
            HGroup(
                    Item(name='plteLow',width = 0.2),
                    Item(name='plteHi'),
                    Item(name = 'apply5_ck',show_label = False),
                    UItem(name='apply5'),
                    ),
            HGroup(
                UItem('flatten5'),
                Item("F_floor"),
            ),
            HGroup(
                Item('square2',style = 'simple', label = 'Sq wrt'),
                Item('plotUnit',style = 'simple', label = 'Units'),
                ),
            ),
            label = "Plot Parameters",
        show_border = True)
    mainplottabs = Group(
            readline_vars,
            cluster_vars,
            histo_vars,
            lineplot_vars,
            layout = "tabbed")
    mainsavegroup = Group(
        HGroup(
            UItem('save_MainPlot_button'),
            UItem('save_folder_image'),
            UItem('justMainplot'),
        ),
        label = 'Save Functions',
        show_labels = True,
        show_border = True)
    viewgroup = Group(
            HGroup(
                VGroup(
                    Item('xLo'),
                    Item('xHi'),
                    ),
                VGroup(
                    Item('yLo'),
                    Item('yHi'),
                    ),
                VGroup(
                    UItem('scale_set'),
                    UItem('reset'),
                ),
            ),
            label = "Plot View",
            show_border = True)
    specialgroup = Group(
            HGroup(
                UItem('colormap'),
                UItem('genfilelist'),
            ),
            HGroup(
                UItem('out_to_mat', label = "To .mat"),
                UItem('special', label = "Custom"),
             ),
            label = "Special Functions",
            show_border =True)
    mainplotgroup = HGroup(
        Item('LineScans', editor=ComponentEditor(), resizable=True, show_label=False, width = 900),
        VGroup(
            mainsavegroup,
            constant_group,
            viewgroup,
            specialgroup,
            mainplottabs,
            layout='split',
        ),
        layout='split',
        show_labels = True,
        label = "Main Plot")
    fourplotgroup = HGroup(
            Item('plot', editor=ComponentEditor(),resizable=True,show_label=False,width = 950),
            VGroup(
                HGroup(
                    UItem("all_prev_button"),
                    UItem('save_plots_button'),
                    UItem("all_next_button"),
                ),
                pltavars,
                pltbvars,
                pltcvars,
                pltdvars,

            ),
        layout='split',
        label = "Multi Plots")
    colocgroup = HGroup(
        Item('colocPlot', editor=ComponentEditor(), resizable=True, show_label=False,width = 950),
        VGroup(
        HGroup(
        UItem('coloc'),
        UItem('save_coloc_button'),
        UItem('save_all_colloc'),
        ),
        Item('titleColoc', label = "Title:"),
        ),
        label = "Colocalisation")
    zstackgroup = HGroup(
        Item('zstack',editor=ComponentEditor(), resizable=True, show_label=False, width = 900),
        UItem('startZstack'),
        Item('pltf'),
        label = 'zstack'
    )
    tabs = Group(mainplotgroup,
                fourplotgroup,
                colocgroup,
                zstackgroup,
                Item('notes', style = 'custom', width=.1), layout = "tabbed")

    lefttop = Group(
                    HGroup(
                        UItem('prevfile'),
                        UItem('load_button'),
                        UItem('nextfile'),
                        UItem('reload_button'),
                        UItem('scale'),
                        Item('value', label = "File", width = 300),
                        Item('auto_view'),
                        Item('presmooth'),
                        Item('safesmooth'),
                        Item('autocolor'),
                        Item('autoColoc'),
                        ),
                show_border = True)
    traits_view = View(
            VGroup(
                    HGroup(
                        lefttop,
                    ),
                    tabs,
            ),
            width=1200, height=700, resizable=True, title="Scan Image Reconstruction")


    """
    Map colors and alter view area
    """
    def _map_(self,data,rangeLow,rangeHi):
        data.color_mapper.range.low = float(rangeLow)
        data.color_mapper.range.high = float(rangeHi)
    def _apply1_fired(self):
        self._map_(self.plot1,self.pltaLow,self.pltaHi)
    def _apply2_fired(self):
        self._map_(self.plot2,self.pltbLow,self.pltbHi)
    def _apply3_fired(self):
        self._map_(self.plot3,self.pltcLow,self.pltcHi)
    def _apply4_fired(self):
        self._map_(self.plot4,self.pltdLow,self.pltdHi)
    def _apply5_fired(self):
        self._map_(self.mainplot,self.plteLow,self.plteHi)

    def _colormap_fired(self): # sets colour map for plots
        if self.apply1_ck:
            self._apply1_fired()
        if self.apply2_ck:
            self._apply2_fired()
        if self.apply3_ck:
            self._apply3_fired()
        if self.apply4_ck:
            self._apply4_fired()
        if self.apply5_ck:
            self._apply5_fired()

        print "Color Mapped"
    def _scale_plot(self,plot,img, pixel, x = True):
        if img:
            if not pixel:
                plot.range2d.x_range.low = self.xLo
                plot.range2d.x_range.high = self.xHi
                plot.range2d.y_range.low = self.yLo
                plot.range2d.y_range.high = self.yHi
            else:
                plot.range2d.x_range.low = self.xLo/self.D["range"][0][1]*self.D["shape"][0]
                plot.range2d.x_range.high = self.xHi/self.D["range"][0][1]*self.D["shape"][0]
                plot.range2d.y_range.low = self.yLo/self.D["range"][1][1]*self.D["shape"][1]
                plot.range2d.y_range.high = self.yHi/self.D["range"][1][1]*self.D["shape"][1]

        else:
            if x:
                plot.range2d.x_range.low = self.yLo
                plot.range2d.x_range.high = self.yHi
            else:
                plot.range2d.x_range.low = self.xLo
                plot.range2d.x_range.high = self.xHi
        return plot
    def _reset_fired(self): # resets view range to original params
        self._initialize_viewrange()
        self._scale()
    def _scale_set_fired(self): # adjusts all plots to view range set by mainplot
        self._catch_bounds_fired()
        self._scale()
    def _scale_fired(self):
        self._scale()
    def _scale(self):
        pixel = False
        if self.plotUnit == "px":
            pixel = True
        self.plot1 = self._scale_plot(self.plot1,True,False)
        self.plot2 = self._scale_plot(self.plot2,True,False)
        self.plot3 = self._scale_plot(self.plot3,True,False)
        self.plot4 = self._scale_plot(self.plot4,True,False)
        self.mainplot = self._scale_plot(self.mainplot,True,pixel)
        #self.colocPlot = self._scale_plot(self.colocPlot,True,True)

        self.slow_plot = self._scale_plot(self.slow_plot,False,False,False)
        self.fast_plot = self._scale_plot(self.fast_plot,False,False)



    """
    -------------------------------
    File loading and saving logic
    """
    def _reload_button_fired(self): # reloads current file (use to "un-flatten")
        self._all_load()
    def _value_changed(self): # forces update of file name displayed in GUI
        self.value = self.value
    def _safesmooth_changed(self):
        if self.safesmooth:
            self.presmooth = False
    def _presmooth_changed(self):
        if self.presmooth:
            self.safesmooth = False
    def _square2_changed(self):
        self._plotMain()
    def _plotUnit_changed(self):
        self._plotMain()
    def _refresh(self): # utility function
        try: self._plot_all()
        except: print "Option will be applied when plotting"

    """
    -----------------------------
    Read Data logic
    """
    def _grab_box(self): #grabs view area of mainplot
        self.lines_fast_Low = int(float(self.mainplot.range2d.x_range.low))
        self.lines_fast_High = int(float(self.mainplot.range2d.x_range.high))
        self.lines_slow_Low = int(float(self.mainplot.range2d.y_range.low))
        self.lines_slow_High = int(float(self.mainplot.range2d.y_range.high))

        if self.lines_fast_Low <0:
            self.lines_fast_Low = 0
        if self.lines_slow_Low <0:
            self.lines_slow_Low = 0

        if self.lines_fast_High > self.plotE['shape'][0]:
            self.lines_fast_High = self.plotE['shape'][0]
        if self.lines_slow_High > self.plotE['shape'][1]:
            self.lines_slow_High = self.plotE['shape'][1]
        #somewhat short sightedly assigns box data to global var rather than 'return's
        self.selectedarea = self.plotE['data'][self.lines_slow_Low : self.lines_slow_High,self.lines_fast_Low : self.lines_fast_High]
    def _line_up_fired(self):
        if int(self.yline) < int(self.D['shape'][1]):
            self.yline = str(int(self.yline)+1)
            self._readlines()
    def _line_down_fired(self):
        if int(self.yline) > 0:
            self.yline = str(int(self.yline)-1)
            self._readlines()
    def _line_right_fired(self):
        if int(self.xline) < int(self.D['shape'][1]):
            self.xline = str(int(self.xline)+1)
            self._readlines()
    def _line_left_fired(self):
        if int(self.xline) > 0:
            self.xline = str(int(self.xline)-1)
            self._readlines()
    def _readline_fired(self): #pulls lines from linescan plot for line viewers
        self._readlines(self.output)
    def _readlines(self,output = False):
        #select which line to scan (this should be input as int value of line number until changed)
        #this needs double checking at some point for consistency
        self.xscanline = int(self.xline)
        self.yscanline = int(self.yline)

        yarray = np.array(self._image_value.data[self.yscanline,:])
        xarray = np.array(self._image_value.data[:,self.xscanline])
        if output:
            print "~~~~~~~~~ Output Line Scans ~~~~~~~~~~~~"
            name = str(self.directory) + "/" + str(self.value) + "linescan_output.txt"
            file = open(name, 'w')
            file.write("%s\n" % str(self.yscanline))
            for item in yarray:
                file.write("%s\n" % item)


        #set data range for fast and slow plots
        self.pd.set_data("line_value",
                                 self._image_value.data[self.yscanline,:])
        self.pd.set_data("line_value2",
                                 self._image_value.data[:,self.xscanline])

        self.fastlinevar = str(np.std(xarray))
        self.fastlinemean = str(np.mean(xarray))
        self.fastlinemax = str(np.amax(xarray))
        self.fastlinemin = str(np.amin(xarray))
        self.slowlinevar = str(np.std(yarray))
        self.slowlinemean = str(np.mean(yarray))
        self.slowlinemax = str(np.amax(yarray))
        self.slowlinemin = str(np.amin(yarray))

        self.slow_plot.title = "Fastline : " + str(self.yline)
        self.fast_plot.title = "Slowline : " + str(self.xline)
    def _average_box_fired(self):
        self._grab_box()
        self.average_box_value = np.mean(self.selectedarea)
    """
    -----------------------------------
    Small data processing functions
    Flatten area by brute force line-by-line removal of line dc value
    """
    def _flatten1_fired(self):
        self._flatten(self.plotA)
    def _flatten2_fired(self):
        self._flatten(self.plotB)
    def _flatten3_fired(self):
        self._flatten(self.plotC)
    def _flatten4_fired(self):
        self._flatten(self.plotD)
    def _flatten5_fired(self):
        self._flatten(self.plotE)
    def _flatten(self, data): # brute force flattens plot A and E
        """
        y=0
        x=0
        for line in self.data['data']:
            ##change back later
            zeropoint = np.average(line[self.xscanline],line[self.xscanline+1], line[self.xscanline+2])##
            x_axis = np.arange(0,int(len(line)))
            y_axis = np.array(line)
            slope,intercept,r_value,p_value,std_err = stats.linregress(x_axis,y_axis)
            x=0
            for point in line:
                data['data'][y,x] = abs(point - (slope*x + zeropoint))##
                x+=1
            y+=1
        """
        y=0
        x=0
        for line in data['data']:
            x_axis = np.arange(0,int(len(line)))
            y_axis = np.array(line)
            slope,intercept,r_value,p_value,std_err = stats.linregress(x_axis,y_axis)
            x=0
            for point in line:
                data['data'][y,x] = abs(point - (slope*x + intercept))
                x+=1
            y+=1
        self._plot_all()
        print "Flattened"

    """
    ----------------------------------
    Bounds and area catching functions
    """
    def _catch_bounds_fired(self):
        try:
            if self.plotUnit == "px":
                self.xLo = float("{0:.2f}".format(float(self.mainplot.range2d.x_range.low)*float(self.D['range'][0][1])/float(self.D["shape"][0])))
                self.xHi = float("{0:.2f}".format(float(self.mainplot.range2d.x_range.high)*float(self.D['range'][0][1])/float(self.D["shape"][0])))
                self.yLo = float("{0:.2f}".format(float(self.mainplot.range2d.y_range.low)*float(self.D['range'][1][1])/float(self.D["shape"][1])))
                self.yHi = float("{0:.2f}".format(float(self.mainplot.range2d.y_range.high)*float(self.D['range'][1][1])/float(self.D["shape"][1])))
            else:
                self.xLo = float("{0:.2f}".format(float(self.mainplot.range2d.x_range.low)))
                self.xHi = float("{0:.2f}".format(float(self.mainplot.range2d.x_range.high)))
                self.yLo = float("{0:.2f}".format(float(self.mainplot.range2d.y_range.low)))
                self.yHi = float("{0:.2f}".format(float(self.mainplot.range2d.y_range.high)))
        except: print "Please plot first"
    def _catch_mainplot_bounds_fired(self):
        try:
            self.mainplot_fast_Low = float(self.fast_plot.range2d.x_range.low)
            self.mainplot_fast_High = float(self.fast_plot.range2d.x_range.high)
            self.mainplot_slow_Low = float(self.slow_plot.range2d.x_range.low)
            self.mainplot_slow_High = float(self.slow_plot.range2d.x_range.high)

            #output to GUI
            self.fast_Low = float("{0:.2f}".format(self.mainplot_fast_Low))
            self.fast_High = float("{0:.2f}".format(self.mainplot_fast_High))
            self.slow_Low = float("{0:.2f}".format(self.mainplot_slow_Low))
            self.slow_High = float("{0:.2f}".format(self.mainplot_slow_High))
            self.fast_Diff = float("{0:.2f}".format(abs(self.mainplot_fast_High-self.mainplot_fast_Low)))
            self.slow_Diff = float("{0:.2f}".format(abs(self.mainplot_slow_High-self.mainplot_slow_Low)))
        except: print "Please plot first"
    """
    --------------------------------------------------
    Cluster Solving Logic
    """
    def _find_clusters_fired(self):
            self._grab_box()

            # this means that the histograms represent real data and need to be weighted by illumination power
            self.maximum = np.max(np.max(self.plotE['data']))

            X = np.arange(self.lines_fast_Low,self.lines_fast_High)
            Y = np.arange(self.lines_slow_Low,self.lines_slow_High)
            X2D, Y2D = np.meshgrid(X,Y)


            if self.plte == "Fluor" and self.apply5_ck:
                print "fluor find"
                self.flooredimage = (self.selectedarea - self.plteLow)/self.plteHi
                self.flooredimage[self.flooredimage < float((self.imagefloor - self.plteLow)/self.plteHi)] = 0
            else:
                self.flooredimage = self.selectedarea/self.maximum
                self.flooredimage[self.flooredimage < float(self.imagefloor/self.maximum)] = 0

            detected_peaks, local_max = self._detect_peaks(self.flooredimage)

            import matplotlib.pyplot as plt
            try:
                plt.close('all')
            except:
                print "not closed"
            thistitle = str(self.value) + "_local_max_found"
            self.fig = plt.figure(thistitle)
            plt.subplot(2,3,1)
            norm = plt.Normalize(vmin = self.mainplot.color_mapper.range.low, vmax = self.mainplot.color_mapper.range.high)
            plt.imshow(self.selectedarea, interpolation="nearest", cmap='gray', norm = norm)
            plt.gca().invert_yaxis()
            plt.title("Scan Area")
            #self.fig2 = plt.figure()
            plt.subplot(2,3,2)
            cmap = 'Greys'
            plt.imshow(self.flooredimage,interpolation="nearest", cmap='gray', norm = norm)
            plt.gca().invert_yaxis()
            plt.title("Detected Local Max")
            # plt.subplot(2,3,3)
            # cmap = 'Greys'
            # plt.imshow(detected_peaks,interpolation="nearest", cmap='gray', norm = norm)
            # plt.gca().invert_yaxis()
            # plt.title("Detected Local Max")
            # plt.show()

            """
            ---------------
            Takes list of local maxs for to create self.maxima which is used for histogram  plotting
            """
            self.maxima = []
            i = 0

            for cell in local_max.flat:
                if cell == True and self.selectedarea.flat[i] != 0:
                    self.maxima.append(self.selectedarea.flat[i])

                i +=1

            """
            ----------------
            Takes true/false peak map and retrieves list of co-ordinates
            ultimately passed to self.maxima_locations
            """
            data = []
            y = 0
            x= 0
            for line in detected_peaks:
                x = 0
                for item in line:
                    if item:
                        data.append([x,y]) #vstack((rand(150,2) + array([.5,.5]),rand(150,2)))
                    x +=1
                y+=1

            self.maxima_locations = np.array(data)

            """
            -------------
            Selected cluster locating routine below
            """
            self._dbscan()
    def _detect_peaks(self, image):


            """
            -------------
            Takes image and solves for local peaks based on self.mapsize
            """

            from scipy.ndimage.filters import maximum_filter
            from scipy.ndimage.morphology import generate_binary_structure, binary_erosion, iterate_structure

            # define a connected neighborhood
            struct = generate_binary_structure(2, 1)
            neighborhood = iterate_structure(struct, int(self.mapsize)).astype(int)

            #apply the local maximum filter; all pixel of maximal value
            #in their neighborhood are set to 1
            local_max = maximum_filter(image, footprint=neighborhood)==image
            #local_max is a mask that contains the peaks we are
            #looking for, but also the background.
            #In order to isolate the peaks we must remove the background from the mask.

            #we create the mask of the background
            background = (image==0)

            #we must erode the background in order to
            #successfully subtract it form local_max, otherwise a line will
            #appear along the background border (artifact of the local maximum filter)
            eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)

            #we obtain the final mask, containing only peaks,
            #by removing the background from the local_max mask
            detected_peaks = local_max - eroded_background
            return detected_peaks, local_max
    def _histogram_fired(self):
        self._histogram_intensities(False)
    def _histogram_intensities(self, lim = True):
        """
        -------------
        Produces a histogram from self.maxima over self.binrange, update as needed
        """
        self.maxima_out = str(self.maxima)
        import matplotlib.pyplot as plt
        thistitle = self.value + "_histogram"
        self.fig3 = plt.figure(thistitle)
        n, bins, patches = plt.hist(self.maxima, float(self.binrange), normed=0, histtype='bar')
        if lim:
            plt.xlim([0,0.005])
        plt.show()
    def _dbscanner_fired(self):
        self._dbscan()
    def _dbscan(self):
        import matplotlib.pyplot as plt
        from sklearn.cluster import DBSCAN
        # try:
            # plt.close('all')
        # except:
            # print "not closed"
        # thistitle = self.value + "_clusters_found"
        # self.fig5 = plt.figure(thistitle)
        plt.subplot(2,3,4) ##plots image next to cluster
        #if self.plte == "Fluor" and self.apply5_ck:
        #    norm = plt.Normalize(vmin = self.plteLow, vmax = self.plteHi)
        #else:
        norm = plt.Normalize(vmin = self.mainplot.color_mapper.range.low, vmax = self.mainplot.color_mapper.range.high)
        plt.imshow(self.selectedarea, interpolation="nearest", cmap='gray', norm = norm)
        plt.gca().invert_yaxis()
        plt.title("Scan Area Above Imposed Data Floor")
        #self.fig2 = plt.figure()

        db = DBSCAN(eps= float(self.eps), min_samples = int(self.minnumparticles)).fit(self.maxima_locations)
        labels = db.labels_

        #detect number of clusters by label length (-1 if noise detected)
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True

        # Black removed and is used for noise instead.
        unique_labels = set(labels)
        colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

        plt.subplot(2,3,3, aspect='equal')
        for k, col in zip(unique_labels, colors):
            if k == -1:
                # Black used for noise.
                col = 'k'
            x1y1 = self.maxima_locations
            plt.plot(x1y1[:, 0], x1y1[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=int(self.dot_size/2))
        plt.xlim(0, self.lines_fast_High-self.lines_fast_Low)
        plt.ylim(0, self.lines_slow_High-self.lines_slow_Low)

        plt.subplot(2,3,5 , aspect='equal')



        # for each label (aka index) in the set of unique labels
        for k, col in zip(unique_labels, colors):
            if k == -1:
                # Black used for noise.
                col = 'k'

            # boolean array as a mask for all labels that match the current one in the loop
            class_member_mask = (labels == k)

            # the xy point pairs from the original data set that match this cluster
            xy = self.maxima_locations[class_member_mask & core_samples_mask]
            plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=int(self.dot_size))

            # and the inverse
            xy = self.maxima_locations[class_member_mask & ~core_samples_mask]
            plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=int(self.dot_size/2))
        if self.plotUnit =="dist":
            plt.title('Failed: Please switch plot units to px')
        else:
            plt.title('Clusters Found (pre-reject): '+str(n_clusters_)+', EPS: '+ str(self.eps)+ ', DataFloor: '+ str(self.imagefloor)+"*MaxSignal")
        plt.xlim(0, self.lines_fast_High-self.lines_fast_Low)
        plt.ylim(0, self.lines_slow_High-self.lines_slow_Low)
        plt.show()

        plt.subplot(2,3,6 , aspect='equal')

        self.maxima = []
        self.particledict = {}
        particlecounter=0
        try:
            if self.data['settings']['scan']['color'] == "":
                print "colour OK"
        except:
            self.data['settings']['scan']['color'] = "NA"
        for k, col in zip(unique_labels, colors):
            if k>=0:
                class_member_mask = (labels == k)
                xy = self.maxima_locations[class_member_mask & core_samples_mask]
                            #<- to catch individual particle locations need to average at these grouped points
                position=[0,0]
                if len(xy) >= int(self.minnumparticles):
                    sum1=0
                    sum2=0
                    count =0
                    for i in xy:
                        count+=1
                        sum1 += i[0]
                        sum2 += i[1]
                    avg1=float(sum1)/(count)
                    avg2=float(sum2)/(count)
                    position = [avg1,avg2]
                total = []
                for x,y in xy:
                    # pull real values (unnormalised) for histogramming
                    total.append(self.selectedarea[y,x])
                if len(total) == 5:
                    mintotal = min(total)
                    total.remove(mintotal)
                if len(total) < 5:
                    avgIntensity = np.average(total)
                    if str(avgIntensity) != "nan":
                        """grab area average centered at point"""
                        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=int(self.dot_size))
                        intensitylist = []
                        self.maxboxwidth = 20
                        particle_area = self.selectedarea[int(position[1])-self.maxboxwidth:int(position[1])+self.maxboxwidth, int(position[0])-self.maxboxwidth:int(position[0])+self.maxboxwidth]
                        avgIntensityBox=0
                        particle = {"position": position, "background" : str(self.average_box_value), "boxtotal" : avgIntensityBox, "area" : particle_area, "total" : avgIntensity, "ref_power": self.ref_power, "ill_power" :self.ill_power, "color" : str(self.data['settings']['scan']['color']), "type" : str(self.plte), "localvals":""}
                        unique = True
                        if len(self.particledict) > 0:
                            for particles in self.particledict:
                                if position == self.particledict[particles]["position"]:
                                     unique = False
                                     print self.particledict[particles]['position']
                                     print 'non unique particles found'
                        if unique:
                            self.maxima.append(avgIntensity)
                            particlecounter +=1
                            particlename = str("p"+ str(particlecounter))
                            self.particledict[particlename] = particle
        plt.xlim(0, self.lines_fast_High-self.lines_fast_Low)
        plt.ylim(0, self.lines_slow_High-self.lines_slow_Low)
        plt.show()
    """
    -------------------------------------------------
    Cluster Saving Logic
    """
    def _collect_max_fired(self):
        #print "\tCollected maxima for " + self.value
        #self.dictOfMaxima.update({str(5) : self.maxima})
        self.dictOfMaxima['name'].append(self.path)
        self.dictOfMaxima['file'].append("maxima"+str(self.data['settings']['scan']['color'])+str(len(self.dictOfMaxima["name"])))
        self.dictOfMaxima['data'].append(np.array(self.maxima))
        name = str("maxima"+str(self.data['settings']['scan']['color'])+str(len(self.dictOfMaxima["name"]))+ str(self.particledict["p1"]['type']) + str(np.random.randint(500)))
        print "Collected set : " + name
        self.areaArray[name] = self.selectedarea
        self.dictOfParticles[name] = self.particledict
        self.pickle(self.particledict)
    def _clear_collect_fired(self):
        #self.dictOfMaxima = {}
        self.dictOfMaxima['name'] = []
        self.dictOfMaxima['file'] = []
        self.dictOfMaxima['data'] = []
        self.dictOfParticles = {}
        self.dictOfPairs = {}
        self.areaArray= {}
    def _write_collect_fired(self):
        suggestedfile =  "Collected_Maxima_"
        fname = self._check_for_save_dir(suggestedfile, self.wildcardsMAT)
        if fname != "":
            dataset = {}
            for i in range(len(self.dictOfMaxima["name"])):
                print i
                dataset.update({str(self.dictOfMaxima["file"][i]):self.dictOfMaxima["data"][i]})
            scio.savemat(fname, dataset, True)
        fname = self._check_for_save_dir(suggestedfile, self.wildcardsCSV)
        print "Saving to:"
        print fname
        ioCSV.toCSV(dataset,fname)
    def _track_particle_over_files_fired(self):
        self.dictOfPairs = {}
        if len(self.dictOfParticles) > 1:
            particlesets = []
            unorderedsets = self.dictOfParticles.keys() #find all keys
            print "unorderedsets"
            print unorderedsets
            relevantsetpresent = False
            for set in unorderedsets:
                print "set's name is : " + str(set)
                particles = self.dictOfParticles[set].keys()
                if self.dictOfParticles[set][particles[0]]['type'] == self.compare_to and not relevantsetpresent: #orders keys by selectec pivot
                    particlesets.append(set)
                    nameofpivot = str(set)
                    print "name of pivot = " + str(nameofpivot)
                    relevantsetpresent = True
            if relevantsetpresent == False:
                print "No relevant data set to pivot, choose another option"
                return
            for set in unorderedsets:
                if str(set) != nameofpivot:
                    print "adding " + set
                    particlesets.append(set)
            for particle in self.dictOfParticles[particlesets[0]]:
                neighbours = []
                for i in range(1,len(particlesets)):
                    found, match = self._find_neighbour(self.dictOfParticles[particlesets[0]][particle], self.dictOfParticles[particlesets[i]])
                    if len(neighbours)==0:
                        neighbours.append(self.dictOfParticles[particlesets[0]][particle])
                    if found:
                        neighbours.append(self.dictOfParticles[particlesets[i]][match])
                if self.track_all and len(neighbours) == len(self.dictOfParticles):
                    self.dictOfPairs[str(particle)] = neighbours
                elif not(self.track_all) and len(neighbours)>0:
                    localvals=[]
                    if self.pull_local_value and len(neighbours) ==1:
                        for i in range(1,len(particlesets)):
                            localvals.append(self._find_average_area(self.areaArray[particlesets[i]],self.dictOfParticles[particlesets[0]][particle]["position"]))
                        l=""
                        for item in localvals:
                            l = l + ", " + str(item)
                        self.dictOfParticles[particlesets[0]][particle]["localvals"] = l

                    self.dictOfPairs[str(particle)] = neighbours

        length = len(self.dictOfPairs)
        print "\n%s particles have been tracked across some/all files from %s total particles" % (len(self.dictOfPairs), len(self.dictOfParticles[particlesets[0]]))
        self._save_pairs(self.dictOfPairs)
    def _save_pairs(self,dict):
        area = []
        if len(dict) > 0:
            stringsave = []
            stringsave.append(" ,type,x,y, wavelength, color, box total, background avg, box average, box width, peak, ill_P, ref_P, normalised, normalised/pow, total/pow,localVals")
            for key in dict:
                totals=[]
                for particle in dict[key]:
                    totals.append(float(particle["total"]))
                max = np.max(np.array(totals))
                stringsave.append(str(len(dict[key])))
                for particle in dict[key]:
                    wavelength = 0
                    if particle["color"] == "R":
                        wavelength = 632
                    if particle["color"] == "G":
                        wavelength = 532
                    if particle["color"] == "B":
                        wavelength = 488
                    selectedarea = particle["area"][self.maxboxwidth-int(self.boxHW):self.maxboxwidth+int(self.boxHW),self.maxboxwidth-int(self.boxHW):self.maxboxwidth+int(self.boxHW)]
                    sum = []
                    total = 0
                    for row in selectedarea:
                        for col in row:
                            sum.append(float(col))
                            total += float(col)
                    averagebox = np.average(sum)
                    totalbox = total
                    if self.ill_power > 0.0 and self.ref_power > 0.0:
                        stringsave.append(" ,"+ str(particle["type"])+","+str(particle["position"][0]) +","+str(particle["position"][1]) +","+ str(wavelength) + ","+ str(particle["color"])+","+str(totalbox)+","+str(particle["background"])+ ","+ str(averagebox)+","+str(self.boxHW)+","+ str(particle["total"])+","+ str(particle["ill_power"])+","+ str(particle["ref_power"])\
                        +","+ str(float(particle["total"])/max) +","+ str(float(particle["total"])/max/(np.sqrt(float(particle["ill_power"])*float(particle["ref_power"]))))+","+ str(float(particle["total"])/(np.sqrt(float(particle["ill_power"])*float(particle["ref_power"])))) + "," +str(particle["localvals"]))
                    else:
                        stringsave.append(" ,"+ str(particle["position"][0]) +","+str(particle["position"][1]) +","+ str(wavelength) + ","+ str(particle["color"])+","+ str(averagebox)+","+ str(particle["total"])+","+ str(particle["ill_power"])+","+ str(particle["ref_power"])\
                        +","+ "none" +","+ "none" +","+ "none"+ "," +str(particle["localvals"]))
                    #self.plotAndSave(selectedarea, "gray",[0,np.max(selectedarea)],True,str(particle), "")
                    area.append(selectedarea)
                stringsave.append("")
            suggestedfile =  "Tracked_Particles_"
            fname = self._check_for_save_dir(suggestedfile, self.wildcardsCSV)
            print "Saving to:"
            print fname
            ioCSV.stringArrayToCSV(stringsave,fname)
        else:
            print "No data found"

    def pickle(self,data):
        pickle.dump(data, open( "save.p", "wb" ) )


    def _find_average_area(self, area, position):
        return np.mean(area[int(position[0])-int(self.trackDistance):int(position[0])+int(self.trackDistance),int(position[1])-int(self.trackDistance):int(position[1])+int(self.trackDistance)])
    def _find_neighbour(self, targetparticle, particleset):
        for particle in particleset:
            if self._close_to_target(particleset[particle]["position"], targetparticle["position"]):
                return True, particle
        return False, None
    def _close_to_target(self,pos1,pos2):
        if abs(pos1[0]-pos2[0])<int(self.trackDistance) and abs(pos1[1]-pos2[1])<int(self.trackDistance) :
            return True
        else:
            return False
    def _plot_collection_fired(self):

        import matplotlib.pyplot as plt
        try:
            plt.close('all')
        except:
            print "not closed"
        thistitle = "Maxima Collection Histogram"
        self.fig3 = plt.figure(thistitle)
        for i in range(len(self.dictOfMaxima["name"])):
            n, bins, patches = plt.hist(self.dictOfMaxima["data"][i], float(self.binrange), normed=0, histtype='step', label = str(self.dictOfMaxima["name"][i]))
        plt.legend()
        plt.show()
    """
    -------------------------------------------------
    Image Saving Logic
    """
    def _check_for_save_dir(self, suggestedfile, wildcards):
        root = Tkinter.Tk()
        if self.directory != "":
            fname = tkFileDialog.asksaveasfilename(initialfile = suggestedfile, initialdir = self.directory, filetypes=(wildcards))
        else:
            print "Directory string empty. Please load a file first"
            fname =""
        root.destroy()
        return fname
    def _save_folder_image_fired(self):
        i = "1"
        length = str(len(self.allfiles))
        for file in self.allfiles:
            print "\nSaving file " +i+ " of " + length
            i = str(int(i) +1)
            self.path  = file
            self._quick_load_main()
            #self.mainplot.draw(self.mainplot)
            if self.justMainplot:
                data = self.mainplot
            else:
                data = self.LineScans
            try:
                self._save_image(self.path, data, True, self.justMainplot)
            except:
                print "Had to skip"
    def _save_image(self, fname, data, quick = False, justMainplot = False):
        if quick:
            fname = fname + "_"+str(self.plte)+"_QS.png"
        else:
            fname = fname + ".png"
        if justMainplot:
            if not quick:
                print "just saving Main"
            self.LineScans.do_layout(force=True)
            plot_gc = PlotGraphicsContext(self.LineScans.outer_bounds)
            plot_gc.render_component(self.LineScans)
        data.do_layout(force=True)
        plot_gc = PlotGraphicsContext(data.outer_bounds)
        plot_gc.render_component(data)
        plot_gc.save(fname)
    def _save_plots_button_fired(self):
        suggestedfile = self.plotA["path"]+ "_4plt"
        fname = self._check_for_save_dir(suggestedfile, self.wildcardsPNG)
        if fname != "":
            self._save_image(fname, self.plot)
        else:
            print "file not saved"
    def _save_MainPlot_button_fired(self):
        suggestedfile = self.filename + "_plt"
        fname = self._check_for_save_dir(suggestedfile, self.wildcardsPNG)
        if fname != "":
            if self.justMainplot:
                data = self.mainplot
                print data
                self._save_image(fname, data , False, self.justMainplot)
            else:
                self._save_image(fname, self.LineScans)
        else:
            print "file not saved"
    def _save_all_colloc_fired(self):
        i = "1"
        length = str(len(self.allfiles))
        for file in self.allfiles:
            print "\nSaving file " +i+ " of " + length
            i = str(int(i) +1)
            self.path  = file
            self._all_load()
            fname = self.path +"coloc"
            try:
                self._save_image(fname,self.colocPlot)
            except:
                print "Had to skip"
    def _save_coloc_button_fired(self):
        suggestedfile = "Coloc_" + self.titleColoc.strip()
        fname = self._check_for_save_dir(suggestedfile, self.wildcardsPNG)
        if fname != "":
            self._save_image(fname, self.colocPlot)
        else:
            print "file not saved"
    """
    ----------------------------
    MatLab Out
    """
    def _out_to_mat_fired(self):
        suggestedfile = self.filename + "_Matlab_"
        fname = self._check_for_save_dir(suggestedfile, self.wildcardsMAT)
        if fname != "":
            print fname
    """
    ------------------------------------------------
    Gen .log file for use with DataLogger.py to log large datacollections
    """
    def _genfilelist_fired(self):   #this feature has been commented out for now
        print "this feature has been commented out for now"
        """
        if self.loaded:
            event = {'trial': 0 , "settings" : "", "notes": "", "time": ""}
            eventlist = {"Description": "", "0" : event}
            i=1
            for afile in self.allfiles:
                #grab file name
                junk,currentfilename = afile.split(self.filedir+"/")
                print "Working on file : " + currentfilename
                #unpickle file and grab data
                try:
                    currentfile = open(afile,'rb')
                    data = pickle.load(currentfile)
                    currentfile.close()

                    foldername,time = currentfilename.split("_")
                    time,junk = time.split(".")
                    settings = data['settings']['scan']
                    strsettings = ""
                    for key, value in settings.iteritems() :
                        strsettings += str(key) + " " + str(value)+ "\n"
                    newtrial = {'trial': i, "settings" : strsettings, "notes": "", "time": time}
                    eventlist[str(i)] = newtrial

                    i +=1
                except:
                    print "\tcorrupt file, skipping"
            settings = ""
            strsettings =""
            newtrial = ""

            #save data to data logger compatible file
            a = os.getcwd() + "/eventlist_"+foldername
            if not os.path.isdir(a):
                print "made"
                os.makedirs(a)
            b = a+ "/filelist.log"
            print "saving to " + b
            f1 = open(b, "w")
            pickle.dump(eventlist, f1)
            f1.close()

            print "File Write Complete"
        else:
            print "Please load a folder first"
        """

    """
    ------------------------------------------------
    Plotting functions
    """
    def _plot_all(self):
        self._plot()
        self._plotMain()
    def _generate_img_plot(self,data, color, plottitle, normalise = False):

        if normalise:
            print "normalising"
            data["data"] = data["data"] /np.amax(data["data"])

        genplotdata = ArrayPlotData(imagedata = data["data"])
        if plottitle == "":
            title = data["plot"]
        else:
            title = data["plot"] + " - " + str(plottitle)
        genplot = Plot(genplotdata, title = title)
        genplot.img_plot("imagedata", xbounds = (data["range"][0][0],data["range"][0][1]), ybounds = (data["range"][1][0],data["range"][1][1]), colormap=color)
        genplot.tools.append(PanTool(genplot))
        zoom = ZoomTool(component=genplot, tool_mode="box", always_on=False)
        genplot.overlays.append(zoom)
        if self.square2 == "dist":
            genplot.aspect_ratio = (self.xHi-self.xLo)/(self.yHi-self.yLo)
        else:
            genplot.aspect_ratio = (data["shape"][0]/data["shape"][1])

        return genplot
    def _generate_colorbar(self,data):
        colorbar = ColorBar(index_mapper=LinearMapper(range=data.color_mapper.range),
                        color_mapper=data.color_mapper,
                        orientation='v',
                        resizable='v',
                        width=20,
                        padding=5)
        colorbar.plot = data
        colorbar.tools.append(PanTool(colorbar, constrain_direction="y", constrain=True))
        zoom_overlay = ZoomTool(colorbar, axis="index", tool_mode="range",
                            always_on=True, drag_button="right")
        colorbar.overlays.append(zoom_overlay)
        return colorbar
    def _plot(self):
        print "Plotting Functions"
        self.container1 = GridPlotContainer(shape = (2,4), spacing = (0,0), use_backbuffer=True,
	                                     valign = 'top', bgcolor = 'white')

        print"\t Generating plots"
        self.path1 = os.path.split(self.plotA["path"])[1]
        self.path2 = os.path.split(self.plotB["path"])[1]
        self.path3 = os.path.split(self.plotC["path"])[1]
        self.path4 = os.path.split(self.plotD["path"])[1]
        self.plot1 = self._generate_img_plot(self.plotA,self.color_Dict[self.color_Enum1], self.title1)
        self.plot2 = self._generate_img_plot(self.plotB,self.color_Dict[self.color_Enum2], self.title2)
        self.plot3 = self._generate_img_plot(self.plotC,self.color_Dict[self.color_Enum3], self.title3)
        self.plot4 = self._generate_img_plot(self.plotD,self.color_Dict[self.color_Enum4], self.title4)

        ##ADD COLORBARS
        self.colorbar1 = self._generate_colorbar(self.plot1)
        self.colorbar1.padding_left = 45
        self.colorbar1.padding_right= 5

        self.colorbar2 = self._generate_colorbar(self.plot2)
        self.colorbar2.padding_left = 10

        self.colorbar3 = self._generate_colorbar(self.plot3)
        self.colorbar3.padding_left = 45
        self.colorbar3.padding_right= 5

        self.colorbar4 = self._generate_colorbar(self.plot4)
        self.colorbar4.padding_left = 15

        self.container1.add(self.colorbar1)
        self.container1.add(self.plot1)
        self.container1.add(self.plot2)
        self.container1.add(self.colorbar2)
        self.container1.add(self.colorbar3)
        self.container1.add(self.plot3)
        self.container1.add(self.plot4)
        self.container1.add(self.colorbar4)

        self.plot1.padding_right = 5
        self.plot2.padding_left = 5
        self.plot1.padding_bottom = 15
        self.plot2.padding_bottom = 15
        self.plot3.padding_top = 15
        self.plot4.padding_top = 15
        self.plot1.x_axis.orientation = "top"
        self.plot2.x_axis.orientation = "top"
        self.plot2.y_axis.orientation = "right"
        self.plot3.padding_right = 5
        self.plot4.padding_left = 5
        self.plot4.y_axis.orientation = "right"


        self.colorbar1.padding_top = self.plot1.padding_top
        self.colorbar1.padding_bottom = self.plot1.padding_bottom
        self.colorbar2.padding_top = self.plot2.padding_top
        self.colorbar2.padding_bottom = self.plot2.padding_bottom
        self.colorbar3.padding_top = self.plot3.padding_top
        self.colorbar3.padding_bottom = self.plot3.padding_bottom
        self.colorbar4.padding_top = self.plot4.padding_top
        self.colorbar4.padding_bottom = self.plot4.padding_bottom

        imgtool = ImageInspectorTool(self.plot1)
        self.plot1.tools.append(imgtool)
        overlay = ImageInspectorOverlay(component=self.plot1, image_inspector=imgtool,
                                    bgcolor="white", border_visible=True)
        self.plot1.overlays.append(overlay)

        self.plot2.range2d = self.plot1.range2d
        self.plot3.range2d = self.plot1.range2d
        self.plot4.range2d = self.plot1.range2d

        self.plot = self.container1
        if self.autocolor:
            self._colormap_fired()
        if self.autoColoc:
            self._plot_Colocal()
    def _plotMain(self):

        print "Generating Main Plot"
        #check for normalising data for plotE
        if self.norm:
            print "normalising main plot"
            self.mainplot = self._generate_img_plot(self.plotE, self.color_Dict[self.color_Enum5],"", True)
        else:
            self.mainplot = self._generate_img_plot(self.plotE, self.color_Dict[self.color_Enum5],"")


        self._image_index = GridDataSource(array([]),
                                          array([]),
                                          sort_order=("ascending","ascending"))


        self.xs = linspace(self.plotE["range"][0][0], self.plotE["range"][0][1], self.plotE["shape"][0])
        self.ys = linspace(self.plotE["range"][1][0], self.plotE["range"][1][1], self.plotE["shape"][1])

        self._image_index.set_data(self.xs, self.ys)

        self._image_value = ImageData(data=array([]), value_depth=1)
        self._image_value.data = self.plotE['data']

        #load in data and bounds for mainplot
        if self.plotUnit == "px":
            img_plot = self.mainplot.img_plot("imagedata")[0]
            imgtool = ImageInspectorTool(img_plot)
            img_plot.tools.append(imgtool)
            overlay = ImageInspectorOverlay(component=img_plot, image_inspector=imgtool,
                                        bgcolor="white", border_visible=True)
            self.mainplot.overlays.append(overlay)



        #+tools
        self.mainplot.overlays.append(LineInspector(component=self.mainplot,
                                               axis='index_x',
                                               inspect_mode="indexed",
                                               write_metadata=True,
                                               is_listener=False,
                                               #constrain_key="right",
                                               color="white"))

        self.mainplot.overlays.append(LineInspector(component=self.mainplot,
                                               axis='index_y',
                                               inspect_mode="indexed",
                                               write_metadata=True,
                                               color="white",
                                               is_listener=False))

        #colorbar + tools
        self.colorbar5  = self._generate_colorbar(self.mainplot)


        self.pd = ArrayPlotData(line_index = array([]),
                                line_value = array([]))


        ##slow plot + tools
        self.slow_plot = Plot(self.pd,   title = "Slowline : " + str(self.xline))
        self.slow_plot.plot(("line_index", "line_value"),
                             line_style='solid')
        self.slow_plot.tools.append(PanTool(self.slow_plot))
        self.zoom_overlayslow = ZoomTool(self.slow_plot, axis="index", tool_mode="range",
                            always_on=True, drag_button="right")
        self.slow_plot.overlays.append(self.zoom_overlayslow)


        self.pd.set_data("line_index2", array([]))
        self.pd.set_data("line_value2", array([]))


        ## fast plot + tools
        self.fast_plot = Plot(self.pd,   title = "Fastline : " + str(self.yline))
        self.fast_plot.plot(("line_index2", "line_value2"),
                             line_style='solid')
        self.fast_plot.tools.append(PanTool(self.fast_plot))
        self.zoom_overlayfast = ZoomTool(self.fast_plot, axis="index", tool_mode="range",
                            always_on=True, drag_button="right")
        self.fast_plot.overlays.append(self.zoom_overlayfast)



        ##set up for line data
        self.pd.set_data("line_index", self.xs)
        self.pd.set_data("line_index2", self.ys)
        self.pd.set_data("line_value",
                                 self._image_value.data[self.xscanline,:])
        self.pd.set_data("line_value2",
                                 self._image_value.data[:,self.yscanline])

        ##organise layout of plots
        self.colorbar5.padding= 0
        self.colorbar5.padding_left = 15
        #self.colorbar5.height = 400
        self.colorbar5.padding_top =50
        self.colorbar5.padding_bottom = 0
        self.colorbar5.padding_right = 25
        self.colorbar5.padding_left = 50

        self.mainplot.width = 300
        self.mainplot.padding_top = 50

        self.mainplot.index_axis.title = 'fast axis'
        self.mainplot.value_axis.title = 'slow axis'

        self.slow_plot.width = 100
        self.slow_plot.padding_right = 20

        self.fast_plot.width = 100
        self.fast_plot.padding_right = 20



        self.container2 = GridPlotContainer(shape = (1,2), spacing = ((0,0)), use_backbuffer=True,
	                                     valign = 'top', halign = 'center', bgcolor = 'white')
        self.container3 = GridPlotContainer(shape = (2,1), spacing = (0,0), use_backbuffer=True,
	                                     valign = 'top', halign = 'center', bgcolor = 'white')
        self.container4 = GridPlotContainer(shape = (1,2), spacing = (0,0), use_backbuffer=True,
	                                     valign = 'top', halign = 'center', bgcolor = 'white')

        self.container2.add(self.colorbar5)
        self.container3.add(self.fast_plot)
        self.container3.add(self.slow_plot)
        self.container4.add(self.container3)
        self.container4.add(self.mainplot)
        self.container2.add(self.container4)
        self.LineScans = self.container2

        if self.autocolor:
            self._colormap_fired()
        self._readlines()
        self._scale()
    def _coloc_fired(self):
        self._plot_Colocal()
    def _plot_Colocal(self):
        image = np.zeros((self.plotA["shape"][0], self.plotA["shape"][1],4), dtype = np.uint8)
        if self.apply1_ck:
            A=self._normalise_array_to(self.plotA['data'], self.pltaLow,self.pltaHi)*255
        else:
            A=self._normalise_array(self.plotA['data'])*255

        if self.apply2_ck:
            B=self._normalise_array_to(self.plotB['data'], self.pltbLow,self.pltbHi)*255.0
        else:
            B=self._normalise_array(self.plotB['data'])*255

        A=self._int_array(A)
        B=self._int_array(B)

        image[:,:,0] =np.add(image[:,:,0], A)    # Vertical red stripe
        image[:,:,1] =np.add(image[:,:,1], B)    # Vertical red stripe
        #image[:,:,1] += B     # Horizontal green stripe; also yellow square
        #image[-80:,-160:,2] += 255 # Blue square
        image[:,:,3] = 255

        # Create a plot data obect and give it this data
        pd = ArrayPlotData()
        pd.set_data("imagedata", image)

        # Create the plot
        plot = Plot(pd, title = self.titleColoc)
        if self.plotUnit == "dist":
            img_plot = plot.img_plot("imagedata", xbounds = (self.plotA["range"][0][0],self.plotA["range"][0][1]), ybounds = (self.plotA["range"][1][0],self.plotA["range"][1][1]))
        else:
            img_plot = plot.img_plot("imagedata")
        # Tweak some of the plot properties
        plot.bgcolor = "white"
        if self.square2 == "dist":
            plot.aspect_ratio = (self.xHi-self.xLo)/(self.yHi-self.yLo)
        else:
            plot.aspect_ratio = (self.D["shape"][0]/self.D["shape"][1])
        # Attach some tools to the plot
        plot.tools.append(PanTool(plot, constrain_key="shift"))
        plot.overlays.append(ZoomTool(component=plot,
                                        tool_mode="box", always_on=False))

        # imgtool = ImageInspectorTool(img_plot)
        # img_plot.tools.append(imgtool)
        # plot.overlays.append(ImageInspectorOverlay(component=img_plot,
                                                   # image_inspector=imgtool))
        container = GridPlotContainer(shape = (1,1), spacing = ((0,0)), use_backbuffer=True,
	                                      valign = 'top', halign = 'center', bgcolor = 'white')
        container.add(plot)
        self.colocPlot = container
    def _plot_zstack(self):
        filelist = self._get_file_names()
        self.zstackarray = []
        a = {"data":[],"shape":[],"range":[], "plot": self.pltf}
        for i in filelist:
            data = self._quick_load(i)
            D = self._treat_file(data)
            a = self._assign_data(a,D)
            self.zstackarray.append(a["data"])
            self._update_zstack(self.zstackarray[0], self.zstack)
    def _update_zstack(self,data, plot):
        genplotdata = ArrayPlotData(imagedata = data)
        genplot = Plot(genplotdata, title = "Z Stack")
        genplot.img_plot("imagedata")
        container =  GridPlotContainer(shape = (1,2), spacing = ((0,0)), use_backbuffer=True,
        	                                     valign = 'top', halign = 'center', bgcolor = 'white')

        self.zstack = container
    def _quick_load(self,name):
        print "Opening: \n" + str(name)
        file = open(str(name),'rb')
        data = pickle.load(file)
        file.close()
        print "File.closed()"
        return data
    #########################################################
    def _special_fired(self):
        #load stitch
##        from mpl_toolkits.mplot3d import Axes3D
##        from matplotlib import cm
##        import matplotlib.pyplot as plt
##        print "starting figure"
##        fig = plt.figure()
##        ax = fig.gca(projection='3d')
##        print "meshing"
##        X, Y = np.meshgrid(self.xs,self.ys)
##        print "doing the easy bits"
##        Z = self.plotB['data']
##        N = self.plotA['data']/(self.plotA['data'].max())
##        print "plotting"
##        surf = ax.plot_surface(
##            X, Y, Z, rstride=1, cstride=1,
##            facecolors=cm.jet(N),
##            linewidth=0, antialiased=False, shade=False)
##        ax.view_init(elev=-92, azim=-37)
##        plt.show()
##        show()


        a = np.array(self.plotE['data'])
        a.shape = (int(self.plotA["shape"][0]*self.plotA["shape"][1]))
        import matplotlib.pyplot as plt
        # the histogram of the data with histtype='step'
        n, bins, patches = plt.hist(a, flaot(self.binrange), normed=1, histtype='bar')

        plt.show()







##        plt.plot([1,2,3,4])
##        plt.ylabel('some numbers')
##        plt.show()
##        histarray, binedges = np.histogram(a, bins = 20, density = True)
##        print histarray
##        print binedges
##        plt.plot(binedges, histarray)
##        plt.show()
####       rint histarray
##        bins = np.arange(self.plot1.color_mapper.range.low, self.plot1.color_mapper.range.high, 20)
##        print "1"
##
##        self.pd = ArrayPlotData(line_index = array([]),
##                                line_value = array([]))
##        print "2"
##        self.slow_plot = Plot(self.pd,   title = "Slowline : " + self.xline)
##        print "3"
##        self.slow_plot.plot(("line_index", "line_value"),
##                             line_style='solid')
##        print "4"
##        self.pd.set_data("line_index", bins)
##        print "5"
##        self.pd.set_data("line_value",histarray)
##
##        print "done"
##        print "All resolutions must be the same"
##        a,b = 2,3 #raw_input("\tset rows and cols: ")
##        size = 512 #raw_input("\tsize:")
##        self.stitchdataA = np.zeros((size*a, size*b))
##        self.stitchdataB = np.zeros((size*a, size*b))
##        i = 1
##        col = 0
##        while i < a*b:
##            j = 1
##            row = 0
##            while j < b:
##                self._treat_file(self._single_plot())
##                self.plotA['plot'] = self.plta
##                self.plotA = self._assign_data(self.plotA)
##                print col*size, row*size
##                self.stitchdataA[col*size : col*self.plotA["shape"][0], row*size : row*self.plotA["shape"][1]] = self.plotA
##                row = row+1
##                j = j+1
##                i = i+1
##            col = col+1
##
##
##        i = 1
##        col = 0
##        while i < a*b:
##            j = 1
##            row = 0
##            while j < b:
##                self._treat_file(self._single_plot())
##                self.plotB['plot'] = self.pltb
##                self.plotB = self._assign_data(self.plotB)
##                self.stitchdataB[col*size : col*self.plotB["shape"][0], row*size : row*self.plotB["shape"][1]] = self.plotB
##                row = row+1
##                j = j+1
##                i = i+1
##            col = col+1
##
##        self.plotA["data"] = self.stitchdataA
##        self.plotB["data"] = self.stitchdataB
##        self.plotC["data"] = self.stitchdataA
##        self.plotD["data"] = self.stitchdataB
##        self.plotA["range"][0][0] = 0
##        self.plotA["range"][1][0] = 0
##        self.plotA["range"][0][1] = size*a
##        self.plotA["range"][1][1] = size*b
##        self.plotA["shape"] = (size*b, size*a)
##          self._plot_all()##
##        gc.collect()
        return
    def _normalise_array_to(self,data, low, high):
        x=0
        y=0
        newdata = np.zeros(data.shape)
        for row in data:
            x=0
            for col in row:
                point = col-low
                if point < 0.0:
                    point = 0.0
                point=point/(high-low)
                if point > 1:
                    point = 1
                newdata[y,x] = point
                x+=1
            y+=1
        return newdata
    def _normalise_array(self,data):
        return data/np.amax(data)
    def _int_array(self,data):
        x=0
        y=0
        for row in data:
            x=0
            for col in row:
                data[y,x] = int(col)
                x+=1
            y+=1
        return data
    ########################################################
    """
    ------------------------------------------------
    File Selection Functions
    """
    """Load helping functions"""
    def _last_file(self):
        print "saved last file"
        f = open("last_file.txt", "w")
        f.write(self.path)
        f.close()
    def __init__(self):
        try:
            self.norm = False
            f = open("last_file.txt", "r")
            self.path = f.read()
            f.close()
            self._assign_plot_type()
            self._update_file_vars()
            self._all_load()
        except:
            complete = False
            print "No last file found"
    def _pre_smooth(self,data):
        print "\tPRESMOOTHING"
        y=0
        x=0
        for line in data:
            x_axis = np.arange(0,int(len(line)))
            y_axis = line
            slope,intercept,r_value,p_value,std_err = stats.linregress(x_axis,y_axis)
            x=0
            for point in line:
                data[y,x] = point - (slope*x + intercept)
                x+=1
            y+=1
        return data
    def _safe_smooth(self,data):
        x = 0
        y = 0
        if self.xscanline < len(data[0])-2:
            for line in data:
                #find value of slow line at safe value

                zeropoint = np.average(line[self.xscanline], line[self.xscanline+1], line[self.xscanline+2])

                x_axis = [self.xscanline, len(line)-1]
                y_axis = [line[self.xscanline],line[len(line)-1]]
                slope,intercept,r_value,p_value,std_err = stats.linregress(x_axis,y_axis)
                x = 0
                for point in line:
                    data[y,x] = point - (slope*x + zeropoint)
                    x+=1
                y+=1
        return data
    def _update_from_path(self):
        self.plotA["path"] = self.path
        self.plotB["path"] = self.path
        self.plotC["path"] = self.path
        self.plotD["path"] = self.path
        self.plotE["path"] = self.path
    def _update_file_vars(self):    #update file quick vars
        self.filename  = os.path.split(self.path)[1]
        self.value = str(self.filename)
        self.directory = os.path.split(self.path)[0]
        self.loaded = True
        self._update_from_path()
    def _get_file_name(self):       #user entered file select set to self.path for ALL FILES
        root = Tkinter.Tk()
        if self.directory != "":
            path = tkFileDialog.askopenfilename(initialdir = self.directory, filetypes=(self.wildcardsLOAD), title ='Choose a file')
        else:
            path = tkFileDialog.askopenfilename(filetypes=(self.wildcardsLOAD))
        root.destroy()
        self._update_from_path()
        self._last_file()
        return path
    def _get_file_names(self):
        root = Tkinter.Tk()
        if self.directory != "":
            filelist = tkFileDialog.askopenfilenames(initialdir = self.directory, filetypes=(self.wildcardsLOAD), title='Choose files')
        else:
            path = tkFileDialog.askopenfilename(filetypes=(self.wildcardsLOAD))
        root.destroy()
        return filelist
    def _update_file_list(self):    #updates list of files in directory along self.path
        """Populate file list"""
        if self.path !="" :
            self.allfiles = []
            for filenames in os.walk(self.directory):
                for files in filenames:
                    for afile in files:
                        if ".zis" in str(afile):
                            if ".png" not in str(afile)and ".mat" not in str(afile):
                                self.allfiles.append(str(self.directory+"/"+afile))
        return
    def _unpickle_file(self,plot):       #returns unpickled data
        if plot["path"] != "":
            print "Opening: \n" + str(plot["path"])
            file = open(str(plot["path"]),'rb')
            data = pickle.load(file)
            file.close()
            print "File.closed()"
        return data
    def _treat_file(self, data):          #np.array() and shapes each data set `` OutPuts treated D(ata)
        filedata = data['settings']['scan']
        #determine shape
        range = np.zeros((2,2))
        for x in xrange(3):
            if filedata['axes'][x] == 0:
                fast = filedata['npoints'][x]
                range[0][1] = filedata['fast_axis_range']
            if filedata['axes'][x] == 1:
                slow = filedata['npoints'][x]
                range[1][1] = filedata['range'][x]
        shape = (fast,slow)

        if range[0][1] == 0:
            range[0][1] = 1
        if range[1][1] == 0:
            range[1][1] = 1

        #shapedata
        X = np.array(data['data']['lia_x']["0"])
        X.shape = shape
        Y = np.array(data['data']['lia_y']["0"])
        Y.shape = shape
        try:
            F= np.array(data['data']['dio2'])
            F[F>int(self.F_floor)] = 0
            F.shape = shape
        except:
            F = np.zeros(shape)
            print "No DIO2 found"

        try:
            X0 = np.array(data['data']['lia_x']["3"])
            X0.shape = shape
            Y0 = np.array(data['data']['lia_y']["3"])
            Y0.shape = shape
        except:
            X0 = []
            Y0 = []
            print "No second channel found"

        #check for presmooth
        if self.presmooth:
            X = self._pre_smooth(X)
            Y = self._pre_smooth(Y)
        if self.safesmooth:
            X = self._safe_smooth(X)
            Y = self._safe_smooth(Y)
        D = {"X":X,"Y":Y,"F":F,"X0":X0,"Y0":Y0,"shape":shape,"range":range}
        return D
    def _assign_data(self,plotdata, D):#assigns data to plot area
        print "...assigning data"
        try:
            if plotdata['plot']== "R":
                print "\t\tplotting R"
                toplot = np.sqrt(np.multiply(D["X"],D["X"]) + np.multiply(D["Y"],D["Y"]))
            if plotdata['plot'] == "Phase":
                print "\t\tplotting Phase"
                toplot = np.arctan(D["Y"]/D["X"])
            if plotdata['plot']== "R0":
                print "\t\tplotting R0"
                toplot = np.arctan2(D["Y"],D["X"])
            if plotdata['plot']== "R/R0":
                print "\t\tplotting R/R0"
                toplot = np.sqrt(np.multiply(D["X"],D["X"]) + np.multiply(D["Y"],D["Y"]))/np.sqrt(np.multiply(D["X0"],D["X0"]) + np.multiply(D["Y0"],D["Y0"]))
            if plotdata['plot']== "Fluor":
                print "\t\tplotting Fluor"
                toplot = D["F"]
            if plotdata['plot']=="X":
                print "\t\tplotting X"
                toplot = D["X"]
            if plotdata['plot']=="Y":
                print "\t\tplotting Y"
                toplot = D["Y"]
        except:
            print "Process failed : Check dropdown assignments"
            toplot = []


        plotdata['data']  = toplot
        plotdata['shape'] = D["shape"]
        plotdata['range'] = D["range"]
        return plotdata
    def _assign_plot_type(self):
        self.plotA['plot'] = self.plta
        self.plotB['plot'] = self.pltb
        self.plotC['plot'] = self.pltc
        self.plotD['plot'] = self.pltd
        self.plotE['plot'] = self.plte
    def _assign_main(self):
        self.plotE['plot'] = self.plte
        self.plotE = self._assign_data(self.plotE, self.D)
    def _assign_all(self):
        """Assign to plots"""
        self._assign_plot_type()

        self.plotA = self._assign_data(self.plotA, self.D)
        self.plotB = self._assign_data(self.plotB, self.D)
        self.plotC = self._assign_data(self.plotC, self.D)
        self.plotD = self._assign_data(self.plotD, self.D)
        self.plotE = self._assign_data(self.plotE, self.D)
    def _initialize_viewrange(self):#sets and resets veiwrange
        self.xLo = float("{0:.2f}".format(self.plotE["range"][0][0]))
        self.xHi = float("{0:.2f}".format(self.plotE["range"][0][1]))
        self.yLo = float("{0:.2f}".format(self.plotE["range"][1][0]))
        self.yHi = float("{0:.2f}".format(self.plotE["range"][1][1]))
    def _pull_notes(self):          #sorts and assigned scan settings to notes
        self.notes = ""
        for k, v in sorted(self.data['settings']['scan'].items()):
            self.notes +=  str(k) + "\t\t:\t" + str(v) + "\n"

    """Load Functions"""
    def _startZstack_fired(self):
        self._plot_zstack()
    def _load_button_fired(self):
        self.path = self._get_file_name()
        self._all_load()
    def _quick_load_main(self):
        self._update_file_vars()
        self.data = self._unpickle_file(self.plotE)
        self.D = self._treat_file(self.data)
        try:
            print "loading powers"
            self.ill_power = float(self.data['settings']['scan']['powers'][0])
            self.ref_power = float(self.data['settings']['scan']['powers'][1])
        except:
            print "no powers saved"
            self.ill_power = 0.0
            self.ref_power = 0.0
        self._assign_main()
        self._initialize_viewrange()
        self._plotMain()
    def _all_load(self):
        """Loads all plots from file"""
        self._update_file_vars()
        self._update_file_list()
        self.data = self._unpickle_file(self.plotE)
        self.D = self._treat_file(self.data)
        self._pull_notes()

        try:
            print "loading powers"
            self.ill_power = float(self.data['settings']['scan']['powers'][0])
            self.ref_power = float(self.data['settings']['scan']['powers'][1])
        except:
            print "no powers saved"
            self.ill_power = 0.0
            self.ref_power = 0.0
        self._assign_all()

        if self.auto_view or self.xHi == 0.0:
            self._initialize_viewrange()
        else:
            self._scale()
        gc.collect()
        self._plot_all()
        return
    def _quick_next_file(self, path):
        if self.loaded:
            self._update_file_list()
            try:
                nextfileidx = self.allfiles.index(str(path))
                nextfileidx +=1
                if nextfileidx < len(self.allfiles):
                    path = self.allfiles[nextfileidx]
                else:
                    print "end of file list"
            except:
                print "Failed"
        return path
    def _quick_prev_file(self, path):
        if self.loaded:
            self._update_file_list()
            try:
                nextfileidx = self.allfiles.index(str(path))
                nextfileidx -=1
                if nextfileidx > 0:
                    path = self.allfiles[nextfileidx]
                else:
                    print "Start of file list"
            except:
                print "Failed"
        return path
    def _quick_load_file(self, path):
        root = Tkinter.Tk()
        if self.directory != "":
            path = tkFileDialog.askopenfilename(initialdir = self.directory, filetypes=(self.wildcardsLOAD))
        else:
            path = tkFileDialog.askopenfilename( filetypes=(self.wildcardsLOAD))
        root.destroy()
        return path
    def _single_plot(self, plot, choice):
        self._assign_plot_type()
        whichfile = {   0:self._quick_prev_file,
                        1:self._quick_load_file,
                        2:self._quick_next_file}
        plot["path"] = whichfile[choice](plot["path"])
        if plot["path"] =="":
            return
        unpickleddata = self._unpickle_file(plot)
        D = self._treat_file(unpickleddata)
        plot = self._assign_data(plot, D)
        self._plot()
        return plot

    """Next File Functions"""
    def _nextfile_fired(self):
        if self.loaded:
            self._update_file_list()
            try:
                nextfileidx = self.allfiles.index(str(self.plotE["path"]))
                nextfileidx +=1
                if nextfileidx < len(self.allfiles):
                    self.path = self.allfiles[nextfileidx]
                    self._update_from_path()
                    self._all_load()
                else:
                    print "end of file list"
            except:
                print "well that didn't work"
    def _prevfile_fired(self):
        if self.loaded:
            try:
                prevfileidx = self.allfiles.index(str(self.plotE["path"]))
                prevfileidx -=1
                if prevfileidx >= 0:
                    self.path = self.allfiles[prevfileidx]
                    self._update_from_path()
                    self._all_load()
                else:
                    print "start of file list"
            except:
                print "well that didn't work"


    """Special Load Functions"""
    def _plte_changed(self):
         self.plotE['plot'] = self.plte
         self.plotE = self._assign_data(self.plotE, self.D)
         self._plotMain()
    def _color_Enum1_changed(self):
        self._plot()
    def _color_Enum2_changed(self):
        self._plot()
    def _color_Enum3_changed(self):
        self._plot()
    def _color_Enum4_changed(self):
        self._plot()
    def _color_Enum5_changed(self):
        self._plotMain()
    def _prev1_button_fired(self):
        self.plotA = self._single_plot(self.plotA,0)
    def _prev2_button_fired(self):
        self.plotB = self._single_plot(self.plotB,0)
    def _prev3_button_fired(self):
        self.plotC = self._single_plot(self.plotC,0)
    def _prev4_button_fired(self):
        self.plotD = self._single_plot(self.plotD,0)
    def _load1_button_fired(self):
        self.plotA = self._single_plot(self.plotA,1)
    def _load2_button_fired(self):
        self.plotB = self._single_plot(self.plotB,1)
    def _load3_button_fired(self):
        self.plotC = self._single_plot(self.plotC,1)
    def _load4_button_fired(self):
        self.plotD = self._single_plot(self.plotD,1)
    def _next1_button_fired(self):
        self.plotA = self._single_plot(self.plotA,2)
    def _next2_button_fired(self):
        self.plotB = self._single_plot(self.plotB,2)
    def _next3_button_fired(self):
        self.plotC = self._single_plot(self.plotC,2)
    def _next4_button_fired(self):
        self.plotD = self._single_plot(self.plotD,2)
    def _all_prev_button_fired(self):
        self._prev1_button_fired()
        self._prev2_button_fired()
        self._prev3_button_fired()
        self._prev4_button_fired()
    def _all_next_button_fired(self):
        self._next1_button_fired()
        self._next2_button_fired()
        self._next3_button_fired()
        self._next4_button_fired()


def mainPlotter():
    print "Running DataViewer.....\n"
    ImagePlot().configure_traits()

    return



mainPlotter()
