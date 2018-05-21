# -*- coding: utf-8 -*-
"""
Make plots for Disturbance Rejection Chapter.
@author: J
"""

import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc
import importlib, os


FigDir = '../Figures/Chapter_DisturbanceRejection/'
if not os.path.isdir(FigDir):
    os.makedirs(FigDir)


figScripts = [x[:-3] for x in os.listdir('../Postprocessing') if 'Ch2_' in x]

dlc = PostProc.DLC('dlc11_1')
dlc_noipc = PostProc.DLC('dlc11_0')

plt.rc('text', usetex=True)
for script in figScripts:
    print(f'Running {script}.py...')
    module = importlib.import_module('Postprocessing.' + script)
    module.run(dlc, dlc_noipc, SAVE = FigDir + script + '.png')
plt.rc('text', usetex=False)


