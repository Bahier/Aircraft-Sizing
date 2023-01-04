import numpy as np
#import pandas as pd
from pandas import read_csv
from scipy import version as scipyv
from scipy.interpolate import interp1d,UnivariateSpline,RectBivariateSpline
from math import *
import sys

min_numpy= '1.11.3'
min_pandas= '0.19.2'
min_scipy= '0.18.1'

if np.__version__ < min_numpy:
    print("min numpy version is {}".format(min_numpy))
    sys.exit(1)

if scipyv.version < min_scipy:
    print("min scipy version is {}".format(min_scipy))
    sys.exit(1)

def standard_temperature(zp):
    """ Standard temperature law below 50 km
    """
    if (zp<=11000.):
        Tstd = 288.15-0.0065*zp 
        Tstd_p = -0.0065 
    elif (zp<=20000.):
        Tstd = 216.65 
        Tstd_p = 0. 
    elif (zp<=32000.):
        Tstd = 216.65+0.001*(zp-20000.) 
        Tstd_p = 0.001 
    elif (zp<=47000.):
        Tstd = 228.65+0.0028*(zp-32000.) 
        Tstd_p = 0.0028 
    elif (zp<=50000.):
        Tstd = 270.65 
        Tstd_p = 0. 
    else:
        raise Exception('Altitude beyond 50 km in standard_temperature')
    return Tstd


def sound_velocity(Tamb):
    """ sound velocity
    """
    return 20.047*(Tamb**0.5) 




def phase(name, start_weight, fuel_burn, time, distance_nm):
    return {
        'name' : name,
        'start_weight' : round(start_weight, 0),
        'end_weight' : round(start_weight - fuel_burn, 0),
        'fuel_burn' : round(fuel_burn, 0),
        'time' : round(time, 1),
        'distance' : round(distance_nm, 0)
    }


def ratio_phase(name, last_phase, fuel_ratio, time, distance):
    fuel = (1 - fuel_ratio) * last_phase['end_weight']
    return phase(name, last_phase['end_weight'], fuel, time, distance)



def create_SAR_func(SAR, Vz, Vzmin):

    altitude_opt = np.zeros(len(SAR['Weights']))
    SAR_opt = np.zeros(len(SAR['Weights']))
    
    for i,mass in enumerate(SAR['Weights']):
        SAR_vs_alt =  UnivariateSpline(SAR['Altitudes'], SAR['data'][i,:],  k=4, s=0)
        try:
            altitude_opt[i] = SAR_vs_alt.derivative().roots()[0]
        except IndexError: # this is to cover cases when at very high weight (and undersized a/c) the max SAR cannot be found (would be lower than 15000)
            altitude_opt[i] = 0
        SAR_opt[i] = SAR_vs_alt(altitude_opt[i])
    
    SAR_func = {
        'SAR_surface' : RectBivariateSpline(SAR['Weights'], SAR['Altitudes'], SAR['data']),
        'altitude_opt' : altitude_opt,
        'SAR_opt' : SAR_opt
    }
    
    Vzmin = Vzmin* 0.3048 / 60 # convert in m/s
    altitudes_ceiling = np.zeros(len(Vz['Weights']))
    
    for i,mass in enumerate(Vz['Weights']):
        vz_vs_alt =  UnivariateSpline(Vz['Altitudes'], Vz['data'][i,:] - Vzmin,  k=3, s=0)
        altitudes_ceiling[i] = vz_vs_alt.roots()[0]
    
    Vz_func = {
        'ceiling' : altitudes_ceiling
    }
    
    return SAR_func, Vz_func



def cruise(last_phase, SAR, Vz, cruise_range_NM, mission_input):
    

    SAR_func, Vz_func = create_SAR_func(SAR, Vz, mission_input['Vzmin'])
    
    cruise_range = cruise_range_NM * 1852
    disa = mission_input['disa']
    crz_alt = np.arange(15000, 55000, 2000)
    N = len(crz_alt)
    init_weight = last_phase['end_weight']
    end_weight = np.zeros(N)
    start_weight = np.zeros(N)
    delta_weight = np.zeros(N)
    USAR = np.zeros(N)
    distance = np.zeros(N)
    time = np.zeros(N)
    
    for i,altitude in enumerate(crz_alt):
        Vtas = mission_input['cruise_mach'] * sound_velocity(standard_temperature(altitude*0.3048) + disa)
        mass_opt =  interp1d(SAR_func['altitude_opt'], SAR['Weights'], fill_value='extrapolate')(altitude + 1000)
        mass_ceil = interp1d(Vz_func['ceiling'], Vz['Weights'], fill_value='extrapolate')(altitude + 2000)
        end_weight[i] = max(min(mass_opt, mass_ceil), 1)
        USAR[i] = end_weight[i] * SAR_func['SAR_surface'](end_weight[i], altitude) # USAR in m
        if i>0:
            USAR_avg = 0
            if end_weight[i-1] != end_weight[i]:    
                ratio = min(max((init_weight-end_weight[i])/(end_weight[i-1]-end_weight[i]), 0), 1)
            else:
                ratio = 0
            if ratio>0:
                USAR_avg = (USAR[i] + ratio*(USAR[i-1]-USAR[i]) + USAR[i]) / 2 
            if init_weight>end_weight[i-1]:
                start_weight[i] = end_weight[i-1]
            elif init_weight>end_weight[i]:
                start_weight[i] = init_weight
            d = USAR_avg * log(start_weight[i]/end_weight[i])  if start_weight[i]!=0  else  0
            distance[i] = distance[i-1] + d
            time[i] = time[i-1] + d / Vtas
            
            if i>1 and init_weight>end_weight[i-1]:
                delta_weight[i-1] = init_weight - start_weight[i]
            if i==N-1:
                delta_weight[i] = init_weight

    final_weight = init_weight - interp1d(distance, delta_weight, fill_value='extrapolate')(cruise_range)
    cruise_time = interp1d(distance, time, fill_value='extrapolate')(cruise_range) / 60
    
    return phase('cruise', init_weight, init_weight-final_weight, cruise_time, cruise_range/1852)




