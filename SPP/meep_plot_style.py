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

def label_plot(ax, title=None, xlabel=None, ylabel=None, elapsed=None):
    """
    Add a title and x/y labels to the plot.
    """
    if title:
        ax.set_title(title)
    elif elapsed is not None:
        ax.set_title(f'{elapsed:0.1f} fs')
    if xlabel is not False:
        ax.set_xlabel('x (μm)'if xlabel is None else xlabel)
    if ylabel is not False:
        ax.set_ylabel('y (μm)'if ylabel is None else ylabel)

def plot_eps_data(eps_data, domain, ax=None, **kwargs):
    """
    Plot the wall geometry (dielectric data) within the domain.
    """
    ax = ax or plt.gca()
    ax.imshow(eps_data.T, cmap=cmap_alpha, extent=domain, origin='lower')
    label_plot(ax, **kwargs)

def plot_ez_data(ez_data, domain, ax=None, vmax=None, aspect=None, **kwargs):
    """
    Plot the amplitude of the complex-valued electric field
    data within the domain.
    """
    ax = ax or plt.gca()
    ax.imshow(
        np.abs(ez_data.T),
        interpolation='spline36',
        cmap=cmap_blue,
        extent=domain,
        vmax=vmax,
        aspect=aspect,
        origin='lower',
        )
    label_plot(ax, **kwargs)

def plot_pml(pml_thickness, domain, ax=None):
    ax = ax or plt.gca()
    x_start = domain[0] + pml_thickness
    x_end = domain[1] - pml_thickness
    y_start = domain[2] + pml_thickness
    y_end = domain[3] - pml_thickness
    rect = plt.Rectangle(
        (x_start, y_start),
        x_end - x_start,
        y_end - y_start,
        fill=None,
        color='#fff',
        linestyle='dashed',
        )
    ax.add_patch(rect)