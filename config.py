#!/home/samile/g2conda/bin/python3
# -*- coding: utf-8 -*-
"""
Python script to run multiple refinements on GSAS II
Configuration file

@author: Joel Eugênio Cordeiro Junior
last updated on: Feb 11 2023

"""

# project name without extension .gpx
PNAME = 'projeto-sem-hid'

# input data directory
INDIR = '/home/samile/Documentos/dados_entrada/'
# output data directory
OUTDIR = '/home/samile/Documentos/dados_saida/'
# preferred orientation model
POM = ['f001', 'f002']
HKL = [1, 0, -1]

# Python Interpreter path
PYPATH = '/home/samile/g2conda/bin'
# GSASII scriptable path
GSPATH = '/home/samile/g2conda/GSASII'

# project file type by extension
PRJEXT = '.gpx'

# phase file type by extension
PHSEXT = '.cif'

# powder data file type by extension
PWDEXT = '.raw'

# exported powder data file type by extension
TXTEXT = '.txt'

# parameter file name
PRM = 'param.prm'
