#!/usr/bin/env python
from __future__ import print_function

import urllib2
import re

from pymatgen.core.periodic_table import PeriodicTable


#pattern = r'elemParams[%d]  = ['%s','%s','%s']'
#'\definecolor{atom-H}{rgb}{1.000000,1.000000,1.000000}'

def atoms_style_jmol():
    url = 'http://jmol.sourceforge.net/jscolors/jmol_constants.js'
    js = urllib2.urlopen(url)
    lines = js.readlines()
    for line in lines:
        r = re.search("elemParams\[(\d+)\].*?=.*?\['(.*?)','(.*?)','(.*?)'\]",line)
        if r:
            val1 = int('0x' + r.group(3)[0:2],0)/255.
            val2 = int('0x' + r.group(3)[2:4],0)/255.
            val3 = int('0x' + r.group(3)[4:6],0)/255.
            print('\\definecolor{atom-%s}{%f,%f,%f}' % (r.group(2),val1,val2,val3))
    print('\\definecolor{atom-%s}{%f,%f,%f}' % ('X',0.,0.,0.))
    
def atoms_style_bytype():
    pt = PeriodicTable()
    for element in pt.all_elements:
        if element.is_noble_gas:
            print('\\colorlet{atom-%s}{green!50}' % element.symbol)
        elif element.is_transition_metal:
            print('\\colorlet{atom-%s}{blue!50}' % element.symbol)
        elif element.is_metalloid:
            print('\\colorlet{atom-%s}{yellow!50}' % element.symbol)
        elif element.is_alkali:
            print('\\colorlet{atom-%s}{orange!50}' % element.symbol)
        elif element.is_alkaline:
            print('\\colorlet{atom-%s}{purple!50}' % element.symbol)
        elif element.is_lanthanoid:
            print('\\colorlet{atom-%s}{brown!50}' % element.symbol)
        elif element.is_actinoid:
            print('\\colorlet{atom-%s}{brown!50}' % element.symbol)
        else:
            print('\\colorlet{atom-%s}{red!50}' % element.symbol)
    print('\\colorlet{atom-X}{black}')