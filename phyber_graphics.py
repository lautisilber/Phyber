# Works together with the Phyber_2D engine
import math
from statistics import mean
import pygame
import phyber_engine
from phyber_math import vec2, vec4, mat4x4

class Renderer_2D_runtime:
    def __init__(self, engine, simSpeed, size, fps):
        import pygame
        self.engine = engine

        self.simSpeed = simSpeed

        self.fps = fps
        self.deltaTime = 0
        self.lastTime = 0
        self.running = True

        pygame.init()
        self. size = size
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        self.loop()

    def window_title(self):
        pygame.display.set_caption('Phyber_2D Engine - {} fps'.format(self.clock.get_fps()))

    def calc_deltaTime(self):
        t = pygame.time.get_ticks()
        self.deltaTime = (t - self.lastTime) / 1000
        self.lastTime = t

    def draw_circle(self, colour, position, radius):
        pygame.draw.circle(self.screen, colour, (int(position[0]), int(position[1])), int(radius))

    def draw_line(self, colour, pos1, pos2, width=5):
        pygame.draw.line(self.screen, colour, pos1, pos2, width)

    def draw_polygon(self, colour, vertices, width=0):
        pygame.draw.polygon(self.screen, colour, vertices, width)

    def draw_bodies(self):
        self.engine.calculate_forces(self.deltaTime * self.simSpeed)
        for b in self.engine.bodies:
            self.draw_circle((0, 255, 0), b.position, b.radius)

    def draw_markers(self):
        self.engine.make_data_markers(self.deltaTime, self.size)
        if self.engine.showData[0]:
            self.draw_circle(self.engine.massCenter.colour, self.engine.massCenter.position, self.engine.massCenter.radius)

        if self.engine.showData[1]:
            for markers in self.engine.linearMomentum:
                self.draw_line(markers.colour, markers.vert1, markers.vert2, markers.thickness)

    def loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.window_title()
            self.screen.fill((0, 0, 0))

            self.draw_bodies()
            self.draw_markers()

            self.deltaTime = self.clock.tick(self.fps)
            pygame.display.update()

        pygame.quit()

