# -*- coding: utf-8 -*-
"""
@author: Jaime Liew
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc

def get_TD_azim_from_sim(sim):
    channels = {'Azim': 2,
                'RBM1': 26, 'RBM2': 29, 'RBM3': 32,
                'TD1' : 49, 'TD2' : 52, 'TD3' : 55}
    for i, seed in enumerate(sim):
        data = seed.loadFromSel(channels)
        if i == 0:
            azim = data.Azim
            td = -data[['TD1', 'TD2', 'TD3']].values
        azim = np.append(azim, data.Azim)
        td = np.append(td, -data[['TD1', 'TD2', 'TD3']].values, 0)

        td -= np.reshape(td.mean(1), [-1, 1])
    return azim, td



def run(dlcs, wsp=20, SAVE=None):

    # normal shear
    azim1, td1 = [], []
    # get data for Ar = 0
    sim = dlcs['dlc11_0'](wsp=wsp)[0]
    azim1, td1 = get_TD_azim_from_sim(sim)




    # inverse shear
    azim2, td2 = [], []
    # get data for Ar = 0
    sim = dlcs['dlc15_0'](wsp=wsp)[0]
    azim2, td2 = get_TD_azim_from_sim(sim)


    # Set up plot
    fig, axes = plt.subplots(1, 2, sharey=True, sharex=True, figsize=[5, 3])
    fig.subplots_adjust( wspace=0.05, hspace=0.05)
    axes[0].set_ylim(-6, 6)
    axes[0].set_xticks([0, 120, 240])
    axes[0].set_yticks(np.arange(-4, 6, 2))
    axes[0].set_xlim(0, 360)

    hexbinConfig = {'gridsize':30,
                    #'extent':extent,
                    'linewidths':0.25,
                    'mincnt':1,
                    'vmin':0,
                    'vmax':2000}
    if SAVE:
        hexbinConfig['linewidths'] = 0.25

    # labels
    fig.text(0.45, 0.0, 'Azimuth Angle [deg]', ha='center', rotation='horizontal')
    fig.text(0.05, 0.5, 'Tip Deflection [m]', va='center', rotation='vertical')

    hexPlot = axes[0].hexbin(azim1, td1[:, 0], cmap='Blues', **hexbinConfig)
    axes[0].annotate('Normal shear' , xy=(0.5, 0.01),
                xycoords='axes fraction', size=10, ha='center', va='bottom',
                bbox=dict(ec='w', fc='w', alpha=0.0))

    hexPlot = axes[1].hexbin(azim2, td2[:, 0], cmap='Blues', **hexbinConfig)
    axes[1].annotate('Inverse shear' , xy=(0.5, 0.01),
                xycoords='axes fraction', size=10, ha='center', va='bottom',
                bbox=dict(ec='w', fc='w', alpha=0.0))


    N = len(azim1)
    cb = fig.colorbar(hexPlot, ax=axes.ravel().tolist(), pad=0.02)
    cb.set_ticks(np.linspace(0, 2000, 6)) #based on vmin and vmax
    ticklabels = ['{:1.1f}%'.format(x*100) for x in np.linspace(0/N, 2000/N, 6)]
    ticklabels[-1] = '$>$' + ticklabels[-1]
    cb.set_ticklabels(ticklabels)
    cb.ax.tick_params(labelsize=8)
    cb.set_label('Probability of Occurences', labelpad=0)

    axes[0].axvline(180, lw=1, ls='--', c='k')
    axes[1].axvline(180, lw=1, ls='--', c='k')
    axes[0].text(185, 0, 'blade downwards', rotation=90, va='center', size=8)
    axes[1].text(185, 0, 'blade downwards', rotation=90, va='center', size=8)


    if SAVE:
        plt.savefig(SAVE, dpi=200, bbox_inches='tight')

    plt.show(); print()




if __name__ is '__main__':
    dlcs = {
    'dlc11_0':PostProc.DLC('dlc11_0'),
    'dlc11_1':PostProc.DLC('dlc11_1'),
    'dlc11_3':PostProc.DLC('dlc11_3'),
    'dlc15_0':PostProc.DLC('dlc15_0'),
    'dlc15_1':PostProc.DLC('dlc15_1'),
    'dlc15_2':PostProc.DLC('dlc15_2')}

    run(dlcs, SAVE=False)