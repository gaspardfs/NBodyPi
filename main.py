import pygame
import os
import sys
import math
from pygame.locals import *
from Classes import *
from Functions import *

#Test

# VARIABLES
CameraMoveSpeed = 10
CameraScrollSpeed = 0.15

mainScreen = Screen(600, 400)

pygame.init()
clock = pygame.time.Clock()
background = pygame.Surface((1920, 1080))
background.fill("gray")

Renderer = []


pygame.mouse.set_visible(1)
pygame.display.set_caption("Simulation Gravitationelle (Q/Esc pour sortir)")

sprite1 = Sprite("Sprites/PlanetRed.png", [20, 20])

sprite2 = Sprite("Sprites/PlanetRed.png", [0, 400])

sprite3 = Sprite("Sprites/PlanetRed.png", [400, 400])

sprite4 = Sprite("Sprites/PlanetRed.png", [400, 0])


Renderer.append(sprite1)
Renderer.append(sprite2)
Renderer.append(sprite3)
Renderer.append(sprite4)

def EventHandler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                pygame.quit()
        if event.type == pygame.MOUSEWHEEL:
            mainScreen.camera.AddZoom(CameraScrollSpeed * math.sqrt(mainScreen.camera.scale) * event.y)
            print(mainScreen.camera.scale)

    #Keyboard movement
    keys = pygame.key.get_pressed()
    if keys[K_w]:
        mainScreen.camera.position[1] -= CameraMoveSpeed
    if keys[K_s]:
        mainScreen.camera.position[1] += CameraMoveSpeed
    if keys[K_a]:
        mainScreen.camera.position[0] -= CameraMoveSpeed
    if keys[K_d]:
        mainScreen.camera.position[0] += CameraMoveSpeed


# Main game loop
while True:
    clock.tick(60)
    mainScreen.screen.blit(background, (0, 0))


    #position = pygame.mouse.get_pos()
    #sprite1.position = position



    EventHandler()

    #Renderer
    for sprite in Renderer:
        sprite.draw(mainScreen)

    pygame.display.update()
