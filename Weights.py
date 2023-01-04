import TestAircraft as ta
import numpy as np


pax = 430
n_crew = 18
l_cabin_ref = 68.040
l_cockpit_ref = 4.34
VF_ref = 2300
l_cargo_ref = 40
l_cargo_cyl_ref = 30.035
V_cargo_ref = 300

l_cabin_proj = 62.247  #ENTER OWN CABIN LENGTH !!!!!
l_cockpit_proj = 4.34 # Constant
l_cargo_proj =  36.08 #ENTER OWN CARGO LENGTH !!!!!!


b = 80 * ta.testAircraft['l_ws']
s = 565 * ta.testAircraft['k_S']
tc = 0.12
print(b,s, tc)
phi = 31.5
Vd = 185.2    # dive speed 360kt = 185.2 m/s
rho_0 = 101325/(287.05 * 288.15)
qD = 0.5 * rho_0 * (Vd ** 2)

LF = 77.417 #PUT OWN VALUE
DF = 6.699 #PUT OWN VALUE
S_htp = 97.8 *0.857 #PUT OWN VALUE
S_vtp = 67.2 *0.857 #PUT OWN VALUE
l_e = ta.testAircraft['l_e']



def fuselageVolume(l_cabin_proj, l_cockpit_proj):
    """

    :param l_cabin_proj: cabin length of project aircraft in [m]
    :param l_cockpit_proj: cockpit length of project aircraft in [m]
    :return: pressurized fuselage volume of the project aircraft in [m^3]
    """
    VF = VF_ref * ((ta.testAircraft['l_fw'])**2) *(l_cabin_proj + l_cockpit_proj) / (l_cabin_ref + l_cockpit_ref)
    return VF

VF_proj = fuselageVolume(l_cabin_proj, l_cockpit_proj)

def cargoHold():
    l_cargo_proj = l_cargo_ref * (((l_cargo_ref - l_cargo_cyl_ref)/l_cargo_ref) * (((ta.testAircraft['l_fw'])**2) ** 0.5) + (l_cargo_cyl_ref/l_cargo_ref) * ta.testAircraft['l_fl_cyl'])

    return l_cargo_proj


def cargoVolume(l_cargo_proj):
    V_cargo_proj = V_cargo_ref * ((ta.testAircraft['l_fw'])**2) * (l_cargo_proj/l_cargo_ref)

    return V_cargo_proj
V_cargo_proj = cargoVolume(l_cargo_proj)


def weightWings(mtow, b, s, tc, phi):

    """
    :param mtow: maxi take-off weight in [kg]
    :param b: wing span in [m]
    :param s: wing area in [m^2]
    :param tc: thickness of wings in [m]
    :param phi: sweep angle in [°]
    :return: w1: weight of wings in [kg]
    """
    w1 = 0.0191 * (mtow**0.8) * (b**1.2) * (s**(-0.2)) * (tc ** -0.2) * np.cos(np.deg2rad(phi))**(-1)
    w1 = 0.0191 * mtow**0.8 * b**1.2 * s**-0.2 * tc **-0.2 * (1/np.cos(np.deg2rad(phi)))
    return w1

def weightFuselage(qD, mzfw, LF, DF):
    """
    :param qD:
    :param mzfw: maxi zero fuel weight in [kg]
    :param LF: length of fuselage in [m]
    :param DF: equivalent diameter in [m]
    :return: w2: load of fuselage in [kg]
    """

    w2 = 26.2 * ((qD/5000) ** 0.25) * ((mzfw/1000) ** 0.9) * (LF/DF) ** 0.7
    return w2

def weightHTP(S_htp):
    """
    :param S_htp: surface of horizontal tail plan in [m]
    :return: w3: weight of horizontal tail plan in [kg]
    """

    w3 = 27 * S_htp
    return w3

def weightVTP(S_vtp):
    """
    :param S_vtp: surface of vertical tail plan in [m]
    :return: w4: weight of vertical tail plan in [kg]
    """
    w4 = 29 * S_vtp
    return w4

def weightLandingGear(mtow, mlw):
    """
    :param mtow: maxi take-off weight in [kg]
    :param mlw: maxi landing weight in [kg]
    :return: w5: weight of landing gear in [kg]
    """

    w5 = 0.0353 * mtow + 0.018 * mlw
    return w5

def weightEngines_Pylons(l_e):
    """
    :param l_e: scaling factor for engines in unitless
    :return: w7: weight of engines in [kg]
    :return: w6: weight of pylons in [kg]
    """

    w7 = 26700 * l_e ** 2
    w6 = 0.135 * w7
    return w6, w7

