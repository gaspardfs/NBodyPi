# Classes utiles pour le jeu


import pygame
from pygame.locals import *
import math


class Screen():
    def __init__(self, width, height):
        self.camera = Camera()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))


class Camera():
    def __init__(self, position=[0, 0], scale=1):
        self.position = position
        self.scale = scale

    def AddZoom(self, zoom):
        self.scale = abs(self.scale + zoom)


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

        # Dessine le sprite relatif a la position de la camera
        position = [position[0] - mainScreen.camera.position[0],
                    position[1] - mainScreen.camera.position[1]]
        image = self.image
        # Dessine le sprite relatif a l'echelle de la camera
        '''
        scale = (mainScreen.camera.scale**2 * self.image.get_width(), mainScreen.camera.scale**2 * self.image.get_height())
        image = pygame.transform.scale(self.image, scale)
        
        signx, signy = 1, 1
        if position[0] < 0:
            signx = -1
        if position[1] < 0:
            signy = -1

        positionx = position[0] + ((position[0] - mainScreen.width / 2))**2 / mainScreen.width * signx
        positiony = position[1] + ((position[1] - mainScreen.height / 2))**2 / mainScreen.height * signy
        position = [positionx, positiony]
        print(position)
        #position = [math.log(abs(mainScreen.width / 2 - position[0])) * signx + position[0], math.log(abs(mainScreen.height / 2 - position[1])) * signy  + position[1]]
        '''
        mainScreen.screen.blit(image, tuple(position))


class Body():
    def __init__(self, position=[0, 0], momentum=[0, 0], mass=0, sprite=None):
        self.position = position
        self.momentum = momentum
        self.mass = mass
        self.sprite = sprite

    def draw(self, mainScreen):
        if self.sprite != None:
            self.sprite.draw(mainScreen)
