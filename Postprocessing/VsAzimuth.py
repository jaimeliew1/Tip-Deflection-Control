# -*- coding: utf-8 -*-
"""
A module which performs analysis on a certain aspect of the tip deflection
controller results.

This script analyses: Vs Azimuth

@author: Jaime Liew
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc


def run(dlc, ref_dlc, c, SAVE=None):

    wsp=16; keyroot='TD'; ylabel='Tip Deflection [m]'
    keys = [keyroot + str(x) for x in [1,2,3]]
    channels = {'Azim': 2, 'TD1': 49, 'TD2' : 52, 'TD3': 55}
    # get ref sim data
    ref = ref_dlc(yaw=0, wsp=wsp)[0]
    for i, seed in enumerate(ref):
        data = seed.loadFromSel(channels)
        if i == 0:
            refx = data.Azim
            refy = data[['TD1', 'TD2', 'TD3']].as_matrix()
        refx = np.append(refx, data.Azim)
        refy = np.append(refy, data[['TD1', 'TD2', 'TD3']].as_matrix(), 0)

     # get sim data to plot
    sim = dlc(yaw=0, wsp=wsp, controller=c)[0]
    for i, seed in enumerate(sim):
        data = seed.loadFromSel(channels)
        if i == 0:
            x = data.Azim
            y = data[['TD1', 'TD2', 'TD3']].as_matrix()
        x = np.append(x, data.Azim)
        y = np.append(y, data[['TD1', 'TD2', 'TD3']].as_matrix(), 0)

    # Set up plot
    fig, ax = plt.subplots(3, 2, sharey=True, figsize=[7, 6])
    fig.subplots_adjust(bottom=0.09, wspace=0.05, hspace=0.05)

    extent = [0, 360, min(refy.min(), y.min()), max(refy.max(), y.max())]
    hexbinConfig = {'gridsize':30, 'extent':extent, 'linewidths':1}
    if SAVE:
        hexbinConfig['linewidths'] = 0.25
    ax[0,0].set_title('Without IPC')
    ax[2,0].set_xlabel('Azimuth Angle [deg]')

    ax[0,1].set_title('With IPC')
    ax[2,1].set_xlabel('Azimuth Angle [deg]')

    ax[1, 0].set_ylabel(ylabel)
    for i in [0,1,2]:
        ax[i, 1].set_ylabel('Blade ' + str(i+1))
        ax[i, 1].yaxis.set_label_position("right")
        ax[i, 0].set_xticks([]); ax[i, 1].set_xticks([])

    # Plotting
    for i in [0,1,2]: # for each blade
        ax[i, 0].hexbin(refx, refy[:, i], cmap='inferno', **hexbinConfig)
        ax[i, 1].hexbin(x, y[:,i], cmap='inferno',** hexbinConfig)
        ax[i,0].autoscale()
        ax[i,1].autoscale()

    # post set up
    ax[2,0].set_xticks([0, 120, 240, 360])
    ax[2,1].set_xticks([120, 240, 360])
    #ax[0,0].axvline(x=45, c='w', ls='--', lw=1)

    if SAVE:
        plt.savefig('../Figures/{}/{}_TDvsAzim.png'.format(c, c), dpi=200)

    plt.show(); print()



if __name__ is '__main__':
    dlc_noipc = PostProc.DLC('dlc11_0')
    dlc = PostProc.DLC('dlc11_1')


    run(dlc, dlc_noipc, 'ipc04', SAVE=False)