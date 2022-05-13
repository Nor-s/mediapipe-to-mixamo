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
from mixamo_helper import get_idx_group, get_mixamo_name_idx_map, Mixamo, frame_json_to_glm_vec_list
import copy
import math


def set_axes(ax, azim=10, elev=10, xrange=1.0, yrange=1.0, zrange=1.0):
    ax.set_xlabel("-Z")
    ax.set_ylabel("X")
    ax.set_zlabel("Y")
    ax.set_title('Vector')
    if xrange > 0.0:
        ax.set_xlim(-xrange, xrange)
        ax.set_ylim(-yrange, yrange)
        ax.set_zlim(-zrange, zrange)
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

    if len(idx_group) == 0:
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
    if len(idx_group) == 0:
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


def find_2d_angle(cx, cy, ex, ey):
    dy = ey - cy
    dx = ex - cx
    theta = math.atan2(dy, dx)
    return theta


class Gizmo:
    def __init__(self, r=glm.vec3(0.0, 0.0, 0.0),
                 x=glm.vec3(1.0, 0.0, 0.0),
                 y=glm.vec3(0.0, 1.0, 0.0),
                 z=glm.vec3(0.0, 0.0, 1.0)):
        self.r = r
        self.x = x
        self.y = y
        self.z = z

    def set_origin(self, r=glm.vec3(0.0, 0.0, 0.0)):
        self.r = r

    def rotate(self, transform_mat):
        r = transform_mat * self.r
        x = transform_mat * self.x
        y = transform_mat * self.y
        z = transform_mat * self.z
        return Gizmo(r, x, y, z)

    def calc_rotation_matrix(self, world_start, world_end):
        local_point1 = glm.normalize(self.get_local_pos(world_start))
        local_point2 = glm.normalize(self.get_local_pos(world_end))
        # print(glm.cross(local_point1, local_point2))
        return glm.rotate(glm.mat4(1.0),
                          glm.acos(glm.dot(local_point1, local_point2)),
                          glm.cross(local_point1, local_point2))

    def calc_roll(self, world_start, world_end):
        local_point1 = glm.normalize(self.get_local_pos(world_start))
        local_point2 = glm.normalize(self.get_local_pos(world_end))
        local_point1.x = 0
        local_point2.x = 0
        return glm.rotate(glm.mat4(1.0),
                          glm.acos(glm.dot(local_point1, local_point2)),
                          glm.cross(local_point1, local_point2))

    # def calc_roll(self, world_start, world_end):

    def get_origin(self):
        return self.r

    def get_local_pos(self, world_pos):
        a, b, c = symbols("a,b,c")
        equation_1 = Eq((self.r.x + a*self.x.x + b *
                         self.y.x + c * self.z.x), world_pos.x)
        equation_2 = Eq((self.r.y + a*self.x.y + b *
                         self.y.y + c * self.z.y), world_pos.y)
        equation_3 = Eq((self.r.z + a*self.x.z + b *
                         self.y.z + c * self.z.z), world_pos.z)

        solution = solve([equation_1, equation_2, equation_3],
                         [a, b, c], dict=True)
        return glm.vec3(solution[0][a], solution[0][b], solution[0][c])


def pixel3d_json_to_glm_vec(pixel3d_json):
    return glm.vec3(pixel3d_json['x'], pixel3d_json['y'], pixel3d_json['z'])


def pixel3d_json_to_glm_quat(pixel3d_json):
    return glm.quat(w=pixel3d_json['w'], x=pixel3d_json['x'], y=pixel3d_json['y'], z=pixel3d_json['z'])


def glm_vec3_to_json(vec):
    return {"x": vec.x, "y": vec.y, "z": vec.z}


def glm_quat_to_json(quat):
    return {"w": quat.w, "x": quat.x, "y": quat.y, "z": quat.z}


def decompose(matrix: glm.mat4):
    scale = glm.vec3()
    rotation = glm.quat()
    translation = glm.vec3()
    skew = glm.vec3()
    perspective = glm.vec4()
    glm.decompose(matrix, scale, rotation, translation, skew, perspective)
    return [translation, rotation, scale]


