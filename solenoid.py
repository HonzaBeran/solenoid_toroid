import solveMagneticField as solB
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
    
class solenoid(object):
    ''' 
    Class for solenoid. It allows creat object solenoid, which have methods for count magnetic field, show magnetic field show how solenodi looks in coordinates system.
    '''
    def __init__(self, choose = "helix", N = 10, R = 1, l = 4, PARTS = 250, description = True):
        '''Arguments: choose = 'circle' or 'helix', N = number of threads, R = radius, l = length, parts = how many parts it be cut into, description = print description of argument of this. 
        Default option is: choose = 'helix', N = 10, R = 1, l = 4, PARTS = 250, descriptiion = True'''
        self.N = N
        self.R = R
        self.l = l
        self.parts = round(PARTS/N)
        self.PARTS = PARTS
        if "circle" == choose.lower():
            self.x, self.y, self.z, self.dx, self.dy, self.dz = self.solenoid_circle_to_parts()
        elif "helix" == choose.lower():
            self.x, self.y, self.z, self.dx, self.dy, self.dz = self.solenoid_helix_to_parts()
        else:
            print("Please creat object again with valid varibale - 'helix' or 'circle'.")
    
#    def description(self):
#        print("Solenoid have " + str(self.N) + " thread, " + str(self.l) + " length, ", self.parts, " part and radius ", self.R, ".")
        
    def creat_solenoid_circle(self):
        '''Creats solenoid from circles.'''
        zStart = -self.l/2
        zStop = self.l/2
        Zcoord = np.linspace(zStart, zStop, self.N)
        x = np.array([])
        y = np.array([])
        z = np.array([])
        for i in range(self.N):
            t = np.linspace(0, 2*np.pi, self.parts)
            x = np.append(x, self.R*np.cos(t))
            y = np.append(y, self.R*np.sin(t))
            z = np.append(z, Zcoord[i]*np.ones(self.parts))
        return x, y, z   
    
    def creat_solenoid_helix(self):
        '''Creats solenoid from circles.'''
        R = self.R
        parts = self.PARTS
        h = self.l/(self.N*2*np.pi)
        N = self.N
        startZ = -self.l/2 # Where helix start
        t = np.linspace(0, N*2*np.pi, parts)
        x = R*np.cos(t)
        y = R*np.sin(t)
        z = h*t + startZ
        return x, y, z
    
    def solenoid_circle_to_parts(self):
        '''Cuts circles to parts.'''
        dx = np.array([])
        dy = np.array([])
        dz = np.array([])
        newx = np.array([])
        newy = np.array([])
        newz = np.array([])
        x, y, z = self.creat_solenoid_circle()
        for i in range(len(x)-1):
            if z[i+1] == z[i]: # Last vector of circle can't connect with next circle 
                dx = np.append(dx, x[i+1]-x[i])
                dy = np.append(dy, y[i+1]-y[i])
                dz = np.append(dz, z[i+1]-z[i])
                # Oddělá poslední bod smyčky, aby měli x, y, z a dx, dy, dz stejné rozměry
                newx = np.append(newx, x[i]) 
                newy = np.append(newy, y[i])
                newz = np.append(newz, z[i])
        return newx, newy, newz, dx, dy, dz
    
    def solenoid_helix_to_parts(self):
        '''Cuts helix to parts.'''
        dx = np.array([])
        dy = np.array([])
        dz = np.array([])
        x, y, z = self.creat_solenoid_helix()
        for i in range(len(x)-1):
            dx = np.append(dx, x[i+1]-x[i])
            dy = np.append(dy, y[i+1]-y[i])
            dz = np.append(dz, z[i+1]-z[i])
        return x[:-1], y[:-1], z[:-1], dx, dy, dz
    
    def show_my_solenoid(self, save = ''):
        '''Show solenoid into coordinates system.
        If you want save image into png you write name of image as arument of this method.'''
        fig = plt.figure(figsize=(25, 10))
        
        ax = fig.add_subplot(1, 2, 1,projection='3d')
        ilim = - (self.R + self.R/10)
        flim = self.R + self.R/10
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
        if save == '':
            fig.savefig(save + '.png')
        plt.show()
        
    def magnetic_field_of_solenoid(self, X = False, Y = False, Z = False, I = 1, permeability = 1.256637062*10**(-6)):
        '''This function have on input points (X, Y, Z coordinates) where you want know magnetic field. 'I' is current and permeability is physical constant permeability.
        This function returns components of magnetic field  Bx, By, Bz.'''
        if isinstance(X, bool):
            X, Y, Z = solB.evaluation_space(-(self.R+self.R/15), (self.R+self.R/15), 7, -(self.l/2+self.l/2), (self.l/2+self.l/2), 7)
            Bx, By, Bz = solB.sol_magnetic_field(X, Y, Z, self.x, self.y, self.z, self.dx, self.dy, self.dz, I, permeability)
        else: 
            Bx, By, Bz = solB.sol_magnetic_field(X, Y, Z, self.x, self.y, self.z, self.dx, self.dy, self.dz, I, permeability)
        return X, Y, Z, Bx, By, Bz
    
    def show_magnetic_field(self, save = '', angles = [[], []], X = False, Y = False, Z = False, I = 1, permeability = 1.256637062*10**(-6)):
        '''angles = [[XYangle1, XYangle2, XYangle3, ...], [XZangle1, XZangle2, XZangle3, ...]], where first is in plane xy and second in plane xz.
        Attentation: This function creates graph of every first angle to every angles.'''
        if isinstance(X, bool) and I == 1 and permeability == 1.256637062*10**(-6):
            X, Y, Z, Bx, By, Bz = self.magnetic_field_of_solenoid()
        elif isinstance(X, bool):
            X, Y, Z, Bx, By, Bz = self.magnetic_field_of_solenoid(False, False, False, I, permeability)
        else:
            X, Y, Z, Bx, By, Bz = self.magnetic_field_of_solenoid(X, Y, Z, I, permeability)

        x = self.x
        y = self.y
        z = self.z
        dx = self.dx
        dy = self.dy
        dz = self.dz
        
        smaller = 8
        
        # For X  coordinate
        if max(X) <= self.R and max(Y) <= self.R:
            xyflim = (self.R + self.R/smaller)
        else:
            if max(X) >= max(Y):
                xyflim = max(X) + max(X)/smaller
            else:
                xyflim = max(Y) + max(Y)/smaller
        if abs(min(X)) <= self.R and abs(min(X)) <= self.R:
            xyilim = -(self.R + self.R/smaller)
        else:
            if abs(min(X)) >= abs(min(Y)):
                xyilim = -(abs(min(X)) + abs(max(X))/smaller)
            else:
                xyilim = -(abs(max(Y)) + abs(max(Y))/smaller)
                                 
        # For Z coordinate                 
        if max(Z) <= self.l/2:
            zflim = (self.l/2 + self.l/(smaller))
        else:
            zflim = max(Z) + max(Z)/(smaller)
        if abs(min(Z)) <= self.l/2:
            zilim = -(self.l/2 + self.l/(2*smaller))
        else:
            zilim = -(abs(min(Z)) + abs(min(Z))/smaller)
          
        
        tempVar = np.array([])
        for i in range(len(Bx)):
            tempVar = np.append(tempVar, solB.magnitude_3D(Bx[i], By[i], Bz[i]))
        mean = np.mean(tempVar)

                          
        lengthOfVec = 5*10**(-1)/(mean)
        
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
                    