w7 = weightEngines_Pylons(l_e)[1]
def weightSystems(VF_proj, b, s, mtow, LF, w7, pax):
    """

    :param VF: pressurized fuselage volume in [m^3]
    :param b: wing span in [m]
    :param s: wing area in [m^2]
    :param mtow: maxi take-off weight in [kg]
    :param LF: fuselage length in [m]
    :param w7: weight of engines in [kg]
    :param pax: number of passenger
    :return: w8_1: weight of air & anti-icing system in [kg]
             w8_2: weight of fuel system in [kg]
             w8_3: weight of hydraulics system in [kg]
             w8_4: weight of fire in [kg]
             w8_5: weight of flight controls system in [kg]
             w8_6: weight of navigation & communication system in [kg]
             w8_7: weight of electrical generation & distribution system in [kg]
             w8_8: weight of APU system in [kg]

    """

    w8_1 = 2 * VF_proj + b
    w8_2 = 2 * s
    w8_3 = 0.15 * mtow**0.7 + 5 * (LF + b)
    w8_4 = 0.005 * w7 + 0.1 * VF_proj
    w8_5 = 0.002 * mtow * (LF**0.1 + b**0.1)
    w8_6 = 900 + pax
    w8_7 = 0.4 * mtow**0.7 + 7 * LF
    w8_8 = 12 * (VF_proj ** 0.5)
    w8_tot= np.sum([w8_1, w8_2, w8_3, w8_4, w8_5, w8_6, w8_7, w8_8])

    return w8_1, w8_2, w8_3, w8_4, w8_5, w8_6, w8_7, w8_8, w8_tot

def weightFurnishings(l_cabin_proj, DF, n_crew, pax, V_cargo_proj, l_cargo_proj, b, VF, LF):
    """

    :param Lcab: cabin length in [m]
    :param DF: fuselage diameter in [m]
    :param n_crew: number of attendants in unitless
    :param pax: number of passengers in unitless
    :param Vcargo: volume of cargo in [m^3]
    :param Lcargo: cargo length in [m]
    :param b: wing span in [m]
    :param VF：pressurized fuselage volume in [m^3]
    :param LF：fuselage length in [m]
    :return: w9_1: weight for cockpit & cabin isolation - grounding lining - doors & panel - hatracks bins & bins in [kg]
             w9_2: weight for crew seats in [kg]
             w9_3: weight for toilet structure in [kg]
             w9_4: weight for cargo fixed structure, loading system in [kg]
             w9_5: weight for fixed oxygen in [kg]
             w9_6: weight for lighting in [kg]
             w9_7: weight for water installation in [kg]

    """
    w9_1 = 14 * l_cabin_proj * DF
    w9_2 = 25 * n_crew
    w9_3 = 2 * pax
    w9_4 = 15 * V_cargo_proj**0.67 + 15 * DF + 45 * l_cargo_proj
    w9_5 = 1.2 * VF**0.75
    w9_6 = 0.1 * LF * b + 0.7 * l_cabin_proj * DF
    w9_7 = 1.5 * l_cabin_proj * DF
    w9_tot = np.sum([w9_1, w9_2, w9_3, w9_4, w9_5, w9_6, w9_7])

    return w9_1, w9_2, w9_3, w9_4, w9_5, w9_6, w9_7, w9_tot

def weightOperatorItems(s, w7, pax, V_cargo_proj, n_crew):
    """

    :param s: wing area in [m^2]
    :param w7: engine weight in [kg]
    :param pax: number of passengers in unitless
    :param Vcargo: volume of cargo in [m^3]
    :param n_crew: number of attendants in unitless
    :return: w10_1: weight for unusable fuel, engine & APU oil in [kg]
             w10_2: weight for passenger seats, safety equipment, galley structure, crew equipment in [kg]
             w10_3: weight for empty LD3s & pallets in [kg]
             w10_4: weight for water, toilet fluid, catering in [kg]
             w10_5: weight for crew & crew rest in [kg]

    """

    w10_1 = s + 0.007 * w7
    w10_2 = 50 + 40.8 * pax
    w10_3 = 9 * V_cargo_proj
    w10_4 = 16 * pax
    w10_5 = 150 * n_crew
    w10_tot = np.sum([w10_1, w10_2, w10_3, w10_4, w10_5])
    return w10_1, w10_2, w10_3, w10_4, w10_5, w10_tot





