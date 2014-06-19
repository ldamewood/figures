#!/usr/bin/env python

import numpy
import itertools

from pymatgen.core.lattice import Lattice
from pymatgen.core.structure import Structure
from crystal import fillcell, tikz_atoms

def SiMn_Isite():
    a = 5.43
    fcc = Lattice([[a/2,a/2,0],[a/2,0,a/2],[0,a/2,a/2]])
    isite = Structure(fcc,['Si']*2,[[0.00,0.00,0.00],[0.25,0.25,0.25]])
    
    # Make the cell cubic
    isite.make_supercell([[1,1,-1],[1,-1,1],[-1,1,1]])
    
    # Insert Mn atom
    isite.append('Mn',[0.50,0.50,0.50])

    return isite
    
def SiMn_Ssite():
    a = 5.43
    fcc = Lattice([[a/2,a/2,0],[a/2,0,a/2],[0,a/2,a/2]])
    ssite = Structure(fcc,['Si']*2,[[0.00,0.00,0.00],[0.25,0.25,0.25]])
    
    # Make the cell cubic
    ssite.make_supercell([[1,1,-1],[1,-1,1],[-1,1,1]])
    
    # Insert Mn atom
    Mnsite = numpy.array([0.25,0.25,0.25]);
    for i,atom in enumerate(ssite):
        if numpy.linalg.norm(atom.frac_coords-Mnsite) < 0.01:
            del ssite[i]
            ssite.append('Mn',Mnsite)

    return ssite

atoms = SiMn_Isite()
atoms_full = fillcell(atoms)
bondatoms = []
for sitei,sitej in itertools.combinations(atoms_full,2):
    radius = sitei.specie.atomic_radius + sitej.specie.atomic_radius
    bondlength = sitei.distance_from_point(sitej.coords)
    if bondlength <= 1.25 * radius:
        if sitei.specie.symbol != 'Mn' and sitej.specie.symbol != 'Mn':
            bondatoms.append((sitei,sitej))
            
tikz_atoms(atoms_full, bondatoms, drawcell = True)