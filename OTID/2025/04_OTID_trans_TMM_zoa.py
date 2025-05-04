import numpy as np
import matplotlib.pyplot as plt

def calculate_transmittance(wavelength, thicknesses, epsilon_1, epsilon_2):
    """
    Calculate transmittance through a 10-layer ABABABABAB structure.
    
    Parameters:
    wavelength : float
        Wavelength of incident light (in meters)
    thicknesses : list or array
        Array of 10 layer thicknesses [d1, d2, ..., d10] (in meters)
    epsilon_1 : float
        Permittivity of material A
    epsilon_2 : float
        Permittivity of material B
    
    Returns:
    float : Transmittance (0 to 1)
    """
    
    # Check input validity
    if len(thicknesses) != 10:
        raise ValueError("Exactly 10 layer thicknesses must be provided")
    
    # Constants
    c = 2.99792458e8  # speed of light in m/s
    omega = 2 * np.pi * c / wavelength  # angular frequency
    
    # Refractive indices
    n1 = np.sqrt(epsilon_1)
    n2 = np.sqrt(epsilon_2)
    n0 = 1.0  # air (incident)
    n_sub = 1.0  # air (substrate)
    
    # Layer properties (ABABABABAB)
    ns = [n1, n2] * 5
    
    # Initialize total transfer matrix
    M_total = np.eye(2, dtype=complex)
    
    # Build total transfer matrix
    for i in range(10):
        n_current = ns[i]
        d = thicknesses[i]
        
        # Phase thickness
        delta = omega * n_current * d / c
        
        # Interface matrix
        if i == 0:
            n_prev = n0
        else:
            n_prev = ns[i-1]
            
        T_interface = np.array([
            [1/(2*n_prev)*(n_current + n_prev), 1/(2*n_prev)*(n_current - n_prev)],
            [1/(2*n_prev)*(n_current - n_prev), 1/(2*n_prev)*(n_current + n_prev)]
        ])
        
        # Propagation matrix
        P = np.array([
            [np.exp(1j * delta), 0],
            [0, np.exp(-1j * delta)]
        ])
        
        # Update total matrix   P2 T2 P1 T1  
        M_total = M_total  @ P @ T_interface
    
    # Final interface to substrate
    nf = ns[-1] # final layer n 
    T_final = np.array([
        [1/(2 * nf)*(n_sub + nf), 1/(2*nf)*(n_sub - nf)],
        [1/(2 * nf)*(n_sub - nf), 1/(2*nf)*(n_sub + nf)]
    ])
    
    M_total = T_final @ M_total 
    
    # Transmission coefficient
    t = 1 / M_total[0,0] # python begins with 0
    
    # Transmittance T = np.abs(t)**2 * n_sub / n0
    T = np.abs(t)**2 * n_sub / n0
    
    return T.real

########################
########################
# Parameters
lambda0 = 500e-9  # 500 nm
d = [120e-9] * 10  # 50 nm each layer
# d = [600e-9, 0, 0, 0, 0, 0, 0, 0, 0, 0] # single layer for test
eps1 = 11.7# 
eps2 = 3.9   # 
# Calculate
T = calculate_transmittance(lambda0, d, eps1, eps2)
print(f'Transmittance: {T:.4f}')
#######################
#######################
# target  transmission
target_wl = np.linspace(600e-9,700e-9,21)
target_trans = np.zeros(21)
target_trans[8] = 1 
target_trans[16] = 1
target_trans[0] = 1 

#  figure of merit
def fom(thicknesses):
    lw = len(target_wl)
    trans = np.zeros(lw)
    for i in range(lw):
        trans[i] = calculate_transmittance(target_wl[i], thicknesses, eps1, eps2)
    output = np.sum((trans - target_trans)**2)/lw
    return output

#####################
#####################
# Zebra Optimization Algorithm
# pip install --upgrade mealpy
from mealpy.swarm_based import ZOA
from mealpy import FloatVar

# Define your objective function
def objective_function(solution):
    return fom(solution)

# Define the problem
problem = {
    "bounds": FloatVar(lb=([0]*10) , ub=([300e-9]*10) , name="delta"),
    "minmax": "min",
    "obj_func": objective_function,
    "verbose": False
}

# Initialize the ZOA model
model = ZOA.OriginalZOA(epoch=100, pop_size=100)

# Solve the optimization problem
best_agent = model.solve(problem)
best_solution = best_agent.solution
best_fitness = best_agent.target.fitness


print(f"Best Solution: {best_solution}")
print(f"Best Fitness: {best_fitness}")

##########################################
# Extract the best fitness values per epoch from the history
best_fitness_per_epoch = model.history.list_global_best_fit
# Ensure the length matches the number of epochs
epochs = list(range(1, len(best_fitness_per_epoch) + 1))

# Plot the best fitness values as a function of epoch
plt.figure(figsize=(10, 6))
plt.plot(epochs, best_fitness_per_epoch,'-.', label='Best Fitness', color='blue')
plt.xlabel('Epoch')
plt.ylabel('Best Fitness Value')
plt.title('Best Fitness Value vs Epoch for ZOA')
plt.grid(True)
plt.xlim([0, len(best_fitness_per_epoch)])
plt.legend()
plt.savefig('history_zoa.png')
##########################################
# Wavelength sweep
wavelengths = np.linspace(600e-9, 700e-9, 21)  # 300-800 nm
transmittances = [calculate_transmittance(wl, best_solution, eps1, eps2) for wl in wavelengths]

# Plot
plt.figure(figsize=(10, 6))
plt.plot(wavelengths*1e9, transmittances, '-')
plt.plot(target_wl * 1e9, target_trans, '--')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Transmittance')
plt.ylim([0,1.05])
plt.title('Transmittance vs Wavelength')
plt.grid(True)
plt.savefig('filter_trans_zoa.png')
# save best d
from datetime import datetime

# Get current time and date
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Open file in append mode ('a')
with open('trans_TMM_zoa_d.txt', 'a') as f:
    # Format the output: timestamp followed by array
    str1 = 'fom=' + f'{best_fitness}'
    array_str = ' '.join([f'{x:.6e}' for x in best_solution])  # Formats numbers to 4 decimal places
    f.write(f'{current_time}   {str1}  {array_str}\n')

