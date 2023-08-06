# Classes utiles pour le jeu

from PIL import ImageTk, Image
import pygame
from pygame.locals import *
import math



class Screen:
    def __init__(self, width, height):
        self.camera = Camera([width, height], [width, height])
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))


class Camera:
    def __init__(self, Dimensions, WorldDimensions, position=[0, 0]):
        self.position = position
        # Width and height defines what range of the world positions is possible to be seen,
        # therefore, the camera pixel position and the position of the bodies are completly independant
        self.WorldDimensions = WorldDimensions  # In world coords
        self.Dimensions = Dimensions  # In pixels
        self.scale = 1

    def AddZoom(self, zoom):
        effectif = self.WorldDimensions[0] + self.WorldDimensions[1]
        dimensions = [
            self.WorldDimensions[0] + zoom / (self.WorldDimensions[0] / effectif),
            self.WorldDimensions[1] + zoom / (self.WorldDimensions[1] / effectif),
        ]
        if dimensions[0] < 0 or dimensions[1] < 0:
            return None
        self.WorldDimensions = dimensions
        self.scale = self.WorldDimensions[0] / self.Dimensions[0]

    def GetTransformFromCamera(self, position):
        """Gets the position in pixels from the world position"""
        center = [int(self.WorldDimensions[0] / 2), int(self.WorldDimensions[1] / 2)]
        position = [
            position[0] - self.position[0] + center[0],
            position[1] - self.position[1] + center[1],
        ]
        scale = self.Dimensions[0] / self.WorldDimensions[0]
        position = [int(position[0] * scale), int(position[1] * scale)]
        return (position, scale)


class Sprite:
    def __init__(self, image, position=[0, 0]) -> None:
        self.imagePath = image
        self.image = pygame.image.load(image)
        # position is in the center of the image
        self.position = position

    def setScale(self, scale):
        self.image = pygame.transform.scale(
            self.image,
            (self.image.get_width() * scale, self.image.get_height() * scale),
        )
        self.scale = self.image.get_width() * scale, self.image.get_height() * scale    

        

    def draw(self, mainScreen):
        # Centre la position du sprite relatif à ses dimensions
        w, h = self.image.get_width(), self.image.get_height()
        position = [self.position[0] - w / 2, self.position[1] - h / 2]

        position, scale = mainScreen.camera.GetTransformFromCamera(position)
        image = self.image
        image = pygame.transform.scale(
            self.image,
            [int(image.get_width() * scale), int(image.get_height() * scale)],
        )
        mainScreen.screen.blit(image, tuple(position))
    
#    def color(r=255, g=255, b=255):
#        """ Entree : PIL.Image
#        Sortie : PIL.Image """
#        global image2
#        image2 = image.copy()
#        pimg1 = img1.load()
#        pimg2 = img2.load()
#        for i in range(image2.size[0]):
#            for j in range(image2.size[1]):
#                (r, v, b) = pimg1[i, j]
#                pimg2[i, j] = (r, g, b)
#        return image2

radiusMassMultiplier = 1500 # Essentialy means the density of the planets

class Body:
    def __init__(self, position=[0, 0], momentum=[0, 0], mass=0, sprite=None, r1=255, g1=255, b1=255, name="Body"):

        # Traitement de couleur
        colored_img = Image.open("Sprites/PlanetRed.png")
        colored_img.save("Sprites/colored_img.png")
        colored_img1 = colored_img.copy()
        pimg = colored_img.load()
        pimg1 = colored_img1.load()
        for i in range(colored_img1.size[0]):
            for j in range(colored_img1.size[1]):
                (r, g, b, a) = pimg[i, j]
                pimg1[i, j] = (r1, g1, b1, a)
        colored_img1.save("Sprites/colored_img1.png")
        pygame.image.load("Sprites/colored_img1.png")
        self.sprite = Sprite("Sprites/colored_img1.png", position)
        self.r1, self.g1, self.b1 = r1, g1, b1

        self.position = position
        self.momentum = momentum
        self.setMass(mass)
        self.name = name

    
    def setRadius(self, radius):
        print("Plus utilisee car c'est fait automatiquement.")
        self.sprite.setScale(int(radius / 16))
        self.radius = radius

    def setMass(self, mass):
        self.mass = mass
        self.radius = (mass * radiusMassMultiplier) ** (1. / 3) 
        self.sprite.setScale(int(self.radius / 16))

    def reloadSprite(self):
        '''Recharge les images (Pour pouvoir sauver les images)'''
        scale = self.sprite.scale
        colored_img = Image.open("Sprites/PlanetRed.png")
        colored_img.save("Sprites/colored_img.png")
        colored_img1 = colored_img.copy()
        pimg = colored_img.load()
        pimg1 = colored_img1.load()
        for i in range(colored_img1.size[0]):
            for j in range(colored_img1.size[1]):
                (r, g, b, a) = pimg[i, j]
                pimg1[i, j] = (self.r1, self.g1, self.b1, a)
        colored_img1.save("Sprites/colored_img1.png")
        pygame.image.load("Sprites/colored_img1.png")
        self.sprite = Sprite("Sprites/colored_img1.png", self.position)
        self.sprite.setScale(int(self.radius / 16))

    def draw(self, mainScreen):
        if self.sprite != None:
            self.sprite.position = self.position
            self.sprite.draw(mainScreen)

    def apply_force(self, force, v_angle):
        delta_momentum = force / self.mass
        vecteur = [math.cos(v_angle) * delta_momentum, math.sin(v_angle) * delta_momentum]
        self.momentum = [self.momentum[0] + vecteur[0], self.momentum[1] + vecteur[1]]

    
