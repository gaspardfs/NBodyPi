from Classes import *
import math

def collisions(bodies : list, merge: bool):
    """Renvoie bodies apres collisions"""
    couples_appliques = []
    for i in range(len(bodies)):
        for j in range(len(bodies)):
            if i == j:
                continue
            if not [j, i] in couples_appliques and not [i, j] in couples_appliques:
                # Calcule la distance entre I et J
                distance = math.sqrt(abs(bodies[i].position[0] - bodies[j].position[0])**2 + 
                                    abs(bodies[i].position[1] - bodies[j].position[1])**2)
                
                if bodies[i].radius + bodies[j].radius > distance: # Si les deux corps se touchent
                    print(f"Colision entre body {i} et body {j}.")
                    if not merge:
                        detruireCorps(bodies, (i, j))
                    else:
                        mergeCorps(bodies, (i, j))
                    bodies = collisions(bodies, merge)
                    return bodies
                
                couples_appliques += [[i, j]]
    return bodies

def detruireCorps(bodies: list, collision: tuple) -> list:
    """Detruit les corps dans la liste collision"""
    index1, index2 = collision
    if index2 > index1:
        bodies.pop(index2)
        bodies.pop(index1)
    else:
        bodies.pop(index1)
        bodies.pop(index2)
    return bodies

def mergeCorps(bodies: list, collision: tuple) -> list:
    """Merge les corps en collision, mergant leurs variables selon leur masse"""
    # Fait la moyene ponderee selon la masse (sauf pour la masse)
    index1, index2 = collision
    mass1, mass2 = bodies[index1].mass, bodies[index2].mass
    massJointe = mass1 + mass2
    ratio1, ratio2 = mass1 / massJointe, mass2 / massJointe

    momentumx =  bodies[index1].momentum[0] * ratio1 + bodies[index2].momentum[0] * ratio2
    momentumy =  bodies[index1].momentum[1] * ratio1 + bodies[index2].momentum[1] * ratio2
    momentum = [momentumx, momentumy]

    positionx =  bodies[index1].position[0] * ratio1 + bodies[index2].position[0] * ratio2
    positiony =  bodies[index1].position[1] * ratio1 + bodies[index2].position[1] * ratio2
    position = [positionx, positiony]

    r = int(bodies[index1].r1 * ratio1 + bodies[index2].r1 * ratio2)
    g = int(bodies[index1].g1 * ratio1 + bodies[index2].g1 * ratio2)
    b = int(bodies[index1].b1 * ratio1 + bodies[index2].b1 * ratio2)

    nouvCorps = Body(position, momentum, massJointe, "Sprites/PlanetRed.png", r, g, b)

    # Enleve les anciens corps
    if index2 > index1:
        bodies.pop(index2)
        bodies.pop(index1)
    else:
        bodies.pop(index1)
        bodies.pop(index2)
    
    bodies.append(nouvCorps)
    return bodies