class Renderer_3D_runtime:
    def __init__(self, engine, simSpeed, size, fps):
        import pygame
        self.engine = engine

        self.simSpeed = simSpeed

        self.projMat = mat4x4.make_identity()
        self.lightSource = vec4(5, 5, 10, 0)
        self.camera = vec4(0, 0, 0, 0)

        self.fps = fps
        self.deltaTime = 0
        self.lastTime = 0
        self.running = True

        pygame.init()
        self. size = size
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

    def set_proj(self, width, height, fov, far, near):
        self.projMat = mat4x4.make_proj(fov, height / width, near, far)
        self.width = width
        self.height = height

    def set_light_source(self, x, y, z):
        self.lightSource = vec4(x, y, z, 1)

    def init(self):
        self.loop()

    def window_title(self):
        pygame.display.set_caption('Phyber_3D Engine - {} fps'.format(self.clock.get_fps()))

    def draw_line(self, colour, pos1, pos2, width=5):
        pygame.draw.line(self.screen, colour, pos1, pos2, width)

    def draw_triangle(self, colour, verts, lum):
        pygame.draw.polygon(self.screen, lum, verts, 0)

    def get_lum_value(self, angle):
        val = 255 * angle
        if val < 0:
            val = 0
        return (val, val, val)

    def to_2D(self, bodies):
        triangles = list()
        for b in bodies:
            for tris in b.tris:
                v1 = b.rotZ * tris.verts[0]
                v2 = b.rotZ * tris.verts[1]
                v3 = b.rotZ * tris.verts[2]

                v1 = b.rotX * v1
                v2 = b.rotX * v2
                v3 = b.rotX * v3

                v1 = b.trans * v1
                v2 = b.trans * v2
                v3 = b.trans * v3

                u1 = v2 - v1
                u2 = v3 - v1
                normal = vec4.vec_cross(u1, u2)
                normal[3] = 0
                normal = normal.normalized()

                if (vec4.dot_product_3d(normal, v1 - self.camera) < 0):

                    #calculate lighting
                    lightDir = self.lightSource - ((((v3 - v2) * (1 / 2)) - v1) * (1 / 2))
                    lightDir[3] = 0
                    lightDir = lightDir.normalized()
                    lum = vec4.dot_product_3d(normal, lightDir)

                    v1 = self.projMat * v1
                    v2 = self.projMat * v2
                    v3 = self.projMat * v3

                    if (v1[3] != 0):
                        v1 *= (1 / v1[3])
                    if (v2[3] != 0):
                        v2 *= (1 / v2[3])
                    if (v3[3] != 0):
                        v3 *= (1 / v3[3])

                    #v1[0] *= -1
                    #v1[1] *= -1
                    #v2[0] *= -1
                    #v2[1] *= -1
                    #v3[0] *= -1
                    #v3[1] *= -1

                    offsetView = vec4(1, 1, 0, 0)
                    v1 = v1 + offsetView
                    v2 = v2 + offsetView
                    v3 = v3 + offsetView
                    v1[0] *= 0.5 * self.width
                    v1[1] *= 0.5 * self.height
                    v2[0] *= 0.5 * self.width
                    v2[1] *= 0.5 * self.height
                    v3[0] *= 0.5 * self.width
                    v3[1] *= 0.5 * self.height

                    triangles.append([v1[:2], v2[:2], v3[:2], self.get_lum_value(lum), mean([v1[2], v2[2], v3[2]])])
        triangles = sorted(triangles, reverse=False, key=lambda t: t[4])
        return triangles

    def draw_bodies(self):
        self.engine.calculate_forces(self.deltaTime * self.simSpeed)
        tris = self.to_2D(self.engine.bodies)
        for t in tris:
            self.draw_triangle((0, 255, 0), [t[0], t[1], t[2]], t[3])  

    def loop(self):
        theta = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.window_title()
            self.screen.fill((0, 0, 0))

            self.draw_bodies()
            theta += 0.0005 * self.deltaTime
            for b in self.engine.bodies:
                b.set_rotationZ(theta)
                b.set_rotationX(theta * 0.5)

            self.deltaTime = self.clock.tick(self.fps)
            pygame.display.update()

        pygame.quit()

