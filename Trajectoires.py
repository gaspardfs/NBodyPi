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
        for body in positions[-1]:
            prochainesPositions += [copy.copy(body)]

        prochainesPositions = LoiGravitation.apply(prochainesPositions, stepSize)

        # Calcule les nouvelles positions
        for body in prochainesPositions:
            body.position = [body.position[0] + body.momentum[0], body.position[1] + body.momentum[1]]
            #print(body.momentum)
            
        positions.append(prochainesPositions)
        #print(positions[-1][0].position)

    return(positions)

def dessinerLignes(positions, mainScreen, couleursDesCorps):
    for bodyI in range(len(couleursDesCorps)):
        for positionI in range(len(positions[bodyI]) - 1):
            pos1 = positions[bodyI][positionI]
            pos2 = positions[bodyI][positionI + 1]
            pos1, scale = mainScreen.camera.GetTransformFromCamera(pos1.position)
            pos2, scale = mainScreen.camera.GetTransformFromCamera(pos2.position)

            # scale n'est pas utilise
            pygame.draw.line(mainScreen.screen, couleursDesCorps[bodyI], pos1, pos2)






            

        