import numpy as np

def magnitude_3D(x, y, z):
    return np.sqrt(x**2 + y**2 + z**2)
     
def meshgrid_to_one(X):
    newX = np.array([])
    for i in range(len(X)):
        for j in range(len(X[i])):
            newX = np.append(newX, X[i])
    return newX

def evaluation_space(xyMax, xyMin, xyPoints, zMax, zMin, zPoints):
    X = np.linspace(xyMin, xyMax, xyPoints)
    Y = np.linspace(xyMin, xyMax, xyPoints)
    Z = np.linspace(zMin, zMax, zPoints)
    X, Y, Z = np.meshgrid(X, Y, Z)
    X = meshgrid_to_one(X)
    Y = meshgrid_to_one(Y)
    Z = meshgrid_to_one(Z)
    return X, Y, Z

def evaluation_space_inside_solenoid(xyMax, xyMin, xyPoints, zMax, zMin, zPoints, R):
    X = np.linspace(xyMin, xyMax, xyPoints)
    Y = np.sqrt(R**2 - X**2)
    Z = np.linspace(zMin, zMax, zPoints)
    X, Y, Z = np.meshgrid(X, Y, Z)
    X = meshgrid_to_one(X)
    Y = meshgrid_to_one(Y)
    Z = meshgrid_to_one(Z)
    return X, Y, Z

def sol_magnetic_field(X, Y, Z, x, y, z, dx, dy, dz, I, permeability):
    '''Function for solve magnetic field, where X, Y, Z are components of vector where you want know magnetic field 
    and x, y, z are components of vector, where is source of current and dx, dy, dz is components of vector of parts and "I" is current.
    This function return components of magnetic field Bx, By, Bz.'''
    SolX = np.array([])
    SolY = np.array([])
    SolZ = np.array([])
    for k in range(len(X)):
        # Presolution - solution without constants 
        preSolX = np.array([])
        preSolY = np.array([])
        preSolZ = np.array([])
        for i in range(len(dx)):
            DeltaX = X[k] - x[i]
            DeltaY = Y[k] - y[i]
            DeltaZ = Z[k] - z[i]
            D = magnitude_3D(DeltaX, DeltaY, DeltaZ)
            preSolX = np.append(preSolX, (dy[i]*DeltaZ - dz[i]*DeltaY)/D)
            preSolY = np.append(preSolY, (dz[i]*DeltaX - dx[i]*DeltaZ)/D)
            preSolZ = np.append(preSolZ, (dx[i]*DeltaY - dy[i]*DeltaZ)/D)
        # Solution magnetic field
        SolX = np.append(SolX, I*permeability/4*np.pi*np.sum(preSolX))
        SolY = np.append(SolY, I*permeability/4*np.pi*np.sum(preSolY))
        SolZ = np.append(SolZ, I*permeability/4*np.pi*np.sum(preSolZ))
    return SolX, SolY, SolZ
 