class Renderer_3D_Offline:
    def __init__(self, engine, size, simSpeed, fps, seconds):
        from PIL import Image
        import numpy as np
        import os

        self.path = os.path.dirname(os.path.abspath(__file__))

        self.engine = engine
        self.simSpeed = simSpeed
        self.loops = seconds * fps

        self.projMat = mat4x4.make_identity()
        self.lightSource = vec4(5, 5, 10, 0)
        self.camera = vec4(0, 0, 0, 0)

        self.fps = fps
        self.deltaTime = 0
        self.size = size
        self.frameBuffer = np.zeros((self.size[1], self.size[0], 3), dtype=np.float32)
        self.tempBuffer = np.zeros((self.size[1], self.size[0]), dtype=np.bool)

    def set_proj(self, fov, near, far):
        self.projMat = mat4x4.make_proj(fov, self.size[1]/self.size[0], near, far)

    def reset_temp_buffer(self):
        import numpy as np
        self.tempBuffer = np.zeros((self.size[1], self.size[0]), dtype=np.bool)

    def reset_frame_buffer(self):
        import numpy as np
        self.frameBuffer = np.zeros((self.size[1], self.size[0], 3), dtype=np.float32)

    def get_lum_value(self, angle):
        val = 255 * angle
        if val < 0:
            val = 0
        return (val, val, val)

    def to_2D(self, bodies):
        triangles = list()
        for b in bodies:
            for tris in b.tris:
                v1 = b.rotZ * tris.verts[0]
                v2 = b.rotZ * tris.verts[1]
                v3 = b.rotZ * tris.verts[2]

                v1 = b.rotX * v1
                v2 = b.rotX * v2
                v3 = b.rotX * v3

                v1 = b.trans * v1
                v2 = b.trans * v2
                v3 = b.trans * v3

                u1 = v2 - v1
                u2 = v3 - v1
                normal = vec4.vec_cross(u1, u2)
                normal[3] = 0
                normal = normal.normalized()

                if (vec4.dot_product_3d(normal, v1 - self.camera) < 0):

                    #calculate lighting
                    lightDir = self.lightSource - ((((v3 - v2) * (1 / 2)) - v1) * (1 / 2))
                    lightDir[3] = 0
                    lightDir = lightDir.normalized()
                    lum = vec4.dot_product_3d(normal, lightDir)

                    v1 = self.projMat * v1
                    v2 = self.projMat * v2
                    v3 = self.projMat * v3

                    if (v1[3] != 0):
                        v1 *= (1 / v1[3])
                    if (v2[3] != 0):
                        v2 *= (1 / v2[3])
                    if (v3[3] != 0):
                        v3 *= (1 / v3[3])

                    #v1[0] *= -1
                    #v1[1] *= -1
                    #v2[0] *= -1
                    #v2[1] *= -1
                    #v3[0] *= -1
                    #v3[1] *= -1

                    offsetView = vec4(1, 1, 0, 0)
                    v1 = v1 + offsetView
                    v2 = v2 + offsetView
                    v3 = v3 + offsetView
                    v1[0] *= 0.5 * self.size[0]
                    v1[1] *= 0.5 * self.size[1]
                    v2[0] *= 0.5 * self.size[0]
                    v2[1] *= 0.5 * self.size[1]
                    v3[0] *= 0.5 * self.size[0]
                    v3[1] *= 0.5 * self.size[1]

                    triangles.append([v1[:2], v2[:2], v3[:2], self.get_lum_value(lum), mean([v1[2], v2[2], v3[2]])])
        triangles = sorted(triangles, reverse=False, key=lambda t: t[4])
        return triangles

    def draw_bodies(self, split):
        self.engine.calculate_forces(split * self.simSpeed)
        tris = self.to_2D(self.engine.bodies)
        for t in tris:
            self.fill_triangle([t[0], t[1], t[2]], t[3]) 

    def draw_buffered(self, x, y):
        if x >= 0 and y >= 0 and x < self.size[0] and y < self.size[1]:
            self.tempBuffer[y][x] = True

    def draw_line_buffered(self, pos1, pos2):
        # borrowed from javidx's olcConsoleGameEngine
        x1 = int(pos1[0])
        y1 = int(pos1[1])
        x2 = int(pos2[0])
        y2 = int(pos2[1])

        dx = x2 - x1
        dy = y2 - y1
        dx1 = abs(dx)
        dy1 = abs(dy)
        px = 2 * dy1 - dx1
        py = 2 * dx1 - dy1

        if dy1 <= dx1:
            if dx >= 0:
                x = x1
                y = y1
                xe = x2
            else:
                x = x2
                y = y2
                xe = x1

            self.draw_buffered(x, y)

            while x < xe:
                x += 1
                if px < 0:
                    px += 2 * dy1
                else:
                    if (dx < 0 and dy < 0) or (dx > 0 and dy > 0):
                        y += 1
                    else:
                        y -= 1
                    px += 2 * (dy1 - dx1)
                self.draw_buffered(x, y)

        else:
            if dy >= 0:
                x = x1
                y = y1
                ye = y2
            else:
                x = x2
                y = y2
                ye = y1

            self.draw_buffered(x, y)

            while y < ye:
                y += 1
                if py <= 0:
                    py += 2 * dx1
                else:
                    if (dx < 0 and dy < 0) or (dx > 0 and dy > 0):
                        x += 1
                    else:
                        x -= 1
                    py += 2 * (dx1 - dy1)
                self.draw_buffered(x, y)

    def draw_triangle_buffered(self, verts):
        assert len(verts) == 3
        self.draw_line_buffered(verts[0], verts[1])
        self.draw_line_buffered(verts[1], verts[2])
        self.draw_line_buffered(verts[2], verts[0])

    def fill_triangle(self, verts, col):
        self.reset_temp_buffer()
        self.draw_triangle_buffered(verts)

        for r in range(self.size[1]):
            left = -1
            right = -1
            for i in range(len(self.tempBuffer[r])):
                if self.tempBuffer[r][i] == True:
                    left = i
                    break
            for i in range(len(self.tempBuffer[r]) - 1, -1, -1):
                if self.tempBuffer[r][i] == True:
                    right = i
                    break
            if left == -1:
                pass
            else:
                if right == -1:
                    self.frameBuffer[r][left] = col
                else:
                    for i in range(left, right + 1):
                        self.frameBuffer[r][i] = col

    def render(self):
        import os
        from PIL import Image

        if not os.path.exists(os.path.join(self.path, 'temp')):
            os.mkdir(os.path.join(self.path, 'temp'))

        temp = os.path.join(self.path, 'temp')
        split = 1 / self.fps

        for i in range(self.loops):
            self.draw_bodies(split)
            img = Image.fromarray(self.frameBuffer, 'RGB')
            img.save(os.path.join(temp, str(i) + '.png'))
            self.reset_frame_buffer()




