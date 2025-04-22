import meep as mp
import numpy as np
from matplotlib import pyplot as plt
from meep.materials import Al, Ag, SiO2
import os
import subprocess
################
# Some parameters to describe the geometry:
resolution = 250
w = 1 # thickness of the metal film
# The cell dimensions
sy = 3  # size of cell in y direction 
sx = 0.1 # periodical in x
dpml = 0.5  # PML thickness (y direction only!)
cell = mp.Vector3(sx, sy)
# 
sr_y = w/2 + 0.01 # the source is  just above the surface

b = mp.Block(size=mp.Vector3(sx, w, ), material=Ag) # metal film
geometry = [b]

# boundary layer
boundary_layers=[mp.Absorber(thickness=dpml, direction=mp.Y)] ## !! Here, I do not use pml since pml can not deal with wave propagating parallel to the plane

################
# source 

fcen = 1.25  # pulse center frequency
df = 2  # pulse freq. width: large df = short impulse
s = [
    mp.Source(
        src=mp.GaussianSource(fcen, fwidth=df),
        component=mp.Ey,
        size=mp.Vector3(sx,0,0),
        center=mp.Vector3(0, sr_y),
    )
]
################

sim = mp.Simulation(
    cell_size=cell,
    geometry=geometry,
    boundary_layers=boundary_layers,
    sources=s,
    resolution=resolution,
    k_point = mp.Vector3(0) 
)

################
# Define a function to catch the mode freqeuncies at a given k_x
def sim_k_point_harminv(sim,kx):
    ey_tmp =[] # 
    time_tmp = [] # 
    
    def collect_ey_tmp(sim):
        ey = sim.get_field_point(mp.Ey, mp.Vector3(0, sr_y))
        ey_tmp.append(ey)
        time_tmp.append(sim.meep_time())

    ##
    sim.reset_meep()  # Reset the simulation
   #sim.restart_fields()
    sim = mp.Simulation(
        cell_size=cell,
        geometry=geometry,
        boundary_layers=boundary_layers,
        sources=s,
        resolution=resolution,
        k_point = mp.Vector3(kx) 
        )
    # Run simulation, collecting Ey at every time step
    sim.run(
        mp.after_time(10,mp.at_every(1/resolution, collect_ey_tmp)),  # Collect Ey every 0.1 time units
        until=30
    )

    # Convert data to numpy arrays for plotting
    ey_tmp = np.array(ey_tmp)
    time_tmp= np.array(time_tmp)

    # 
    # Save the time and Ey data to a file
    filename = "ey_time_tmp.txt"
    # Check if file exists and modify filename if necessary
    counter = 1
    while os.path.exists(filename):
        filename = f"ey_time_tmp_{counter}.txt"
        counter += 1
        
    with open(filename, "w") as f:
        for t, ey in zip(time_tmp, ey_tmp):
            f.write(f"{ey.real}+{ey.imag}i\n") # Save time, Ey
    
    # Run harminv command and capture output
    cmd = f"OMP_NUM_THREADS=1 harminv -t {1/resolution} -Q 1 0-3 < {filename}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    # Process the output
    output = result.stdout.splitlines()
    frequencies = []

    # Skip header and extract positive frequencies
    for line in output:
        if line.startswith("frequency") or not line.strip():
            continue  # Skip header or empty lines
        try:
            freq = np.float64(line.split(",")[0].strip())
            if freq > 0:
                frequencies.append(freq)
        except (ValueError, IndexError):
            continue  # Skip invalid lines
    return frequencies
    
#### FDTD simulation
nk = 101
kpoint = np.linspace(0,0.5,nk) / sx
fre_kx = []

for i in range(nk):
    mp.verbosity(0) # Reset verbosity to minimal
    fre_tmp = sim_k_point_harminv(sim,kpoint[i])
    fre_kx.append(fre_tmp)
    print(f'{i}/{nk} \n')
    
#### analytic formula

# Frequency array in Meep units (f = c/a)
f_ls = np.linspace(0.1, 4, 100)  # Adjust range if not in Meep units
k_ls = f_ls*sx
# Function to compute epsilon for silver at a given frequency
def epsilon_Ag(f):
    """
    Compute the dielectric function epsilon for silver at frequency f (Meep units).
    Args:
        f (float): Frequency in Meep units (c/a).
    Returns:
        complex: Dielectric function epsilon(f).
    """
    eps_tensor = Ag.epsilon(f)
    return eps_tensor[0][0]  # Scalar epsilon for isotropic material

# Compute epsilon for each frequency in f_ls
epsilon_1 = np.array([epsilon_Ag(f) for f in f_ls])
k_spp = np.real(np.sqrt( epsilon_1/(1+epsilon_1 )))  * f_ls * sx
# omega_spp = np.sqrt( np.real(epsilon_1+1)/np.real(epsilon_1 )) * k_ls/sx

########################################
import matplotlib
matplotlib.use('Agg')  # Set Agg backend
fig = plt.figure(dpi=100, figsize=(5, 5))
ax = plt.subplot(111)
for i in range(nk):
    for ii in range(len(fre_kx[i])):
        plt.scatter(kpoint[i]*sx, fre_kx[i][ii], color="green",marker='.')

ax.fill_between(kpoint,  kpoint/sx, 5.0, interpolate=True, color="blue", alpha=0.2)
plt.plot(k_ls,f_ls,'k')
plt.plot(k_spp,f_ls,'r')
plt.xlim(0, 0.5)
plt.ylim(0, 4)
plt.grid(True)
plt.xlabel("$k_x(2\pi/s_x)$")
plt.ylabel("$\omega(2\pi c)$")
plt.tight_layout()

# Define the base filename
base_filename = "disp_SPP.png"
filename = base_filename
counter = 1

# Check if file exists and modify filename if necessary
while os.path.exists(filename):
    filename = f"disp_SPP_{counter}.png"
    counter += 1

# Save the figure
plt.savefig(filename, bbox_inches='tight')
plt.close(fig)  # Close to free memory


