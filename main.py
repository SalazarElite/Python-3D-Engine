import pygame as pg
from object import *
from camera import *
from projection import *


class Software:
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH //  2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_object()

    def create_object(self):
        self.camera = Camera(self, [-5, 6, -55])
        self.projection = Projection(self)
        self.object = Object(self, "3d_tank.obj")
        self.object.rotate_y((math.pi)/4)


    def draw(self):
        self.screen.fill(pg.Color('gray'))
        self.object.draw()

    def run(self):
        while True:
            self.draw()
            self.camera.control()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.set_caption(str(self.clock.get_fps))
            pg.display.flip()
            self.clock.tick(self.FPS)

if __name__ == "__main__":
    app = Software()
    app.run()