import pygame
import os
import sys
import math
from pygame.locals import *
from Classes import *
from Functions import *

# Test

# VARIABLES
appDimensions = [600, 400]
screen = Screen(appDimensions[0], appDimensions[1])
CameraMoveSpeed = 10
CameraScrollSpeed = 300

mainScreen = Screen(600, 400)

pygame.init()
clock = pygame.time.Clock()
background = pygame.Surface((1920, 1080))
background.fill("gray")

Bodies = []
Renderer = []


pygame.mouse.set_visible(1)
pygame.display.set_caption("Simulation Gravitationelle (Q/Esc pour sortir)")

sprite1 = Body([0, 0], [0, 0], 1, "Sprites/PlanetRed.png")

sprite2 = Body([100, 0], [0, 0], 1, "Sprites/PlanetRed.png")

sprite3 = Body([300, 200], [0, 0], 1, "Sprites/PlanetRed.png")

sprite4 = Body([-200, 100], [0, 0], 1, "Sprites/PlanetRed.png")


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
            mainScreen.camera.AddZoom(event.y * -CameraScrollSpeed)

    # Keyboard movement
    keys = pygame.key.get_pressed()
    if keys[K_w]:
        mainScreen.camera.position[1] -= CameraMoveSpeed * \
            mainScreen.camera.scale
    if keys[K_s]:
        mainScreen.camera.position[1] += CameraMoveSpeed * \
            mainScreen.camera.scale
    if keys[K_a]:
        mainScreen.camera.position[0] -= CameraMoveSpeed * \
            mainScreen.camera.scale
    if keys[K_d]:
        mainScreen.camera.position[0] += CameraMoveSpeed * \
            mainScreen.camera.scale
        
body1 = Body([0, 0], [0, 0], 1, "Sprites/PlanetRed.png")
body1.force(0.5, 20)
Bodies.append(body1)

# Main game loop
while True:
    clock.tick(60)
    mainScreen.screen.blit(background, (0, 0))

    EventHandler()
    # Bodies
    for body in Bodies:
        body.position = [body.position[0] + body.momentum[0], body.position[0] + body.momentum[0]]
        body.draw(mainScreen)
        
    # Renderer
    for sprite in Renderer:
        sprite.draw(mainScreen)

    print(body1.position)
    pygame.display.update()
