import numpy
import itertools

def celledges(lattice):
    tol = 1E-3
    edges = []
    for i,j in itertools.combinations(itertools.product([0,1], repeat=3),2):
        if abs(numpy.linalg.norm(numpy.array(i)-numpy.array(j)) - 1.0) > tol:
            continue
        edges.append((numpy.dot(lattice.matrix,i),numpy.dot(lattice.matrix,j)))
    return edges

def tikz_atoms(atoms, bonds = [], drawcell = False):
    output = []
    pos = []
    tikz = []
    atom_tikz = "\\addatom at site (%+5.3f,%+5.3f,%+5.3f) {%s};"
    bond_tikz = "\\addbond from (%+5.3f,%+5.3f,%+5.3f) {%s} to (%+5.3f,%+5.3f,%+5.3f) {%s};"
    edge_tikz = "\\addedge from (%+5.3f,%+5.3f,%+5.3f) to (%+5.3f,%+5.3f,%+5.3f);"
    edges = celledges(atoms.lattice)
    for atom in atoms:
        pos.append(atom.coords)
        tikz.append(atom_tikz % (tuple(atom.coords)+tuple((atom.specie.symbol,))))
    if drawcell == True:
        for edge1,edge2 in edges:
            pos.append(0.5*(edge1 + edge2))
    	    tikz.append(edge_tikz % tuple(tuple(edge1)+tuple(edge2)))
    for sitei,sitej in bonds:
        pos.append(0.5*(sitei.coords+sitej.coords))
        tikz.append(bond_tikz % (tuple(sitei.coords)+(sitei.specie.symbol,)+tuple(sitej.coords)+(sitej.specie.symbol,)))
    pos = numpy.round(numpy.array(pos),3)
    idx = numpy.lexsort((pos[:,0],pos[:,2],-pos[:,1]))
    #idx = numpy.lexsort((pos[:,0],pos[:,1],pos[:,2]))
    for i in idx:
        output.append(tikz[i])
    return output
            
def fillcell(atoms):
    tol = 1E-3
    newAtoms = atoms.copy()
    
    for atom in atoms:
        if numpy.abs(atom.frac_coords[0]) < tol:
            newAtoms.append(atom.specie.symbol,atom.frac_coords+numpy.array([1,0,0]))
            if numpy.abs(atom.frac_coords[1]) < tol:
                newAtoms.append(atom.specie.symbol,atom.frac_coords+numpy.array([1,1,0]))
                if numpy.abs(atom.frac_coords[2]) < tol:
                    newAtoms.append(atom.specie.symbol,atom.frac_coords+numpy.array([1,1,1]))
            if numpy.abs(atom.frac_coords[2]) < tol:
                newAtoms.append(atom.specie.symbol,atom.frac_coords+numpy.array([1,0,1]))
        if numpy.abs(atom.frac_coords[1]) < tol:
            newAtoms.append(atom.specie.symbol,atom.frac_coords+numpy.array([0,1,0]))
            if numpy.abs(atom.frac_coords[2]) < tol:
                newAtoms.append(atom.specie.symbol,atom.frac_coords+numpy.array([0,1,1]))
        if numpy.abs(atom.frac_coords[2]) < tol:
            newAtoms.append(atom.specie.symbol,atom.frac_coords+numpy.array([0,0,1]))
        
        if numpy.abs(atom.frac_coords[0]-1) < tol:
            newAtoms.append(atom.specie.symbol,atom.frac_coords-numpy.array([1,0,0]))
            if numpy.abs(atom.frac_coords[1]-1) < tol:
                newAtoms.append(atom.specie.symbol,atom.frac_coords-numpy.array([1,1,0]))
                if numpy.abs(atom.frac_coords[2]-1) < tol:
                    newAtoms.append(atom.specie.symbol,atom.frac_coords-numpy.array([1,1,1]))
            if numpy.abs(atom.frac_coords[2]-1) < tol:
                newAtoms.append(atom.specie.symbol,atom.frac_coords-numpy.array([1,0,1]))
        if numpy.abs(atom.frac_coords[1]-1) < tol:
            newAtoms.append(atom.specie.symbol,atom.frac_coords-numpy.array([0,1,0]))
            if numpy.abs(atom.frac_coords[2]-1) < tol:
                newAtoms.append(atom.specie.symbol,atom.frac_coords-numpy.array([0,1,1]))
        if numpy.abs(atom.frac_coords[2]-1) < tol:
            newAtoms.append(atom.specie.symbol,atom.frac_coords-numpy.array([0,0,1]))
    
    return newAtoms