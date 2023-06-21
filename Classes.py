# Classes utiles pour le jeu


import pygame
from pygame.locals import *
import math
from math import cos
from math import sin


class Screen():
    def __init__(self, width, height):
        self.camera = Camera([width, height], [width, height])
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))


class Camera():
    def __init__(self, Dimensions, WorldDimensions, position=[0, 0]):
        self.position = position
        # Width and height defines what range of the world positions is possible to be seen,
        # therefore, the camera pixel position and the position of the bodies are completly independant
        self.WorldDimensions = WorldDimensions  # In world coords
        self.Dimensions = Dimensions  # In pixels
        self.scale = 1

    def AddZoom(self, zoom):
        effectif = self.WorldDimensions[0] + self.WorldDimensions[1]
        dimensions = [self.WorldDimensions[0] +
                      zoom / (self.WorldDimensions[0] / effectif), self.WorldDimensions[1] + zoom / (self.WorldDimensions[1] / effectif)]
        if dimensions[0] < 0 or dimensions[1] < 0:
            return None
        self.WorldDimensions = dimensions
        self.scale = self.WorldDimensions[0] / self.Dimensions[0]

    def GetTransformFromCamera(self, position):
        """Gets the position in pixels from the world position"""
        center = [int(self.WorldDimensions[0] / 2),
                  int(self.WorldDimensions[1] / 2)]
        position = [position[0] - self.position[0] + center[0],
                    position[1] - self.position[1] + center[1]]
        scale = self.Dimensions[0] / self.WorldDimensions[0]
        position = [int(position[0] * scale), int(position[1] * scale)]
        return (position, scale)


class Sprite():

    def __init__(self, image, position=[0, 0]) -> None:
        self.image = pygame.image.load(image)
        # position is in the center of the image
        self.position = position

    def setScale(self, scale):
        self.image = pygame.transform.scale(
            self.image, scale * (self.image.get_width() * 1.0, self.image.get_height() * 1.0))

    def draw(self, mainScreen):
        # Centre la position du sprite relatif à ses dimensions
        w, h = self.image.get_width(), self.image.get_height()
        position = [self.position[0] - w / 2, self.position[1] - h / 2]

        position, scale = mainScreen.camera.GetTransformFromCamera(position)
        image = self.image
        image = pygame.transform.scale(
            self.image, [int(image.get_width() * scale), int(image.get_height() * scale)])
        mainScreen.screen.blit(image, tuple(position))


class Body():
    def __init__(self, position=[0, 0], momentum=[0, 0], mass=0, sprite=None):
        self.position = position
        self.momentum = momentum
        self.mass = mass
        self.sprite = Sprite(sprite, position)

    def draw(self, mainScreen):
        if self.sprite != None:
            self.sprite.position = self.position
            self.sprite.draw(mainScreen)

    def force(self, force, v_angle):
        delta_momentum = force / self.mass
        vx = cos(v_angle) * 1 * delta_momentum # vx est égale au côté adjacent, 1 est égale à l'hypoténuse
        vy = sin(v_angle) * 1 * delta_momentum # vy est égale au côté opposé, 1 est égale à l'hypoténuse
        self.momentum = [self.momentum[0] + vx, self.momentum[1] + vy]
