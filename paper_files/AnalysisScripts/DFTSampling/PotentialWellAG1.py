import numpy as np
import numpy.linalg as LA
from matplotlib import pyplot as plt
from scipy import io
from scipy.linalg import fractional_matrix_power

from gauopen import QCOpMat as qco
from gauopen import QCBinAr as qcb
from gauopen import QCUtil as qcu

hartree_to_eV = 27.211386
bohr_to_Angstrom = 0.529177211
fn="SingleCAg2T1BP"
modifier="medDist"

nGrid = 17
minDist = -0.5
maxDist = 0.5
#unitVec = -1*np.array([-0.54738554, -0.72969988,  0.40976476])
unitVec = -1*np.array([0.19129108, -0.72015464, 0.66692205])
atomInd = 62

print('Running initial calculation...')
bar = qcb.BinAr(debug=False,lenint=8,inputfile=fn+".chk")
bar.update(model='b3lyp', toutput='out.log', dofock="scfread", miscroute="10f 6d scf=xqc scrf=solvent=water")
print('Done!')

dist = np.linspace(minDist,maxDist,nGrid)
E = np.zeros(nGrid)
initVector = bar.c[atomInd*3:atomInd*3+3].copy()
for i in range(nGrid):
    vec = unitVec*dist[i]/bohr_to_Angstrom
    bar.c[atomInd*3:atomInd*3+3]= initVector+vec
    bar.update(model="b3lyp", toutput=f'out_ind{atomInd}{modifier}_{i}.log', dofock="scfread", miscroute="10f 6d scf=xqc scrf=solvent=water")
    E[i] = bar.scalar("escf")
    print(dist[i], E[i])
bar.c[atomInd*3:atomInd*3+3]= initVector

plt.plot(dist,E*hartree_to_eV)
plt.xlabel('Distance (Angstroms)')
plt.ylabel('Energy (eV)')
plt.savefig(fn+'_'+str(atomInd)+'_DFTwell.png')
io.savemat(fn+'_'+str(atomInd)+modifier+'DFTwell.mat', {"dist":dist, "E":E*hartree_to_eV})

