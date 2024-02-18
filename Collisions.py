from Classes import *
import math
import uuid

def collisions(corps : list, fusionner: bool):
    """Renvoie corps apres collisions"""
    couples_appliques = []
    for i in range(len(corps)):
        for j in range(len(corps)):
            if i == j:
                continue
            if not [j, i] in couples_appliques and not [i, j] in couples_appliques:
                # Calcule la distance entre I et J
                distance = math.sqrt(abs(corps[i].position[0] - corps[j].position[0])**2 + 
                                    abs(corps[i].position[1] - corps[j].position[1])**2)
                
                if corps[i].rayon + corps[j].rayon > distance: # Si les deux corps se touchent
                    if not fusionner:
                        detruireCorps(corps, (i, j))
                    else:
                        fusionnerCorps(corps, (i, j))
                    corps = collisions(corps, fusionner)
                    return corps
                
                couples_appliques += [[i, j]]
    return corps

def detruireCorps(corps: list, collision: tuple) -> list:
    """Detruit les corps dans la liste collision"""
    index1, index2 = collision
    if index2 > index1:
        corps.pop(index2)
        corps.pop(index1)
    else:
        corps.pop(index1)
        corps.pop(index2)
    return corps

def fusionnerCorps(corps: list, collision: tuple) -> list:
    """Fusionne les corps en collision, mergant leurs variables selon leur masse"""
    # Fait la moyene ponderee selon la masse (sauf pour la masse)
    index1, index2 = collision
    mass1, mass2 = corps[index1].masse, corps[index2].masse
    massJointe = mass1 + mass2
    ratio1, ratio2 = mass1 / massJointe, mass2 / massJointe

    momentumx =  corps[index1].momentum[0] * ratio1 + corps[index2].momentum[0] * ratio2
    momentumy =  corps[index1].momentum[1] * ratio1 + corps[index2].momentum[1] * ratio2
    momentum = [momentumx, momentumy]

    positionx =  corps[index1].position[0] * ratio1 + corps[index2].position[0] * ratio2
    positiony =  corps[index1].position[1] * ratio1 + corps[index2].position[1] * ratio2
    position = [positionx, positiony]
    
    rouge = int(corps[index1].couleur[0] * ratio1 + corps[index2].couleur[0] * ratio2)
    vert = int(corps[index1].couleur[1] * ratio1 + corps[index2].couleur[1] * ratio2)
    bleu = int(corps[index1].couleur[2] * ratio1 + corps[index2].couleur[2] * ratio2)
    couleur = (rouge, vert, bleu)

    nouvCorps = Corp(position, momentum, massJointe, "Sprites/PlanetRed.png", couleur, "Corp", uuid.uuid4())
    nouvCorps.id = uuid.uuid4()
    # Enleve les anciens corps
    if index2 > index1:
        corps.pop(index2)
        corps.pop(index1)
    else:
        corps.pop(index1)
        corps.pop(index2)
    
    corps.append(nouvCorps)
    return corps

