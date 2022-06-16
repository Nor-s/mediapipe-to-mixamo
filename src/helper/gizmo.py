import glm
import math

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
        b = world_pos - self.r
        A = glm.mat3(self.x, self.y, self.z)
        x = glm.inverse(A)*b
        if math.isnan(x.x):
            x.x = 0.0
        if math.isnan(x.y):
            x.y = 0.0
        if math.isnan(x.z):
            x.z = 0.0
        return x