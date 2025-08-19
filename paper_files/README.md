# Manuscript files

This directory contains all input and data files from the manuscript ([Preprint](https://chemrxiv.org/engage/chemrxiv/article-details/67d4af74fa469535b9427ce8). In Review). Below is a list of the files and their description, as well as relevant sections/figures:

## AnalysisScripts/
- **BPStats.py**: A Python module for collecting DNA geometry information (twist, propeller angle, distances)
- **getBPData.py**: A script that analyzes the 100ns trajectory PDB files to gather statistics on DNA geometry, Figures 6 and S9-S12 in the manuscript
- **DFTSampling/**: Files for DFT energy sampling. Uses gauopen 3.0 python interface (only available for Gaussian Development Version) and included *.gjf files
  - **PotentialWellAG1.py**: Samples DFT energy for AG1 atom in the C-Ag<sub>2</sub>-T "large" structure, Figures 2 and S3 in the manuscript
  - **PotentialWellAG2.py**: Samples DFT energy for AG1 atom in the C-Ag<sub>2</sub>-T "large" structure, Figures 2 and S3 in the manuscript
  - **PotentialWellDT.py**: Samples DFT energy for H3 atom in the DT structure, Figure S4 in the manuscript
- **MDSampling/**: Files for MD energy sampling. Uses PyTraj and libsander, referenced *.pdb and *.prmtop files included in folder.
  - **MDSampling.ipynb** Jupyter notebook for sampling all MD data, Figures 2, S3, and S4 in the manuscript

## EnergyScanData.xlsx
All collected energy scan data used for Figures 2, S3, and S13 in the manuscript

## EnergyScanData.xlsx
All collected MD trajectory statistics used for Figures 6, S10, and S12 in the manuscript

## InputFiles/
- A directory containing input files for DFT and MD calculations, organized into subdirectories for different software.

### Amber/
- **waterIonMin.in**: Initial minimization (step 1, water and ions only)
- **min.in**: Minimization step (step 2, also used to generate mineq and mdmin files)
- **heat.in**: Heating step (step 3)
- **eq.in**: 1 ns equilibration step (step 4)
- **md.in**: 100 ns MD trajectory (step 5)
- **angRestCAg2T.in**: Angle restrained minimization (step 2, also used to generate mineq files)
- **CAg2T.na**: Harmonic restraints file for N3-Ag-N3 angle and O4-AG bond
- **CHgT.na**: Harmonic restraints file for N3-Hg-N3 angle

### Gaussian/
- **SingleCAg2T_angRestmineq.gjf**: SingleCAg2T Force calculation for the angle retrained mineq output, Figure 3 and Table 1 in manuscript
- **SingleCAg2T_fullFFmineq.gjf**: SingleCAg2T Force calculation for the generated force field mineq output, Figure 3 and Table 1 in manuscript
- **SingleCAg2T_partialDFTmin.gjf**: SingleCAg2T Force calculation for the generated force field mineq output, Figure 3 and Table 1 in manuscript
- **SingleCAg2T.gjf**:  SingleCAg2T Force calculation for the initial structure, Figure 3 and Table 1 in manuscript
- **SingleCHgT_angRestmineq.gjf**: SingleCHgT Force calculation for the angle retrained mineq output, Figure 3 and Table 1 in manuscript
- **SingleCHgT_fullFFmineq.gjf**: SingleCHgT Force calculation for the generated force field mineq output, Figure 3 and Table 1 in manuscript
- **SingleCHgT_partialDFTmin.gjf**:  SingleCHgT Force calculation for the generated force field mineq output, Figure 3 and Table 1 in manuscript
- **SingleCHgT.gjf**: SingleCHgT Force calculation for the initial structure, Figure 3 and Table 1 in manuscript
- **TripleCAg2T_fullFFcut3.4mineq.gjf**: TripleCAg2T Force calculation for the 3.4 Angstrom cutoff 3BP generated force field mineq structure, Figure S6 in manuscript
- **TripleCAg2T_fullFFmineq.gjf**:  TripleCAg2T Force calculation for the 3.0 Angstrom cutoff 3BP generated force field mineq structure, Figure S6 in manuscript
- **TripleCAg2T_singleFFmineq.gjf**: TripleCAg2T Force calculation for the SingleCAg2T generated force field mineq structure, Figure S6 in manuscript

## PDBFiles/
- A directory containing various PDB files related to molecular structures, organized into subdirectories. Matches the zip file included with the manuscript.

### Final MD Structures/
- **SingleCAg2T_solv_mdmin.pdb**: SingleCAg2T at the end of the 100ns trajectory after minimization (solvent and ions included), Figure 5 in manuscript
- **SingleCHgT_solv_mdmin.pdb**: SingleCHgT at the end of the 100ns trajectory after minimization (solvent and ions included), Figure 5 in manuscript
- **StableTripleCAg2T_solv_mdmin.pdb**: Stabilized TripleCAg2T at the end of the 100ns trajectory after minimization (solvent and ions included), Figure 5 in manuscript
- **TripleCAg2T_solv_mdmin.pdb**: TripleCAg2T at the end of the 100ns trajectory after minimization (solvent and ions included), Figure 5 in manuscript

### Initial Structures/
- **Complementary.pdb**: Seven basepair dsDNA complementary case
- **SingleCAg2T.pdb**: Seven basepair dsDNA with C-Ag2-T at basepair 4.
- **SingleCHgT.pdb**: Seven basepair dsDNA with C-Hg-T at basepair 4.
- **SingleCTMismatch.pdb**: Seven basepair dsDNA with C-T at basepair 4.
- **TripleCAg2T.pdb**: Seven basepair dsDNA with C-Ag2-T at basepair 3, 4, and 5.
- **StableTripleCAg2T.pdb**: Same as *TripleCAg2T.pdb* but with a GC at basepair 1 replacing the AT

### Minimized Structures/
- **SingleCAg2T_AngRest_mineq.pdb**: SingleCAg2T case after minimization, heating, equilibration, and a final minimization using the angle restrained method, Figure 3 in manuscript
- **SingleCAg2T_FF_mineq.pdb**: SingleCAg2T case after minimization, heating, equilibration, and a final minimization using the generated force field, Figure 2 in manuscript
- **SingleCAg2T_partialDFTmin.pdb**: SingleCAg2T case after partial DFT minimization used in previous works, Figure 3 in manuscript
- **SingleCHgT_AngRest_mineq.pdb**: SingleCAg2T case after minimization, heating, equilibration, and a final minimization using the angle restrained method, Figure 3 in manuscript
- **SingleCHgT_FF_mineq.pdb**: SingleCHgT case after minimization, heating, equilibration, and a final minimization using the generated force field, Figure 3 in manuscript
- **SingleCHgT_partialDFTmin.pdb**: SingleCHgT case after partial DFT minimization used in previous works, Figure 3 in manuscript
- **TripleCAg2T_fullFF_mineq.pdb**: TripleCAg2T case after minimization, heating, equilibration, and a final minimization using the 3BP parameterization (3.0 Angstrom cutoff), Figure 4 in manuscript
- **TripleCAg2T_fullFF3.4_mineq.pdb**: TripleCAg2T case after minimization, heating, equilibration, and a final minimization using the 3BP parameterization (3.4 Angstrom cutoff), Figure 4 in manuscript
- **TripleCAg2T_singleFF_mineq.pdb**: TripleCAg2T case after minimization, heating, equilibration, and a final minimization using the parameterization generated for SingleCAg2T, Figure 4 in manuscript
