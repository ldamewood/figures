#!/usr/bin/env python

import numpy
import itertools

from pymatgen.core.lattice import Lattice
from pymatgen.core.operations import SymmOp
from pymatgen.core.structure import Structure
from crystal import fillcell, tikz_atoms

def cluster_Mn4():
    a = 5.43
    c = a/2*7/4
    bcc = Lattice([[a/2,a/2,-c/2],[a/2,-a/2,c/2],[-a/2,a/2,c/2]])
    cluster = Structure(bcc,['Mn']*2,[[0.00,0.00,0.00],[1./2,1./4,3./4]])
    
    # Make the orthogonal cubic
    cluster.make_supercell([[1,1,0],[1,0,1],[0,1,1]])
    
    return cluster

def cluster_Si4():
    a = 5.43
    c = a/2
    fcc = Lattice([[a/2,a/2,0],[a/2,0,c/2],[0,a/2,c/2]])
    cluster = Structure(fcc,['Si'],[[0.25,0.25,0.25]])
    
    cluster.make_supercell([[1,1,-1],[1,-1,1],[-1,1,1]])
    
    return cluster

def cluster_full():
    cluster_Mn = cluster_Mn4()
    cluster_Mn.make_supercell([1,1,4])
    cluster_Si = cluster_Si4()
    cluster_Si.make_supercell([1,1,7])
    cluster_full = cluster_Mn.copy()
    for site in cluster_Si:
        cluster_full._sites.append(site)
    return cluster_full

atoms = cluster_full()
atoms_full = fillcell(atoms)
bondatoms = []
for sitei,sitej in itertools.combinations(atoms_full,2):
    radius = sitei.specie.atomic_radius + sitej.specie.atomic_radius
    bondlength = sitei.distance_from_point(sitej.coords)
    if bondlength <= 1.25 * radius:
        bondatoms.append((sitei,sitej))
            
tikz = tikz_atoms(atoms_full, bondatoms, drawcell = True)