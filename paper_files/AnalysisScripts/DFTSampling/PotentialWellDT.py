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
fn="DT"
modifier="water"

nGrid = 16
minDist = 2.5
maxDist = 10
unitVec = -1*np.array([-0.53807896, 0.04858294, -0.84149316])#[0,1,0])
atomInd = 21

print('Running initial calculation...')
bar = qcb.BinAr(debug=False,lenint=8,inputfile=fn+".chk")
bar.update(model='b3lyp', toutput='out'+modifier+'.log', dofock="scf", miscroute="")#scrf=(solvent=water)")
print('Done!')

dist = np.linspace(minDist,maxDist,nGrid)
E = np.zeros(nGrid)
initVector = bar.c[atomInd*3:atomInd*3+3].copy()
for i in range(nGrid):
    vec = unitVec*dist[i]/bohr_to_Angstrom
    bar.c[atomInd*3:atomInd*3+3]= initVector+vec
    bar.update(model="b3lyp", toutput=f'out_ind{atomInd}_{dist[i]}Ang{modifier}.log', dofock="scfread", miscroute="geom=nocrowd scf=xqc scrf=solvent=water")
    E[i] = bar.scalar("escf")
    print(dist[i], E[i])
bar.c[atomInd*3:atomInd*3+3]= initVector

plt.plot(dist,E*hartree_to_eV)
plt.xlabel('Distance (Angstroms)')
plt.ylabel('Energy (eV)')
plt.savefig(fn+'_'+str(atomInd)+'_DFTwell'+modifier+'.png')
io.savemat(fn+'_'+str(atomInd)+'DFTwell'+modifier+'.mat', {"dist":dist, "E":E*hartree_to_eV})

