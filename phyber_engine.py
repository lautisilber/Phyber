import math

class p_Ball:
    def __init__(self, mass, radius):
        self.mass = mass
        self.radius = radius
        self.acceleration = [0, 0]
        self.velocity = [0, 0]
        self.position = [0, 0]

    def set_velocity(self, vel):
        self.velocity = vel

    def set_position(self, pos):
        self.position = pos

    def apply_acceleration(self, deltaTime):
        self.velocity[0] += self.acceleration[0] * deltaTime
        self.velocity[1] += self.acceleration[1] * deltaTime

        self.acceleration = [0, 0]

        self.position[0] += self.velocity[0] * deltaTime
        self.position[1] += self.velocity[1] * deltaTime

    def log_info(self):
        print('\ninfo ball:\n\taccel = ({}, {})\n\tvel = ({}, {})\n\tpos = ({}, {})'.format(self.acceleration[0], self.acceleration[1], self.velocity[0], self.velocity[1], self.position[0], self.position[1]))

class p_CircleMarker:
    def __init__(self, radius, colour, name, position = [0, 0]):
        self.name = name
        self.radius = radius
        self.colour = colour
        self.position = position
        self.velocity = [0, 0]
        self.acceleration = [0, 0]

    def set_radius(self, radius):
        self.radius = radius

    def set_colour(self, colour):
        self.colour = colour

    def set_position(self, position):
        self.position = position

    def set_velocity(self, vel):
        self.velocity = vel

    def set_acceleration(self, acc):
        self.acceleration = acc

    def log_info(self):
        print('{}\n\tpos = ({}, {})\n\tvel = ({}, {})\n\tacc = ({}, {})'.format(self.name, self.position[0], self.position[1], self.velocity[0], self.velocity[1], self.acceleration[0], self.acceleration[1]))

class p_ArrowMarker:
    def __init__(self, colour, thickness, pos2, pos1 = [0, 0], scale = 30000000, minLength = 10):
        self.colour = colour
        self.thickness = thickness
        self.scale = scale
        self.minLength = minLength
        self.pos1 = pos1
        self.pos2 = pos2
        self.magnitude = p_math.vec_magnitude(p_math.vec_from_points(self.pos1, self.pos2))

        self.vertices = list()
        for i in range(7):
            self.vertices.append([0, 0])

    def calc_vertices(self):
        self.magnitude = p_math.vec_magnitude(p_math.vec_from_points(self.pos1, self.pos2))
        mag = max(self.magnitude * self.scale, self.minLength)
        angle = p_math.vec_angle_x(p_math.vec_from_points(self.pos1, self.pos2))

        self.vertices[0] = p_math.cartesian_from_polar(self.thickness / 2, angle + math.pi / 2)
        self.vertices[1] = p_math.vec_add(p_math.cartesian_from_polar(mag - ((2/3) * self.thickness), angle), self.vertices[0])
        self.vertices[2] = p_math.vec_add(self.vertices[0], self.vertices[1])
        self.vertices[3] = [self.pos2[0], self.pos2[1]]
        self.vertices[4] = p_math.vec_sust(self.vertices[1], p_math.vec_mult(self.vertices[0], 2))
        self.vertices[5] = p_math.vec_add(self.vertices[4], self.vertices[0])
        self.vertices[6] = p_math.vec_mult(self.vertices[0], -1)

    def translate(self, trans):
        for i in range(len(self.vertices)):
            self.vertices[i][0] = p_math.vec_add(self.vertices[i], trans)

    def set_pos2(self, p):
        self.pos2 = p

