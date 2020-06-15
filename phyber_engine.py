import math
from phyber_math import vec2, vec4, mat4x4

class p_Ball_2D:
    def __init__(self, mass, radius):
        self.mass = mass
        self.radius = radius
        self.acceleration = vec2(0, 0)
        self.velocity = vec2(0, 0)
        self.position = vec2(0, 0)

    def set_velocity(self, vel):
        assert isinstance(vel, vec2)
        self.velocity = vel

    def set_position(self, pos):
        self.position = pos

    def apply_acceleration(self, deltaTime):
        self.velocity += self.acceleration * deltaTime

        self.acceleration = vec2(0, 0)

        self.position += self.velocity * deltaTime

    def log_info(self):
        print('\ninfo ball:\n\taccel = ({}, {})\n\tvel = ({}, {})\n\tpos = ({}, {})'.format(self.acceleration[0], self.acceleration[1], self.velocity[0], self.velocity[1], self.position[0], self.position[1]))

class p_CircleMarker_2D:
    def __init__(self, radius, colour, name, position = [0, 0]):
        self.name = name
        self.radius = radius
        self.colour = colour
        self.position = vec2(position[0], position[1])
        self.velocity = vec2(0, 0)
        self.acceleration = vec2(0, 0)

    def set_radius(self, radius):
        self.radius = radius

    def set_colour(self, colour):
        self.colour = colour

    def set_position(self, pos):
        self.position = vec2(pos[0], pos[1])

    def set_velocity(self, vel):
        self.velocity = vec2(vel[0], vel[1])

    def set_acceleration(self, acc):
        self.acceleration = vec2(acc[0], acc[1])

    def log_info(self):
        print('{}\n\tpos = ({}, {})\n\tvel = ({}, {})\n\tacc = ({}, {})'.format(self.name, self.position[0], self.position[1], self.velocity[0], self.velocity[1], self.acceleration[0], self.acceleration[1]))

class p_LineMarker_2D:
    def __init__(self, colour, thikness, pos, scale = 10000):
        self.colour = colour
        self.thickness = thikness
        self.pos = vec2(pos[0], pos[1])
        self.scale = scale
        self.magnitude = self.pos.magnitude()

        self.vert1 = vec2(0, 0)
        self.vert2 = self.pos

    def scale_line(self):
        self.vert1 = vec2(0, 0)
        v = self.pos * self.scale
        assert isinstance(v, vec2)
        self.vert2 = v
        assert isinstance(self.vert2, vec2)

    def translate(self, trans):
        t = vec2(trans[0], trans[1])
        self.vert1 += t
        self.vert2 += t #p_math_2D.vec_add(self.pos, trans)
        pass

    def set_pos(self, p):
        assert isinstance(p, vec2)
        self.pos = p

    def get_magnitude(self):
        self.pos.magnitude()

class Phyber_2D:
    def __init__(self, bodies, markers):
        self.G = 6.67408 * (10 ** -11)

        self.bodies = list()
        for b in bodies:
            self.bodies.append(b)

        # list containing toggles for showing (or not) certain data
        # mass center, linear momentum, angular momentum
        self.showData = markers #[False, False, False]
        self.dataMarkers = list()
        self.massCenter = None
        self.linearMomentum = list()
        self.angularMomentum = list()

        if self.showData[0]:
            self.massCenter = p_CircleMarker_2D(10, (255, 0, 0), 'mass center')
        if self.showData[1]:
            for i in range(len(self.bodies) + 1):
                self.linearMomentum.append(p_LineMarker_2D((255, 255, 0), 3, [0, 0]))

    def calculate_forces(self, deltaTime):
        # gravity
        self.calc_gravity()

        for b in self.bodies:
            b.apply_acceleration(deltaTime)

    def calc_gravity(self):
        for i in range(len(self.bodies)):
            for n in range(i + 1, len(self.bodies), 1):
                distance = vec2.vec_distance(self.bodies[i].position, self.bodies[n].position)
                if distance != 0:
                    force = self.G * ((self.bodies[i].mass * self.bodies[n].mass) / (distance ** 2))
                else:
                    log = 'Distance between bodies {} and {} is 0'.format(i, n)
                    raise Exception(log)

                unionVec = vec2.vec_from_points(self.bodies[i].position, self.bodies[n].position)
                self.bodies[i].acceleration += (force * unionVec) * (1 / self.bodies[i].mass)
                self.bodies[n].acceleration += (force * unionVec) * (-1 / self.bodies[n].mass)

    def make_data_markers(self, deltaTime, size):
        if self.showData[0]:
            self.calc_mass_center(deltaTime)

        if self.showData[1]:
            self.calc_linear_momentum()

    def calc_mass_center(self, deltaTime):
        if (deltaTime == 0):
            deltaTime = 0.00001
        totMass = 0
        posSum = [0, 0]
        for b in self.bodies:
            posSum[0] += b.position[0] * b.mass
            posSum[1] += b.position[1] * b.mass
            totMass += b.mass
        oldPos = self.massCenter.position
        self.massCenter.set_position((posSum[0] / totMass, posSum[1] / totMass))
        
        oldVel = self.massCenter.velocity
        self.massCenter.set_velocity(vec2((self.massCenter.position[0] - oldPos[0]) / deltaTime, (self.massCenter.position[1] - oldPos[1]) / deltaTime))

        self.massCenter.set_acceleration(((self.massCenter.velocity[0] - oldVel[0]) / deltaTime, (self.massCenter.velocity[1] - oldVel[1]) / deltaTime))

    def calc_linear_momentum(self):
        linMomTot = [0, 0]
        for i in range(len(self.bodies)):
            pos = self.bodies[i].velocity * self.bodies[i].mass
            assert isinstance(pos, vec2)
            self.linearMomentum[i + 1].pos = pos
            linMomTot[0] += self.linearMomentum[i + 1].pos[0]
            linMomTot[1] += self.linearMomentum[i + 1].pos[1]
            self.linearMomentum[i + 1].scale_line()
            self.linearMomentum[i + 1].translate(self.bodies[i].position)
        self.linearMomentum[0].set_pos(vec2(linMomTot[0], linMomTot[1]))
        self.linearMomentum[0].scale_line()
        if self.showData[0]:
            self.linearMomentum[0].translate(self.massCenter.position)
        else:
            self.linearMomentum[0].translate([100, 100])
        #print('({}, {}), ({}, {})'.format(self.linearMomentum[1].vert1[0], self.linearMomentum[1].vert1[1], self.linearMomentum[1].vert2[0], self.linearMomentum[1].vert2[1]))
        print(self.linearMomentum[1].vert2)

