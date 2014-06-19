#!/usr/bin/env python

import numpy
import itertools

from pymatgen.core.lattice import Lattice
from pymatgen.core.operations import SymmOp
from pymatgen.core.structure import Structure
from crystal import fillcell, tikz_atoms

def dfh(single = True, defect = False):
    if defect:
        single = False
    a = 5.43
    fcc = Lattice([[a/2,a/2,0],[a/2,0,a/2],[0,a/2,a/2]])
    dfh = Structure(fcc,['Si']*2,[[0.00,0.00,0.00],[0.25,0.25,0.25]])
    
    # Make the orthogonal cubic
    dfh.make_supercell([[0,0,1],[1,-1,0],[1,1,-1]])
    
    # Rotate the cell
    rt = 0.70710678118654746
    symmop = SymmOp.from_rotation_and_translation([[0,rt,rt],[0,rt,-rt],[1,0,0]])
    dfh.apply_operation(symmop)
    
    # Make supercell
    if single == True:
        dfh.make_supercell([1,1,8])
    else:
        dfh.make_supercell([2,2,8])
    
    # Insert Mn atoms
    for i,atom in enumerate(dfh):
        if abs(atom.frac_coords[2] - 0.5) < 0.01 and atom.specie.symbol == 'Si':
            dfh.append('Mn',atom.frac_coords)
            del dfh[i]
    
    # Do defects
    if defect == 1:
        defectMn = numpy.array([0,0,0.5])
        for i,atom in enumerate(dfh):
            if numpy.linalg.norm(atom.frac_coords - defectMn) < 0.01 and atom.specie.symbol == 'Mn':
                dfh.append('Si',defectMn)
                del dfh[i]
    if defect == 2:
        defectMn = numpy.array([0.5,0.5,0.5])
        for i,atom in enumerate(dfh):
            if numpy.linalg.norm(atom.frac_coords - defectMn) < 0.01 and atom.specie.symbol == 'Mn':
                del dfh[i]
    if defect == 3:
        defectMn = numpy.array([0.5,0.25,0.5-1./32])
        for i,atom in enumerate(dfh):
            if numpy.linalg.norm(atom.frac_coords - defectMn) < 0.01 and atom.specie.symbol == 'Si':
                dfh.append('Mn',defectMn)
                del dfh[i]

    return dfh

atoms = dfh(single = True)
atoms_full = fillcell(atoms)
bondatoms = []
snsite = numpy.array([0.625,0.625,0.625])
for sitei,sitej in itertools.combinations(atoms_full,2):
    radius = sitei.specie.atomic_radius + sitej.specie.atomic_radius
    bondlength = sitei.distance_from_point(sitej.coords)
    if bondlength <= 1.25 * radius:
        bondatoms.append((sitei,sitej))
            
tikz = tikz_atoms(atoms_full, bondatoms, drawcell = True)