class p_LineMarker:
    def __init__(self, colour, thikness, pos2, pos1 = [0, 0], scale = 30000000):
        self.colour = colour
        self.thickness = thikness
        self.pos1 = pos1
        self.pos2 = pos2
        self.scale = scale
        self.magnitude = p_math.vec_magnitude(p_math.vec_from_points(self.pos1, self.pos2))

        self.vert1 = self.pos1
        self.vert2 = self.pos2

    def scale_line(self):
        vec = p_math.vec_mult(p_math.vec_from_points(self.pos1, self.pos2), self.scale)

    def translate(self, trans):
        self.vert1 = p_math.vec_add(self.pos1, trans)
        self.vert2 = p_math.vec_add(self.pos2, trans)

    def set_pos2(self, p):
        self.pos2 = p


class p_math:
    @staticmethod
    def vec_add(v1, v2):
        return [v1[0] + v2[0], v1[1] + v2[1]]

    @staticmethod
    def vec_sust(v1, v2):
        return [v1[0] - v2[0], v1[0] - v2[1]]

    @staticmethod
    def vec_mult(v, k):
        return [k * v[0], k * v[1]]

    @staticmethod
    def vec_dot(v1, v2):
        return [v1[0] * v2[0], v1[1] * v2[1]]

    @staticmethod
    def vec_from_points(v1, v2):
        return [v2[0] - v1[0], v2[1]- v1[1]]

    @staticmethod
    def vec_magnitude(v):
        return math.sqrt((v[0] ** 2) + (v[1] ** 2))

    @staticmethod
    def vec_distance(v1, v2):
        return p_math.vec_magnitude(p_math.vec_from_points(v1, v2))

    @staticmethod
    def vec_angle_x(v):
        if v[0] != 0 or v[1] != 0:
            return math.acos(v[0] / p_math.vec_magnitude(v))
        else:
            return 0

    @staticmethod
    def cartesian_from_polar(mag, angle):
        return[math.cos(angle) * mag, math.sin(angle) * mag]

class Phyber:
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
        self.linearMomentum = None
        if self.showData[0]:
            self.massCenter = p_CircleMarker(10, (255, 0, 0), 'mass center')
        if self.showData[1]:
            self.linearMomentum = p_LineMarker((255, 255, 0), 3, [0, 0])

    def calculate_forces(self, deltaTime):
        # gravity
        self.calc_gravity()

        for b in self.bodies:
            b.apply_acceleration(deltaTime)

    def calc_gravity(self):
        for i in range(len(self.bodies)):
            for n in range(i + 1, len(self.bodies), 1):
                distance = p_math.vec_distance(self.bodies[i].position, self.bodies[n].position)
                if distance != 0:
                    force = self.G * ((self.bodies[i].mass * self.bodies[n].mass) / (distance ** 2))
                else:
                    log = 'Distance between bodies {} and {} is 0'.format(i, n)
                    raise Exception(log)

                unionVec = p_math.vec_from_points(self.bodies[i].position, self.bodies[n].position)
                self.bodies[i].acceleration[0] += (force * unionVec[0]) / self.bodies[i].mass
                self.bodies[i].acceleration[1] += (force * unionVec[1]) / self.bodies[i].mass
                self.bodies[n].acceleration[0] += (force * -unionVec[0]) / self.bodies[n].mass
                self.bodies[n].acceleration[1] += (force * -unionVec[1]) / self.bodies[n].mass

    def make_data_markers(self, deltaTime):
        if self.showData[0]:
            self.calc_mass_center(deltaTime)

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
        self.massCenter.set_velocity(((self.massCenter.position[0] - oldPos[0]) / deltaTime, (self.massCenter.position[1] - oldPos[1]) / deltaTime))

        self.massCenter.set_acceleration(((self.massCenter.velocity[0] - oldVel[0]) / deltaTime, (self.massCenter.velocity[1] - oldVel[1]) / deltaTime))


def main():
    b1 = p_Ball(5, 10)
    b1.set_position([5, 10])
    b2 = p_Ball(2, 5)

    phyber = Phyber([b1, b2], [True, True, False])
    phyber.calculate_forces(0.1)

    b1.log_info()
    b2.log_info()

if __name__ == '__main__':
    main()
