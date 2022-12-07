import numpy as np
import matplotlib.pyplot as plt
from Aerodynamics import *

"""CL/CD vs CL"""

Lref = [9.178, 5.3, 83.210, 53.800, 11.7, 6.6, 4.975, 6.608]
Kf = [1.5, 1.1, 1.3, 1.1, 1.1, 1.1, 1.5, 1.5]
Swet= [918, 34, 1334, 211, 28, 178, 164, 130]

height=35000*0.3048
rho = density(height)
mu = viscosity(height)
Re = reUnitLength(height, 0.85, rho, mu)
Cl= np.arange(0,1.1,0.025)

Cd=[]
for i in Cl:
    Cdi = dragFriction(0.85, Re, Lref, Swet, Kf) + dragInduced(11.33,i) + dragParasitic() + dragInstallation() + dragCompressibility(i)
    Cd.append(Cdi)

# print(totaldrag)

CloverCd=np.array(Cl)/np.array(Cd)
plt.plot(Cl,CloverCd)
plt.plot(Cl,Cd)
plt.show()
print(max(CloverCd))


"""Height VS Friction Drag"""
altitude = np.arange(0,11000,1000)
Lref = [9.178, 5.3, 83.210, 53.800, 11.7, 6.6, 4.975, 6.608]
Kf = [1.5, 1.1, 1.3, 1.1, 1.1, 1.1, 1.5, 1.5]
Swet= [918, 34, 1334, 211, 28, 178, 164, 130]

Cdp=[]
for height in altitude:
    rho = density(height)
    mu = viscosity(height)
    Re = reUnitLength(height, 0.85, rho, mu)
    Cdf = dragFriction(0.85, Re, Lref, Swet, Kf)
    Cdp.append(Cdf)

plt.plot(altitude, Cdp)
plt.show()