"Loop"
mtow = 375000
mzfw = 265319.1489
mlw = 280872.3404

oldOWE =1
newOWE=9
difference = 100
while difference >= 0.02:
    oldOWE =newOWE
    W1 = weightWings(mtow,b,s,tc,phi)
    W2 = weightFuselage(qD,mzfw,LF,DF)
    W3 = weightHTP(S_htp)
    W4 = weightVTP(S_vtp)
    W5 = weightLandingGear(mtow, mlw)
    W6 = weightEngines_Pylons(l_e)[0]
    W7 = weightEngines_Pylons(l_e)[1]
    W8 = weightSystems(VF_proj,b,s,mtow,LF,W7,pax)[-1]
    W9 = weightFurnishings(l_cabin_proj,DF,n_crew,pax, V_cargo_proj, l_cargo_proj, b, VF_proj, LF)[-1]
    W10 = weightOperatorItems(s,W7, pax, V_cargo_proj, n_crew)[-1]
    newOWE = 1.04 * np.sum([W1, W2, W3, W4, W5, W6, W7, W8, W9 , W10])
    mzfw = newOWE + 1.45 *105 *pax
    mlw = 1.06 * mzfw
    difference = abs(((newOWE-oldOWE)/oldOWE)*100)
    print(newOWE, oldOWE,difference)

print(newOWE,mzfw, mlw)







print('fuselage volume:', fuselageVolume(l_cabin_proj, l_cockpit_proj))
print('cargo hold length:', cargoHold())
print('cargo volume:', cargoVolume(l_cargo_proj))
print('w1:', weightWings(mtow, b, s, tc, phi))
print('w2:',weightFuselage(qD, mzfw, LF, DF) )
print('w3:', weightHTP(S_htp))
print('w4:', weightVTP(S_vtp))
print('w5', weightLandingGear(mtow, mlw))
print('w6:',weightEngines_Pylons(l_e)[0])
print('w7:', weightEngines_Pylons(l_e)[1])
print('w8_1:', weightSystems(VF_proj, b, s, mtow, LF, w7, pax)[0])
print('w8_2:', weightSystems(VF_proj, b, s, mtow, LF, w7, pax)[1])
print('w8_3:', weightSystems(VF_proj, b, s, mtow, LF, w7, pax)[2])
print('w8_4:', weightSystems(VF_proj, b, s, mtow, LF, w7, pax)[3])
print('w8_5:', weightSystems(VF_proj, b, s, mtow, LF, w7, pax)[4])
print('w8_6:', weightSystems(VF_proj, b, s, mtow, LF, w7, pax)[5])
print('w8_7:', weightSystems(VF_proj, b, s, mtow, LF, w7, pax)[6])
print('w8_8:', weightSystems(VF_proj, b, s, mtow, LF, w7, pax)[7])
print('w9_1:', weightFurnishings(l_cabin_proj, DF, n_crew, pax, V_cargo_proj, l_cargo_proj, b, VF_proj, LF)[0])
print('w9_2:', weightFurnishings(l_cabin_proj, DF, n_crew, pax, V_cargo_proj, l_cargo_proj, b, VF_proj, LF)[1])
print('w9_3:', weightFurnishings(l_cabin_proj, DF, n_crew, pax, V_cargo_proj, l_cargo_proj, b, VF_proj, LF)[2])
print('w9_4:', weightFurnishings(l_cabin_proj, DF, n_crew, pax, V_cargo_proj, l_cargo_proj, b, VF_proj, LF)[3])
print('w9_5:', weightFurnishings(l_cabin_proj, DF, n_crew, pax, V_cargo_proj, l_cargo_proj, b, VF_proj, LF)[4])
print('w9_6:', weightFurnishings(l_cabin_proj, DF, n_crew, pax, V_cargo_proj, l_cargo_proj, b, VF_proj, LF)[5])
print('w9_7:', weightFurnishings(l_cabin_proj, DF, n_crew, pax, V_cargo_proj, l_cargo_proj, b, VF_proj, LF)[6])
print('w10_1:', weightOperatorItems(s, w7, pax, V_cargo_proj, n_crew)[0])
print('w10_2:', weightOperatorItems(s, w7, pax, V_cargo_proj, n_crew)[1])
print('w10_3:', weightOperatorItems(s, w7, pax, V_cargo_proj, n_crew)[2])
print('w10_4:', weightOperatorItems(s, w7, pax, V_cargo_proj, n_crew)[3])
print('w10_5:', weightOperatorItems(s, w7, pax, V_cargo_proj, n_crew)[4])