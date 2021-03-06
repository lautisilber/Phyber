# Works together with the Phyber_2D engine
import math, os
from statistics import mean
import pygame
from PIL import Image
import numpy as np
tqdmInstalled = False
try:
    from tqdm import tqdm
    tqdmInstalled = True
except:
    tqdmInstalled = False
import phyber_engine_3D
from phyber_math import vec2, vec4, mat4x4

class Renderer_3D_runtime:
    def __init__(self, engine, simSpeed, size, fps):
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
                    lightDir = self.lightSource - v1 + ((((v3 - v2) * (1 / 2)) - v1) * (1 / 2))
                    lightDir[3] = 0
                    lightDir = lightDir.normalized()
                    lum = vec4.dot_product_3d(normal, lightDir)#+ ((((v3 - v2) * (1 / 2)) - v1) * (1 / 2)))

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
    def __init__(self, engine, simSpeed, size, fps, seconds):
        self.engine = engine

        self.simSpeed = simSpeed
        self.fps = fps
        self.iterations = seconds * self.fps
        self.tick = (1 / fps) * simSpeed

        self.size = size

        self.projMat = mat4x4.make_identity()
        self.lightSource = vec4(5, 5, 10, 0)
        self.camera = vec4(0, 0, 0, 0)

        self.path = os.path.dirname(os.path.realpath(__file__))
        self.tempPath = os.path.join(self.path, 'temp')

        self.frameBuffer = np.zeros((self.size[1], self.size[0], 3), dtype=np.uint8)

    def set_proj(self, fov, near, far):
        self.projMat = mat4x4.make_proj(fov, self.size[1] / self.size[0], near, far)

    def set_light_source(self, x, y, z):
        self.lightSource = vec4(x, y, z, 1)

    def reser_frame_buffer(self):
        self.frameBuffer = np.zeros((self.size[1], self.size[0], 3), dtype=np.uint8)

    def fill_triangle(self, verts, col):
        assert len(verts) == 3
        for v in verts:
            assert len(v) == 2
        
        tempBuffer = np.zeros((self.size[1], self.size[0]), dtype=np.bool)

        def draw_buffered(xf, yf):
            x = int(xf)
            y = int(yf)
            if x >= 0 and y >= 0 and x < self.size[0] and y < self.size[1]:
                tempBuffer[y][x] = True

        def draw_line_buffered(pos1, pos2):
            # borrowed from javidx's olcConsoleGameEngine
            x1 = pos1[0]
            y1 = pos1[1]
            x2 = pos2[0]
            y2 = pos2[1]

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

                draw_buffered(x, y)

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
                    draw_buffered(x, y)

            else:
                if dy >= 0:
                    x = x1
                    y = y1
                    ye = y2
                else:
                    x = x2
                    y = y2
                    ye = y1

                draw_buffered(x, y)

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
                    draw_buffered(x, y)

        def draw_triangle_buffered(verts):
            draw_line_buffered(verts[0], verts[1])
            draw_line_buffered(verts[1], verts[2])
            draw_line_buffered(verts[2], verts[0])

        draw_triangle_buffered(verts)

        for r in range(self.size[1]):
            left = -1
            right = -1
            for i in range(len(tempBuffer[r])):
                if tempBuffer[r][i]:
                    left = i
                    break
            for i in range(len(tempBuffer[r]) - 1, -1, -1):
                if tempBuffer[r][i]:
                    right = i
                    break
            if left == -1:
                pass
            else:
                if right == -1:
                    self.frameBuffer[r][left] = col
                else:
                    #for i in range(left, right + 1):
                    #    self.frameBuffer[r][i] = col
                    self.frameBuffer[r][left:right+1] = col

    def get_lum_value(self, angle):
        val = 255 * angle
        if val < 0:
            val = 0
        val = int(val)
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
                    lightDir = self.lightSource - v1 + ((((v3 - v2) * (1 / 2)) - v1) * (1 / 2))
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

    def render(self):
        if not os.path.exists(self.tempPath):
            os.mkdir(self.tempPath)
        theta = 0
        if tqdmInstalled:
            for i in tqdm(range(self.iterations)):
                self.engine.calculate_forces(self.tick)
                tris = self.to_2D(self.engine.bodies)
                for t in tris:
                    self.fill_triangle(t[:3], t[3])
                img = Image.fromarray(self.frameBuffer, 'RGB')
                img.save(os.path.join(self.tempPath, str(i) + '.png'))
                self.reser_frame_buffer()
                theta += 0.05 * self.tick / self.simSpeed
                for b in self.engine.bodies:
                    b.set_rotationZ(theta)
                    b.set_rotationX(theta * 0.5)
        else:
            for i in range(self.iterations):
                self.engine.calculate_forces(self.tick)
                tris = self.to_2D(self.engine.bodies)
                for t in tris:
                    self.fill_triangle(t[:3], t[3])
                img = Image.fromarray(self.frameBuffer, 'RGB')
                img.save(os.path.join(self.tempPath, str(i) + '.png'))
                self.reser_frame_buffer()
                theta += 0.05 * self.tick / self.simSpeed
                for b in self.engine.bodies:
                    b.set_rotationZ(theta)
                    b.set_rotationX(theta * 0.5)

        try:
            import cv2

            images = list()
            i = 0
            getImages = True
            while getImages:
                getImages = False
                for file in os.listdir(self.tempPath):
                    if file == (str(i) + '.png'):
                        images.append(os.path.join(self.tempPath, file))
                        i += 1
                        getImages = True
                        break

            frame = cv2.imread(os.path.join(self.tempPath, images[0]))
            height, width, layers = frame.shape

            video = cv2.VideoWriter(os.path.join(self.tempPath, 'video.avi'), 0, 1, (width,height))

            for image in images:
                video.write(cv2.imread(os.path.join(self.tempPath, image)))

            cv2.destroyAllWindows()
            video.release()
        except:
            print("cv2 required to render video! All frames are stored under './temp'")



# --------------------------------------------------------------------------- #

def demo3d():
    b1 = phyber_engine_3D.p_Ball_3D(60, 2)
    b2 = phyber_engine_3D.p_Ball_3D(30, 1)
    

    b1.set_translation(1, 0, -5)
    b1.set_velocity(vec4(-0.00005, 0, 0, 1))
    b2.set_translation(-1, -2, -10)
    b2.set_velocity(vec4(0.00005, 0, 0, 1))

    size = (600, 400)
    phyber = phyber_engine_3D.Phyber_3D([b1, b2])

    sim = Renderer_3D_runtime(phyber, 16, size, 60)
    sim.set_proj(size[0], size[1], 90, 100, 0.01)
    sim.init()

def demo3dOffline():
    b1 = phyber_engine_3D.p_Ball_3D(60, 2)
    b2 = phyber_engine_3D.p_Ball_3D(60, 1)
    

    b1.set_translation(5, -2, -10)
    b2.set_translation(-5, -2, -10)

    size = (600, 400)
    phyber = phyber_engine_3D.Phyber_3D([b1, b2])

    sim = Renderer_3D_Offline(phyber, 1, size, 1, 1)
    sim.set_proj(90, 0.01, 100)
    sim.set_light_source(0, 3, 0)
    sim.render()

if __name__ == '__main__':
    demo3d()
