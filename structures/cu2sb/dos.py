#!/usr/bin/env python
import numpy
import pandas as pd
import itertools

file1 = "/Users/liam/Work/cu2sb/DOSCAR_Li3MnAs2_Li0"

with open(file1) as f:
    lines = f.readlines()

n = 1001
lim = map(float,lines[5].split())
emin = lim[1]
emax = lim[0]
efermi = lim[3]

spins = ["up", "dn"]
atoms = ["As1", "As2", "Li1", "Li2", "Li3", "Mn"]
lms = ["s", "px", "pz", "py", "dxy", "dyz", "dz2", "dxz", "dx2"]

dostot = numpy.array([map(float,line.split()) for line in lines[6:6+n]])
dostot[:,0] = dostot[:,0] - efermi
dos = pd.DataFrame({'energy': dostot[:,0]})
dos['total.up'] = dostot[:,1]
dos['total.dn'] = dostot[:,2]
for iatom,atom in enumerate(atoms):
    dospar = numpy.array([map(float,line.split()) for line in lines[7+iatom+n*(iatom+1):7+iatom+n*(iatom+2)]])
    for i,(lm,spin) in enumerate(itertools.product(lms, spins)):
        column = atom + "." + lm + "." + spin
        dos[column] = dospar[:,i+1]
        print str(i+1) + " " + column
        
dos.to_csv('li3mnas2_li0_pdos.csv')

file1 = "/Users/liam/Work/cu2sb/DOSCAR_Li3MnAs2_Li3"

with open(file1) as f:
    lines = f.readlines()

n = 1001
lim = map(float,lines[5].split())
emin = lim[1]
emax = lim[0]
efermi = lim[3]

spins = ["up", "dn"]
atoms = ["As1", "As2", "Li1", "Li2", "Li3", "Mn"]
lms = ["s", "px", "pz", "py", "dxy", "dyz", "dz2", "dxz", "dx2"]

dostot = numpy.array([map(float,line.split()) for line in lines[6:6+n]])
dostot[:,0] = dostot[:,0] - efermi
dos = pd.DataFrame({'energy': dostot[:,0]})
dos['total.up'] = dostot[:,1]
dos['total.dn'] = dostot[:,2]
for iatom,atom in enumerate(atoms):
    dospar = numpy.array([map(float,line.split()) for line in lines[7+iatom+n*(iatom+1):7+iatom+n*(iatom+2)]])
    for i,(lm,spin) in enumerate(itertools.product(lms, spins)):
        column = atom + "." + lm + "." + spin
        dos[column] = dospar[:,i+1]
        print str(i+1) + " " + column
        
dos.to_csv('li3mnas2_li3_pdos.csv')
