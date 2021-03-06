import math, os
from statistics import mean
import pygame
import phyber_engine
from phyber_math import vec2, vec4, mat4x4

class Renderer_3D_runtime:
    def __init__(self, engine, simSpeed, size, fps):
        import pygame
        self.engine = engine

        self.simSpeed = simSpeed

        self.projMat = mat4x4.make_identity()
        self.lightSource = vec4(5, 5, 10, 0)
        self.camera = vec4(0, 0, 0, 0)

        self.fps = fps * 1000
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
        print(self.fps * self.simSpeed)
        self.engine.calculate_forces(self.fps * self.simSpeed)
        tris = self.to_2D(self.engine.bodies)
        for t in tris:
            self.draw_triangle((0, 255, 0), [t[0], t[1], t[2]], t[3])  

    def loop(self):
        theta = 0
        pressed = False
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not pressed:
                            self.screen.fill((0, 0, 0))

                            self.draw_bodies()

                            pygame.display.update()

                            pressed = True
                            print('pressed')
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        pressed = False
                

        pygame.quit()

def demo3d():
    b1 = phyber_engine.p_Ball_3D(60, 12)
    b1.set_translation(1, 0, -5)
    b1.set_velocity(vec4(-0.00005, 0, 0, 1))

    b2 = phyber_engine.p_Ball_3D(60, 6)
    b2.set_translation(-1, -2, -10)
    b2.set_velocity(vec4(0.00005, 0, 0, 1))

    b3 = phyber_engine.p_Ball_3D(30, 3)
    b3.set_translation(-2, -1, -7)
    b3.set_velocity(vec4(0.00001, 0, 0, 1))

    size = (600, 400)
    phyber = phyber_engine.Phyber_3D([b1, b2])

    sim = Renderer_3D_runtime(phyber, 16, size, 1)
    sim.set_proj(size[0], size[1], 90, 100, 0.01)
    sim.init()

if __name__ == '__main__':
    demo3d()