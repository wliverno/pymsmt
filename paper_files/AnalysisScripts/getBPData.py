from BPStats import BPStats
import numpy as np
from scipy.io import savemat
files = ['md_NoMetalStrand_solv_nWI.pdb','md_SingleCAg2T_solv_nWI.pdb','md_SingleCT_solv_nWI.pdb', 'md_SingleCHgT_solv_nWI.pdb','md_TripleCAg2T_solv_nWI.pdb', 'md_TripleCAg2T_solv_nWI.pdb']

for fn in files:
    print(fn)
    b = BPStats(fn)
    print('...Loaded!')
    BPTwist = np.zeros((6, b.nFrames))
    propAngs = np.zeros((7, b.nFrames))
    C1dists = np.zeros((7, b.nFrames))
    Ndists = np.zeros((3, b.nFrames))
    nMetals = len(b.metals)
    metAngs = np.zeros((nMetals, b.nFrames))
    COMdists = np.zeros((7, b.nFrames))
    for i in range(b.nFrames):
        b.setFrame(i+1)
        BPTwist[:, i] = b.BP_twists()
        Ndists[:, i] = [b.BP_nDist(j) for j in [3,4,5]]
        metAngs[:, i] = [b.BP_metalAng(j+1) for j in range(nMetals)]
        propAngs[:, i] = b.BP_props()
        C1dists[:, i] = b.distancesAtom()
        COMdists[:, i] = b.distancesCOM()
    print("--ANGLES--")
    for i in range(6):
        print(f"{b.BP[i]}-Twist: mean= {np.mean(propAngs[i,:]):.2f} stdev= {np.std(propAngs[i,:]):.2f}")
        print(f"BPTwist: mean= {np.mean(BPTwist[i, :]):.2f} stdev= {np.std(BPTwist[i, :]):.2f}")
    print(f"{b.BP[6]}-Twist: mean= {np.mean(propAngs[6,:]):.2f} stdev= {np.std(propAngs[6,:]):.2f}")
    for i, met in enumerate(b.metals):
        print(f"N3-{met.get_name()}{i+1}-N3 Angle: mean= {np.mean(metAngs[i, :]):.2f} stdev= {np.std(metAngs[i, :]):.2f}")
    print("--DISTANCES--")
    for i in range(7):
        print(f"{b.BP[i]} C1\'-C1\' dist: mean= {np.mean(C1dists[i,:]):.2f} stdev= {np.std(C1dists[i,:]):.2f}")
    for i in range(7):
        print(f"{b.BP[i]} COM dist: mean= {np.mean(COMdists[i,:]):.2f} stdev= {np.std(COMdists[i,:]):.2f}")
    for i in [3,4,5]:
        print(f"{b.BP[i-1]} N-N dist: mean= {np.mean(Ndists[i-3, :]):.2f} stdev= {np.std(Ndists[i-3, :]):.2f}")
    matFile = fn[:-4]+'_stats.mat'
    savemat(matFile, {"BPTwist":BPTwist, "propAngs":propAngs, "metAngs":metAngs, "C1dists":C1dists, "Ndists":Ndists, "COMdists":COMdists})
    print(f'{matFile} saved!')
