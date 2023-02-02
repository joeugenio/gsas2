#!/home/samile/g2conda/bin/python3
# -*- coding: utf-8 -*-
"""
Python script to run multiple refinements on GSAS II
Main script

@author: Joel Eugênio Cordeiro Junior
last updated on: 2023/02/02

"""

import os,sys
import shutil
from config import *
sys.path.insert(0,GSPATH)
import GSASIIscriptable as G2sc

# set verbosity level (all, warn, error or None)
G2sc.SetPrintLevel('error')

# ----------------------------------------------
# Create projects
# ----------------------------------------------

# select powder data files
powders = []
for file in os.listdir(INDIR):
	if file.lower().endswith(PWDEXT):
		powders.append(file)

# sort list of powder files by name
powders.sort()

# select phase files
phases = []
for file in os.listdir(INDIR):
	if file.lower().endswith(PHSEXT):
		phases.append(file)

# sort list of phases by name
phases.sort()

# creating and setting projects
projs = []
proj_dirs = []

# create outout dir
if not os.path.exists(OUTDIR):
	os.makedirs(OUTDIR)

for powder in powders:
	# create dirs
	proj_dir = os.path.join(OUTDIR, powder[:powder.lower().find(PWDEXT)])
	proj_dirs.append(proj_dir)
	if os.path.exists(proj_dir):
		#os.rmdir(proj_dir)
		shutil.rmtree(proj_dir)
	os.makedirs(proj_dir)
	# create project
	gpx = G2sc.G2Project(newgpx=os.path.join(proj_dir, PNAME+PRJEXT))
	# add phases
	for phase in phases:
		gpx.add_phase(os.path.join(INDIR, phase))
	# add powder data
	gpx.add_powder_histogram(datafile=os.path.join(INDIR, powder), iparams=os.path.join(INDIR, PRM), phases='all')
#	# set controls
	gpx.set_Controls('cycles', 10)
	# save project
	gpx.save()
#	print(gpx)
	projs.append(gpx)

# ----------------------------------------------
# Refinements 
# ----------------------------------------------

# parameters dictionary step 1
dict1 = {'set': { 'Background': {'type': 'chebyschev', 'no. coeffs' : 3, 'refine': True}, 'Scale': True}, 'clear': {'Sample Parameters': ['Scale']}}
# parameters dictionary step 2
dict2 = {'set': { 'Background': {'type': 'chebyschev', 'no. coeffs' : 8, 'refine': True}}}
# parameters dictionary step 3
dict3 = {'set': { 'Sample Parameters': ['Shift']}}
# parameters dictionary step 4
dict4 = {'set': {'Cell': True}}
# parameters dictionary step 5
dict5 = {'set': {'Instrument Parameters': ['W']}}
# parameters dictionary step 6
dict6 = {'set': {'Instrument Parameters': ['X']}}
# parameters dictionary step 7
dict7 = {'set': {'Instrument Parameters': ['V']}}
# parameters dictionary step 8
dict8 = {'set': {'Instrument Parameters': ['U']}}
# parameters dictionary step 9
dict9 = {'set': {'Instrument Parameters': ['SH/L']}}
# list of parameters dictionaries
# params = [dict1, dict2, dict3, dict4, dict5, dict6, dict7, dict8, dict9]
params = [dict1, dict2, dict3, dict4]

# parameters dictionary step 10, preferred orientation model (optional)
dict10 = {'Pref.Ori.': True}
hkl = [1, 0, -1]
#dict10 = {'Pref.Ori.': ['MD', 1.0, True, [1, 0, -1], 0, {}, [''], 0.1]}

# run refinement steps from 1 to 9 for all projects
for proj, proj_dir in zip(projs, proj_dirs):
	try:
		proj.do_refinements(params, makeBack=True)
	except Exception as e:
		print('An exception occurred when running refinements steps from 1 to 9: {}.'.format(e))
		for h in proj.histograms():
			print('Verify {} refinement parameters.'.format(h.name))
	proj.save()
	# export powder data as text file
	for h in proj.histograms():
		h.Export(os.path.join(proj_dir,PNAME), TXTEXT)

# run refinement step 10 for all projects
run_step10 = False
for proj, proj_dir in zip(projs, proj_dirs):
	# set march dollase preferred orientation model from POM list for some phases 
	for fname, phs in zip(phases, proj.phases()):
		for pname in POM:
			if pname.lower() in fname.lower():
				phs.set_HAP_refinements(dict10)
				# set HKL parameters
				for h in phs.data['Histograms'].keys():
					phs.data['Histograms'][h]['Pref.Ori.'][3] = hkl
				run_step10 = True
	if run_step10:
		try:
			outname = os.path.join(proj_dir, 'march-dollase.gpx')
			proj.do_refinements(outputnames=[outname])
		except Exception as e:
			print('An exception occurred when running refinements with preferred orientation: {}'.format(e))
			for h in proj.histograms():
				print('Verify {} refinement parameters.'.format(h.name))
		proj.save()
		# export powder data as text file
		for h in proj.histograms():
			h.Export(outname, TXTEXT)

print('Refinements finished, see {} folder.'.format(OUTDIR))
# ----------------------------------------------
# End
# ----------------------------------------------
