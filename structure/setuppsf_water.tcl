package require psfgen
topology toppar_water_ions.str
segment WAT1 {pdb wat1.pdb}
segment WAT2 {pdb wat2.pdb}
segment WAT3 {pdb wat3.pdb}
segment WAT4 {pdb wat4.pdb}
segment WAT5 {pdb wat5.pdb}
segment WAT6 {pdb wat6.pdb}
segment WAT7 {pdb wat7.pdb}
segment WAT8 {pdb wat8.pdb}
segment WAT9 {pdb wat9.pdb}
coordpdb wat1.pdb WAT1
coordpdb wat2.pdb WAT2
coordpdb wat3.pdb WAT3
coordpdb wat4.pdb WAT4
coordpdb wat5.pdb WAT5
coordpdb wat6.pdb WAT6
coordpdb wat7.pdb WAT7
coordpdb wat8.pdb WAT8
coordpdb wat9.pdb WAT9

guesscoord
regenerate angles dihedrals

writepdb water_1.pdb
writepsf water_1.psf
