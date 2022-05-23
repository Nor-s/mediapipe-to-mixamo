import matplotlib.pyplot as plt
import matplotlib.animation as animation
import ntpath
import glm
import copy
from enum import auto, IntEnum
import math


class Mixamo(IntEnum):
    Hips = 0
    Spine = auto()
    Spine1 = auto()
    Spine2 = auto()
    Neck = auto()
    Head = auto()
    LeftArm = auto()
    LeftForeArm = auto()
    LeftHand = auto()
    LeftHandThumb1 = auto()
    LeftHandIndex1 = auto()
    LeftHandPinky1 = auto()
    RightArm = auto()
    RightForeArm = auto()
    RightHand = auto()
    RightHandThumb1 = auto()
    RightHandIndex1 = auto()
    RightHandPinky1 = auto()
    LeftUpLeg = auto()
    LeftLeg = auto()
    LeftFoot = auto()
    LeftToeBase = auto()
    RightUpLeg = auto()
    RightLeg = auto()
    RightFoot = auto()
    RightToeBase = auto()


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
    ['LeftHandIndex1', 10, 8, "left_index"],
    ['LeftHandPinky1', 11, 8, "left_pinky"],

    ['RightArm', 12, 3, "right_shoulder"],
    ['RightForeArm', 13, 12, "right_elbow"],
    ['RightHand', 14, 13, "right_wrist"],
    ['RightHandThumb1', 15, 14, "right_thumb"],
    ['RightHandIndex1', 16, 14, "right_index"],
    ['RightHandPinky1', 17, 14, "right_pinky"],

    ['LeftUpLeg', 18, 0, "left_hip"],
    ['LeftLeg', 19, 18, "left_knee"],
    ['LeftFoot', 20, 19, "left_ankle"],
    ['LeftToeBase', 21, 20, "left_foot_index"],

    ['RightUpLeg', 22, 0, "right_hip"],
    ['RightLeg', 23, 22, "right_knee"],
    ['RightFoot', 24, 23, "right_ankle"],
    ['RightToeBase', 25, 24, "right_foot_index"]
]


def set_axes(ax, azim=10, elev=10, xrange=1.0, yrange=1.0, zrange=1.0):
    ax.set_xlim(-xrange, xrange)
    ax.set_xlabel("Z")
    ax.set_ylim(-yrange, yrange)
    ax.set_ylabel("X")
    ax.set_zlim(-zrange, zrange)
    ax.set_zlabel("Y")
    ax.set_title('Mixamo')
    ax.view_init(elev=elev, azim=azim)


def get_frame_dot(json_object, fidx):
    dot1 = []
    size = len(json_object['frames'][fidx]['keypoints3D'])
    for idx in range(0, size):
        landmark = json_object['frames'][fidx]["keypoints3D"][idx]
        dot1.append([landmark['z'], landmark['x'], landmark['y']])
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
        dots['x'].append(landmark['z'])
        dots['y'].append(landmark['x'])
        dots['z'].append(landmark['y'])
        if idx == 5:
            dots['color'] = 'r'
        elif idx == 11:  # left Arm
            dots['color'] = 'g'
        elif idx == 17:  # right Arm
            dots['color'] = 'b'
        elif idx == 21:  # left leg
            dots['color'] = 'k'
        elif idx == size - 1:
            dots['color'] = 'm'
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
        dot1.append([landmark['z'], landmark['x'], landmark['y']])
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
    dot1 = get_mixamo_json_keypoints_with_color_and_mark_for_plot(
        json_object, fidx)
    ax1 = plt.axes(projection='3d')
    set_axes(ax1, elev=10, azim=azim)
    for x in dot1:
        ax1.scatter(x['x'], x['y'], x['z'], c=x['color'], marker=x['mark'])
        ax1.plot(x['x'], x['y'], x['z'], color=x['color'])
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
    frame = get_mixamo_json_keypoints_with_color_and_mark_for_plot(
        json_object, frame_idx)

    def update_round(i):
        set_axes(ax, i, 10)
    ax.clear()
    for plist in frame:
        ax.scatter3D(plist['x'], plist['y'], plist['z'],
                     c=plist['color'], marker=plist['mark'])
        ax.plot(plist['x'], plist['y'], plist['z'], color=plist['color'])
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
        frame = get_mixamo_json_keypoints_with_color_and_mark_for_plot(
            json_object, idx)
        for plist in frame:
            ax.scatter3D(plist['x'], plist['y'], plist['z'],
                         c=plist['color'], marker=plist['mark'])
            ax.plot(plist['x'], plist['y'], plist['z'], color=plist['color'])
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
    frame_json = json_object['frames'][frame_idx]['keypoints3D']
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
            idx_stack.append(name[2])
        idx_stack.append(name[1])
        before_parent = name[2]
    ret.append(idx_stack)
    return ret


