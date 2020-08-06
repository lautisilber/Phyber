import pygame
import phyber_engine_2D
from phyber_math import vec2, vec4, mat4x4

class Renderer_2D_runtime:
    def __init__(self, engine, simSpeed, size, fps):
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

    def init(self):
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
            self.engine.log()

            self.deltaTime = self.clock.tick(self.fps)
            pygame.display.update()

        pygame.quit()



def demo2d():
    b1 = phyber_engine_2D.p_Ball_2D(60, 30)
    b1.set_position(vec2(100, 20))
    b1.set_velocity(vec2(0.00003, 0.00002))

    b2 = phyber_engine_2D.p_Ball_2D(30, 15)
    b2.set_position(vec2(400, 60))
    b2.set_velocity(vec2(-0.00005, 0))

    b3 = phyber_engine_2D.p_Ball_2D(20, 10)
    b3.set_position(vec2(250, 200))

    phyber = phyber_engine_2D.Phyber_2D([b1, b2, b3], [True, True, False])
    sim = Renderer_2D_runtime(phyber, 250, (600, 400), 30)
    sim.init()

if __name__ == '__main__':
    demo2d()
