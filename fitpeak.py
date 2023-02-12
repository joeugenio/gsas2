# -*- coding: utf-8 -*-
"""
Estimation of non-crystalline phases by fitting multiple peaks

@author: Joel Eugênio Cordeiro Junior
last updated on Feb 11 2023

References
1 - https://lmfit.github.io/lmfit-py/builtin_models.html#example-3-fitting-multiple-peaks-and-using-prefixes
2 - https://chrisostrouchov.com/post/peak_fit_xrd_python/

"""
import os
import numpy as np
import matplotlib.pyplot as plt
from lmfit.models import PseudoVoigtModel
import csv

DATADIR = 'clinqueres'

# -----------------------------------------------------------------------------
# Fitting multiple peaks
# -----------------------------------------------------------------------------
def fitting_peaks(data, label, peaks, datadir=DATADIR, plot_bkg=True, plot_obs=False, plot_init=False,
                  plot_init_comps=False, plot_comps=True, plot_bestfit=True,
                  plot_area_pv1=True, saveplots=True):  
    x = data[:, 0]
    y = data[:, 4]
    y_obs = data[:, 1]
    
    plt.figure(figsize=(8,5))
    
    if plot_bkg:
        plt.plot(x, y, '-y', lw=3, label='y_bkg')
        
    if plot_obs:
        plt.plot(x, y_obs, label='y_obs')
    
    pv0 = PseudoVoigtModel(prefix='pv0_')
    pars = pv0.guess(y, x=x)
    p = peaks[0]
    pars['pv0_center'].set(value=p, min=p-1, max=p+1)
    pars['pv0_sigma'].set(value=10)
    pars['pv0_amplitude'].set(value=20*y.max())
    
    if plot_init_comps:
        init_pv0 = pv0.eval(pars, x=x)
        plt.plot(x, init_pv0, '--', label='init_pv0')
    
    pv1 = PseudoVoigtModel(prefix='pv1_')
    pars.update(pv1.make_params())
    p = peaks[1]
    pars['pv1_center'].set(value=p, min=p-2, max=p+2)
    pars['pv1_sigma'].set(value=15)
    pars['pv1_amplitude'].set(value=20*y.max())
    
    if plot_init_comps:
        init_pv1 = pv1.eval(pars, x=x)
        plt.plot(x, init_pv1, '--', label='init_pv1')
        
    pv2 = PseudoVoigtModel(prefix='pv2_')
    pars.update(pv2.make_params())
    p = peaks[2]
    pars['pv2_center'].set(value=p, min=p-2, max=p+2)
    pars['pv2_sigma'].set(value=20)
    pars['pv2_amplitude'].set(value=20*y.max())
    
    if plot_init_comps:
        init_pv2 = pv2.eval(pars, x=x)
        plt.plot(x, init_pv2, '--', label='init_pv2')
    
    mod = pv0 + pv1 + pv2
    
    if plot_init:
        init = mod.eval(pars, x=x)
        plt.plot(x, init, '--', label='init_fit')
    
    out = mod.fit(y, pars, x=x)
    comps = out.eval_components(x=x)
    
    if plot_bestfit:
        plt.plot(x, out.best_fit, '--k', lw=2, label='best_fit')
    
    if plot_comps:
        plt.plot(x, comps['pv0_'], '--g', label='pv0')
        plt.plot(x, comps['pv1_'], '--b', label='pv1')
        plt.plot(x, comps['pv2_'], '--r', label='pv2')
        
    # area under pv1
    a_pv1 = np.trapz(comps['pv1_'], x)
    a_y_obs = np.trapz(y_obs, x)
    acn = 100*a_pv1/a_y_obs
    
    if plot_area_pv1:
        plt.fill_between(x, comps['pv1_'], alpha=0.4)    
    
    plt.legend()
    plt.title(label)
    plt.ylabel('intensidade')
    plt.xlabel(r'2$\theta$')
    if saveplots:
        plt.savefig(os.path.join(datadir,label+'.png'), dpi=120, format='png')
    # plt.show()
    
    return (a_pv1, a_y_obs, acn)

# -----------------------------------------------------------------------------
# data from files
# -----------------------------------------------------------------------------


data = {}
for file in os.listdir(DATADIR):
    if file.endswith('.txt'):
        data[file[:-4]] = (np.loadtxt(os.path.join(DATADIR, file)))  

"""
File columns

0              1            2            3            4
x            y_obs        weight       y_calc       y_bkg        
"""
# # peak guesses
# for k,v in data.items():
#     x = v[:, 0]
#     y = v[:, 4]
#     plt.plot(x, y, label=k)
# plt.vlines([11, 34, 54], 0, 2100, ls='--', colors='k')
# plt.legend()
# plt.show()

"""
Peaks at 11, 34 and 54
"""
peaks = [11, 34, 54]

header = ['amostra','area_pv1', 'area_y_obs', 'acn']
rows = [header]
for k,v in data.items():
    a_pv1, a_y_obs, acn = fitting_peaks(v, k, peaks, saveplots=False)
    row = [k, a_pv1, a_y_obs, acn]
    rows.append(row)

with open(os.path.join(DATADIR,'areas.csv'), 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

for r in rows:
    print(r)
    
