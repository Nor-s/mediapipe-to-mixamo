from .mixamo_helper import Mixamo, get_mixamo_name_idx_map, get_mixamo_name_mediapipe_name_map
from .mediapipe_helper import get_name_idx_map
from .pyglm_helper import get_3d_len,  find_pixel3d_json, find_bones, find_hips, ModelNode, glm_list_to_image
import json
import cv2
import glm
import mediapipe as mp
import math
import matplotlib.pyplot as plt

def mediapipe_to_mixamo(mixamo_bindingpose_path, 
                        video_path, 
                        is_hips_move = False, 
                        min_visibility = 0.5, 
                        min_detection_confidence = 0.5, 
                        model_complexity = 1, 
                        static_image_mode = False, 
                        max_frame_num = 5000,
                        is_show_result = False):
    mm_name_idx_map  = get_mixamo_name_idx_map()
    mixamo_json = None
    with open(mixamo_bindingpose_path) as f:
        mixamo_json = json.load(f)
    is_find, hip_node = find_hips(mixamo_json["node"])
    if not is_find:
        return [False, None]
    
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    anim_result_json = {
        "fileName": video_path,
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

        mediapipe_to_mixamo2(anim_result_json, 
                                cap, 
                                mixamo_json,
                                root_node, 
                                is_hips_move=is_hips_move, 
                                min_visibility=min_visibility, 
                                min_detection_confidence=min_detection_confidence, 
                                model_complexity=model_complexity, 
                                static_image_mode=static_image_mode, 
                                max_frame_num=max_frame_num,
                                is_show_result= is_show_result)
        anim_result_json["duration"]= anim_result_json["frames"][-1]["time"]

    except Exception as e:
        print(e)
        if cap.isOpened():
            cap.release()
        return [False, None]
    if cap.isOpened():
        cap.release()
    return [True, anim_result_json]


def mediapipe_to_mixamo2(anim_result_json, 
                         cap, 
                         mixamo_bindingpose_json, 
                         mixamo_bindingpose_root_node, 
                         is_hips_move = False, 
                         min_visibility = 0.5, 
                         min_detection_confidence = 0.5, 
                         model_complexity = 1,
                         static_image_mode = False, 
                         max_frame_num = 5000,
                         is_show_result = False):
    # init dicts
    mp_name_idx_map = get_name_idx_map()
    mm_mp_map = get_mixamo_name_mediapipe_name_map()
    mm_name_idx_map  = get_mixamo_name_idx_map()
    mp_idx_mm_idx_map = dict()
    for mm_name in mm_mp_map.keys():
        mp_name = mm_mp_map[mm_name]
        mp_idx = mp_name_idx_map[mp_name]
        mm_idx = mm_name_idx_map[mm_name]
        mp_idx_mm_idx_map[mp_idx] = mm_idx
    
    # for hips move var
    _, model_right_up_leg = find_pixel3d_json(mixamo_bindingpose_json["node"], Mixamo.RightUpLeg.name)
    model_scale = 100
    if _ != False:
        model_scale = get_3d_len(model_right_up_leg["position"])
    origin = None
    factor = 1.0
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # init medaipipe
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils 
    pose_video = mp_pose.Pose(static_image_mode=static_image_mode,
                        min_detection_confidence=min_detection_confidence, 
                        model_complexity=model_complexity)
    frame_num = -1
    
    fig = plt.figure()
    
    try:
        while cap.isOpened():

            success, image = cap.read()
            frame_num += 1
            if not success or max_frame_num < frame_num :
                break

            image, glm_list, visibility_list, hip2d_left, hip2d_right = detect_pose_to_glm_pose(mp_pose, mp_drawing, image, pose_video, mp_idx_mm_idx_map)
            if glm_list[0] != None:
                bones_json = {
                   "time": frame_num,
                   "bones": []
                } 
                mixamo_bindingpose_root_node.normalize(glm_list, mm_name_idx_map)
                mixamo_bindingpose_root_node.calc_animation(glm_list, mm_name_idx_map)
                mixamo_bindingpose_root_node.tmp_to_json(bones_json, visibility_list, mm_name_idx_map, min_visibility)
                anim_result_json["frames"].append(bones_json)
                if is_show_result:
                    rg = []
                    rv = []
                    mixamo_bindingpose_root_node.get_vec_and_group_list(rv, rg, is_apply_tmp_transform= True)
                    cv2.imshow("result", glm_list_to_image(fig, rv, rg))
                if is_hips_move:
                    hip2d_left.x *=  width
                    hip2d_left.y *=  height
                    hip2d_left.z *=  width
                    hip2d_right.x *= width
                    hip2d_right.y *= height
                    hip2d_right.z *= width
                    if origin == None:
                       origin = avg_vec3(hip2d_left, hip2d_right)
                       hips2d_scale = glm.distance(hip2d_left, hip2d_right)
                       factor = model_scale/hips2d_scale
                    else:
                        hips_bone_json = find_bones(anim_result_json["frames"][-1]["bones"], Mixamo.Hips.name)
                        if hips_bone_json != None:
                            set_hips_position(hips_bone_json["position"], origin, avg_vec3(hip2d_left, hip2d_right),  factor)

            cv2.imshow('MediaPipe pose', image)

            if cv2.waitKey(5) & 0xFF == 27:
                break
        cap.release()
        plt.close()
    except Exception as e:
        print(e)
        plt.close()
        if cap.isOpened():
            cap.release()
                
        

def detect_pose_to_glm_pose(mp_pose, mp_drawing, image, pose, mp_idx_mm_idx_map):
    # Create a copy of the input image.
    output_image = image.copy()
    
    image.flags.writeable = False

    # Convert the image from BGR into RGB format.
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform the Pose Detection.
    results = pose.process(image_rgb)
    
    image.flags.writeable = True

    # Initialize a list to store the detected landmarks.
    glm_list = [None]*26
    visibility_list = [None]*26
    hip2d_left, hip2d_right = glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 0.0, 0.0)

    if results.pose_world_landmarks:
        landmark = results.pose_world_landmarks.landmark

        glm_list[Mixamo.Hips] = avg_vec3(landmark[mp_pose.PoseLandmark.LEFT_HIP], landmark[mp_pose.PoseLandmark.RIGHT_HIP])
        visibility_list[Mixamo.Hips] = (landmark[mp_pose.PoseLandmark.LEFT_HIP].visibility +  landmark[mp_pose.PoseLandmark.RIGHT_HIP].visibility)*0.5
        glm_list[Mixamo.Neck]  = avg_vec3(landmark[mp_pose.PoseLandmark.LEFT_SHOULDER], landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER])
        visibility_list[Mixamo.Neck] = (landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].visibility +  landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].visibility)*0.5
        glm_list[Mixamo.Spine1] = avg_vec3(glm_list[Mixamo.Hips], glm_list[Mixamo.Neck])
        visibility_list[Mixamo.Spine1] = (visibility_list[Mixamo.Hips] + visibility_list[Mixamo.Neck])*0.5
        glm_list[Mixamo.Spine] = avg_vec3(glm_list[Mixamo.Hips], glm_list[Mixamo.Spine1])
        visibility_list[Mixamo.Spine] = (visibility_list[Mixamo.Hips] + visibility_list[Mixamo.Spine1])*0.5
        glm_list[Mixamo.Spine2] = avg_vec3(glm_list[Mixamo.Spine1], glm_list[Mixamo.Neck])
        visibility_list[Mixamo.Spine2] = (visibility_list[Mixamo.Spine1] + visibility_list[Mixamo.Neck])*0.5
        glm_list[Mixamo.Head]  = avg_vec3(landmark[mp_pose.PoseLandmark.LEFT_EAR], landmark[mp_pose.PoseLandmark.RIGHT_EAR])
        visibility_list[Mixamo.Head] = (landmark[mp_pose.PoseLandmark.LEFT_EAR].visibility +  landmark[mp_pose.PoseLandmark.RIGHT_EAR].visibility)*0.5
        glm_list[Mixamo.Neck].y *= -1
        glm_list[Mixamo.Neck].z *= -1
        glm_list[Mixamo.Spine].y *= -1
        glm_list[Mixamo.Spine].z *= -1
        glm_list[Mixamo.Spine1].y *= -1
        glm_list[Mixamo.Spine1].z *= -1
        glm_list[Mixamo.Spine2].y *= -1
        glm_list[Mixamo.Spine2].z *= -1
        glm_list[Mixamo.Head].y *= -1
        glm_list[Mixamo.Head].z *= -1
        for mp_idx in mp_idx_mm_idx_map.keys():
            mm_idx = mp_idx_mm_idx_map[mp_idx]
            glm_list[mm_idx] = glm.vec3(landmark[mp_idx].x, -landmark[mp_idx].y, -landmark[mp_idx].z)
            visibility_list[mm_idx] = landmark[mp_idx].visibility


    image_height, image_width, _ = image.shape

    # calculate hips2d
    if results.pose_landmarks:
        landmark = results.pose_landmarks.landmark
        hip2d_left.x = landmark[mp_pose.PoseLandmark.LEFT_HIP].x
        hip2d_left.y = landmark[mp_pose.PoseLandmark.LEFT_HIP].y
        hip2d_left.z = landmark[mp_pose.PoseLandmark.LEFT_HIP].z
        hip2d_right = glm.vec3(landmark[mp_pose.PoseLandmark.RIGHT_HIP].x,landmark[mp_pose.PoseLandmark.RIGHT_HIP].y,landmark[mp_pose.PoseLandmark.RIGHT_HIP].z)

    mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
                              connections=mp_pose.POSE_CONNECTIONS)

    return output_image, glm_list, visibility_list, hip2d_left, hip2d_right

def avg_vec3(v1, v2):
    v3 = glm.vec3((v1.x + v2.x)* 0.5, 
                 (v1.y + v2.y)* 0.5, 
                 (v1.z + v2.z)* 0.5)
    return v3

def set_hips_position(hips_bone_json, origin_hips, current_hips, factor):
    x = (current_hips.x - origin_hips.x)* factor
    y = (current_hips.y - origin_hips.y) * factor
    z = (current_hips.z - origin_hips.z) * factor
    hips_bone_json["x"] = x
    hips_bone_json["y"] = -y
    hips_bone_json["z"] = z
