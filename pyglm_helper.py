import glm
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import json
import matplotlib.animation as animation
from IPython.display import clear_output
import ntpath

def set_axes(ax, azim=10, elev=10, xrange=1.0, yrange=1.0, zrange=1.0):
    ax.set_xlim(-xrange, xrange)
    ax.set_xlabel("-Z")
    ax.set_ylim(-yrange, yrange)
    ax.set_ylabel("X")
    ax.set_zlim(-zrange, zrange)
    ax.set_zlabel("-Y")
    ax.set_title('Vector')
    ax.view_init(elev=elev, azim=azim)


def draw_list(vec_list = [], draw_lists=[[]], azim=10, range=1.0):
    ax1 = plt.axes(projection='3d')
    set_axes(ax1, elev=10, azim=azim, xrange=range, yrange=range, zrange=range)
    dots = []
    for draw_list in draw_lists: 
        dot_group = {
            'x': [],
            'y': [],
            'z': []
        }
        for idx in draw_list:
            dot_group['x'].append(-vec_list[idx][2])
            dot_group['y'].append(vec_list[idx][0])
            dot_group['z'].append(-vec_list[idx][1])
        dots.append(dot_group)

    for dot in dots:
        ax1.plot(dot['x'], dot['y'], dot['z'], marker='o')
        
    plt.show()