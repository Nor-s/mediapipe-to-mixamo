import glm
from helper.gizmo import Gizmo
import math
from helper.mixamo import Mixamo
import copy


def find_2d_angle(cx, cy, ex, ey):
    dy = ey - cy
    dx = ex - cx
    theta = math.atan2(dy, dx)
    return theta


def pixel3d_json_to_glm_vec(pixel3d_json):
    return glm.vec3(pixel3d_json['x'], pixel3d_json['y'], pixel3d_json['z'])


def pixel3d_json_to_glm_quat(pixel3d_json):
    return glm.quat(w=pixel3d_json['w'], x=pixel3d_json['x'], y=pixel3d_json['y'], z=pixel3d_json['z'])


def glm_vec3_to_json(vec):
    return {"x": vec.x, "y": vec.y, "z": vec.z}


def glm_quat_to_json(quat):
    return {"w": quat.w, "x": quat.x, "y": quat.y, "z": quat.z}


def check_quat_isnan(quat):
    if math.isnan(quat.x):
        quat.x = 0.0
    if math.isnan(quat.w):
        quat.w = 1.0
    if math.isnan(quat.y):
        quat.y = 0.0
    if math.isnan(quat.z):
        quat.z = 0.0


def check_vec3_isnan(vec, num=0.0):
    if math.isnan(vec.x):
        vec.x = num
    if math.isnan(vec.y):
        vec.y = num
    if math.isnan(vec.z):
        vec.z = num


def decompose(matrix: glm.mat4):
    scale = glm.vec3()
    rotation = glm.quat()
    translation = glm.vec3()
    skew = glm.vec3()
    perspective = glm.vec4()
    glm.decompose(matrix, scale, rotation, translation, skew, perspective)
    check_quat_isnan(rotation)
    check_vec3_isnan(scale, 1.0)
    check_vec3_isnan(translation, 0.0)
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
        childlist = pix3d_node_json["child"]
        transform_list = [None for i in range(len(childlist))]
        transform_list_idx = -1

        for child in childlist:
            transform_list_idx += 1
            if child['name'] in mixamo_idx_map:
                new_node = ModelNode()
                new_node.set_mixamo(child, mixamo_idx_map, copy.deepcopy(
                    transform_list[transform_list_idx]))
                self.child.append(new_node)
            else:
                for child_of_child in child["child"]:
                    childlist.append(child_of_child)
                    position = pixel3d_json_to_glm_vec(child["position"])
                    rotation = pixel3d_json_to_glm_quat(child["rotation"])
                    scale = pixel3d_json_to_glm_vec(child["scale"])
                    transform = calc_transform(position, rotation, scale)
                    transform_list.append(transform)

    def normalize_spine(self, parent_node=None, parent_transform=glm.mat4(1.0)):
        if Mixamo.Spine.name in self.name or self.name == Mixamo.LeftArm.name or self.name == Mixamo.RightArm.name or self.name == Mixamo.Neck.name:
            self.position.z = 0  # local_pos.z


        for child in self.child:
            child.normalize_spine(
                parent_node=self, parent_transform=self.tmp_transform*self.get_transform())

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
            target_vec = world_mixamo_adjust + mixamo_list[mixamo_idx_map[target_node.name]]
            self.tmp_transform = current_gizmo.calc_rotation_matrix(
                target_gizmo.get_origin(), target_vec)

        for child in self.child:
            adjust_vec1 = child.get_gizmo(
                parent_transform*self.get_transform()*self.tmp_transform).get_origin()
            adjust_vec = adjust_vec1 - mixamo_list[mixamo_idx_map[child.name]]
            child.calc_animation(mixamo_list, mixamo_idx_map,
                                 parent_transform*self.get_transform()*self.tmp_transform, world_mixamo_adjust=adjust_vec)

    def get_transform(self):
        return calc_transform(self.position, self.rotate, self.scale)

    def get_gizmo(self, parent_transform=glm.mat4(1.0), is_apply_transform=True):
        if is_apply_transform:
            return self.gizmo.rotate(parent_transform*self.get_transform())
        else:
            return self.gizmo.rotate(parent_transform)

    def get_gizmo_apply_tmp(self, parent_transform=glm.mat4(1.0)):
        return self.gizmo.rotate(parent_transform*self.get_transform()*self.tmp_transform)

    def get_vec_and_group_list(self, result_vec_list, result_group_list, parent_transform=glm.mat4(1.0),  group_list=None, is_apply_tmp_transform=False):
        if is_apply_tmp_transform:
            result_vec_list.append(self.get_gizmo_apply_tmp(
                parent_transform).get_origin())
        else:
            result_vec_list.append(self.get_gizmo(
                parent_transform).get_origin())
        if group_list == None:
            group_list = []
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

    def tmp_to_json(self, bones_json, visibility_list, mixamo_idx_map, min_visibility=0.6):
        [t, r, s] = decompose(self.tmp_transform)
        visibility = visibility_list[mixamo_idx_map[self.name]]
        if visibility >= min_visibility and (not (r.w == 1.0 and r.x == 0.0 and r.y == 0.0 and r.z == 0.0)):
            bone_json = {
                "name": self.name,
                "rotation": glm_quat_to_json(r),
                "position": glm_vec3_to_json(t),
                "scale": glm_vec3_to_json(s)
            }
            bones_json["bones"].append(bone_json)
        for child in self.child:
            child.tmp_to_json(bones_json, visibility_list,
                              mixamo_idx_map, min_visibility)