import json
import cv2
import glm
import mediapipe as mp
import math
import matplotlib.pyplot as plt
import os
import pafy
from helper.mixamo import Mixamo
from helper.model_node import ModelNode


def get_3d_len(left):
    return math.sqrt((left["x"])**2 + (left["y"])**2 + (left["z"])**2)


def set_axes(ax, azim=10, elev=10, xrange=1.0, yrange=1.0, zrange=1.0):
    ax.set_xlabel("Z")
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
            dot_group['x'].append(vec_list[idx][2])
            dot_group['y'].append(vec_list[idx][0])
            dot_group['z'].append(vec_list[idx][1])
        dots.append(dot_group)
    return dots


def draw_list2(fig, vec_list=[], group_lists=[[]], azim=10, range=1.0):
    ax1 = plt.axes(projection='3d')
    set_axes(ax1, elev=10, azim=azim, xrange=range, yrange=range, zrange=range)
    dots = get_dot(vec_list, group_lists)
    for dot in dots:
        ax1.plot(dot['x'], dot['y'], dot['z'], marker='o')

    fig.canvas.draw()


def find_bones(bones, name):
    for bone in bones:
        if bone["name"] == name:
            return bone
    return None


def find_hips(pixel3d_json):
    return find_pixel3d_json(pixel3d_json, Mixamo.Hips.name)


def find_pixel3d_json(pixel3d_json, name):
    if pixel3d_json["name"] == name:
        return [True, pixel3d_json]
    else:
        for child in pixel3d_json["child"]:
            is_find, result = find_pixel3d_json(child, name)
            if is_find:
                return [is_find, result]
        return [False, None]


def get_name_idx_map():
    mediapipe_names = [
        "nose",
        "left_eye_inner", "left_eye", "left_eye_outer", "right_eye_inner", "right_eye", "right_eye_outer", "left_ear", "right_ear", "mouth_left", "mouth_right", "left_shoulder", "right_shoulder", "left_elbow", "right_elbow", "left_wrist", "right_wrist", "left_pinky", "right_pinky", "left_index", "right_index", "left_thumb", "right_thumb", "left_hip", "right_hip", "left_knee", "right_knee", "left_ankle", "right_ankle", "left_heel", "right_heel", "left_foot_index", "right_foot_index"]

    name_idx_map = {}
    for idx in range(0, len(mediapipe_names)):
        name_idx_map[mediapipe_names[idx]] = idx
    return name_idx_map


