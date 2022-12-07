import numpy as np
import matplotlib.pyplot as plt
"""
Altitude is 35000 ft
Cruise Speed in 0.85 Mach
Make a Cl/CD graph with Cl as the variable on the total drag equation
"""


def density(height):

    if height <= 11000:
        T= 288.16 -0.0065*height
    else:
        T= 273.15-56.5
    print(T-273.15)
    pressure = 101325 * (T/288.16)**(-9.80665/(-0.0065*287))
    rho = pressure/(287*T)
    return rho

def viscosity(height):
    """
    :param T: Temperature in Kelvin
    :return: Viscosity in Pa S
    """

    if height <= 11000:
        T= 288.16 -0.0065*height
    else:
        T= 273.15-56.5

    mu= (1.4537e-6 * T**(3/2))/(T+110.4)
    return mu

def reUnitLength(height, M , rho, mu):
    """
    :param rho: Density in kg/m^3
    :param V: Velocity in m/s
    :param mu: Viscosity in Pa S
    :return: reynoldnumber in unitless
    """
    if height <= 11000:
        T= 288.16 -0.0065*height
    else:
        T= 273.15-56.5
    a=np.sqrt(1.4*287*T)
    V=M*a
    Re=(rho*V)/mu
    return Re

def dragFriction(M, Re, Lref,Swet, Kf):
    """
    :param M: Machnumber in unitless [-]
    :param Re: Reynoldsnumber in [1/m]
    :param Lref: array of reference length per part in [m]
    :return: total frictiondrag coefficient value
    """
    Cd = []
    for i in range(len(Lref)):
        Cdi = ((0.455)/( (1 + 0.126 * M**2) * np.log10(Re*Lref[i])**2.58 ) *Swet[i]* Kf[i])/565
        Cd.append(Cdi)
    return sum(Cd)

def dragInduced(AReff,Cl):
    Cdind= (1.17*Cl**2) /(np.pi * AReff)
    return Cdind

def dragParasitic():
    Cdpara = 10e-4
    return Cdpara

def dragInstallation():
    Cdinstall = 2e-4
    return Cdinstall

def dragCompressibility(Cl):
    Cdcomp = 0.8 * Cl**11.5
    return Cdcomp


# """CL/CD vs CL"""
#
# Lref = [9.178, 5.3, 83.210, 53.800, 11.7, 6.6, 4.975, 6.608]
# Kf = [1.5, 1.1, 1.3, 1.1, 1.1, 1.1, 1.5, 1.5]
# Swet= [918, 34, 1334, 211, 28, 178, 164, 130]
#
# height=35000*0.3048
# rho = density(height)
# mu = viscosity(height)
# Re = reUnitLength(height, 0.85, rho, mu)
# Cl= np.arange(0,1.1,0.025)
#
# Cd=[]
# for i in Cl:
#     Cdi = dragFriction(0.85, Re, Lref, Swet, Kf) + dragInduced(11.33,i) + dragParasitic() + dragInstallation() + dragCompressibility(i)
#     Cd.append(Cdi)
#
# # print(totaldrag)
#
# CloverCd=np.array(Cl)/np.array(Cd)
# plt.plot(Cl,CloverCd)
# plt.plot(Cl,Cd)
# plt.show()
# print(max(CloverCd))
#
#
# """Height VS Friction Drag"""
# altitude = np.arange(0,11000,1000)
# Lref = [9.178, 5.3, 83.210, 53.800, 11.7, 6.6, 4.975, 6.608]
# Kf = [1.5, 1.1, 1.3, 1.1, 1.1, 1.1, 1.5, 1.5]
# Swet= [918, 34, 1334, 211, 28, 178, 164, 130]
#
# Cdp=[]
# for height in altitude:
#     rho = density(height)
#     mu = viscosity(height)
#     Re = reUnitLength(height, 0.85, rho, mu)
#     Cdf = dragFriction(0.85, Re, Lref, Swet, Kf)
#     Cdp.append(Cdf)
#
# plt.plot(altitude, Cdp)
# plt.show()