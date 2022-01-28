import solveMagneticField as solB
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
    
class toroid(object):
    ''' 
    Class for solenoid. It allows creat object solenoid, which have methods for count magnetic field, shows magnetic field and shows how solenodi looks in coordinates system.
    '''
    def __init__(self, N = 20, R = 1, l = 4, PARTS = 300):
        '''Arguments: N = number of threads, R = minor radius of toroid, l = major radius of toroid, parts = how many parts it be cut into, description = print description of argument of this function.
        Default option is: N = 20, R = 1, l = 4, PARTS = 300 '''
        self.N = N
        self.R = R
        self.l = l
        self.PARTS = PARTS
        self.x, self.y, self.z, self.dx, self.dy, self.dz = self.toroid_to_parts()
    
#    def description(self):
#        print("Solenoid have " + str(self.N) + " thread, " + str(self.l) + " length, ", self.parts, " part and radius ", self.R, ".")
        
    def creat_toroid(self):
        '''Creating toroid.'''
        t = np.linspace(0, 2*np.pi, 200)
        x=(self.l+self.R*np.sin(self.N*t))*np.cos(t)
        y=(self.l+self.R*np.sin(self.N*t))*np.sin(t)
        z=self.R*np.cos(self.N*t)
        return x, y, z
    
    
    def toroid_to_parts(self):
        '''Cuts toroid to parts.'''
        x, y, z = self.creat_toroid()
        dx = np.array([])
        dy = np.array([])
        dz = np.array([])
        for i in range(len(x)-1):
            dx = np.append(dx, x[i+1]-x[i])
            dy = np.append(dy, y[i+1]-y[i])
            dz = np.append(dz, z[i+1]-z[i])
        return x[:-1], y[:-1], z[:-1], dx, dy, dz
    
    def show_my_toroid(self):
        '''Show solenoid into coordinates system.
        If you want save image into png you write name of image as arument of this method.'''
        fig = plt.figure(figsize=(25, 10))
        
        ax = fig.add_subplot(1, 2, 1,projection='3d')
        ilim = - (self.l + self.l/10)
        flim = self.l + self.l/10
        zilim = - (self.l/2 + self.l/10)
        zflim = self.l/2 + self.l/10
        plt.xlabel('X')
        plt.ylabel('Y')
        ax.set_xlim(ilim, flim)
        ax.set_ylim(ilim, flim)
        ax.set_zlim(zilim, zflim)
        ax.quiver(self.x, self.y, self.z, self.dx, self.dy, self.dz, length=0.8)

        ax = fig.add_subplot(1, 2, 2, projection='3d')
        plt.xlabel('X')
        plt.ylabel('Y')
        ax.set_xlim(ilim, flim)
        ax.set_ylim(ilim, flim)
        ax.set_zlim(zilim, zflim)
        ax.scatter(self.x, self.y, self.z)

        plt.show()
        
    def magnetic_field_of_toroid(self, X = False, Y = False, Z = False, I = 1, permeability = 1.256637062*10**(-6)):
        '''This function have on input points (X, Y, Z coordinates) where you want know magnetic field. 'I' is current and permeability is physical constant permeability.
        This function returns components of magnetic field  Bx, By, Bz.'''
        if isinstance(X, bool):
            X, Y, Z = solB.evaluation_space(-(self.l+self.l/15), (self.l+self.l/15), 7, -(self.l/2+self.l/2), (self.l/2+self.l/2), 7)
            Bx, By, Bz = solB.sol_magnetic_field(X, Y, Z, self.x, self.y, self.z, self.dx, self.dy, self.dz, I, permeability)
        else: 
            Bx, By, Bz = solB.sol_magnetic_field(X, Y, Z, self.x, self.y, self.z, self.dx, self.dy, self.dz, I, permeability)
        return X, Y, Z, Bx, By, Bz
    
    def show_magnetic_field(self, save = '', angles = [[], []], X = False, Y = False, Z = False, I = 1, permeability = 1.256637062*10**(-6)):
        '''angles = [[XYangle1, XYangle2, XYangle3, ...], [XZangle1, XZangle2, XZangle3, ...]], where first is in plane xy and second in plane xz.'''
        if isinstance(X, bool) and I == 1 and permeability == 1.256637062*10**(-6):
            X, Y, Z, Bx, By, Bz = self.magnetic_field_of_toroid()
        elif isinstance(X, bool):
            X, Y, Z, Bx, By, Bz = self.magnetic_field_of_toroid(False, False, False, I, permeability)
        else:
            X, Y, Z, Bx, By, Bz = self.magnetic_field_of_toroid(X, Y, Z, I, permeability)

        x = self.x
        y = self.y
        z = self.z
        dx = self.dx
        dy = self.dy
        dz = self.dz
        
        smaller = 1000
        
        #Redefine R for total radius (major + 2xminor radius)
        R = self.R*2 + self.l
        # For X  coordinate
        if max(X) <= R and max(Y) <= R:
            xyflim = (R + R/smaller)
        else:
            if max(X) >= max(Y):
                xyflim = max(X) + max(X)/smaller
            else:
                xyflim = max(Y) + max(Y)/smaller
        if abs(min(X)) <= R and abs(min(X)) <= R:
            xyilim = -(R + R/smaller)
        else:
            if abs(min(X)) >= abs(min(Y)):
                xyilim = -(abs(min(X)) + abs(max(X))/smaller)
            else:
                xyilim = -(abs(max(Y)) + abs(max(Y))/smaller)
                                 
        # For Z coordinate                 
        if max(Z) <= self.R:
            zflim = (self.R + self.R/(smaller))
        else:
            zflim = max(Z) + max(Z)/(smaller)
        if abs(min(Z)) <= self.R:
            zilim = -(self.R + self.R(2*smaller))
        else:
            zilim = -(abs(min(Z)) + abs(min(Z))/smaller)
                
                          
        tempVar = np.array([])
        for i in range(len(Bx)):
            tempVar = np.append(tempVar, solB.magnitude_3D(Bx[i], By[i], Bz[i]))
        mean = np.mean(tempVar)
            
        lengthOfVec = 5*10**(-1)/mean
        
        if angles == [[], []]:
            fig = plt.figure(figsize=(30, 10))
            
            ax = fig.add_subplot(1, 2, 1,projection='3d')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.view_init(30, 30)
            ax.set_xlim(xyilim, xyflim)
            ax.set_ylim(xyilim, xyflim)
            ax.set_zlim(zilim, zflim)
            ax.quiver(X, Y, Z, Bx, By, Bz, length=lengthOfVec)
            ax.quiver(x, y, z, dx, dy, dz, length=0.9, color='red')
            
            ax = fig.add_subplot(1, 2, 2,projection='3d')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.view_init(60, 60)
            ax.set_xlim(xyilim, xyflim)
            ax.set_ylim(xyilim, xyflim)
            ax.set_zlim(zilim, zflim)
            ax.quiver(X, Y, Z, Bx, By, Bz, length=lengthOfVec)
            ax.quiver(x, y, z, dx, dy, dz, length=0.9, color='red')
            fig.savefig(save + '.png')
            plt.show()
            
        else:
            for i in angles[0]:
                for j in angles[1]:
                    fig = plt.figure(figsize=(25, 18))
                    ax = fig.gca(projection='3d')
                    ax.set_xlabel('X')
                    ax.set_ylabel('Y')
                    ax.set_zlabel('Z')
                    ax.view_init(i, j)
                    ax.set_xlim(xyilim, xyflim)
                    ax.set_ylim(xyilim, xyflim)
                    ax.set_zlim(zilim, zflim)
                    ax.quiver(X, Y, Z, Bx, By, Bz, length=lengthOfVec)
                    ax.quiver(x, y, z, dx, dy, dz, length=0.9, color='red')
                    if save != '':
                        fig.savefig(save + str(i) + str(j) + '.png')
                    plt.show()