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
            return self[0] * other[0] + self[1] * other[1]
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

    def __setitem__(self, key, item):
        self.values[key] = item

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
            return self[0] * other[0] + self[1] * other[1] + self[2] * other[2] + self[3] * other[3]
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

    def normalized(self):
        return self * (1 / self.magnitude())

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
        return vec4((v1[1] * v2[2]) - (v1[2] * v2[1]), (v1[2] * v2[0]) - (v1[0] * v2[2]), (v1[0] * v2[1]) - (v1[1] * v2[0]), 1)

    @staticmethod
    def dot_product_3d(v1, v2):
        return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

class mat4x4:
    def __init__(self):
        self.mat = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    def __iter__(self):
        return self.mat.__iter__()

    def __getitem__(self, key):
        return self.mat[key]

    def __setitem__(self, key, item):
        self.mat[key] = item

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

    def __mul__(self, other):
        if isinstance(other, vec4):
            vec = vec4(0, 0, 0, 0)
            vec[0] = other[0] * self[0][0] + other[1] * self[1][0] + other[2] * self[2][0] + other[3] * self[3][0]
            vec[1] = other[0] * self[0][1] + other[1] * self[1][1] + other[2] * self[2][1] + other[3] * self[3][1]
            vec[2] = other[0] * self[0][2] + other[1] * self[1][2] + other[2] * self[2][2] + other[3] * self[3][2]
            vec[3] = other[0] * self[0][3] + other[1] * self[1][3] + other[2] * self[2][3] + other[3] * self[3][3]
            return vec
        elif type(other) == type(1) or type(other) == type(1.0):
            mat = mat4x4()
            for c in range(4):
                for r in range(4):
                    mat[r][c] = self[r][c] * other
            return mat
        else:
            raise Exception

    @staticmethod
    def make_identity():
        mat = mat4x4()
        for i in range(4):
            mat[i][i] = 1
        return mat

    @staticmethod
    def mat_mat_multiply(m1, m2):
        assert isinstance(m1, mat4x4)
        assert isinstance(m2, mat4x4)
        mat = mat4x4()
        for c in range(4):
            for r in range(4):
                mat[r][c] = m1[r][0] * m2[0][c] + m1[r][1] * m2[1][c] + m1[r][2] * m2[2][c] + m1[r][3] * m2[3][c]
        return mat

    @staticmethod
    def mat_translation(x, y, z):
        mat = mat4x4.make_identity()
        mat[3][0] = x
        mat[3][1] = y
        mat[3][2] = z
        return mat

    @staticmethod
    def make_proj(fovDeg, aspectRatio, near, far):
        fovRad = math.radians(fovDeg)
        mat = mat4x4()
        mat[0][0] = aspectRatio * fovRad
        mat[1][1] = fovRad
        mat[2][2] = far / (far - near)
        mat[3][2] = (-far * near) / (far - near)
        mat[2][3] = 1
        mat[3][3] = 0
        return mat

    @staticmethod
    def make_rot_x(angleRad):
        mat = mat4x4()
        mat[0][0] = 1
        mat[1][1] = math.cos(angleRad)
        mat[1][2] = math.sin(angleRad)
        mat[2][1] = -math.sin(angleRad)
        mat[2][2] = math.cos(angleRad)
        mat[3][3] = 1
        return mat

    @staticmethod
    def make_rot_y(angleRad):
        mat = mat4x4()
        mat[0][0] = math.cos(angleRad)
        mat[0][2] = math.sin(angleRad)
        mat[2][0] = -math.sin(angleRad)
        mat[1][1] = 1
        mat[2][2] = math.cos(angleRad)
        mat[3][3] = 1
        return mat

    @staticmethod
    def make_rot_z(angleRad):
        mat = mat4x4()
        mat[0][0] = math.cos(angleRad)
        mat[0][1] = math.sin(angleRad)
        mat[1][0] = -math.sin(angleRad)
        mat[1][1] = math.cos(angleRad)
        mat[2][2] = 1
        mat[3][3] = 1
        return mat

    @staticmethod
    def mat_point_at(pos, target, up):
        assert isinstance(pos, vec4)
        assert isinstance(target, vec4)
        assert isinstance(up, vec4)

        newForward = target - pos
        newForward.normalize()

        a = newForward * (up * newForward)
        newUp = up - a
        newUp.normalize()

        newRight = vec4.vec_cross(newUp, newForward)

        mat = mat4x4()
        mat[0][0] = newRight[0]
        mat[0][1] = newRight[1]
        mat[0][2] = newRight[2]
        mat[0][3] = 0
        mat[1][0] = newUp[0]
        mat[1][1] = newUp[1]
        mat[1][2] = newUp[2]
        mat[1][3] = 0
        mat[2][0] = newForward[0]
        mat[2][1] = newForward[1]
        mat[2][2] = newForward[2]
        mat[2][3] = 0
        mat[3][0] = pos[0]
        mat[3][1] = pos[1]
        mat[3][2] = pos[2]
        mat[3][3] = 1

    @staticmethod
    def mat_scale(scale):
        mat = mat4x4()
        for i in range(4):
            mat[i][i] = scale
            return mat






