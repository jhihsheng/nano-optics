from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import numpy as np

# Increase the default resolution for images
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 100

# Plot everything on a dark background
plt.style.use('dark_background')

# Some custom colormaps
cmap_alpha = LinearSegmentedColormap.from_list(
    'custom_alpha', [[1, 1, 1, 0], [1, 1, 1, 1]])
cmap_blue = LinearSegmentedColormap.from_list(
    'custom_blue', [[0, 0, 0], [0, 0.66, 1], [1, 1, 1]])
cmap_br = LinearSegmentedColormap.from_list(
    'custom_br', [[1,0.1,0],[1,0.66,0.1],[0, 0, 0], [0.1, 0.66, 1],[0, 0.1, 1]])
