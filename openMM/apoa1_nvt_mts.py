#!/usr/bin/env python3

from simtk.openmm.app import *
from simtk.openmm import *
import simtk.unit as u
#from openmmplumed import *
from sys import stdout, exit, stderr
from customInte import *

# helper function to generate an unused index
def genUnusedForceGroupIndex(usedForceGroupIndex):
    i = 0
    while True:
        if i not in usedForceGroupIndex:
            return i
        i = i + 1

precision = 'mixed'
platform = Platform.getPlatformByName('CUDA')
properties = {'DeviceIndex': '0', 'Precision': f'{precision}'}
step = 50000
psf = CharmmPsfFile('apoa1_merge.psf')
pdb = PDBFile('apoa1_merge.pdb')
param = CharmmParameterSet('par_all36_lipid.prm', 'par_all36m_prot.prm', 'top_all36_lipid.rtf', 'top_all36_prot.rtf', 'toppar_water_ions.prm')
psf.setBox(108.8612*u.angstroms, 108.8612*u.angstroms, 77.758*u.angstroms)
system = psf.createSystem(param, nonbondedMethod=PME, nonbondedCutoff=12*u.angstroms, switchDistance=10*u.angstroms, constraints=HBonds, rigidWater=True, temperature=300.0*u.kelvin)
# get all nonbonded forces
nonbonded = [f for f in system.getForces() if isinstance(f, NonbondedForce)][0]
# since this is a system created by using CHARMM PSF file, 
# and the system should have 8 (or more?) force groups by defaults, 
# we should set the force group index of reciprocal space  
# to an ununsed index for multi-time stepping
# for force groups pre-defined in openmm's CHARMM implementation:
# https://github.com/openmm/openmm/blob/8c43e37a887eeaa919f31c762c5ee8841bba9a22/wrappers/python/simtk/openmm/app/charmmpsffile.py#L159
usedForceGroupIndex = [f.getForceGroup() for f in system.getForces()]
# unique the index list
usedForceGroupIndex = list(set(usedForceGroupIndex))
# get an unused number for indexing the PME reciprocal force
reciprocalIndex = genUnusedForceGroupIndex(usedForceGroupIndex)
# set the force group for electrostatic interactions in reciprocal space (PME)
nonbonded.setReciprocalSpaceForceGroup(reciprocalIndex)
print(f'The index of PME reciprocal force group is set to {reciprocalIndex}')
# evaluate once for force group 1 (PME) in a timestep
MTSList = [(reciprocalIndex, 1)]
# evaluate twice for other force groups in a timestep
for i in usedForceGroupIndex:
    MTSList.append((i,2))
print(MTSList)
# use 2fs timestep
integrator = MTSLangevinIntegrator(temperature=300.0*u.kelvin, friction=1/u.picosecond, dt=2*u.femtoseconds, groups=MTSList)
# setup PME grid parameters
nonbonded.setPMEParameters(0, 108, 108, 80)
simulation = Simulation(psf.topology, system, integrator, platform, properties)
simulation.context.setPositions(pdb.positions)
simulation.reporters.append(StateDataReporter(f'output/nanma_openmm_nvt_mts_{precision}.log', 5000, step=True, time=True, remainingTime=True, potentialEnergy=True, kineticEnergy=True, totalEnergy=True, temperature=True, totalSteps=step, speed=True))

simulation.step(step)
