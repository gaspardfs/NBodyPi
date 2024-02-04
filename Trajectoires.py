from Regles import LoiGravitation
import pygame
from pygame.locals import *
import Classes
import Collisions
import copy
import uuid

'''
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
'''
def calculerPositions(bodies, stepSize, steps):
    for i in range(len(bodies)):
        bodies[i].id = uuid.uuid4()
    positions = [bodies]

    marquesColisions = []
    couleurs = {}
    for body in bodies:
        couleurs[body.id] = [body.r1, body.g1, body.b1]
        

    for i in range(steps):

        # Calcule le nouveau momentum
        prochainesPositions = []
        for body in positions[len(positions) - 1]:
            prochainesPositions += [copy.copy(body)]

        prochainesPositions = LoiGravitation.apply(prochainesPositions, stepSize)

        # Calcule les nouvelles positions
        for body in prochainesPositions:
            body.position = [body.position[0] + body.momentum[0], body.position[1] + body.momentum[1]]

        lastBodies = [bodies[i].id for i in range(len(prochainesPositions))]
        prochainesPositions = Collisions.collisions(prochainesPositions, True)

        if len(prochainesPositions) != len(lastBodies):
            for body in prochainesPositions: 
                couleurs[body.id] = [body.r1, body.g1, body.b1]
                if body.id not in lastBodies:
                    marquesColisions.append(body)
                    lastBodies.append(body.id)


        positions.append(prochainesPositions)
    
    tout = []
    for body in positions:
        pos = []
        for posit in body:
            pos += [posit.position]
        tout += [pos]
    return((positions, couleurs, marquesColisions))

def dessinerLignes(positions, mainScreen, couleursDesCorps, marquesColisions):
    bodies = {}
    for positionI in range(len(positions) - 1):
        for bodyI in range(len(positions[positionI])):
            pos1 = positions[positionI][bodyI].position
            try:
                pos2 = positions[positionI + 1][bodyI].position
            except:
                continue
            pos1, scale = mainScreen.camera.GetTransformFromCamera(pos1)
            pos2, scale = mainScreen.camera.GetTransformFromCamera(pos2)
            
            if positions[positionI][bodyI].id in bodies: 
                bodies[positions[positionI][bodyI].id].append([pos1, pos2])
            else:
                bodies[positions[positionI][bodyI].id] = [couleursDesCorps[positions[positionI][bodyI].id]]
                bodies[positions[positionI][bodyI].id].append([pos1, pos2])
        
    bodies = bodies.values()
    for body in bodies:
        for i in range(1, len(body)):
            try:
                pygame.draw.line(mainScreen.screen, (body[0][0], body[0][1], body[0][2]), body[i][0], body[i][1], 2)
            except:
                pass

    for collision in marquesColisions:
        collision = copy.copy(collision)
        collision.r1 = int(collision.r1 * 0.6)
        collision.g1 = int(collision.g1 * 0.6)
        collision.b1 = int(collision.b1 * 0.6)
        collision.reloadSprite()
        collision.sprite.draw(mainScreen)


    '''
    for positionI in range(len(positions) - 1):
        for bodyI in range(len(positions[positionI])):
            pos1 = positions[positionI][bodyI]
            pos2 = positions[positionI + 1][bodyI]
            pos1, scale = mainScreen.camera.GetTransformFromCamera(pos1)
            pos2, scale = mainScreen.camera.GetTransformFromCamera(pos2)
            # scale n'est pas utilise
            try:
                pygame.draw.line(mainScreen.screen, couleursDesCorps[bodyI], pos1, pos2, 2)
            except:
                pass
    '''






            

        