#!/usr/bin/env python
# plot_density.py

import argparse
import itertools
import matplotlib
import numpy
import os
import interpolate
import charge_density

#if "DISPLAY" not in os.environ:
#    matplotlib.use('Agg')
import matplotlib.pyplot as plt

__all__ = [
    "plot_density",
]      
                  
class plot_density:
    pass
    """Class to handle displaying of charge density data."""
    
    # Private vars
    _density = None
    _atoms = None

    # Set default variables
    _settings = dict(
        filename = 'CHGCAR',
        format = 'vasp',
        spin_channel = 'total',
        display = 'matplotlib',
        center_cartesian = [0.,0.,0.],
        xaxis = [1.,0.,0.],
        yaxis = [0.,0.,1.],
        xrepeat = 1, # approximate number of unit cells to interpolate
        yrepeat = 1, # approximate number of unit cells to interpolate
        xresolution = 500, # points to interpolate
        yresolution = 500, # points to interpolate
        xsize = 1, # Size of the plot in angstrom
        ysize = 1, # Size of the plot in angstrom
        xlabel = None,
        ylabel = None,
        contour_levels = 10
    )

    def __init__(self, **kwargs):
        self._settings.update(**kwargs)

    def _get(self, key):
        if key in self._settings:
            return self._settings[key]
        else:
            return None
        
    def get_settings(self):
       return self._settings.copy()
    
    def load(self, filename = None, format = None, spin_channel = None):
        if filename is None:
            filename = self._get('filename')
        if format is None:
            format = self._get('format')
        if spin_channel is None:
            spin_channel = self._get('spin_channel')

        # Load CHGCAR using ASE
        if format.lower() == 'vasp':
            with open(filename, 'r') as file:
                chgden = charge_density.charge_density.loadVaspCHGCAR(file)
                self._atoms = chgden.atoms
        elif format.lower() == 'abinit':
            chgden = charge_density.charge_density.loadAbinitDEN(filename)
        else:
            raise NotImplementedError('File using "%s" format not implemented' % format.lower())
        
        if spin_channel.lower() == 'total':
            self._density = chgden.get_charge_density()
        elif spin_channel.lower() == 'polarization':
            self._density = chgden.get_polarization_density()
        elif spin_channel.lower() == 'up':
            self._density = chgden.get_spinup_density()
        elif spin_channel.lower() == 'down':
            self._density = chgden.get_spindown_density()
        else:
            raise NotImplementedError('Spin channel "%s" is not implemented' % spin_channel.lower())
            
    # Determine the center atom reduced coordinates
    def _get_center(self):

        # Decide where to obtain center from
        # Cartisian option set
        if self._get('center_cartesian') is not None:

            # Convert from cartesian to reduced coordinates
            self._settings['center_reduced'] = numpy.linalg.solve(self._atoms.get_cell(),self._get('center_cartesian')).tolist()
            self._settings['center_cartesian'] = None

        # Atomic option is set
        if self._get('center_atom') is not None:

            # Convert from atom number to reduced coordinates
            self._settings['center_reduced'] = numpy.linalg.solve(self._atoms.get_cell(),self._atoms[self._get('center_atom')].position).tolist()
            self._settings['center_atom'] = None

        return self._get('center_reduced')

    # Determine the level spacing in contour plots
    def _get_levels(self, data = None):
        if data is None:
            data = self._density
            
        # Determine default contour levels from density data
        if self._get('contour_minimum') is None:
            self._settings['contour_minimum'] = numpy.min(data)
        if self._get('contour_maximum') is None:
            self._settings['contour_maximum'] = numpy.max(data)

        # Calculate contour spacing from min and max and spacing
        if self._get('contour_spacing') is None:
            self._settings['contour_spacing'] = (self._get('contour_maximum') - self._get('contour_minimum'))/(1.0*self._get('contour_levels'))

        # Return array of contour levels
        return numpy.arange(self._get('contour_minimum'), self._get('contour_maximum'), self._get('contour_spacing'))

    # Interpolation interface        
    def _interpolate(self):

        # Get parameters for interpolation
        center = self._get_center()
        plane = numpy.array([self._get('xaxis'),self._get('yaxis')],dtype=float)
        repeat = [self._get('xrepeat'),self._get('yrepeat')]
        res = map(int,[self._get('xresolution'),self._get('yresolution')])
    
        # Interpolate density data
        return interpolate.interpolate.interpolate_plane(self._density,self._atoms.get_cell(),plane=plane,center=center,dim=repeat,res=res)
    
    def _atoms_inplane(self):
        cs = interpolate.interpolate.plane_to_cs(numpy.array([self._get('xaxis'),self._get('yaxis')],dtype=float))
        positions = numpy.mod(self._atoms.positions - numpy.dot(self._get_center(),self._atoms.cell),self._atoms.cell.max(1))
        return numpy.dot(cs,positions.T).T
    
    # Decide which printing routine to use
    def display(self, view=None):
        if view is None:
            view = self._get('display')
        if view == 'TikZ':
            return self._display_TikZ_contour()
        elif view == 'matplotlib':
            return self._display_matplotlib()
        elif view == 'info':
            return self._display_info()
        else:
            raise NotImplementedError('display "%s" not implemented' % view)

    # Print a contour as a list of tikz "addplot" commands using the contour package
    def _display_TikZ_contour(self):
        addplot_text = '\\addplot[mesh,point meta=%f] coordinates {%s};'
        atom_text = '\\node[atom=%s,pin=%s] at (axis cs:%+f,%+f) {};'
        x,y,z = self._interpolate()
        levels = self._get_levels(z)
        C = plt.contour(x,y,z,levels)
        tikz = []
        # Loop over contour levels
        for collection, level in itertools.izip(C.collections, C.levels):
            # Loop over paths
            for path in collection._paths:
                string = ' '.join('(%f,%f)' % tuple(vertex) for vertex in path.vertices)
                tikz.append(addplot_text % (level,string))
        for atom,position in itertools.izip(self._atoms,self._atoms_inplane()):
            if abs(position[2]) < 1E-3:
                tikz.append(atom_text % (tuple([atom.symbol,atom.symbol]) + tuple(position[:2])))
        return "\n".join(tikz)
    
    # Decide how to plot matplotlib
    def _display_matplotlib(self):
        x,y,z = self._interpolate()
        levels = self._get_levels(z)
        plt.figure()
        plt.contour(x,y,z,levels)
        plt.xlim(-self._get('xsize')/2.,self._get('xsize')/2.)
        plt.ylim(-self._get('ysize')/2.,self._get('ysize')/2.)
        plt.axis('equal')
        plt.savefig(self._get('fileout'),dpi=self._get('outdpi'))
        plt.show()

    def _display_info(self):
        self._atoms.print_info()
        density_string = '  %15s :\t% f\t% f\t% f'
        print '\nDensity Information:'
        print '  density channel :\t minimum\t maximum\t total'
        data = self._density
        print density_string % (self._get('spin_channel'),data.min(),data.max(),data.sum())

    # Create command-line parser
    @staticmethod
    def build_parser():
        # Setup parser
        parser = argparse.ArgumentParser(prog='plot_density',description='Plot charge density file')

        # Add options
        parser.add_argument('filename',type=str,default='CHGCAR')
        parser.add_argument('-fmt','--format',choices=['vasp','abinit'],default='vasp')
        parser.add_argument('-s','--spin-channel',choices=['total','polarization','up','down'],default='total')
        parser.add_argument('-d','--display',choices=['raw','matplotlib','TikZ','none'],default='matplotlib')
    
        # Set default commands

        # Coordinate system options
        group_coord = parser.add_argument_group('coordinate system')
        group_coord.add_argument('-ca','--center-atom',nargs='?', type=int)
        group_coord.add_argument('-cc','--center-cartesian',nargs=3, type=float)
        group_coord.add_argument('-cr','--center-reduced',nargs=3, type=float, default=[0.,0.,0.])
        group_coord.add_argument('-xa','--x-axis',nargs=3, type=float, default=[1.,0.,0.])
        group_coord.add_argument('-ya','--y-axis',nargs=3, type=float, default=[0.,0.,1.])

        # Interpolation options
        group_interpolate = parser.add_argument_group('interpolation')
        group_interpolate.add_argument('-xrep','--x-repeat',nargs='?', type=int, default=1)
        group_interpolate.add_argument('-yrep','--y-repeat',nargs='?', type=int, default=1)
        group_interpolate.add_argument('-xres','--x-res',nargs='?', type=int, default=100)
        group_interpolate.add_argument('-yres','--y-res',nargs='?', type=int, default=100)

        # Plot options
        group_plot = parser.add_argument_group('plotting')
        group_plot.add_argument('-xs','--x-size',nargs='?', type=float, default=1)
        group_plot.add_argument('-ys','--y-size',nargs='?', type=float, default=1)
        group_plot.add_argument('-cmin','--contour-minimum', type=float)
        group_plot.add_argument('-cmax','--contour-maximum', type=float)
        group_plot.add_argument('-cl','--contour-levels', type=int, default=10)
        group_plot.add_argument('-cs','--contour-spacing', type=float)
        return parser

if __name__ == '__main__':
    # Parse input
    options = vars(plot_density.build_parser().parse_args())
    try:
        plotter = plot_density(**options)
        plotter.load()
        plotter.display()
    except Exception, e:
        print "Error:", e
