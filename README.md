# pymsmt + mmDNA
Python Metal Site Modeling Toolbox with mmDNA Patch

It is developed by Pengfei Li in Prof. Kenne Merz's Research Group at Michigan State University. Compatibility with metal modified DNA (mmDNA) implemented by William Livernois in Prof. Anantram's Research group at University of Washington.
# Installation
While this repository is a fork of PyMSMT and can be installed with the `install.sh` script, it has been built to be added as a patch to the AmberTools installation. The easiest way to install is with the AmberTools conda environment, which must be activated before installation. The guide for this is [on the Amber website](https://ambermd.org/GetAmber.php), and can be done simply installing the package from conda-forge:
    
    conda create --name AmberTools python=3.12
    conda activate AmberTools
    conda install ambertools -c conda-forge

Then, from the activate conda environment the patch can be applied simply by running

	./patch.sh

which creates back-ups of all replaced files. To restore these files simply run

	./patch.sh --restore

If you have installed AmberTools without a conda environment, you can still install the files with the patch. Just make sure the following requirements are met before running: 
- `$AMBERTOOLS` environmental variable set
- Python 3 with a version of the `pymsmt` package installed

## Usage
Please refer to the [Amber manual](https://ambermd.org/doc12/Amber23.pdf) (Chapter 18, page 345-350) for `MCPB.py` usage information. Only one added optional variable has been implemented in this patch:

> **include_carbon** This variable turns on metal-carbon bonding. This can be set to 0 or 1 to switch on or off (set to 0 by default)

and step 3 charge fitting restraints have been added for DNA as well, making the default method (3b)  match those used for parmBSC0 and parmBSC1 force field development:

> 3a - Allows all the charges of the atoms in the ligating residues to change without restrictions (_unmodified_)

> 3b - Restrains the charges of the phosphate and sugar atoms to force field values (default)

> 3c - Restrains the charges of the phosphate backbone atoms to force field values

> 3d - Restrains the charges of the phosphorus only
