#!/usr/bin/env python

import numpy
import sys

def dos_from_file(filename):
    lines = open(filename).readlines()[:15]
    dimline = lines[3].split(',')
    try:
        nsppol = int(dimline[0].split()[-1])
    except:
        nsppol = 1
    #nkpt = int(dimline[1].split()[-1])
    #nband = int(dimline[2].split()[-1])
    efermi = float(lines[7].split()[-1])
    #nene = int(lines[10].split()[2])
    #elo = float(lines[11].split()[2])
    #ehi = float(lines[11].split()[4])
    dos = numpy.loadtxt(filename)
    n = dos.shape[0]
    dos = dos.reshape(nsppol,n/nsppol,3)
    x = dos[0,:,0]
    return x-efermi,dos[:,:,1]
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        x,dos = dos_from_file(sys.argv[1])
        z = numpy.logical_and(x > -0.1,x < 0.1)
        for spin in range(2):
            print ('\\addplot coordinates{')
            for e,d in zip(x[z],dos[:,z].T):
                print('(%f,%f)' % (e*27.2,d[spin]/27.2))
            print ('} \\closedcycle;')