import math, os
from phyber_math import vec2, vec4, mat4x4
import phyber_logging

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

        import sys
        self.host = sys.platform
        self.clear = ''
        if self.host == 'windows':
            self.clear = 'cls'
        else:
            self.clear = 'clear'

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
            for _ in range(len(self.bodies) + 1):
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

    def log(self):
        table = list()
        table.append(['Object', '', 'x', 'y'])
        table.append(['Mass Center:'])
        table.append(['', 'Position', '{:0<7}'.format(round(self.massCenter.position[0], 7)), '{:0<7}'.format(round(self.massCenter.position[1], 7))])
        table.append(['', 'Velocity', '{:0<7}'.format(round(self.massCenter.velocity[0], 7)), '{:0<7}'.format(round(self.massCenter.velocity[1], 7))])
        table.append(['', 'Acceleration', '{:0<7}'.format(round(self.massCenter.acceleration[0], 7)), '{:0<7}'.format(round(self.massCenter.acceleration[1], 7))])
        table.append(['', 'Linear Momentum', '{:0<7}'.format(round(self.linearMomentum[0].pos[0], 7)), '{:0<7}'.format(round(self.linearMomentum[0].pos[1], 7))])
        for i in range(len(self.bodies)):
            table.append(['Body {}'.format(i + 1)])
            table.append(['', 'Position', '{:0<7}'.format(round(self.bodies[i].position[0], 7)), '{:0<7}'.format(round(self.bodies[i].position[1], 7))])
            table.append(['', 'Velocity', '{:0<7}'.format(round(self.bodies[i].velocity[0], 7)), '{:0<7}'.format(round(self.bodies[i].velocity[1], 7))])
            table.append(['', 'Acceleration', '{:0<7}'.format(round(self.bodies[i].acceleration[0], 7)), '{:0<7}'.format(round(self.bodies[i].acceleration[1], 7))])
            table.append(['', 'Linear Momentum', '{:0<7}'.format(round(self.linearMomentum[i + 1].pos[0], 7)), '{:0<7}'.format(round(self.linearMomentum[i + 1].pos[1], 7))])
        phyber_logging.table(table, 20)