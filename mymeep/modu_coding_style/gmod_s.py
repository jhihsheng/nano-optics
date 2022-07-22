
resolution = 1000                 # pixels/um
dpml = 1.0                      # PML thickness
sz = 6 + 2*dpml
cell_size = mp.Vector3(z=sz)
pml_layers = [mp.PML(dpml)]
d = 0.5 # thickness = 500 nm 
epsi = 12
geometry = [mp.Block(mp.Vector3(mp.inf,mp.inf,d), center=mp.Vector3(z=0),
                     material= mp.Medium(epsilon=epsi))]
dimensions = 1