import OBJ_Reader
class p_Ball_3D:
    class Triangle:
        def __init__(self, verts):
            self.verts = verts

    def __init__(self, mass, radius):
        self.radius = radius
        self.mass = mass
        self.acceleration = [0, 0, 0]
        self.velocity = [0, 0, 0]
        self.position = [0, 0, 0]
        self.tris = list()
        reader = OBJ_Reader.ObjReader('CenteredCube.obj')
        for t in reader.trios:
            v1 = t[0]
            v2 = t[1]
            v3 = t[2]
            v1.append(1)
            v2.append(1)
            v3.append(1)
            self.tris.append(p_Ball_3D.Triangle([v1, v2, v3]))

        self.trans = mat4x4()

    def set_velocity(self, vel):
        self.velocity = vel

    def set_position(self, pos):
        self.position = pos

    def apply_acceleration(self, deltaTime):
        self.velocity[0] += self.acceleration[0] * deltaTime
        self.velocity[1] += self.acceleration[1] * deltaTime
        self.velocity[2] += self.acceleration[2] * deltaTime

        self.acceleration = [0, 0, 0]

        self.position[0] += self.velocity[0] * deltaTime
        self.position[1] += self.velocity[1] * deltaTime
        self.position[2] += self.velocity[2] * deltaTime

    def translate(self, x, y, z):
        pass
'''
class Phyber_3D:
    def __init__(self, bodies):
        self.G = 6.67408 * (10 ** -11)
        self.bodies = bodies
        #self.proj = p_math_3D.mat4x4.mat_id()
        self.width = 1
        self.height = 1

    def init_graphics(self, width, height, fov, far, near):
        #self.proj = p_math_3D.mat4x4.mat_proj(fov, height / width, near, far)
        self.width = width
        self.height = height


    def calculate_forces(self, deltaTime):
        # gravity
        self.calc_gravity()

        for b in self.bodies:
            b.apply_acceleration(deltaTime)

    def calc_gravity(self):
        for i in range(len(self.bodies)):
            for n in range(i + 1, len(self.bodies), 1):
                #distance = p_math_3D.vec_distance(self.bodies[i].position, self.bodies[n].position)
                if distance != 0:
                    force = self.G * ((self.bodies[i].mass * self.bodies[n].mass) / (distance ** 2))
                else:
                    log = 'Distance between bodies {} and {} is 0'.format(i, n)
                    raise Exception(log)

                unionVec = vec4.vec_from_points(self.bodies[i].position, self.bodies[n].position)
                self.bodies[i].acceleration[0] += (force * unionVec[0]) / self.bodies[i].mass
                self.bodies[i].acceleration[1] += (force * unionVec[1]) / self.bodies[i].mass
                self.bodies[i].acceleration[2] += (force * unionVec[2]) / self.bodies[i].mass
                self.bodies[n].acceleration[0] += (force * -unionVec[0]) / self.bodies[n].mass
                self.bodies[n].acceleration[1] += (force * -unionVec[1]) / self.bodies[n].mass
                self.bodies[n].acceleration[2] += (force * -unionVec[2]) / self.bodies[n].mass

    def to_2D(self):
        triangles = list()
        for b in self.bodies:
            for tris in b.tris:
                v1 = p_math_3D.mat4x4.mat_vec_mult(self.proj, tris.verts[0])
                v2 = p_math_3D.mat4x4.mat_vec_mult(self.proj, tris.verts[1])
                v3 = p_math_3D.mat4x4.mat_vec_mult(self.proj, tris.verts[2])

                v1 = p_math_3D.vec_mult(v1, 1 / v1[3])
                v2 = p_math_3D.vec_mult(v2, 1 / v2[3])
                v3 = p_math_3D.vec_mult(v3, 1 / v3[3])

                v1[0] *= -1
                v1[1] *= -1
                v2[0] *= -1
                v2[1] *= -1
                v3[0] *= -1
                v3[1] *= -1

                offsetView = (1, 1, 0)
                v1 = p_math_3D.vec_add(v1, offsetView)
                v2 = p_math_3D.vec_add(v2, offsetView)
                v3 = p_math_3D.vec_add(v3, offsetView)
                v1[0] *= 0.5 * self.width
                v1[1] *= 0.5 * self.height
                v2[0] *= 0.5 * self.width
                v2[1] *= 0.5 * self.height
                v3[0] *= 0.5 * self.width
                v3[1] *= 0.5 * self.height

                triangles.append([v1[:2], v2[:2], v3[:2]])
        return triangles'''

def main():
    b1 = p_Ball_2D(5, 10)
    b1.set_position([5, 10])
    b2 = p_Ball_2D(2, 5)

    phyber = Phyber_2D([b1, b2], [True, True, False])
    phyber.calculate_forces(0.1)

    b1.log_info()
    b2.log_info()

if __name__ == '__main__':
    main()
