from Regles import LoiGravitation
import pygame
from pygame.locals import *
import Classes
import copy

def calculerPositions(bodies, stepSize, steps):
    positions = [bodies]
    for i in range(steps):

        # Calcule le nouveau momentum
        prochainesPositions = []
        for body in positions[len(positions) - 1]:
            prochainesPositions += [copy.copy(body)]

        prochainesPositions = LoiGravitation.apply(prochainesPositions, stepSize)

        # Calcule les nouvelles positions
        for body in prochainesPositions:
            body.position = [body.position[0] + body.momentum[0], body.position[1] + body.momentum[1]]
            #print(body.position)
            
        positions.append(prochainesPositions)
        #print(positions[-1][0].position)
    tout = []
    for body in positions:
        pos = []
        for posit in body:
            pos += [posit.position]
        tout += [pos]

    return(tout)

def dessinerLignes(positions, mainScreen, couleursDesCorps):
    for positionI in range(len(positions) - 1):
        for bodyI in range(len(positions[positionI])):
            pos1 = positions[positionI][bodyI]
            pos2 = positions[positionI + 1][bodyI]
            pos1, scale = mainScreen.camera.GetTransformFromCamera(pos1)
            pos2, scale = mainScreen.camera.GetTransformFromCamera(pos2)
            # scale n'est pas utilise
            pygame.draw.line(mainScreen.screen, couleursDesCorps[bodyI], pos1, pos2, 1)






            

        