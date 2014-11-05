#!/usr/bin/env python

from pymatgen.core.periodic_table import all_symbols, Element
import urllib

def get_nist_data(element):
    url = "http://physics.nist.gov/cgi-bin/Elements/elInfo.pl?element=%d&context=text"
    lines = urllib.urlopen(url % element.Z).read().split('\n')
    data = {}
    for line in lines:
        if "Atomic Weight" in line:
            print line.split()[2]
    
    

for symbol in all_symbols():
	element = Element(symbol)
	print element.Z
	print element.symbol
	print element.name
	print element.atomic_mass
	print element.data['Electronic structure']
        
