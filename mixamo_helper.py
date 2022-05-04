import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import json
import matplotlib.animation as animation
from IPython.display import clear_output
import ntpath
import glm
import copy

mixamo_names = [
    ['Hips', 0, -1],  # left hip <->right hip
    ['Spine', 1, 0],
    ['Spine1', 2, 1],
    ['Spine2', 3, 2],

    ['Neck', 4, 3],  # left_shoulder <-> right_shoulder
    ['Head', 5, 4],  # left_ear <-> right_ear

    ['LeftArm', 6, 3, "left_shoulder"],
    ['LeftForeArm', 7, 6, "left_elbow"],
    ['LeftHand', 8, 7, "left_wrist"],
    ['LeftHandThumb1', 9, 8, "left_thumb"],
    ['LeftHandIndex1', 10, 9, "left_index"],
    ['LeftHandPinky1', 11, 10, "left_pinky"],

    ['RightArm', 12, 3, "right_shoulder"],
    ['RightForeArm', 13, 12, "right_elbow"],
    ['RightHand', 14, 13, "right_wrist"],
    ['RightHandThumb1', 15, 14, "right_thumb"],
    ['RightHandIndex1', 16, 15, "right_index"],
    ['RightHandPinky1', 17, 16, "right_pinky"],

    ['LeftLeg', 18, 0, "left_hip"],
    ['LeftUpLeg', 19, 18, "left_knee"],
    ['LeftFoot', 20, 19, "left_ankle"],
    ['LeftToeBase', 21, 20, "left_foot_index"],

    ['RightLeg', 22, 0, "right_hip"],
    ['RightUpLeg', 23, 22, "right_knee"],
    ['RightFoot', 24, 23, "right_ankle"],
    ['RightToeBase', 25, 24, "right_foot_index"]
]


def set_axes(ax, azim=10, elev=10, xrange=1.0, yrange=1.0, zrange=1.0):
    ax.set_xlim(-xrange, xrange)
    ax.set_xlabel("-Z")
    ax.set_ylim(-yrange, yrange)
    ax.set_ylabel("X")
    ax.set_zlim(-zrange, zrange)
    ax.set_zlabel("-Y")
    ax.set_title('Mixamo')
    ax.view_init(elev=elev, azim=azim)


def get_frame_dot(json_object, fidx):
    dot1 = []
    size = len(json_object['frames'][fidx]['keypoints3D'])
    for idx in range(0, size):
        landmark = json_object['frames'][fidx]["keypoints3D"][idx]
        dot1.append([-landmark['z'], landmark['x'], -landmark['y']])
    return dot1

def get_mixamo_json_keypoints_with_color_and_mark_for_plot(json_object, fidx):
    dots = {
        'x': [],
        'y': [],
        'z': [],
        'color': None,
        'mark': 'o'
    }
    ret = []
    size = len(json_object['frames'][fidx]['keypoints3D'])
    for idx in range(0, size):
        landmark = json_object['frames'][fidx]["keypoints3D"][idx]
        dots['x'].append(-landmark['z'])
        dots['y'].append(landmark['x'])
        dots['z'].append(-landmark['y'])
        if idx == 5:
            dots['color'] = 'r'
        elif idx == 11:  # left Arm
            dots['color']= 'g'
        elif idx == 17:  # right Arm
            dots['color']= 'b'
        elif idx == 21:  # left leg
            dots['color']= 'k'
        elif idx == size -1:
            dots['color']= 'm'
        if dots['color'] != None:
            ret.append(dots)
            dots = {
                'x': [],
                'y': [],
                'z': [],
                'color': None,
                'mark': 'o'
            }
    return ret


def get_mixamo_json_keypoints_with_color_and_mark(json_object, fidx):
    dot1 = []
    size = len(json_object['frames'][fidx]['keypoints3D'])
    for idx in range(0, size):
        landmark = json_object['frames'][fidx]["keypoints3D"][idx]
        dot1.append([-landmark['z'], landmark['x'], -landmark['y']])
        if idx <= 5:
            dot1[idx].append('r')
        elif idx <= 11:  # left Arm
            dot1[idx].append('g')
        elif idx <= 17:  # right Arm
            dot1[idx].append('b')
        elif idx <= 21:  # left leg
            dot1[idx].append('k')
        else:
            dot1[idx].append('m')
        dot1[idx].append('o')
    return dot1


