## Define a color map
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

colors = ["darkslateblue","blue", "black", "red","maroon"]
nodes = [0.0,0.35, 0.5, 0.65, 1.0]
mycmap = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))

colors1 = ["red","violet", "black", "lime","blue"]
nodes1 = [0.0,0.25, 0.5, 0.75, 1.0]
mycmap1 = LinearSegmentedColormap.from_list("mycmap1", list(zip(nodes1, colors1)))

colors2 = ["white","cyan","blue","red","yellow"]
nodes2 = [0.0,0.25, 0.5, 0.75, 1.0]
mycmap2 = LinearSegmentedColormap.from_list("mycmap2", list(zip(nodes2, colors2)))

colors3 = ["red","violet", "white", "lime","blue"]
nodes3 = [0.0,0.25, 0.5, 0.75, 1.0]
bicmap = LinearSegmentedColormap.from_list("mycmap3", list(zip(nodes3, colors3)))