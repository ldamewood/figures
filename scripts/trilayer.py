#!/usr/bin/env python

import numpy
import itertools

from pymatgen.core.lattice import Lattice
from pymatgen.core.operations import SymmOp
from pymatgen.core.structure import Structure
from crystal import fillcell, tikz_atoms

def trilayer(doped = None):
    a = 5.43
    fcc = Lattice([[a/2,a/2,0],[a/2,0,a/2],[0,a/2,a/2]])
    trilayer = Structure(fcc,['Si']*2,[[0.00,0.00,0.00],[0.25,0.25,0.25]])
    
    # Make the cell cubic
    trilayer.make_supercell([[1,1,-1],[1,-1,1],[-1,1,1]])
    trilayer.make_supercell([[1,1,0],[1,-1,0],[0,0,4]])
    # Rotate the cell
    rt = 0.70710678118654746
    symmop = SymmOp.from_rotation_and_translation([[rt,rt,0],[rt,-rt,0],[0,0,1]])
    trilayer.apply_operation(symmop)
    
    if doped is not None:
        frac_coords = numpy.array([0.5,0.0,0.5])
        for i,atom in enumerate(trilayer):
            if numpy.linalg.norm(atom.frac_coords-frac_coords) < 0.001:
                trilayer.replace(i,doped,frac_coords)


    for z in [0.375,0.625]:
        for xy in [0.00,0.50]:
            trilayer.append('Mn',[xy,xy,z])

    return trilayer

atoms = trilayer(doped=None)
atoms_full = fillcell(atoms)

bondatoms = []
for sitei,sitej in itertools.combinations(atoms_full,2):
    radius = sitei.specie.atomic_radius + sitej.specie.atomic_radius
    bondlength = sitei.distance_from_point(sitej.coords)
    if bondlength <= 1.25 * radius:
        if sitei.specie.symbol != 'Mn' and sitej.specie.symbol != 'Mn':
            bondatoms.append((sitei,sitej))
            
tikz_atoms(atoms_full, bondatoms, drawcell = True)