def draw_mixamo(json_object, fidx, azim=10):
    dot1 = get_mixamo_json_keypoints_with_color_and_mark_for_plot(json_object, fidx)
    ax1 = plt.axes(projection='3d')
    set_axes(ax1, elev=10, azim=azim)
    for x in dot1:
        ax1.scatter(x['x'], x['y'], x['z'], c=x['color'], marker=x['mark'])
        ax1.plot(x['x'], x['y'], x['z'], color= x['color'])
    plt.show()


def draw_list(json_object, fidx, draw_lists=[[0, 1, 2, 3, 4, 5]], azim=10, range=1.0):
    dot1 = get_mixamo_json_keypoints_with_color_and_mark(json_object, fidx)
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
            dot_group['x'].append(dot1[idx][0])
            dot_group['y'].append(dot1[idx][1])
            dot_group['z'].append(dot1[idx][2])
        dots.append(dot_group)

    for dot in dots:
        ax1.plot(dot['x'], dot['y'], dot['z'], marker='o')
        
    plt.show()


def json_one_frame_to_360_gif(json_object, frame_idx, save_path='.'):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    frame = get_mixamo_json_keypoints_with_color_and_mark_for_plot(json_object, frame_idx)

    def update_round(i):
        set_axes(ax, i, 10)
    ax.clear()
    for plist in frame:
        ax.scatter3D(plist['x'], plist['y'], plist['z'], c= plist['color'], marker= plist['mark'])
        ax.plot(plist['x'], plist['y'], plist['z'], color= plist['color'])
    ani = animation.FuncAnimation(
        fig, update_round, frames=360, interval=json_object["ticksPerSecond"])
    if save_path[-1] == '/':
        save_path = save_path[0: -1]
    ani.save(save_path + '/' + ntpath.basename(
        json_object['fileName']) + '_json_mm_1frame.gif', writer='pillow')


def json_to_gif(json_object, save_path='.', max_frame_num=100, is_axes_move=False):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    frames = min(len(json_object["frames"]), max_frame_num)

    def update(idx):
        ax.clear()
        frame = get_mixamo_json_keypoints_with_color_and_mark_for_plot(json_object, idx)
        for plist in frame:
            ax.scatter3D(plist['x'], plist['y'], plist['z'], c= plist['color'], marker= plist['mark'])
            ax.plot(plist['x'], plist['y'], plist['z'], color= plist['color'])
        if is_axes_move:
            set_axes(ax, idx)
        else:
            set_axes(ax, 0)

    ani = animation.FuncAnimation(
        fig, update, frames=frames, interval=json_object["ticksPerSecond"])
    if save_path[-1] == '/':
        save_path = save_path[0: -1]
    if is_axes_move:
        ani.save(save_path + '/' + ntpath.basename(
            json_object['fileName']) + '_json_mm_round_.gif', writer='pillow')
    else:
        ani.save(save_path + '/' + ntpath.basename(
            json_object['fileName']) + '_json_mm_.gif', writer='pillow')


def get_mixamo_name_mediapipe_name_map():
    mixamo_name_mediapipe_name_map = {}
    for idx in range(6, len(mixamo_names)):
        mixamo_name_mediapipe_name_map[mixamo_names[idx]
                                       [0]] = mixamo_names[idx][3]
    return mixamo_name_mediapipe_name_map


def get_mixamo_name_idx_map():
    mixamo_name_idx_map = {}
    for name in mixamo_names:
        mixamo_name_idx_map[name[0]] = name[1]
    return mixamo_name_idx_map

def frame_json_to_glm_vec_list(json_object, frame_idx):
    glm_list = []
    visibility_list = []
    parent_list = []
    frame_json = json_object['frames'][frame_idx]['keypoints3D'];
    for frame in frame_json:
        glm_list.append(glm.vec3(frame['x'], frame['y'], frame['z']))
        visibility_list.append(frame['score'])
        parent_list.append(frame['parent'])
    return [glm_list, visibility_list, parent_list]

def get_idx_group():
    ret = []
    before_parent = -2
    idx_stack = []
    for name in mixamo_names:
        if before_parent > name[2]:
            ret.append(copy.deepcopy(idx_stack))
            idx_stack.clear()
        idx_stack.append(name[1])
        before_parent = name[2]
    ret.append(idx_stack)
    return ret