def get_mixamo_names():
    return [
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


def get_mixamo_name_idx_map():
    mixamo_names = get_mixamo_names()
    mixamo_name_idx_map = {}
    for name in mixamo_names:
        mixamo_name_idx_map[name[0]] = name[1]
    return mixamo_name_idx_map


def get_mixamo_name_mediapipe_name_map():
    mixamo_name_mediapipe_name_map = {}
    mixamo_names = get_mixamo_names()
    for idx in range(6, len(mixamo_names)):
        mixamo_name_mediapipe_name_map[mixamo_names[idx]
                                       [0]] = mixamo_names[idx][3]
    return mixamo_name_mediapipe_name_map

##################################################################################################################################################################################


class MediapipeManager():
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.pose_dict = dict()
        self.key = ""
        self.set_key()
        self.is_hips_move = False
        self.min_visibility = 0.5
        self.max_frame_num = 5000
        self.is_show_result = False

    def set_key(self, model_complexity=1, static_image_mode=False, min_detection_confidence=0.5):
        self.key = str(model_complexity) + ' ' + \
            str(min_detection_confidence)+' ' + str(static_image_mode)
        if self.key not in self.pose_dict:
            items = self.key.split()

            self.pose_dict[self.key] = self.mp_pose.Pose(
                static_image_mode=(items[2] == "True"),
                min_detection_confidence=float(items[1]),
                model_complexity=int(items[0])
            )

    def get_pose(self):
        return self.pose_dict[self.key]


def mediapipe_to_mixamo(mp_manager,
                        mixamo_bindingpose_path,
                        video_path):
    mm_name_idx_map = get_mixamo_name_idx_map()
    mixamo_json = None
    with open(mixamo_bindingpose_path) as f:
        mixamo_json = json.load(f)
    is_find, hip_node = find_hips(mixamo_json["node"])
    if not is_find:
        return [False, None]

    if video_path[:4] == "http":
        video = pafy.new(video_path)
        best = video.getbest(preftype="any")
        video_path = best.url

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    anim_result_json = {
        "fileName": os.path.basename(video_path),
        "duration": 0,
        "width":  cap.get(cv2.CAP_PROP_FRAME_WIDTH),
        "height": cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
        "ticksPerSecond": math.trunc(fps),
        "frames": [
        ]
    }

    try:
        root_node = ModelNode()
        root_node.set_mixamo(hip_node, mm_name_idx_map)
        root_node.normalize_spine()

        mediapipe_to_mixamo2(mp_manager,
                             anim_result_json,
                             cap,
                             mixamo_json,
                             root_node)
        anim_result_json["duration"] = anim_result_json["frames"][-1]["time"]

    except Exception as e:
        if cap.isOpened():
            cap.release()
        return [False, None]
    if cap.isOpened():
        cap.release()
    return [True, anim_result_json]


def mediapipe_to_mixamo2(mp_manager,
                         anim_result_json,
                         cap,
                         mixamo_bindingpose_json,
                         mixamo_bindingpose_root_node):
    # init dicts
    mp_name_idx_map = get_name_idx_map()
    mm_mp_map = get_mixamo_name_mediapipe_name_map()
    mm_name_idx_map = get_mixamo_name_idx_map()
    mp_idx_mm_idx_map = dict()
    for mm_name in mm_mp_map.keys():
        mp_name = mm_mp_map[mm_name]
        mp_idx = mp_name_idx_map[mp_name]
        mm_idx = mm_name_idx_map[mm_name]
        mp_idx_mm_idx_map[mp_idx] = mm_idx

    # for hips move var
    _, model_right_up_leg = find_pixel3d_json(
        mixamo_bindingpose_json["node"], Mixamo.RightUpLeg.name)
    model_scale = 100
    if _ != False:
        model_scale = get_3d_len(model_right_up_leg["position"])*2.0
    origin = None
    factor = 1.0
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    frame_num = -1
    plt.ion()
    plt.close()
    fig = None
    if mp_manager.is_show_result:
        fig = plt.figure()
        plt.show()

    # init mediapipe
    try:
        max_frame_num = mp_manager.max_frame_num
        is_show_result = mp_manager.is_show_result
        min_visibility = mp_manager.min_visibility
        is_hips_move = mp_manager.is_hips_move
        while cap.isOpened():

            success, cap_image = cap.read()
            frame_num += 1
            if not success or max_frame_num < frame_num:
                break
            height1, width1, _ = cap_image.shape
            cap_image = cv2.resize(
                cap_image, (int(width1 * (640 / height1)), 640))
            height2, width2, _ = cap_image.shape
            height = height2
            width = width2
            cap_image, glm_list, visibility_list, hip2d_left, hip2d_right = detect_pose_to_glm_pose(
                mp_manager, cap_image, mp_idx_mm_idx_map)
            if glm_list[0] != None:
                bones_json = {
                    "time": frame_num,
                    "bones": []
                }
                mixamo_bindingpose_root_node.normalize(
                    glm_list, mm_name_idx_map)
                mixamo_bindingpose_root_node.calc_animation(
                    glm_list, mm_name_idx_map)
                mixamo_bindingpose_root_node.tmp_to_json(
                    bones_json, visibility_list, mm_name_idx_map, min_visibility)
                anim_result_json["frames"].append(bones_json)
                if is_show_result:
                    rg = []
                    rv = []
                    mixamo_bindingpose_root_node.get_vec_and_group_list(
                        rv, rg, is_apply_tmp_transform=True)
                    plt.clf()
                    draw_list2(fig, rv, rg)
                if is_hips_move:
                    hip2d_left.x *= width
                    hip2d_left.y *= height
                    hip2d_left.z *= width
                    hip2d_right.x *= width
                    hip2d_right.y *= height
                    hip2d_right.z *= width
                    if origin == None:
                        origin = avg_vec3(hip2d_left, hip2d_right)
                        hips2d_scale = glm.distance(hip2d_left, hip2d_right)
                        factor = model_scale/hips2d_scale
                    else:
                        hips_bone_json = find_bones(
                            anim_result_json["frames"][-1]["bones"], Mixamo.Hips.name)
                        if hips_bone_json != None:
                            set_hips_position(hips_bone_json["position"], origin, avg_vec3(
                                hip2d_left, hip2d_right),  factor)

            cv2.imshow('MediaPipe pose', cap_image)
            key = cv2.waitKey(5)
            if key & 0xFF == 27:
                break
        cap.release()
        # plt.close(fig)
        cv2.destroyAllWindows()

    except Exception as e:
        # plt.close(fig)
        if cap.isOpened():
            cap.release()
            cv2.destroyAllWindows()


def detect_pose_to_glm_pose(mp_manager, image, mp_idx_mm_idx_map):
    # Create a copy of the input image.
    output_image = image.copy()

    image.flags.writeable = False

    # Convert the image from BGR into RGB format.
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform the Pose Detection.
    results = mp_manager.get_pose().process(image_rgb)

    image.flags.writeable = True

    # Initialize a list to store the detected landmarks.
    glm_list = [None]*26
    visibility_list = [None]*26
    hip2d_left, hip2d_right = glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 0.0, 0.0)

    if results.pose_world_landmarks:
        landmark = results.pose_world_landmarks.landmark

        glm_list[Mixamo.Hips] = avg_vec3(
            landmark[mp_manager.mp_pose.PoseLandmark.LEFT_HIP], landmark[mp_manager.mp_pose.PoseLandmark.RIGHT_HIP])
        visibility_list[Mixamo.Hips] = (landmark[mp_manager.mp_pose.PoseLandmark.LEFT_HIP].visibility +
                                        landmark[mp_manager.mp_pose.PoseLandmark.RIGHT_HIP].visibility)*0.5
        glm_list[Mixamo.Neck] = avg_vec3(
            landmark[mp_manager.mp_pose.PoseLandmark.LEFT_SHOULDER], landmark[mp_manager.mp_pose.PoseLandmark.RIGHT_SHOULDER])
        visibility_list[Mixamo.Neck] = (landmark[mp_manager.mp_pose.PoseLandmark.LEFT_SHOULDER].visibility +
                                        landmark[mp_manager.mp_pose.PoseLandmark.RIGHT_SHOULDER].visibility)*0.5
        glm_list[Mixamo.Spine1] = avg_vec3(
            glm_list[Mixamo.Hips], glm_list[Mixamo.Neck])
        visibility_list[Mixamo.Spine1] = (
            visibility_list[Mixamo.Hips] + visibility_list[Mixamo.Neck])*0.5
        glm_list[Mixamo.Spine] = avg_vec3(
            glm_list[Mixamo.Hips], glm_list[Mixamo.Spine1])
        visibility_list[Mixamo.Spine] = (
            visibility_list[Mixamo.Hips] + visibility_list[Mixamo.Spine1])*0.5
        glm_list[Mixamo.Spine2] = avg_vec3(
            glm_list[Mixamo.Spine1], glm_list[Mixamo.Neck])
        visibility_list[Mixamo.Spine2] = (
            visibility_list[Mixamo.Spine1] + visibility_list[Mixamo.Neck])*0.5
        glm_list[Mixamo.Head] = avg_vec3(
            landmark[mp_manager.mp_pose.PoseLandmark.LEFT_EAR], landmark[mp_manager.mp_pose.PoseLandmark.RIGHT_EAR])
        visibility_list[Mixamo.Head] = (landmark[mp_manager.mp_pose.PoseLandmark.LEFT_EAR].visibility +
                                        landmark[mp_manager.mp_pose.PoseLandmark.RIGHT_EAR].visibility)*0.5

        glm_list[Mixamo.Spine].y *= -1
        glm_list[Mixamo.Neck].y *= -1
        glm_list[Mixamo.Spine1].y *= -1
        glm_list[Mixamo.Spine2].y *= -1
        glm_list[Mixamo.Head].y *= -1

        glm_list[Mixamo.Neck].z *= -1
        glm_list[Mixamo.Spine].z *= -1
        glm_list[Mixamo.Spine1].z *= -1
        glm_list[Mixamo.Spine2].z *= -1
        glm_list[Mixamo.Head].z *= -1
        for mp_idx in mp_idx_mm_idx_map.keys():
            mm_idx = mp_idx_mm_idx_map[mp_idx]
            glm_list[mm_idx] = glm.vec3(
                landmark[mp_idx].x, -landmark[mp_idx].y, -landmark[mp_idx].z)
            visibility_list[mm_idx] = landmark[mp_idx].visibility

    # calculate hips2d
    if results.pose_landmarks:
        landmark = results.pose_landmarks.landmark
        hip2d_left.x = landmark[mp_manager.mp_pose.PoseLandmark.LEFT_HIP].x
        hip2d_left.y = landmark[mp_manager.mp_pose.PoseLandmark.LEFT_HIP].y
        hip2d_left.z = landmark[mp_manager.mp_pose.PoseLandmark.LEFT_HIP].z
        hip2d_right = glm.vec3(landmark[mp_manager.mp_pose.PoseLandmark.RIGHT_HIP].x,
                               landmark[mp_manager.mp_pose.PoseLandmark.RIGHT_HIP].y, landmark[mp_manager.mp_pose.PoseLandmark.RIGHT_HIP].z)

    mp_manager.mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
                                         connections=mp_manager.mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=mp_manager.mp_drawing_styles.get_default_pose_landmarks_style())

    return output_image, glm_list, visibility_list, hip2d_left, hip2d_right


def avg_vec3(v1, v2):
    v3 = glm.vec3((v1.x + v2.x) * 0.5,
                  (v1.y + v2.y) * 0.5,
                  (v1.z + v2.z) * 0.5)
    return v3


def set_hips_position(hips_bone_json, origin_hips, current_hips, factor):
    x = (current_hips.x - origin_hips.x) * factor
    y = (current_hips.y - origin_hips.y) * factor
    z = (current_hips.z - origin_hips.z) * factor
    hips_bone_json["x"] = x
    hips_bone_json["y"] = -y
    hips_bone_json["z"] = z
