from Regles import LoiGravitation
from Regles import LoiGravitationLeapfrog
from pygame.locals import *
import Collisions
import copy
import uuid
import pygame



def calculerPositions(Corps, taillePas, pas):
    for i in range(len(Corps)):
        if Corps[i].id == None or Corps[i].id == -1:
            Corps[i].id = uuid.uuid4()

    positions = [] # Structure position = [x, y, id]
    prochainesPositions = [] # Element qui sert a calculer les corps actuels
    #accelerations = None
    for corp in Corps:
        prochainesPositions += [copy.copy(corp)]

    marquesColisions = []
    couleurs = {}
    for corp in Corps:
        couleurs[corp.id] = [corp.couleur]
        

    for i in range(pas):

        # Calcule le nouveau momentum et positions
        #prochainesPositions, accelerations = LoiGravitationLeapfrog.apply(prochainesPositions, taillePas, accelerations)
        prochainesPositions = LoiGravitation.apply(prochainesPositions, taillePas)

        lastCorps = [Corps[i].id for i in range(len(prochainesPositions))]
        prochainesPositions = Collisions.collisions(prochainesPositions, True)

        if len(prochainesPositions) != len(lastCorps):
            for corp in prochainesPositions: 
                couleurs[corp.id] = [corp.couleur]
                if corp.id not in lastCorps:
                    marquesColisions.append(corp)
                    lastCorps.append(corp.id)

        positionsEtape = [[corp.position[0], corp.position[1], corp.id] for corp in prochainesPositions]
        positions.append(positionsEtape)
    
    return((positions, couleurs, marquesColisions))

def dessinerLignes(positions, ecranPrincipal, couleursDesCorps, marquesColisions, reference = None):
    Corps = {}
    mouv = [0, 0]
    #positions = [[copy.copy(positions[i][j]) for j in range(len(positions[i]))] for i in range(positions)]
    positions = copy.copy(positions)

    for etape in range(len(positions) - 1):
        if reference != None:
            for corps in range(len(positions[etape])):
                if reference.id == positions[etape][corps][2]:
                    mouv = [positions[etape + 1][corps][0] - positions[etape][corps][0], 
                            positions[etape + 1][corps][1] - positions[etape][corps][1]]
                    break


        for corps in range(len(positions[etape])):
            pos1 = [positions[etape][corps][0], positions[etape][corps][1]]
            
            # Cas où le corps est detruit par une collision
            try:
                pos2 = [positions[etape + 1][corps][0] - mouv[0], 
                        positions[etape + 1][corps][1] - mouv[1]]
            except:
                continue
            
            positions[etape + 1][corps][0] = pos2[0]
            positions[etape + 1][corps][1] = pos2[1]


            pos1, echelle = ecranPrincipal.camera.CalculerPosEtEchelleParCamera(pos1)
            pos2, echelle = ecranPrincipal.camera.CalculerPosEtEchelleParCamera(pos2)
                      
            if positions[etape][corps][2] in Corps: 
                Corps[positions[etape][corps][2]].append([pos1, pos2])
            else:
                Corps[positions[etape][corps][2]] = [couleursDesCorps[positions[etape][corps][2]]]
                Corps[positions[etape][corps][2]].append([pos1, pos2])
        
    Corps = Corps.values()

    for corp in Corps:
        for i in range(1, len(corp)):
            try:
                pygame.draw.line(ecranPrincipal.screen, corp[0][0], corp[i][0], corp[i][1], 2)
            except:
                pass
    

    for collision in marquesColisions:
        collision = copy.copy(collision)
        collision.couleur = (int(collision.couleur[0] * 0.6), int(collision.couleur[1] * 0.6), int(collision.couleur[2] * 0.6))
        collision.rechargerSprite()
        collision.sprite.draw(ecranPrincipal)






            

        