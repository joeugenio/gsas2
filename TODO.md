# TODO List

## Basic steps

[x] Open GSASII
[x] Create new project _*.gpx_
[x] Import phase file _*.cif_ with default name
[x] Save project _*.gpx_
[x] Import Poweder Data .raw and .prm files. Select all phases
[x] Save project _*.gpx_

## Refinements

[x] Set Controls Max cycles = 10
[x] For each powder hist, unset Sample Paramenters, Histogram Scale Factor options
[x] For each powder hist, set Background Refine Chebyshev option
[x] For each phase, data, phase fraction

## Caculate refine

[x] Step 1: Background 3
[x] Step 2: Background 15
[x] Step 3: Sample Paramenters, Sample displacement
[x] Step 4: Phases, Refine unit cell
[x] Step 5: Instruments paraments W
[x] Step 6: Instruments paraments X
[x] Step 7: Instruments paraments V
[x] Step 8: Instruments paraments U
[x] Step 9: Instruments paraments SH/L
[x] Step 10: Phase[nome_fase] Data, March Dollase, save new _*.lst_ file


## Others
[ ] Move dictionary from `run_refinement.py` to `config.py`
[ ] Open each project separately
[ ] Adjust March Dollase
[ ] Document the code
[ ] Put more detailed information in `README.md`
[ ] Adapt the script to the MS Windows

## Check out the following projects
