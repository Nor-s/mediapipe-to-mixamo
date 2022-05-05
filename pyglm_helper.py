import glm
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import json
import matplotlib.animation as animation
from IPython.display import clear_output
import ntpath
import os

from mixamo_helper import get_idx_group


def set_axes(ax, azim=10, elev=10, xrange=1.0, yrange=1.0, zrange=1.0):
    ax.set_xlim(-xrange, xrange)
    ax.set_xlabel("-Z")
    ax.set_ylim(-yrange, yrange)
    ax.set_ylabel("X")
    ax.set_zlim(-zrange, zrange)
    ax.set_zlabel("-Y")
    ax.set_title('Vector')
    ax.view_init(elev=elev, azim=azim)


def get_dot(vec_list, group_lists):
    dots = []
    for group_list in group_lists:
        dot_group = {
            'x': [],
            'y': [],
            'z': []
        }
        for idx in group_list:
            dot_group['x'].append(-vec_list[idx][2])
            dot_group['y'].append(vec_list[idx][0])
            dot_group['z'].append(-vec_list[idx][1])
        dots.append(dot_group)
    return dots


def draw_list(vec_list=[], group_lists=[[]], azim=10, range=1.0):
    ax1 = plt.axes(projection='3d')
    set_axes(ax1, elev=10, azim=azim, xrange=range, yrange=range, zrange=range)
    dots = get_dot(vec_list, group_lists)
    for dot in dots:
        ax1.plot(dot['x'], dot['y'], dot['z'], marker='o')

    plt.show()


def glm_list_to_gif(glm_lists, fps=24, save_path='.', is_axes_move=False):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    frames = len(glm_lists)
    idx_group = get_idx_group()

    def update(idx):
        ax.clear()
        dots = get_dot(glm_lists[idx], idx_group)

        for dot in dots:
            ax.plot(dot['x'], dot['y'], dot['z'], marker='o')

        if is_axes_move:
            set_axes(ax, idx)
        else:
            set_axes(ax, 0)

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=fps)
    if save_path[-1] == '/':
        save_path = save_path[0: -1]
    filename = save_path + '/' + 'glm'
    if is_axes_move:
        filename += '_round'
    outputpath = filename + '.gif'
    uniq = 1
    while os.path.exists(outputpath):
        outputpath = '%s(%d).gif' % (filename, uniq)
        uniq += 1
    ani.save(outputpath, writer='pillow')
