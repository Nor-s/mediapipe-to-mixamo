from tokenize import group
import glm
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import json
import matplotlib.animation as animation
from IPython.display import clear_output
import ntpath
import os
from sympy import symbols, Eq, solve
from mixamo_helper import get_idx_group
import copy


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
            dot_group['z'].append(vec_list[idx][1])
        dots.append(dot_group)
    return dots


def draw_list(vec_list=[], group_lists=[[]], azim=10, range=1.0):
    ax1 = plt.axes(projection='3d')
    set_axes(ax1, elev=10, azim=azim, xrange=range, yrange=range, zrange=range)
    dots = get_dot(vec_list, group_lists)
    for dot in dots:
        ax1.plot(dot['x'], dot['y'], dot['z'], marker='o')

    plt.show()


def glm_list_to_gif(glm_list, idx_group=[], fps=24, save_path='.', range=1.0):
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    if len(idx_group) is 0:
        idx_group = get_idx_group()

    dots = get_dot(glm_list, idx_group)

    def update(idx):
        ax.clear()

        for dot in dots:
            ax.plot(dot['x'], dot['y'], dot['z'], marker='o')

        set_axes(ax, idx, xrange=range, yrange=range, zrange=range)

    ani = animation.FuncAnimation(fig, update, frames=360, interval=fps)
    if save_path[-1] == '/':
        save_path = save_path[0: -1]
    filename = save_path + '/' + 'glm'
    outputpath = filename + '_360.gif'
    uniq = 1
    while os.path.exists(outputpath):
        outputpath = '%s(%d)_360.gif' % (filename, uniq)
        uniq += 1
    ani.save(outputpath, writer='pillow')


def glm_lists_to_gif(glm_lists, idx_group=[], fps=24, save_path='.', is_axes_move=False):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    frames = len(glm_lists)
    if len(idx_group) is 0:
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


class Gizmo:
    def __init__(self, r=glm.vec3(0.0, 0.0, 0.0),
                 x=glm.vec3(1.0, 0.0, 0.0),
                 y=glm.vec3(0.0, 1.0, 0.0),
                 z=glm.vec3(0.0, 0.0, 1.0)):
        self.r = r
        self.x = x
        self.y = y
        self.z = z

    def rotate(self, transform_mat):
        r = transform_mat * self.r
        x = transform_mat * self.x
        y = transform_mat * self.y
        z = transform_mat * self.z
        return Gizmo(r, x, y, z)

    def get_origin(self):
        return self.r

    def get_local_pos(self, world_pos):
        a, b, c = symbols("a b c")
        equation_1 = Eq((self.r.x + a*self.x.x + b *
                        self.y.x + c * self.z.x), world_pos.x)
        equation_2 = Eq((self.r.y + a*self.x.y + b *
                        self.y.y + c * self.z.y), world_pos.y)
        equation_3 = Eq((self.r.z + a*self.x.z + b *
                        self.y.z + c * self.z.z), world_pos.z)

        solution = solve((equation_1, equation_2, equation_3), (a, b, c))
        return glm.vec3(solution.a, solution.b, solution.c)


def pixel3d_json_to_glm_vec(pixel3d_json):
    return glm.vec3(pixel3d_json['x'], pixel3d_json['y'], pixel3d_json['z'])


def pixel3d_json_to_glm_quat(pixel3d_json):
    return glm.quat(w=pixel3d_json['w'], x=pixel3d_json['x'], y=pixel3d_json['y'], z=pixel3d_json['z'])


class ModelNode:
    def __init__(self, gizmo=Gizmo()):
        self.child = []
        self.gizmo = gizmo
        self.name = ""
        self.position = glm.vec3(x=0.0, y=0.0, z=0.0)
        self.scale = glm.vec3(x=1.0, y=1.0, z=1.0)
        self.rotate = glm.quat(w=1.0, x=0.0, y=0.0, z=0.0)

    def set_pixel3d(self, pixel3d_node_json):
        self.name = pixel3d_node_json["name"]
        self.position = pixel3d_json_to_glm_vec(pixel3d_node_json["position"])
        self.rotate = pixel3d_json_to_glm_quat(pixel3d_node_json["rotation"])
        self.scale = pixel3d_json_to_glm_vec(pixel3d_node_json["scale"])
        for child in pixel3d_node_json["child"]:
            new_node = ModelNode()
            new_node.set_pixel3d(child)
            self.child.append(new_node)

    def get_transform(self):
        pos = glm.translate(glm.mat4(1.0), self.position)
        rot = pos * glm.mat4(self.rotate)
        scale = glm.scale(rot, self.scale)
        return scale

    def get_gizmo(self, parent_transform):
        return self.gizmo.rotate(parent_transform*self.get_transform())

    def get_vec_and_group_list(self, result_vec_list, result_group_list, parent_transform=glm.mat4(1.0),  group_list=[]):

        if self.name != 'RootNode':
            result_vec_list.append(self.get_gizmo(
                parent_transform).get_origin())
            group_list.append(len(result_vec_list) - 1)

        if len(self.child) is 0:
            result_group_list.append(copy.deepcopy(group_list))
            group_list.clear()
            return

        for child in self.child:
            child.get_vec_and_group_list(
                result_vec_list, result_group_list, group_list=group_list, parent_transform=copy.deepcopy(parent_transform*self.get_transform()))


class BindingPose:
    pass
