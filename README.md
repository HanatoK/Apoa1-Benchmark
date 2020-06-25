# Benchmarks of MD engines using ApoA1

## System

Apolipoprotein A1 (ApoA1) has been a standard benchmarking system of NAMD for years. For more information about ApoA1 itself, please see [here](https://en.wikipedia.org/wiki/Apolipoprotein_A1). The system is parameterized using CHARMM36m force field with TIP3P water model and consists of 92,224 atoms.

## Common settings

- Periodic boundary condition: X = 108.8612 Å, Y = 108.8612 Å, Z = 77.758 Å
- Initial temperature: 300 K
- Cutoff of short-range nonbonded interactions (both electrostatic and van der Waals): 12.0 Å
- Smooth-switching before nonbonded interactions cut-off: 10.0 Å
- Calculation of long-range electrostatic interactions: PME
- Number of PME grids in each dimension: X = 108, Y = 108, Z = 80
- Rigid waters: hydrogen-oxygen and hydrogen-hydrogen bonds in water molecules
- Bond constraints: all covalent bonds involving H atoms

## Test cases

1. NVE, 2.0 fs timestep for integration of all interactions except long-range nonbonded interactions, and long-range nonbonded interactions is computed every 2.0 fs. (multi-time stepping)
2. NVT using Langevin thermostat (or integrating with Langevin dynamics), 2.0 fs timestep for integration of all interactions. (no MTS)
3. NVT using Langevin thermostat (or integrating with Langevin dynamics), 2.0 fs timestep for integration of all interactions except long-range nonbonded interactions, and long-range nonbonded interactions is computed every 2.0 fs. (MTS)

## Running MD simulations

### NAMD

- NVE (MTS): `namd3 +p1 +devices 0 +idlepoll apoa1_nve_mts.namd | tee output/nve_mts.log`
- NVT (no MTS): `namd3 +p1 +devices 0 +idlepoll apoa1_nvt.namd | tee output/nvt.log`
- NVT (MTS): `namd3 +p1 +devices 0 +idlepoll apoa1_nvt_mts.namd | tee output/nvt_mts.log`

### GROMACS

NOTE: GROMACS requires pre-processing all the input files by `gmx grompp`, so if you want to change options you need to do the modifications in `.mdp` files, and then run `gmx grompp -f <MDP file> -c <GRO file> -p <TOP file> -o <TPR output file> -maxwarn 1` to generate the necessary `.tpr` file for running simulations. In addition, GROMACS does not support Langevin dynamics and SHAKE constraints in GPU-resident mode.

- NVE (MTS): (Not available)
- NVT (no MTS): `gmx mdrun -ntomp 1 -nb gpu -pme gpu -bonded gpu -update gpu -gpu_id 1 -s ./apoa1_nvt.tpr`
- NVT (MTS): (Not available)

### AMBER

- NVE (MTS): (Not available)
- NVT (no MTS): `pmemd.cuda -O -i apoa1_nvt.in -o output/nvt.out -p apoa1_merge_2.parm7 -c apoa1_merge_2.rst7 -inf output/mdinfo`
- NVT (MTS): (Not available)

### OpenMM

- NVE (MTS): `python3 apoa1_nve_mts.py`
- NVT (no MTS): `python3 apoa1_nvt.py`
- NVT (MTS): `python3 apoa1_nvt_mts.py`