# Mediapipe To Mixamo
def avg3D(point1, point2):
    return [float(point1[0] + point2[0])/2.0,
            float(point1[1] + point2[1])/2.0,
            float(point1[2] + point2[2])/2.0,
            float(point1[3] + point2[3])/2.0]


def avgMixamoData(mediapipe_name_idx_map, mediapipeJsonObject, frameNum, name1, name2):
    left = mediapipeJsonObject[frameNum]["keypoints3D"][mediapipe_name_idx_map[name1]]
    right = mediapipeJsonObject[frameNum]["keypoints3D"][mediapipe_name_idx_map[name2]]
    x = float(left['x'] + right['x']) / 2.0
    y = float(left['y'] + right['y']) / 2.0
    z = float(left['z'] + right['z']) / 2.0
    score = (left['score'] + right['score']) / 2.0
    return [x, y, z, score]


def mediapipeToMixamoHip(mediapipe_name_idx_map, resultKeyPointsJsonObject, mediapipeJsonObject, frameNum):
    # left hip <->right hip
    x, y, z, score = avgMixamoData(mediapipe_name_idx_map,
                                   mediapipeJsonObject, frameNum, "left_hip", "right_hip")
    resultKeyPointsJsonObject["keypoints3D"].append({'x': 0.0,
                                                     'y': 0.0,
                                                     'z': 0.0,
                                                     'score': score,
                                                     'name': mixamo_names[0][0],
                                                     'parent': mixamo_names[0][2]})
    lefthip2d = mediapipeJsonObject[frameNum]["keypoints"][mediapipe_name_idx_map["left_hip"]]
    righthip2d = mediapipeJsonObject[frameNum]["keypoints"][mediapipe_name_idx_map["right_hip"]]
    resultKeyPointsJsonObject["keypoints"].append({'x': (lefthip2d['x'] + righthip2d['x']) / 2.0,
                                                   'y': (lefthip2d['y'] + righthip2d['y']) / 2.0,
                                                   'z': (lefthip2d['z'] + righthip2d['z']) / 2.0,
                                                   'score': (lefthip2d['score'] + righthip2d['score']) / 2.0,
                                                   'name': mixamo_names[0][0],
                                                   'len': math.sqrt((lefthip2d['x'] - righthip2d['x'])**2 + (lefthip2d['y'] - righthip2d['y'])**2 + (lefthip2d['z'] - righthip2d['z'])**2)
                                                   })
    return


def mediapipeToMixamoSpine(mediapipe_name_idx_map, resultKeyPointsJsonObject, mediapipeJsonObject, frameNum):
    # left_hip, right_hip, left_shoulder, right_shoulder
    hip = avgMixamoData(mediapipe_name_idx_map,
                        mediapipeJsonObject, frameNum, "left_hip", "right_hip")
    neck = avgMixamoData(mediapipe_name_idx_map, mediapipeJsonObject, frameNum,
                         "left_shoulder", "right_shoulder")
    spine2 = avg3D(hip, neck)
    spine1 = avg3D(hip, spine2)
    spine3 = avg3D(spine2, neck)
    spine = [spine1, spine2, spine3]
    for idx in range(0, len(spine)):
        resultKeyPointsJsonObject["keypoints3D"].append({'x': spine[idx][0],
                                                         'y': -spine[idx][1],
                                                         'z': -spine[idx][2],
                                                         'score': spine[idx][3],
                                                         'name': mixamo_names[idx+1][0],
                                                         'parent': mixamo_names[idx+1][2]})


def mediapipeToMixamoNeck(mediapipe_name_idx_map, resultKeyPointsJsonObject, mediapipeJsonObject, frameNum):
    # left_shoulder <-> right_shoulder
    x, y, z, score = avgMixamoData(
        mediapipe_name_idx_map,
        mediapipeJsonObject, frameNum, "left_shoulder", "right_shoulder")
    resultKeyPointsJsonObject["keypoints3D"].append({'x': x,
                                                     'y': -y,
                                                     'z': -z,
                                                     'score': score,
                                                     'name': mixamo_names[4][0],
                                                     'parent': mixamo_names[4][2]})
    return


