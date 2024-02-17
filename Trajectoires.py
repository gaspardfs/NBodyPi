from Regles import LoiGravitation
import pygame
from pygame.locals import *
import Classes
import Collisions
import copy
import uuid

'''
def calculerPositions(corps, taillePas, pas):
    positions = [corps]
    for i in range(pas):

        # Calcule le nouveau momentum
        prochainesPositions = []
        for corp in positions[len(positions) - 1]:
            prochainesPositions += [copy.copy(corp)]

        prochainesPositions = LoiGravitation.apply(prochainesPositions, taillePas)

        # Calcule les nouvelles positions
        for corp in prochainesPositions:
            corp.position = [corp.position[0] + corp.momentum[0], corp.position[1] + corp.momentum[1]]
            #print(corp.position)
            
        positions.append(prochainesPositions)
        #print(positions[-1][0].position)
    tout = []
    for corp in positions:
        pos = []
        for posit in corp:
            pos += [posit.position]
        tout += [pos]

    return(tout)
'''
def calculerPositions(corps, taillePas, pas):
    for i in range(len(corps)):
        corps[i].id = uuid.uuid4()
    positions = [corps]

    marquesColisions = []
    couleurs = {}
    for corp in corps:
        couleurs[corp.id] = [corp.rouge1, corp.vert1, corp.blue1]
        

    for i in range(pas):

        # Calcule le nouveau momentum
        prochainesPositions = []
        for corp in positions[len(positions) - 1]:
            prochainesPositions += [copy.copy(corp)]

        prochainesPositions = LoiGravitation.apply(prochainesPositions, taillePas)

        # Calcule les nouvelles positions
        for corp in prochainesPositions:
            corp.position = [corp.position[0] + corp.momentum[0], corp.position[1] + corp.momentum[1]]

        lastCorps = [corps[i].id for i in range(len(prochainesPositions))]
        prochainesPositions = Collisions.collisions(prochainesPositions, True)

        if len(prochainesPositions) != len(lastCorps):
            for corp in prochainesPositions: 
                couleurs[corp.id] = [corp.rouge1, corp.vert1, corp.blue1]
                if corp.id not in lastCorps:
                    marquesColisions.append(corp)
                    lastCorps.append(corp.id)


        positions.append(prochainesPositions)
    
    tout = []
    for corp in positions:
        pos = []
        for posit in corp:
            pos += [posit.position]
        tout += [pos]
    return((positions, couleurs, marquesColisions))

def dessinerLignes(positions, ecranPrincipal, couleursDesCorps, marquesColisions):
    corps = {}
    for positionI in range(len(positions) - 1):
        for corpI in range(len(positions[positionI])):
            pos1 = positions[positionI][corpI].position
            try:
                pos2 = positions[positionI + 1][corpI].position
            except:
                continue
            pos1, echelle = ecranPrincipal.camera.CalculerPosEtEchelleParCamera(pos1)
            pos2, echelle = ecranPrincipal.camera.CalculerPosEtEchelleParCamera(pos2)
            
            if positions[positionI][corpI].id in corps: 
                corps[positions[positionI][corpI].id].append([pos1, pos2])
            else:
                corps[positions[positionI][corpI].id] = [couleursDesCorps[positions[positionI][corpI].id]]
                corps[positions[positionI][corpI].id].append([pos1, pos2])
        
    corps = corps.values()
    for corp in corps:
        for i in range(1, len(corp)):
            try:
                pygame.draw.line(ecranPrincipal.screen, (corp[0][0], corp[0][1], corp[0][2]), corp[i][0], corp[i][1], 2)
            except:
                pass

    for collision in marquesColisions:
        collision = copy.copy(collision)
        collision.rouge1 = int(collision.rouge1 * 0.6)
        collision.vert1 = int(collision.vert1 * 0.6)
        collision.blue1 = int(collision.blue1 * 0.6)
        collision.rechargerSprite()
        collision.sprite.draw(ecranPrincipal)


    '''
    for positionI in range(len(positions) - 1):
        for corpI in range(len(positions[positionI])):
            pos1 = positions[positionI][corpI]
            pos2 = positions[positionI + 1][corpI]
            pos1, echelle = ecranPrincipal.camera.CalculerPosEtEchelleParCamera(pos1)
            pos2, echelle = ecranPrincipal.camera.CalculerPosEtEchelleParCamera(pos2)
            # echelle n'est pas utilise
            try:
                pygame.draw.line(ecranPrincipal.screen, couleursDesCorps[corpI], pos1, pos2, 2)
            except:
                pass
    '''






            

        