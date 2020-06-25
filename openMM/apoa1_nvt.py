#!/usr/bin/env python3

from simtk.openmm.app import *
from simtk.openmm import *
import simtk.unit as u
#from openmmplumed import *
from sys import stdout, exit, stderr

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
integrator = LangevinIntegrator(300.0*u.kelvin, 1/u.picosecond, 0.002*u.picoseconds)
#integrator = VerletIntegrator(0.001*u.picoseconds)
# setup PME grid parameters
nonbonded.setPMEParameters(0, 108, 108, 80)
simulation = Simulation(psf.topology, system, integrator, platform, properties)
simulation.context.setPositions(pdb.positions)
simulation.reporters.append(StateDataReporter(f'output/nanma_openmm_nvt_{precision}.log', 5000, step=True, time=True, remainingTime=True, potentialEnergy=True, kineticEnergy=True, totalEnergy=True, temperature=True, totalSteps=step, speed=True))

simulation.step(step)
