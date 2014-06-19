#!/usr/bin/env python

import numpy
import itertools

from pymatgen.core.lattice import Lattice
from pymatgen.core.operations import SymmOp
from pymatgen.core.structure import Structure
from crystal import fillcell, tikz_atoms

def Si512Mn():
    a = 5.43
    fcc = Lattice([[a/2,a/2,0],[a/2,0,a/2],[0,a/2,a/2]])
    supercell = Structure(fcc,['Si']*2,[[0.00,0.00,0.00],[0.25,0.25,0.25]])
    
    # Make the cell cubic
    supercell.make_supercell([[1,1,-1],[1,-1,1],[-1,1,1]])
    supercell.make_supercell([4,4,4])
    
    # Insert Mn atom
    Mnsite = numpy.array([0.50,0.50,0.50])
    for i,atom in enumerate(supercell):
        if numpy.linalg.norm(atom.frac_coords - Mnsite) < 0.01:
            supercell.translate_sites([i],[1./8,1./8,1./8])
            supercell.append('Mn',[0.50,0.50,0.50])
            break

    return supercell

atoms = Si512Mn()
atoms_full = fillcell(atoms)
bondatoms = []
snsite = numpy.array([0.625,0.625,0.625])
for sitei,sitej in itertools.combinations(atoms_full,2):
    radius = sitei.specie.atomic_radius + sitej.specie.atomic_radius
    bondlength = sitei.distance_from_point(sitej.coords)
    if bondlength <= 1.25 * radius:
        if numpy.linalg.norm(sitei.frac_coords-snsite) > 0.01 and numpy.linalg.norm(sitej.frac_coords-snsite) > 0.01:
            bondatoms.append((sitei,sitej))
            
tikz = tikz_atoms(atoms_full, bondatoms, drawcell = False)