def mission(SAR, Vz, TOW, total_range, mission_input):
    '''SAR is a dict containing 3 keys: 
        'data' a 2D array of SAR (in m/kg) for a range of weights (x) and altitudes (y) (see description for more info)
        'Weights' a 1D array giving the list of weights (in kg) used in the SAR table
        'Altitudes' a 1D array giving the list of altitudes (in ft) used in the SAR table
       Vz is a dict similar to SAR, containing 3 keys: 
        'data' a 2D array of Vz (in m/s) for a range of weights (x) and altitudes (y) (see description for more info)
        'Weights' a 1D array giving the list of weights (in kg) used in the Vz table
        'Altitudes' a 1D array giving the list of altitudes (in ft) used in the Vz table
       TOW in kg
       total_range: range of the mission in NM
       mission_input: dict (see description)'''
    
    SAR_func, Vz_func = create_SAR_func(SAR, Vz, mission_input['Vzmin'])
    
    mission_out = {}
    phases = []
    
    phases.append(phase('taxi-out', TOW+mission_input['taxi-out']['FB'], mission_input['taxi-out']['FB'],\
                        mission_input['taxi-out']['time']/60, mission_input['taxi-out']['dist']))
    phases.append(phase('take-off', phases[-1]['end_weight'], mission_input['take-off']['FB'], \
                            mission_input['take-off']['time']/60, mission_input['take-off']['dist']))
    phases.append(ratio_phase('climb', phases[-1], mission_input['climb']['weight_ratio'], \
                              mission_input['climb']['time']/60, mission_input['climb']['dist']))
    phases.append(cruise(phases[-1], SAR, Vz, total_range - 200, mission_input))
    phases.append(ratio_phase('descent', phases[-1], mission_input['descent']['weight_ratio'], \
                              mission_input['descent']['time']/60, mission_input['descent']['dist']))
    phases.append(ratio_phase('landing', phases[-1], mission_input['landing']['weight_ratio'], \
                              mission_input['landing']['time']/60, mission_input['landing']['dist']))
    phases.append(phase('taxi-in', phases[-1]['end_weight'], mission_input['taxi-in']['FB'], \
                            mission_input['taxi-in']['time']/60, mission_input['taxi-in']['dist']))
    
    block_fuel = sum([p['fuel_burn'] for p in phases])
    block_time = sum([p['time'] for p in phases]) / 60
    
    
    # reserves
    
    rte_rsv = mission_input['route_reserve']['pct']/100. * block_fuel
    fuel_holding = mission_input['holding_reserve']['FB']
    phases.append(phase('route reserve%', phases[-1]['end_weight'], rte_rsv, 0, 0))
    phases.append(phase('reserves diversion', phases[-1]['end_weight'], \
                        mission_input['diversion']['holding_ratio']*mission_input['holding_reserve']['FB'],\
                        0, mission_input['diversion']['dist']))
    phases.append(phase('reserves holding', phases[-1]['end_weight'], mission_input['holding_reserve']['FB'],\
                        mission_input['holding_reserve']['time']/60, 0))
    
    reserves = rte_rsv + (mission_input['diversion']['holding_ratio'] + 1)*mission_input['holding_reserve']['FB']
    
    
    fuel_to_board = block_fuel + reserves
    ZFW = phases[-1]['end_weight']
    
    mission_out['phases'] = phases
    mission_out['block_fuel'] = block_fuel
    mission_out['block_time'] = block_time
    mission_out['reserves'] = reserves
    mission_out['fuel_to_board'] = fuel_to_board
    mission_out['ZFW'] = ZFW

    return mission_out