def mediapipeToMixamoHead(mediapipe_name_idx_map, resultKeyPointsJsonObject, mediapipeJsonObject, frameNum):
    # left_shoulder <-> right_shoulder
    x, y, z, score = avgMixamoData(
        mediapipe_name_idx_map,
        mediapipeJsonObject, frameNum, "left_ear", "right_ear")
    resultKeyPointsJsonObject["keypoints3D"].append({'x': x,
                                                     'y': -y,
                                                     'z': -z,
                                                     'score': score,
                                                     'name': mixamo_names[5][0],
                                                     'parent': mixamo_names[5][2]})
    return


def mediapipeToMixamoAll(mediapipe_name_idx_map, mixamo_name_mediapipe_name_map, resultKeyPointsJsonObject, mediapipeJsonObject, frameNum):
    frameKeypoints = mediapipeJsonObject[frameNum]["keypoints3D"]
    for idx in range(6, len(mixamo_names)):
        mediapipeName = mixamo_name_mediapipe_name_map[mixamo_names[idx][0]]
        mediapipeIdx = mediapipe_name_idx_map[mediapipeName]
        keypoint = frameKeypoints[mediapipeIdx]
        resultKeyPointsJsonObject["keypoints3D"].append({'x': keypoint['x'],
                                                         'y': -keypoint['y'],
                                                         'z': -keypoint['z'],
                                                         'score': keypoint['score'],
                                                         'name': mixamo_names[idx][0],
                                                         'parent': mixamo_names[idx][2]})
    return


def mediapipeToMixamo(mediapipe_name_idx_map, mediapipeJsonObject):
    mm_name_mp_name_map = get_mixamo_name_mediapipe_name_map()
    jsonObject = {
        "fileName": mediapipeJsonObject['fileName'],
        "duration": mediapipeJsonObject['duration'],
        "ticksPerSecond": mediapipeJsonObject['ticksPerSecond'],
        "frames": []
    }
    for fidx in range(0, len(mediapipeJsonObject['frames'])):
        if len(mediapipeJsonObject['frames'][fidx]['keypoints3D']) == 0:
            continue

        mediapipeJsonObject['frames'][fidx]['keypoints3D'][mediapipe_name_idx_map['left_heel']]['x'],
        keypointsJsonObject = {
            "frameNum":  fidx,
            "keypoints3D": [],
            "keypoints": [],
            "heel3D": [
                {
                    "name": "LeftHeel",
                    "x": mediapipeJsonObject['frames'][fidx]['keypoints3D'][mediapipe_name_idx_map['left_heel']]['x'],
                    "y": -mediapipeJsonObject['frames'][fidx]['keypoints3D'][mediapipe_name_idx_map['left_heel']]['y'],
                    "z": -mediapipeJsonObject['frames'][fidx]['keypoints3D'][mediapipe_name_idx_map['left_heel']]['z'],
                    "score":mediapipeJsonObject['frames'][fidx]['keypoints3D'][mediapipe_name_idx_map['left_heel']]['score']
                },
                {
                    "name": "RightHeel",
                    "x": mediapipeJsonObject['frames'][fidx]['keypoints3D'][mediapipe_name_idx_map['right_heel']]['x'],
                    "y": -mediapipeJsonObject['frames'][fidx]['keypoints3D'][mediapipe_name_idx_map['right_heel']]['y'],
                    "z": -mediapipeJsonObject['frames'][fidx]['keypoints3D'][mediapipe_name_idx_map['right_heel']]['z'],
                    "score":mediapipeJsonObject['frames'][fidx]['keypoints3D'][mediapipe_name_idx_map['right_heel']]['score']
                },
            ]
        }
        mediapipeToMixamoHip(mediapipe_name_idx_map, keypointsJsonObject,
                             mediapipeJsonObject['frames'], fidx)
        mediapipeToMixamoSpine(mediapipe_name_idx_map, keypointsJsonObject,
                               mediapipeJsonObject['frames'], fidx)
        mediapipeToMixamoNeck(mediapipe_name_idx_map, keypointsJsonObject,
                              mediapipeJsonObject['frames'], fidx)
        mediapipeToMixamoHead(mediapipe_name_idx_map, keypointsJsonObject,
                              mediapipeJsonObject['frames'], fidx)
        mediapipeToMixamoAll(mediapipe_name_idx_map, mm_name_mp_name_map, keypointsJsonObject,
                             mediapipeJsonObject['frames'], fidx)
        jsonObject["frames"].append(keypointsJsonObject)
    return jsonObject