# --------------------------------------------------------------------------- #

def demo2d():
    b1 = phyber_engine.p_Ball_2D(60, 30)
    b1.set_position(vec2(100, 20))
    b1.set_velocity(vec2(0.00003, 0.00002))

    b2 = phyber_engine.p_Ball_2D(30, 15)
    b2.set_position(vec2(400, 60))
    b2.set_velocity(vec2(-0.00005, 0))

    b3 = phyber_engine.p_Ball_2D(20, 10)
    b3.set_position(vec2(250, 200))

    phyber = phyber_engine.Phyber_2D([b1, b2, b3], [True, True, False])
    sim = Renderer_2D_runtime(phyber, 250, (600, 400), 30)

def demo3d():
    b1 = phyber_engine.p_Ball_3D(120, 12)
    b1.set_translation(1, 0, -5)
    b1.set_velocity(vec4(-0.00005, 0, 0, 1))

    b2 = phyber_engine.p_Ball_3D(60, 6)
    b2.set_translation(-1, -2, -10)
    b2.set_velocity(vec4(0.00005, 0, 0, 1))

    b3 = phyber_engine.p_Ball_3D(30, 3)
    b3.set_translation(-2, -1, -7)
    b3.set_velocity(vec4(0.00001, 0, 0, 1))

    size = (600, 400)
    phyber = phyber_engine.Phyber_3D([b1, b2, b3])

    sim = Renderer_3D_runtime(phyber, 16, size, 60)
    sim.set_proj(size[0], size[1], 90, 100, 0.01)
    sim.init()

def demo3dOffline():
    b1 = phyber_engine.p_Ball_3D(120, 12)
    b1.set_translation(1, 0, -5)
    b1.set_velocity(vec4(-0.00005, 0, 0, 1))

    b2 = phyber_engine.p_Ball_3D(60, 6)
    b2.set_translation(-1, -2, -10)
    b2.set_velocity(vec4(0.00005, 0, 0, 1))

    b3 = phyber_engine.p_Ball_3D(30, 3)
    b3.set_translation(-2, -1, -7)
    b3.set_velocity(vec4(0.00001, 0, 0, 1))

    size = (600, 400)
    phyber = phyber_engine.Phyber_3D([b1, b2, b3])

    sim = Renderer_3D_Offline(phyber, size, 16, 60, 10)
    sim.set_proj(90, 0.01, 100)
    sim.render()

if __name__ == '__main__':
    demo3dOffline()
