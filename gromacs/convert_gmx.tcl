mol new apoa1_merge.psf
mol addfile apoa1_merge.pdb
topo writegmxtop apoa1_merge.top [list toppar_water_ions.prm par_all36m_prot.prm par_all36_lipid.prm]
