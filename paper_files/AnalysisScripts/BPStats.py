from Bio import PDB
from Bio.PDB.Atom import Atom
from Bio.PDB.vectors import Vector, calc_angle, calc_dihedral
import numpy as np
import matplotlib.pyplot as plt
import io

baseDict = {
    'C':['N1','C6', 'C5', 'N4', 'C4', 'N3', 'C2', 'O2', 'H6', 'H5', 'H41', 'H42'],
    'T':['N1','C6', 'C5', 'O4', 'C4', 'N3', 'C2', 'O2', 'C7', 'H73', 'H72', 'H71', 'H6', 'H3'],
    'M':['N1','C6', 'C5', 'O4', 'C4', 'N3', 'C2', 'O2', 'C7', 'H73', 'H72', 'H71', 'H6', 'H3'],
    'U':['N1','C6', 'C5', 'O4', 'C4', 'N3', 'C2', 'O2', 'H6', 'H5', 'H3'],
    'G':['N9', 'C8', 'N7', 'C5', 'C6', 'O6', 'C4', 'N3', 'C2', 'N2', 'N1', 'H8', 'H21', 'H22', 'H1'],
    'A':['N9', 'C8', 'N7', 'C5', 'C6', 'N6', 'C4', 'N3', 'C2', 'N1', 'H8', 'H61', 'H62', 'H2']

}
metalDict = ['AG', 'HG']
NDict = {'C':'N3', 'T':'N3', 'M':'N3', 'G':'N1', 'A':'N1', 'U':'N3'}
massDict = {'H':1.00784, 'C':12.011, 'N':14.0067, 'O':15.999, 'P':30.973762}

## Geometry helper functions

# Calculate angle between two vectors, use ref vector to determine sign
def angle(v1, v2, ref=[0,0,1]):
    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)
    angle = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    #Use cross product to set sign (default reference is z-axis)
    sign = np.sign(np.dot(np.cross(v1_u, v2_u),np.array(ref)))
    return np.degrees(angle)*sign

# Dihedral angle between 4 points specified by bond vectors:
# A-[b1]->B-[b2]->C-[b3]->D
def dihedral(b1, b2, b3):
    n1 = np.cross(b1, b2)
    n2 = np.cross(b2, b3)
    m1 = np.cross(n1, n2)
    x = np.dot(n1, n2)*np.linalg.norm(b2)
    y = np.dot(b2, m1)
    angle = np.arctan2(y, x)
    return np.degrees(angle)

