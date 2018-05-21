# -*- coding: utf-8 -*-
"""
Calculates the lifetime equivalent load for simulation data which has
simulation for each wind speed over a range wsp_range = [4, 26]
@author: Jaime Liew
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import Analysis, PostProc
from Configuration import Config
#from matplotlib import patches
import math


def run(dlc, dlc_noipc, SAVE=False):
    c =  'ipcpi'
    keys = ['RBMf', 'RBMe', 'MBt', 'MBy']
    labels = ['Blade (flapwise)', 'Blade (edgewise)', 'Main Bearing (tilt)', 'Main Bearing (yaw)']
    N = len(keys)
    Req_l = []
    Req_l_ref = []
    for key in keys:
        Req_l_ref.append(lifetimeReq(dlc_noipc(yaw=0), key))
        Req_l.append(lifetimeReq(dlc(yaw=0, controller=c), key))
    print(Req_l_ref)
    print(Req_l)

    # make a bargraph
    width = 0.35
    ind = np.arange(N)
    fig, ax = plt.subplots()
    ax.grid(zorder=0)
    ax.set_title('Lifetime Equivalent Load')
    ax.set_ylabel('Moment [kNm]')
    ax.bar(ind, Req_l_ref, width, zorder=3, label='No IPC')
    ax.bar(ind + width, Req_l, width, zorder=3, label=c.upper())
    ax.set_xticks(ind)
    ax.set_xticklabels(labels, rotation = 30)
    ax.legend()

    if SAVE:
        plt.savefig('../Figures/{}/{}_Lifetime_Req.png'.format(c, c), dpi=200)

    plt.show(); print()




def wsp_probs(Class=1, dx=2, Range= [4, 26.1]):
    # Weibull Parameters
    k = 2
    if Class == 1:
        A = 10/math.gamma(1+1/k)
    elif Class == 2:
        A = 8.5/math.gamma(1+1/k)
    elif Class == 3:
        A = 7.5/math.gamma(1+1/k)

    # Weibull cdf function
    cdf = lambda x: 1 - np.exp(-(x/A)**k)
    #Discrete wind speeds
    Y = np.arange(Range[0], Range[1], dx)

    # Probabilities of each wind speed
    P = [cdf(y+dx/2) - cdf(y-dx/2) for y in Y]

    return dict(zip(Y, P))

def lifetimeReq(sims_, key='RBM'):
    #wohler = Config.Config.wohler[key]
    wohler = {'RBMf':10, 'RBMe':10, 'RBMt':10, 'MBt':4, 'MBy':4}
    # Probability of each wind speed occuring
    P = wsp_probs()
    Y = 0
    for sim in sims_:
        wsp = sim.wsp
        Y += float(sim.data[key]**wohler[key]*P[wsp])

    Req_l = Y**(1/wohler[key])

    return Req_l

def fullDatasetGen(dlc):
    # A generator function that yields lists of Simulation objects of a set.
    # Each set has the same controller and gain parameters (yaw = 0),
    # and contains simulations for the full range of windspeeds from 4 to 26 m/s.
    # Additionally, there is no shutdown in any of the simulations.
    wsp_range = range(4, 27, 2)

    param_combs = dlc.unique(['controller', 'Kp'])
    for i, (c, g) in enumerate(param_combs):
        sims_ = dlc(controller=c, Kp=g, yaw=0)

        # skip simulation sets without fill range of wind speeds.
        if not all(x.wsp in wsp_range for x in sims_):
            continue
        # skip simulation sets with shutdown
        if any(x.shutdown for x in sims_):
            continue
        yield sims_

if __name__ is '__main__':

    dlc_noipc = PostProc.DLC('dlc11_0')
    dlc_noipc.analysis()

    dlc = PostProc.DLC('dlc11_1')
    dlc.analysis()

    run(dlc, dlc_noipc, SAVE=False)






