import math, os
from phyber_math import vec2, vec4, mat4x4

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

class Triangle:
        def __init__(self, verts, normal = [0, 0, 0]):
            self.verts = verts
            self.normal = vec4(normal[0], normal[1], normal[2], 1)
            self.normal = self.normal.normalized()

        def check(self):
            assert len(self.verts)
            if len(self.verts) == 3:
                return True
            else:
                return False

class p_Ball_3D:
    def __init__(self, mass, radius):
        import OBJ_Reader

        self.radius = radius
        self.mass = mass
        self.acceleration = vec4(0, 0, 0, 1)
        self.velocity = vec4(0, 0, 0, 1)
        self.position = vec4(0, 0, 0, 1)

        self.trans = mat4x4.make_identity()
        self.rotX = mat4x4.make_identity()
        self.rotY = mat4x4.make_identity()
        self.rotZ = mat4x4.make_identity()
        self.scale = mat4x4.mat_scale(self.radius)

        self.tris = list()
        reader = OBJ_Reader.ObjReader('Sphere.obj')
        for t in reader.triangles:
            v1 = vec4(t[0][0], t[0][1], t[0][2], 1)
            v2 = vec4(t[1][0], t[1][1], t[1][2], 1)
            v3 = vec4(t[2][0], t[2][1], t[2][2], 1)
            v1 = self.scale * v1
            v2 = self.scale * v2
            v3 = self.scale * v3
            self.tris.append(Triangle([v1, v2, v3], t[3]))

    def set_velocity(self, vel):
        self.velocity = vel

    def set_position(self, pos):
        self.position = pos

    def apply_acceleration(self, deltaTime):
        self.velocity += self.acceleration * deltaTime

        self.acceleration = vec4(0, 0, 0, 1)

        self.position += self.velocity * deltaTime
        self.trans = mat4x4.mat_translation(self.position[0], self.position[1], self.position[2])

    def set_translation(self, x, y, z):
        self.position = vec4(x, y, z, 1)
        self.trans = mat4x4.mat_translation(self.position[0], self.position[1], self.position[2])

    def set_rotationX(self, angleRad):
        self.rotX = mat4x4.make_rot_x(angleRad)

    def set_rotationY(self, angleRad):
        self.rotY = mat4x4.make_rot_y(angleRad)

    def set_rotationZ(self, angleRad):
        self.rotZ = mat4x4.make_rot_z(angleRad)

class Phyber_3D:
    def __init__(self, bodies):
        self.G = 6.67408 * (10 ** -11)
        self.bodies = bodies
        self.width = 1
        self.height = 1

    def calculate_forces(self, deltaTime):
        # gravity
        self.calc_gravity()

        for b in self.bodies:
            b.apply_acceleration(deltaTime)

    def calc_gravity(self):
        for i in range(len(self.bodies)):
            for n in range(i + 1, len(self.bodies), 1):
                distance = vec4.vec_distance(self.bodies[i].position, self.bodies[n].position)
                if distance != 0:
                    force = self.G * ((self.bodies[i].mass * self.bodies[n].mass) / (distance ** 2))
                else:
                    log = 'Distance between bodies {} and {} is 0'.format(i, n)
                    raise Exception(log)

                unionVec = vec4.vec_from_points(self.bodies[i].position, self.bodies[n].position)
                self.bodies[i].acceleration += (unionVec * force) * (1 / self.bodies[i].mass)
                self.bodies[n].acceleration += (unionVec * force) * (-1 / self.bodies[n].mass)

def main():
    b1 = p_Ball_2D(5, 10)
    b1.set_position([5, 10])
    b2 = p_Ball_2D(2, 5)

    phyber = Phyber_2D([b1, b2], [True, True, False])
    phyber.calculate_forces(0.1)

if __name__ == '__main__':
    main()
