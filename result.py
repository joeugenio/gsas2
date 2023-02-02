#!/home/samile/g2conda/bin/python3
# -*- coding: utf-8 -*-
"""
Python script to run multiple refinements on GSAS II
Create table with results
Main script

@author: Joel Eugênio Cordeiro Junior
last updated on: 2023/02/02

"""

import os,sys
from config import *
import csv

# ----------------------------------------------
# Read files
# ----------------------------------------------

FILE = 'results.csv'

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

first_row = ['Fases']
last_row1 = ['GOF']
last_row2 = ['wR']
wf = []
sig = []

rows = [first_row]
for ph in phases:
	rows.append([ph[5:-4]])

for h in powders:
	first_row.append(h[:-4])
	wf = []
	sig = []
	proj_file = os.path.join(OUTDIR, h[:h.lower().find(PWDEXT)], 'march-dollase.lst')
	with open(proj_file, 'r') as f:
	  	lines = f.readlines()
	for l in lines:
		l = l.replace(' ','')
		index = l.find('GOF')
		if index != -1:
			last_row1.append(l[index+4:-1])
			last_row2.append(l[l.find('=')+1:l.find('%')+1])
		index = l.find('Weightfraction')
		if index != -1:
			wf.append(l[l.find(':',index)+1:l.find(',',index)])
			sig.append(l[l.find('sig',index)+3:-1])
	# next rows
	for r,w,s in zip(rows[1:],wf,sig):
		r.append(w+' ('+s+')')

rows.append(last_row1)
rows.append(last_row2)

for r in rows:
	print(r)

with open(os.path.join(OUTDIR,FILE), 'w', newline='') as file:
	writer = csv.writer(file)
	writer.writerows(rows)

print('Table finished, see {} file.'.format(FILE))
# ----------------------------------------------
# End
# ----------------------------------------------
