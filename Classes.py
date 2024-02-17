# Classes utiles pour le jeu

from PIL import ImageTk, Image
import pygame
from pygame.locals import *
import math



class Screen:
    def __init__(self, largeur, hauteur):
        self.camera = Camera([largeur, hauteur], [largeur, hauteur])
        self.width = largeur
        self.hauteur = hauteur
        self.screen = pygame.display.set_mode((largeur, hauteur), pygame.RESIZABLE)


class Camera:
    def __init__(self, Dimensions, DimensionsSim, position=[0, 0]):
        self.position = position
        # largeur et hauteur definissent les dimensions de la caméra initalement
        self.DimensionsSim = DimensionsSim  # Coordonnées dans l'espace de simulation
        self.Dimensions = Dimensions  # En pixels
        self.echelle = 1

    def AddZoom(self, zoom):
        effectif = self.DimensionsSim[0] + self.DimensionsSim[1]
        dimensions = [
            self.DimensionsSim[0] + zoom / (self.DimensionsSim[0] / effectif),
            self.DimensionsSim[1] + zoom / (self.DimensionsSim[1] / effectif),
        ]
        if dimensions[0] < 0 or dimensions[1] < 0:
            return None
        self.DimensionsSim = dimensions
        self.echelle = self.DimensionsSim[0] / self.Dimensions[0]

    def CalculerPosEtEchelleParCamera(self, position):
        """Calcule la position en pixels de la position dans la simulation"""
        centre = [int(self.DimensionsSim[0] / 2), int(self.DimensionsSim[1] / 2)]
        position = [
            position[0] - self.position[0] + centre[0],
            position[1] - self.position[1] + centre[1],
        ]
        echelle = self.Dimensions[0] / self.DimensionsSim[0]
        position = [int(position[0] * echelle), int(position[1] * echelle)]
        return (position, echelle)


class Sprite:
    def __init__(self, image, position=[0, 0]) -> None:
        self.imagePath = image
        self.image = pygame.image.load(image)
        # position est le centre de l'image
        self.position = position

    def defEchelle(self, echelle):
        if self.image != None:
            self.image = pygame.transform.scale(
                self.image,
                (self.image.get_width() * echelle, self.image.get_height() * echelle),
            )
            self.echelle = self.image.get_width() * echelle, self.image.get_height() * echelle 
        else:
            self.echelle = 64 * echelle, 64 * echelle 

        

    def draw(self, ecranPrincipal):
        # Centre la position du sprite relatif à ses dimensions
        w, h = self.image.get_width(), self.image.get_height()
        position = [self.position[0] - w / 2, self.position[1] - h / 2]

        position, echelle = ecranPrincipal.camera.CalculerPosEtEchelleParCamera(position)
        image = self.image
        image = pygame.transform.scale(
            self.image,
            [int(image.get_width() * echelle), int(image.get_height() * echelle)],
        )
        self.realImage = image
        self.realRayon = image.get_width() / 2
        self.realPosition = position
        ecranPrincipal.screen.blit(image, tuple(position))


rayonMasseMultiplier = 1500 # Densité des planètes

class Corp:
    def __init__(self, position=[0, 0], momentum=[0, 0], masse=0, sprite=None, rouge1=255, vert1=255, blue1=255, nom="Corp", id = -1):

        # Traitement de couleur
        img_colorie = Image.open("Sprites/PlanetRed.png")
        img_colorie.save("Sprites/img_colorie.png")
        img_colorie1 = img_colorie.copy()
        pimg = img_colorie.load()
        pimg1 = img_colorie1.load()
        for i in range(img_colorie1.size[0]):
            for j in range(img_colorie1.size[1]):
                (rouge, vert, bleu, alpha) = pimg[i, j]
                pimg1[i, j] = (rouge1, vert1, blue1, alpha)
        img_colorie1.save("Sprites/img_colorie1.png")
        pygame.image.load("Sprites/img_colorie1.png")
        self.sprite = Sprite("Sprites/img_colorie1.png", position)
        self.rouge1, self.vert1, self.blue1 = rouge1, vert1, blue1

        self.position = position
        self.momentum = momentum
        self.definirMasse(masse)
        self.nom = nom

    
    def setRayon(self, rayon):
        print("Plus utilisée car c'est fait automatiquement.")
        self.sprite.defEchelle(int(rayon / 16))
        self.rayon = rayon

    def definirMasse(self, masse):
        self.masse = masse
        self.rayon = (masse * rayonMasseMultiplier) ** (1. / 3) 
        self.sprite.defEchelle(int(self.rayon / 16))

    def rechargerSprite(self):
        '''Recharge les images (Pour pouvoir sauver les images)'''
        echelle = self.sprite.echelle
        img_colorie = Image.open("Sprites/PlanetRed.png")
        img_colorie.save("Sprites/img_colorie.png")
        img_colorie1 = img_colorie.copy()
        pimg = img_colorie.load()
        pimg1 = img_colorie1.load()
        for i in range(img_colorie1.size[0]):
            for j in range(img_colorie1.size[1]):
                (rouge, vert, bleu, alpha) = pimg[i, j]
                pimg1[i, j] = (self.rouge1, self.vert1, self.blue1, alpha)
        img_colorie1.save("Sprites/img_colorie1.png")
        pygame.image.load("Sprites/img_colorie1.png")
        self.sprite = Sprite("Sprites/img_colorie1.png", self.position)
        self.sprite.defEchelle(int(self.rayon / 16))

    def draw(self, ecranPrincipal):
        if self.sprite != None:
            self.sprite.position = self.position
            self.sprite.draw(ecranPrincipal)


    def apply_force(self, force, v_angle):
        if self.masse == 0:
            return None
        delta_momentum = force / self.masse
        vecteur = [math.cos(v_angle) * delta_momentum, math.sin(v_angle) * delta_momentum]
        self.momentum = [self.momentum[0] + vecteur[0], self.momentum[1] + vecteur[1]]

    