def calc_transform(position, rotation, scale):
    pos = glm.translate(glm.mat4(1.0), position)
    rot = pos * glm.mat4(rotation)
    return glm.scale(rot, scale)


def calc_hip_transform_1(mixamo_list, hips_gizmo, left_up_leg_gizmo, spine_gizmo):
    transform = hips_gizmo.calc_rotation_matrix(
        left_up_leg_gizmo.get_origin(), mixamo_list[Mixamo.LeftUpLeg])

    hip_gizmo_r = hips_gizmo.rotate(transform)

    roll = hip_gizmo_r.calc_roll(
        transform*spine_gizmo.get_origin(), mixamo_list[Mixamo.Spine])
    return transform * roll


def calc_hip_transform(mixamo_list, hips_node, left_up_leg_node, spine_node):
    hip_gizmo = hips_node.get_gizmo()
    left_up_leg_gizmo = left_up_leg_node.get_gizmo(hips_node.get_transform())
    spine_gizmo = spine_node.get_gizmo(hips_node.get_transform())

    return calc_hip_transform_1(mixamo_list, hip_gizmo, left_up_leg_gizmo, spine_gizmo)


class ModelNode:
    def __init__(self, gizmo=Gizmo()):
        self.child = []
        self.gizmo = gizmo
        self.name = ""
        self.position = glm.vec3(x=0.0, y=0.0, z=0.0)
        self.scale = glm.vec3(x=1.0, y=1.0, z=1.0)
        self.rotate = glm.quat(w=1.0, x=0.0, y=0.0, z=0.0)

        self.tmp_transform = glm.mat4(1.0)

    def find_node(self, name):
        if self.name == name:
            return [True, self]
        for child in self.child:
            is_find, node = child.find_node(name)
            if is_find:
                return [True, node]
        return [False, None]

    def set_pixel3d(self, pixel3d_node_json):
        self.name = pixel3d_node_json["name"]
        self.position = pixel3d_json_to_glm_vec(pixel3d_node_json["position"])
        self.rotate = pixel3d_json_to_glm_quat(pixel3d_node_json["rotation"])
        self.scale = pixel3d_json_to_glm_vec(pixel3d_node_json["scale"])
        for child in pixel3d_node_json["child"]:
            new_node = ModelNode()
            new_node.set_pixel3d(child)
            self.child.append(new_node)

    def init_model_node(self):
        mixamo_idx_map = get_mixamo_name_idx_map()

    def set_mixamo(self, pix3d_node_json, mixamo_idx_map, before_transform=None):
        self.name = pix3d_node_json["name"]
        self.position = pixel3d_json_to_glm_vec(
            pix3d_node_json["position"])
        self.rotate = pixel3d_json_to_glm_quat(pix3d_node_json["rotation"])
        self.scale = pixel3d_json_to_glm_vec(pix3d_node_json["scale"])
        if before_transform != None:
            self.position, self.rotate, self.scale = decompose(
                before_transform*self.get_transform())
        if self.name == Mixamo.LeftUpLeg.name or self.name == Mixamo.RightUpLeg.name:
            self.position.y = 0
            self.position.z = 0

        # find child
        list = pix3d_node_json["child"]
        transform_list = [None for i in range(len(list))]
        transform_list_idx = -1

        for child in list:
            transform_list_idx += 1
            if child['name'] in mixamo_idx_map:
                new_node = ModelNode()
                new_node.set_mixamo(child, mixamo_idx_map, copy.deepcopy(
                    transform_list[transform_list_idx]))
                self.child.append(new_node)
            else:
                for child_of_child in child["child"]:
                    list.append(child_of_child)
                    position = pixel3d_json_to_glm_vec(child["position"])
                    rotation = pixel3d_json_to_glm_quat(child["rotation"])
                    scale = pixel3d_json_to_glm_vec(child["scale"])
                    transform = calc_transform(position, rotation, scale)
                    transform_list.append(transform)

    def normalize(self, mixamo_list, mixamo_idx_map, len=0.0):
        if self.name == "Hips":
            self.position = mixamo_list[mixamo_idx_map[self.name]]
        else:
            n_position = glm.normalize(self.position)
            self.position = len*n_position

        for child in self.child:

            a = mixamo_list[mixamo_idx_map[self.name]]
            b = mixamo_list[mixamo_idx_map[child.name]]
            new_len = glm.distance(a, b)
            child.normalize(mixamo_list, mixamo_idx_map, new_len)

    def find_child(self, name):
        for child in self.child:
            if child.name == name:
                return child
        return None

    def calc_animation(self, mixamo_list, mixamo_idx_map, parent_transform=glm.mat4(1.0), world_mixamo_adjust=glm.vec3(0.0, 0.0, 0.0)):
        self.tmp_transform = glm.mat4(1.0)
        if self.name == "Hips":
            self.tmp_transform = calc_hip_transform(mixamo_list,
                                                    self,
                                                    self.find_child(
                                                        Mixamo.LeftUpLeg.name),
                                                    self.find_child(Mixamo.Spine.name))
        elif len(self.child) > 0:
            current_gizmo = self.get_gizmo(parent_transform)
            target_node = self.child[0]
            target_gizmo = target_node.get_gizmo(
                parent_transform*self.get_transform())
            target_vec = world_mixamo_adjust + \
                mixamo_list[mixamo_idx_map[target_node.name]]
            self.tmp_transform = current_gizmo.calc_rotation_matrix(
                target_gizmo.get_origin(), target_vec)

        for child in self.child:
            adjust_vec = child.get_gizmo(
                parent_transform*self.get_transform()*self.tmp_transform).get_origin()
            adjust_vec -= (world_mixamo_adjust +
                           mixamo_list[mixamo_idx_map[child.name]])
            child.calc_animation(mixamo_list, mixamo_idx_map,
                                 parent_transform*self.get_transform()*self.tmp_transform, world_mixamo_adjust=adjust_vec)

    def get_transform(self):
        return calc_transform(self.position, self.rotate, self.scale)

    def get_gizmo(self, parent_transform=glm.mat4(1.0)):
        return self.gizmo.rotate(parent_transform*self.get_transform())

    def get_gizmo_apply_tmp(self, parent_transform=glm.mat4(1.0)):
        return self.gizmo.rotate(parent_transform*self.get_transform()*self.tmp_transform)

    def get_vec_and_group_list(self, result_vec_list, result_group_list, parent_transform=glm.mat4(1.0),  group_list=[], is_apply_tmp_transform=False):
        if is_apply_tmp_transform:
            result_vec_list.append(self.get_gizmo_apply_tmp(
                parent_transform).get_origin())
        else:
            result_vec_list.append(self.get_gizmo(
                parent_transform).get_origin())

        group_list.append(len(result_vec_list) - 1)

        if len(self.child) == 0:
            result_group_list.append(copy.deepcopy(group_list))
            group_list.clear()
            return

        for child in self.child:
            if is_apply_tmp_transform:
                child.get_vec_and_group_list(
                    result_vec_list, result_group_list, group_list=group_list, parent_transform=copy.deepcopy(parent_transform*self.get_transform() * self.tmp_transform), is_apply_tmp_transform=is_apply_tmp_transform)
            else:
                child.get_vec_and_group_list(
                    result_vec_list, result_group_list, group_list=group_list, parent_transform=copy.deepcopy(parent_transform*self.get_transform()), is_apply_tmp_transform=is_apply_tmp_transform)

    def tmp_to_json(self, bones_json):
        [t, r, s] = decompose(self.tmp_transform)
        bone_json = {
            "name": self.name,
            "rotation": glm_quat_to_json(r),
            "position": glm_vec3_to_json(t),
            "scale": glm_vec3_to_json(s)
        }
        bones_json["bones"].append(bone_json)
        for child in self.child:
            child.tmp_to_json(bones_json)


def get_anim_frame_json(anim_json_object,  fidx, hip_node, mixamo_name_idx_map):
    bones_json = {
        "time": fidx,
        "bones": []
    }
    glm_list, visibility_list, parent_list = frame_json_to_glm_vec_list(
        anim_json_object, fidx)
    root_node = ModelNode()
    root_node.set_mixamo(hip_node, mixamo_name_idx_map)
    root_node.normalize(glm_list, mixamo_name_idx_map)
    root_node.calc_animation(glm_list, mixamo_name_idx_map)
    root_node.tmp_to_json(bones_json)
    return bones_json