# Class for loading multiframe PDB files and characterizing distances/angles
class BPStats:
    def __init__(self, pdbfile):
        #Open PDB File and load first frame of PDB
        parser = PDB.PDBParser()
        with open(pdbfile, 'r') as file:
            pdb_content = file.read()
        self.pdbfile = parser.get_structure("in_memory_structure", io.StringIO(pdb_content))
        self.nFrames = len(self.pdbfile)
        self.setFrame(1)

    #Collect base pairs from frame of DNA
    def setFrame(self, nFrame):
        self.pdb = self.pdbfile[nFrame-1]
        self.nucleotides = []
        self.bNames = []
        self.metals = []
        # Find Bases
        for chain in self.pdb:
            for residue in chain:
                if 'O3\'' in residue:  # Check for backbone O3 to ensure it's a nucleotide
                    self.nucleotides.append(residue)
                    self.bNames.append(residue.get_resname().strip()[1:])
                elif residue.get_resname()[:2] in metalDict:
                    self.metals.append(list(residue)[0])

        #Find Basepairs
        self.nBP = len(self.nucleotides) //2
        self.BP = []
        for i in range(self.nBP):
            b1 = self.bNames[i]
            b2 = self.bNames[self.nBP*2-i-1]
            if b1=='TM':
                pair = 'T-M-'+b2
            elif b2=='TM':
                pair = b1+'-M-T'
            else:
                pair = b1+b2
            self.BP.append(pair)
    
    def savePDB(self, fn='out.pdb'):
        io = PDB.PDBIO()
        io.set_structure(self.pdb)
        io.save(fn)

    #Calculate center of mass for the base
    def com(self, base_num):
        base = self.nucleotides[base_num-1]
        atomList = baseDict[base.get_resname().strip()[1]]
        totalMass = 0
        weightSum = np.zeros(3)
        for atom in atomList:
            m = massDict[atom[0]]
            coord = base[atom].get_coord()
            totalMass+= m
            weightSum += m*coord
        return weightSum/totalMass

    # Distance Methods
    def BP_vecAtom(self, base_num, atomType='C1\''):
        base_num2 = self.nBP*2 - base_num   # Zero indexing, don't need to add 1
        A1 = self.nucleotides[base_num-1][atomType].get_coord() # But need to subtract 1 here
        A2 = self.nucleotides[base_num2][atomType].get_coord()
        return (A1 - A2)
    
    def BP_nDist(self, base_num):
        base_num2 = self.nBP*2 - base_num
        aType1 = NDict[self.bNames[base_num-1][0]]
        aType2 = NDict[self.bNames[base_num2][0]]
        A1 = self.nucleotides[base_num-1][aType1].get_coord()
        A2 = self.nucleotides[base_num2][aType2].get_coord()
        return np.linalg.norm(A1 - A2)

    def BP_metalAng(self, metalInd, atomType='N3'):
        minDist = 1e6
        metal = self.metals[metalInd - 1].get_coord()
        ang = -1
        for i in range(self.nBP):
            a1 = self.nucleotides[i][atomType].get_coord()
            a2 = self.nucleotides[self.nBP*2 - i - 1][atomType].get_coord()
            v = (a1-metal, a2-metal)
            aDist = min([np.linalg.norm(l) for l in v])
            if aDist < minDist:
                minDist = aDist
                ang = abs(angle(v[0], v[1]))
        assert ang != -1, "metal basepair not found!"
        return ang
    
    def BP_distanceAtom(self, base_num, atomType='C1\''):
        return np.linalg.norm(self.BP_vecAtom(base_num, atomType))

    def BP_distanceCOM(self, base_num):
        base_num2 = self.nBP*2 - base_num + 1
        A1 = self.com(base_num)
        A2 = self.com(base_num2)
        return np.linalg.norm(A1 - A2)

    def distancesCOM(self):
        return [self.BP_distanceCOM(i+1) for i in range(self.nBP)]

    def distancesAtom(self, atomType='C1\''):
        return [self.BP_distanceAtom(i+1, atomType) for i in range(self.nBP)]

    # Orientation Methods
    def base_CNVec(self, base_num):
        base = self.nucleotides[base_num-1]
        C1 = base['C1\''].get_coord()
        if 'N9' in base:
            N = base['N9'].get_coord()
        else:
            N = base['N1'].get_coord()
        return N-C1

    def base_CCVec(self, base_num):
        base = self.nucleotides[base_num-1]
        P1 = []
        P2 = []
        if '3' in base.get_resname():
            base2 = self.nucleotides[base_num-2]
            P1 = base2['C1\''].get_coord()
            P2 = base['C1\''].get_coord()
        else:
            base2 = self.nucleotides[base_num]
            P1 = base['C1\''].get_coord()
            P2 = base2['C1\''].get_coord()
        return P1-P2

    def base_NormVec(self, base_num):
        base = self.nucleotides[base_num-1]
        atomList = baseDict[base.get_resname().strip()[1]]
        # Get coordinates of non-hydrogen atoms
        points = [base[a].get_coord() for a in atomList if 'H' not in a]
        points = np.array(points)
        # Center points and use SVD to find normal vector
        center = np.mean(points, axis=0)
        centered_points = points - center
        _, _, vh = np.linalg.svd(centered_points)
        normal = vh[2]
        # Create unit vector
        normal /= np.linalg.norm(normal)
        # Ensure direction using CC vec
        CC = self.base_CCVec(base_num)
        if np.dot(normal, CC) < 0:
            normal = -normal
        return normal, CC
    
    # Angle methods
    def base_gatorAngs(self):
        aList = []
        bList = list(range(1,self.nBP))
        bList += [i+self.nBP for i in bList]
        for base_num in bList:
            # Use normal vecs
            n1, _ = self.base_NormVec(base_num)
            n2, _ = self.base_NormVec(base_num+1)
            # create plane between normal vec and CN vec
            plane1 = np.cross(self.base_CNVec(base_num), n1)
            plane1 /= np.linalg.norm(plane1)
            plane2 = np.cross(self.base_CNVec(base_num+1), n2)
            plane2 /= np.linalg.norm(plane2)
            # Average two planes to create reference direction orthagonal to the gator direction
            avgPlane = (plane1 + plane2)/2
            # Remove projection onto that normal vector (twist between neigboring basepairs)
            V1 = n1 - (np.dot(n1, avgPlane)*avgPlane)
            V2 = n2 - (np.dot(n2, avgPlane)*avgPlane)
            # Calculate angle, using that normal vector to set the sign of the angle
            aList.append(angle(V1, V2, avgPlane))
        return aList
    
    #Propeller angle: [n1]->COM->COM2-[n2] 
    def BP_prop(self, base_num):
        base_num2 = self.nBP*2 - base_num + 1
        C1 = self.com(base_num)
        C2 = self.com(base_num2)
        N1, ref1 = self.base_NormVec(base_num)
        N2, ref2 = self.base_NormVec(base_num2)
        ref = ref1 - ref2
        if np.dot(N1,ref) < 0:
            N1 = -N1
        if np.dot(N2, -ref) < 0:
            N2 = -N2
        return dihedral(N1, C2-C1, N2)

    def BP_props(self):
        twistList = []
        for base_num in range(0, self.nBP):
            twistList.append(self.BP_twist(base_num+1))
        return twistList
    
    #"Basepair Twist" angles using neighboring bases
    def BP_twists(self):
        heList = []
        for base_num in range(1, self.nBP):
            V1 = self.BP_vecAtom(base_num)
            V2 = self.BP_vecAtom(base_num+1)
            heList.append(np.abs(angle(V1, V2)))
        return heList
