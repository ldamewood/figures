import numpy

__all__ = [
    "interpolate",
]

class interpolate:
    # Convert two vectors into a normalzied coordinate system via GS orthogonalization
    @staticmethod
    def plane_to_cs(cs):
        # Normalize vectors
        cs[0] = cs[0]/numpy.linalg.norm(cs[0])
        cs[1] = cs[1]/numpy.linalg.norm(cs[1])
        # Orthogonalize second vector to first
        cs[1] = cs[1] - cs[0] * numpy.dot(cs[0],cs[1])
        # Return array with third vector orthogonal to other two
        return numpy.vstack([cs,numpy.cross(cs[0],cs[1])])

    # Genreate a grid on a 2d plane in 3d space
    @staticmethod
    def grid_intersection(plane, res, dim):
        # Create grid
        x, y, z = numpy.mgrid[0:res[0],0:res[1],0.:1.]
        # Center grid
        x -= numpy.floor(res[0]/2); y -= numpy.floor(res[1]/2)
        # Scale grid
        x *= 1.*dim[0]/res[0]
        y *= 1.*dim[1]/res[1]
        # List of points in the grid
        element = numpy.array([x.flatten(),y.flatten(),z.flatten()])
        # Generate coordinate system
        cs = interpolate.plane_to_cs(plane)
        # Rotate points to plane cs
        return x,y,numpy.dot(element.T,cs)

    # Linearlly interpolate 3d periodic data on a plane grid
    @staticmethod
    def interpolate_plane(datain, cell=[[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]],
                          plane = [[1.,0.,0.],[0.,0.,1.]], center = [0.5,0.5,0.5],
                          dim = [1.,1.], res = [100.,100.]):
        # Convert to numpy
        cell = numpy.array(cell)
        center = numpy.array(center)
        plane = numpy.array(plane)
        datain = numpy.array(datain)
        # Define the cell size
        boxsize = max(sum(abs(cell)))
        # Generate grid in Cartesian coordinates
        x,y,elements = interpolate.grid_intersection(plane,res,dim)
        # Scale the coordinates to the size of the box
        x *= boxsize; y *= boxsize; elements *= boxsize
        # Rotate points to primitive cell coordinates
        rr = numpy.linalg.solve(cell.T,elements.T)
        # Add the center point to all elements
        rr += numpy.array([center]).T.repeat(rr.shape[1],1)
        # Interpolate the density on the plane
        dataout = numpy.reshape(interpolate.pinterpn(datain,rr.T),res)
        # Return x,y,z data
        return x[:,:,0],y[:,:,0],dataout
    
    # Interpolate regularly spaced periodic nd data at an arbitrary point.
    @staticmethod
    def pinterpn(datain, rr):
        # Grid dimensions. e.g. [100,100,100]
        grid = datain.shape
        # Number of grid dimensions. e.g. 3
        dim = len(grid)
        # Number of points to interpolate. e.g. rr is 100x3
        nelem = rr.shape[0]
        # Dimension of points should agree with grid dimension. 
        assert rr.shape[1] == dim
        # Force rr to be between 0 and 1
        rr = numpy.mod(numpy.mod(rr, 1) + 1, 1)
        
        # allocate space for the results
        data = numpy.zeros((nelem, 1),dtype=datain.dtype);
    
        # dimmatrix is a nelem list of the grid dimentions.
        # Ex: [[100,100,100],
        #      [100,100,100],
        #      ...
        #      [100,100,100]]
        dimmatrix = numpy.tile(grid, (nelem, 1))
    
        # ir and pr are zero-indexed integers that define two opposite corners of an
        # n-dimensional box with density points defined at all of the corners given
        # by datain. First, scale rr points to the size of the grid and then round
        # to smallest integer to define the "lower corner".
        ir = numpy.fix(numpy.dot(rr, numpy.diag(grid)))
        # Find the "higher corner" by adding 1 to each lower corner and then wrapping
        # the edges back to zero
        pr = numpy.mod(ir + 1, dimmatrix)
        # Check if any upper corners are on the boundary,
        idx = (pr == dimmatrix)
        # and wrap the boundary points back to zero.
        pr[idx] =- dimmatrix[idx]
        # xr is a vector from the lower corner of a box to the position of
        # the interpolation point.
        xr = numpy.dot(rr, numpy.diag(grid)) - ir
        
        # Iterator over the 2^d corners of each box
        corners = range(2 ** dim)
        
        # Iterator over the dimensions of the space
        dims = range(dim)
        
        # Distance to nearest edge in each dimension. Initialize to zero
        r = dim * [0]
        
        # Lower and upper corners
        ir = numpy.array([ir, pr])
        # Distance weight factors on lower and upper corners
        xr = numpy.array([1 - xr, xr])
        
        # Loop over each position
        for j in range(nelem):
            # Initialize density value to zero
            denval = 0
            # Loop over each corner
            # Add up the contribution from each corner weighted 
            # by the distance to that corner
            for corner in corners:
                x = 1
                # loop over each dimension
                for dim in dims:
    
                    # determine if this corner is low or high,
                    lohi = corner % 2
                    # and remove last bit.
                    corner /= 2
                    
                    # distance weight factor
                    x *= xr[lohi, j, dim]
                    
                    # nearest edge
                    r[dim] = ir[lohi, j, dim]
    
                denval += x * datain[tuple(r)]
            data[j] = denval
        return data