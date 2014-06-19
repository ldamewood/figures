#!/usr/bin/env python
from __future__ import print_function


from pymatgen.core.periodic_table import PeriodicTable

pt = PeriodicTable()

atom_string = '/unitcell/atom-style-%s/.style={minimum size=%f\\@atom@scale},'

print('\\tikzset{')
for element in pt:
    try:
        radius = float(element.data['Atomic radius calculated'])
        print('    ' + atom_string % (element,radius))
    except:
        pass
print('}')