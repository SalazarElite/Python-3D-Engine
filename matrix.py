import math
import numpy as np


def translate(pos):
    tx, ty, tz = pos
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [tx, ty, tz, 1],
    ])


def rotate_x(angle):
    return np.array([
        [1, 0, 0, 0],
        [0, math.cos(angle), math.sin(angle), 0],
        [0, math.sin(angle)*-1, math.cos(angle), 0],
        [0, 0, 0, 1]
    ])


def rotate_y(angle):
    return np.array([
        [math.cos(angle), 0, math.sin(angle)*-1, 0],
        [0, 1, 0, 0],
        [0, math.sin(angle), 0, math.cos(angle)],
        [0, 0, 0, 1]
    ])


def rotate_z(angle):
    return np.array([
        [math.cos(angle), math.sin(angle), 0, 0],
        [math.sin(angle)*-1, math.cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


def scale(size):
    return np.array([
        [size, 0, 0, 0],
        [0, size, 0, 0],
        [0, 0, size, 0],
        [0, 0, 0, 1]
    ])