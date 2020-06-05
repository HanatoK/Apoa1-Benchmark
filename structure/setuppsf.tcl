package require psfgen
topology top_all36_prot.rtf
topology top_all36_lipid.rtf
# topology toppar_water_ions.rtf
segment PRO1 {pdb pro1.pdb}
segment PRO2 {pdb pro2.pdb}
segment LIP1 {pdb lip1.pdb}
segment LIP2 {pdb lip2.pdb}
# segment WAT1 {pdb water.pdb}
coordpdb pro1.pdb PRO1
coordpdb pro2.pdb PRO2
coordpdb lip1.pdb LIP1
coordpdb lip2.pdb LIP2
# coordpdb water.pdb WAT1
guesscoord
regenerate angles dihedrals
writepdb apoa1_nowater_1.pdb
writepsf apoa1_nowater_1.psf
