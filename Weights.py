
import numpy as np
import matplotlib.pyplot as plt



def VF(VF_ref, l_fw, l_cabin, l_cockpit):





def weightWings(mtow, b, s, tc, phi):

    """
    :param mtow: maxi take-off weight in [kg]
    :param b: wing span in [m]
    :param s: wing area in [m^2]
    :param tc: thickness of wings in [m]
    :param phi: sweep angle in [°]
    :return: w1: weight of wings in [kg]
    """
    w1 = 0.0191 * mtow**0.8 * b**1.2 * s**(-0.2) * (tc ** -0.2) * (np.cos(phi))**(-1)
    return w1

def fuselageLoads(qD, mzfw, LF, DF):
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

    w5 = 0.0353 * mtow + 0.018 mlw
    return w5

def weightEngines(l_e):
    """
    :param l_e: scaling factor for engines in unitless
    :return: w7: weight of engines in [kg]
    """

    w7 = 26700 * l_e^2
    return w7

def weightPylons(w7):
    """

    :param w7: weight of engines in [kg]
    :return: w6: weight of pylons in [kg]
    """
    w6 = 0.135 * w7
    return w6

def weightSystems(VF, b, s, mtow, LF, w7, pax):
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
    w8_1 = 2 * VF + b
    w8_2 = 2 * s
    w8_3 = 0.15 * mtow**0.7 + 0.5 * (LF + b)
    w8_4 = 0.005 * w7 + 0.1 * VF
    w8_5 = 0.002 * mtow * (LF**0.1 + b**0.1)
    w8_6 = 900 + pax
    w8_7 = 0.4 * mtow**0.7 + 7 * LF
    W8_8 = 12 * (VF ** 0.5)

    return w8_1, w8_2, w8_3, w8_4, w8_5, w8_6, w8_7, w8_8

def weightFurnishings(Lcab, DF, n_crew, pax, Vcargo, Lcargo, b, VF, LF):
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
    w9_1 = 14 * Lcab * DF
    w9_2 = 25 * n_crew
    w9_3 = 2 * pax
    w9_4 = 15 * Vcargo**0.67 + 15 * DF + 45 * Lcargo
    w9_5 = 1.2 * VF**0.75
    W9_6 = 0.1 * LF * b + 0.7 * Lcargo * DF
    w9_7 = 1.5 * Lcab * DF

    return w9_1, w9_2, w9_3, w9_4, w9_5, w9_6, w9_7

def weightOperatorItems(s, w7, pax, Vcargo, n_crew):
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
    w10_3 = 9 * Vcargo
    w10_4 = 16 * pax
    w10_5 = 150 * n_crew

    return w10_1, w10_2, w10_3, w10_4, w10_5