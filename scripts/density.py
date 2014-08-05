#!/usr/bin/env python

from __future__ import print_function

import numpy
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import interpolate
import itertools

import cut3d

def TikZ_contour(x,y,z,levels = 20):
    # Create plot
    fig = plt.figure()
    C = plt.contour(x,y,z,levels)
    plt.axis('image')
    plt.axis([x.min(),x.max(),y.min(),y.max()])
    plt.colorbar()
    plt.show()
    
    addplot_text = '\\addplot[mesh,point meta=%f] coordinates {%s};'
    
    tikz = []
    # Loop over contour levels
    for collection, level in itertools.izip(C.collections, C.levels):
        # Loop over paths
        for path in collection._paths:
            string = ' '.join('(%f,%f)' % tuple(vertex) for vertex in path.vertices)
            tikz.append(addplot_text % (level,string))
    return "\n".join(tikz)

path = '/Users/liam/Work/tikz_figures/structures/limnsi'

DEN_file1 = os.path.join(path,'MnSi_opt_DEN')
DEN_file2 = os.path.join(path,'beta_LiMnSi_opt_DEN')

data1 = cut3d.getden(DEN_file1)
data2 = cut3d.getden(DEN_file2)

acell = 5.778 / 0.529177249
primd = acell*numpy.array([[0.5,0.5,0],[0.5,0,0.5],[0,0.5,0.5]])
datadiff = data2 - data1
dendiff = datadiff[:,:,:,0]

[x,y,z] = interpolate.interpolate.interpolate_plane(dendiff,primd,dim=[1.25,1.25],center=[0.5,0.5,0.5],plane=[[1.,1.,0.],[0.,0.,1.]])

tikz = TikZ_contour(x,y,z,levels = numpy.linspace(-0.01,0.01,21))