import math

class vec2:
    def __init__(self, x, y):
        self.values = [x, y]

    def __iter__(self):
        return self.values.__iter__()

    def __len__(self):
        return self.values.__len__()

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, item):
        self.values[key] = item

    def __repr__(self):
        return str('vec2 -> ') + str(self.values)

    def __add__(self, other):
        assert type(other) == type(self)
        return vec2(self[0] + other[0], self[1] + other[1])

    def __sub__(self, other):
        assert type(other) == type(self)
        return vec2(self[0] - other[0], self[1] - other[1])

    def __mul__(self, other):
        if type(other) == type(self):
            return vec2(self[0] * other[0], self[1] * other[1])
        elif type(other) == type(1) or type(other) == type(1.0):
            return vec2(self[0] * other, self[1] * other)
        else:
            raise Exception

    def __rmul__(self, other):
        v = self.__mul__(other)
        return vec2(v[0], v[1])

    def __iadd__(self, other):
        assert type(other) == type(self)
        self = self + other
        return self

    def __isub__(self, other):
        assert type(other) == type(self)
        self = self - other
        return self

    def __imul__(self, other):
        if type(other) == type(self):
            self = self * other
            return self
        elif type(other) == type(1) or type(other) == type(1.0):
            self = self * other
            return self

    def magnitude(self):
        return math.sqrt((self[0] ** 2) + (self[1] ** 2))

    def normalize(self):
        self = self * (1 / self.magnitude())

    @staticmethod
    def vec_magnitude(v):
        return math.sqrt((v[0] ** 2) + (v[1] ** 2))

    @staticmethod
    def vec_from_points(v1, v2):
        return vec2(v2[0] - v1[0], v2[1]- v1[1])

    @staticmethod
    def vec_distance(v1, v2):
        return vec2.vec_magnitude(vec2.vec_from_points(v1, v2))

    @staticmethod
    def vec_angle_x(v):
        if v[0] != 0 or v[1] != 0:
            return math.acos(v[0] / vec2.vec_magnitude(v))
        else:
            return 0

    @staticmethod
    def cartesian_from_polar(mag, angle):
        return vec2(math.cos(angle) * mag, math.sin(angle) * mag)

class vec4:
    def __init__(self, x, y, z, w):
        self.values = [x, y, z, w]

    def __iter__(self):
        return self.values.__iter__()

    def __len__(self):
        return self.values.__len__()

    def __getitem__(self, key):
        return self.values[key]

    def __repr__(self):
        return str('vec4 -> ') + str(self.values)

    def __add__(self, other):
        assert type(other) == type(self)
        return vec4(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3])

    def __sub__(self, other):
        assert type(other) == type(self)
        return vec4(self[0] - other[0], self[1] - other[1], self[2] - other[2], self[3] - other[3])

    def __mul__(self, other):
        if type(other) == type(self):
            return vec4(self[0] * other[0], self[1] * other[1], self[2] * other[2], self[3] * other[3])
        elif type(other) == type(1) or type(other) == type(1.0):
            return vec4(self[0] * other, self[1] * other, self[2] * other, self[3] * other)
        else:
            raise Exception

    def __rmul__(self, other):
        return self.__mul__(other)

    def __iadd__(self, other):
        assert type(other) == type(self)
        self = self + other
        return self

    def __isub__(self, other):
        assert type(other) == type(self)
        self = self - other
        return self

    def __imul__(self, other):
        if type(other) == type(self):
            self = self * other
            return self
        elif type(other) == type(1) or type(other) == type(1.0):
            self = self * other
            return self
        else:
            raise Exception

    def magnitude(self):
        return math.sqrt((self[0] ** 2) + (self[1] ** 2) + (self[2] ** 2) + (self[3] ** 2))

    def normalize(self):
        self = self * (1 / self.magnitude())

    @staticmethod
    def vec_from_points(v1, v2):
        return vec4(v2[0] - v1[0], v2[1]- v1[1], v2[2] - v1[2], v2[3] - v1[3])

    @staticmethod
    def vec_magnitude(v):
        return math.sqrt((v[0] ** 2) + (v[1] ** 2) + (v[1] ** 2) + (v[1] ** 2))

    @staticmethod
    def vec_distance(v1, v2):
        return vec4.vec_magnitude(vec4.vec_from_points(v1, v2))

    @staticmethod
    def vec_cross(v1, v2):
        # 3D
        v1.append(0)
        v2.append(0)
        return vec4((v1[1] * v2[2]) - (v1[2] * v2[1]), (v1[2] * v2[0]) - (v1[0] * v2[2]), (v1[0] * v2[1]) - (v1[1] * v2[0]), 1)

class mat4x4:
    def __init__(self):
        self.mat = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    def __iter__(self):
        return self.mat.__iter__()

    def __getitem__(self, key):
        return self.mat[key]

    def __repr__(self):
        return str('mat4x4 -> ') + str(self.mat)

    def __add__(self, other):
        mat = mat4x4()
        for r in range(4):
            for c in range(4):
                mat[r][c] = self[r][c] + other[r][c]

    def __sub__(self, other):
        mat = mat4x4()
        for r in range(4):
            for c in range(4):
                mat[r][c] = self[r][c] - other[r][c]

    def __mult__(self, other):
        mat = mat4x4()
        if type(other) == type(self):
            pass

