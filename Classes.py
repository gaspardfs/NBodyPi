# Classes utiles pour le jeu

from PIL import ImageTk, Image
import pygame
from pygame.locals import *
import math
import uuid
from shapely.geometry import Point, Polygon



class Screen:
    def __init__(self, width, height):
        self.camera = Camera([width, height], [width, height])
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)


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


    def EstVisible(self, PositionEcran):
        if PositionEcran[0] < 0 or PositionEcran[1] < 0 or PositionEcran[0] > self.Dimensions[0] or PositionEcran[1] > self.Dimensions[1]:
            return False
        return True
        


class Sprite:
    def __init__(self, image, position=[0, 0]) -> None:
        self.imagePath = image
        self.image = pygame.image.load(image)
        # position is in the center of the image
        self.position = position

    def setScale(self, scale):
        if self.image != None:
            self.image = pygame.transform.scale(
                self.image,
                (self.image.get_width() * scale, self.image.get_height() * scale),
            )
            self.scale = self.image.get_width() * scale, self.image.get_height() * scale 
        else:
            self.scale = 64 * scale, 64 * scale 

        

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
        self.realImage = image
        self.realRadius = image.get_width() / 2
        self.realPosition = position
        mainScreen.screen.blit(image, tuple(position))

radiusMassMultiplier = 1500 # Essentialy means the density of the planets

class Body:
    def __init__(self, position=[0, 0], momentum=[0, 0], mass=0, sprite=None, r1=255, g1=255, b1=255, name="Body", id = -1):

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
        if id == -1:
            self.id = uuid.uuid4()
        else:
            self.id = id

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
        if self.mass == 0:
            return None
        delta_momentum = force / self.mass
        vecteur = [math.cos(v_angle) * delta_momentum, math.sin(v_angle) * delta_momentum]
        self.momentum = [self.momentum[0] + vecteur[0], self.momentum[1] + vecteur[1]]

class Fleche:
    def __init__(self, debut=[0, 0], fin=[0, 0], largeur=10, couleur=(255, 255, 255), normalizerCamera = False, dimensionsPointe = 8):
        self.debut = debut
        self.fin = fin
        self.largeur = largeur
        self.couleur = couleur
        self.dimensionsPointe = dimensionsPointe
        self.normalizerCamera = normalizerCamera
    
    def draw(self, mainScreen):
        # Code non original
        debut, scale = mainScreen.camera.GetTransformFromCamera(self.debut)
        fin, scale = mainScreen.camera.GetTransformFromCamera(self.fin)
        rad = math.pi / 180

        pygame.draw.line(mainScreen.screen, self.couleur, debut, fin, self.largeur)
        rotation = (math.atan2(debut[1] - fin[1], fin[0] - debut[0])) + math.pi/2
        pygame.draw.polygon(mainScreen.screen, self.couleur, ((fin[0] + self.dimensionsPointe * math.sin(rotation),
                                        fin[1] + self.dimensionsPointe * math.cos(rotation)),
                                    (fin[0] + self.dimensionsPointe * math.sin(rotation - 120*rad),
                                        fin[1] + self.dimensionsPointe * math.cos(rotation - 120*rad)),
                                    (fin[0] + self.dimensionsPointe * math.sin(rotation + 120*rad),
                                        fin[1] + self.dimensionsPointe * math.cos(rotation + 120*rad))))

    
    def PointDansFleche(self, mainScreen, point):
        # Code non original
        debut, scale = mainScreen.camera.GetTransformFromCamera(self.debut)
        fin, scale = mainScreen.camera.GetTransformFromCamera(self.fin)
        point = Point(point)

        rad = math.pi / 180
        pygame.draw.line(mainScreen.screen, self.couleur, debut, fin, self.largeur)
        rotation = (math.atan2(debut[1] - fin[1], fin[0] - debut[0])) + math.pi/2
        dimensions = ((fin[0] + self.dimensionsPointe * math.sin(rotation),
                                        fin[1] + self.dimensionsPointe * math.cos(rotation)),
                                       (fin[0] + self.dimensionsPointe * math.sin(rotation - 120*rad),
                                        fin[1] + self.dimensionsPointe * math.cos(rotation - 120*rad)),
                                       (fin[0] + self.dimensionsPointe * math.sin(rotation + 120*rad),
                                        fin[1] + self.dimensionsPointe * math.cos(rotation + 120*rad)))
        dimensions = Polygon(dimensions)
        
        if point.within(dimensions):
            return True
        
        dimensions = ((debut[0] - self.largeur / 2, debut[1] + self.largeur / 2),
                      (fin[0] + self.largeur / 2, fin[1] + self.largeur / 2),
                      (fin[0] + self.largeur / 2, fin[1] - self.largeur / 2),
                      (debut[0] - self.largeur / 2, debut[1] - self.largeur / 2))
        dimensions = Polygon(dimensions)
        if point.within(dimensions):
            return True
        return False


