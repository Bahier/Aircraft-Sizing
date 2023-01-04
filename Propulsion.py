import numpy as np
import matplotlib.pyplot as plt
from referenceAircraft import *
from TestAircraft import *


def engineScaling(referencedict,l_e):
    """
    :param l_e: engine scaling factor
    :return: updated length
    """
    for key,value in referencedict.items():
        newvalue = value * l_e
        referencedict[key] = newvalue
    return

def thrustMCL(referenceMCL,pressure):
    print(referenceMCL * 4.4482216153)
    updateMCL = referenceMCL * 2
    zpMCL = updateMCL * pressure/23842
    return print(zpMCL * 4.4482216153)



