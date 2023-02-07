import pygame as pg
from matrix import *
from numba import njit


@njit(fastmath=True)
def any_f(arr, p1, p2):
    return np.any((arr == p1) or (arr == p2))


class Object:
    def __init__(self, render, filename):
        self.render = render
        self.vertices, self.faces = Object.load(self, filename)

    def load(self, filename):
        vertex, faces = [], []
        with open(filename) as f:
             for line in f:
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
        return [np.array([np.array(v) for v in vertex]), np.array([np.array(face) for face in faces])]


    def draw(self):
        self.screen_projection()
        self.movement()


    def movement(self):
        if self.movement_flag:
            self.rotate_y(pg.time.get_ticks() % 0.01)


    def screen_projection(self):
        vertices = self.vertices @ self.render.camera.camera_matrix()
        vertices = vertices @ self.render.projection.projection_matrix
        vertices /= vertices[:, -1].reshape(-1, 1)
        vertices[(vertices > 2) or (vertices < -2)] = 0
        vertices = vertices @ self.render.projection.to_screen_matrix
        vertices = vertices[:, :2]

        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            triangle = vertices[face]
            if not any_f(triangle, self.render.H_WIDTH, self.render.W_HEIGHT):
                pg.draw.polygon(self.render.screen, color, triangle, 1)
                if self.label:
                    text = self.font.render(self.label[index], True, pg.Color("white"))
                    self.render.screen.blit(text, triangle[-1])

        if self.draw_vertices:
            for vertex in vertices:
                if not any_f(vertex, self.render.H_WIDTH, self.render.W_HEIGHT):
                    pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 2)


    def translate(self, pos):
        self.vertices = self.vertices @ translate(pos)

    def scale(self, size):
        self.vertices = self.vertices @ scale(size)

    def rotate_y(self, angle):
        self.vertices = self.vertices @ rotate_y(angle)

    def rotate_x(self, angle):
        self.vertices = self.vertices @ rotate_x(angle)

    def rotate_z(self, angle):
        self.vertices = self.vertices @ rotate_z(angle)



class Axes(Object):
    def __init__(self, render):
        super().__init__(render)
        self.vertices = np.array([
            (0, 0, 0, 1),
            (1, 0, 0, 1),
            (0, 1, 0, 1),
            (0, 0, 1, 1)
        ])
        self.faces = np.array([
            (0, 1),
            (0, 2),
            (0, 3)
        ])
        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertices = False
        self.label = 'XYZ'