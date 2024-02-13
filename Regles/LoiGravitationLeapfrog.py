import sys
sys.path.append("..")
from Classes import *
import math

'''
Cela c'est une tentative de l'integration leapfrog, qui apres son application a ete plus lent que celle normale.
'''

# Original
G_constant = 0.000000066743

# Modifie
#G_constant = 0.000000066743

# Integration leapfrog 
def apply(bodies : list, stepSize, dernieresAccelerations) -> list:
    couples_appliques = []
    
    if dernieresAccelerations == None:
        accelerations = [[0, 0] for i in range(len(bodies))]
        
        for i in range(len(bodies)):
            for j in range(len(bodies)):
                if i == j: 
                    continue # Pas appliquer au meme corps
                if [j, i] in couples_appliques or [i, j] in couples_appliques:
                    continue
                distX = bodies[j].position[0] - bodies[i].position[0]
                distY = bodies[j].position[1] - bodies[i].position[1]
                distance = math.sqrt(abs(distX)**2 + abs(distY)**2)
                
                
                try:
                    force = G_constant * ((bodies[i].mass * bodies[j].mass) / distance**2)
                except:
                    force = 0

                accelerationI = force * stepSize / bodies[i].mass
                accelerationJ = force * stepSize / bodies[j].mass

                # THALES!!
                try:
                    vecteurI = [distX * (accelerationI / distance), distY * (accelerationI / distance)]
                    vecteurJ = [-distX * (accelerationJ / distance), -distY * (accelerationJ / distance)]
                except:
                    vecteurI = [0, 0]
                    vecteurJ = [0, 0]

                accelerations[i] = [accelerations[i][0] + vecteurI[0], accelerations[i][1] + vecteurI[1]]
                accelerations[j] = [accelerations[j][0] + vecteurJ[0], accelerations[j][1] + vecteurJ[1]]

                couples_appliques += [[i, j]]
    else:
        accelerations = dernieresAccelerations
        
    accelerationsProchaines = [[0, 0] for i in range(len(bodies))]
        
    for i in range(len(bodies)):
        bodies[i].position = [bodies[i].position[0] + bodies[i].momentum[0] + 0.5 * accelerations[i][0],
                              bodies[i].position[1] + bodies[i].momentum[1] + 0.5 * accelerations[i][1]]
        
    couples_appliques = []
    for i in range(len(bodies)):
        for j in range(len(bodies)):
            if i == j: 
                continue # Pas appliquer au meme corps
            if [j, i] in couples_appliques or [i, j] in couples_appliques:
                continue

            distX = bodies[j].position[0] - bodies[i].position[0]
            distY = bodies[j].position[1] - bodies[i].position[1]
            distance = math.sqrt(abs(distX)**2 + abs(distY)**2)
            try:
                force = G_constant * ((bodies[i].mass * bodies[j].mass) / distance**2)
            except:
                force = 0

            accelerationProchaineI = force * stepSize / bodies[i].mass
            accelerationProchaineJ = force * stepSize / bodies[j].mass

            try:
                vecteurIProchain = [distX * (accelerationProchaineI / distance), distY * (accelerationProchaineI / distance)]
                vecteurJProchain = [-distX * (accelerationProchaineJ / distance), -distY * (accelerationProchaineJ / distance)]
            except:
                vecteurIProchain = [0, 0]
                vecteurJProchain = [0, 0]

            accelerationsProchaines[i] = [accelerationsProchaines[i][0] + vecteurIProchain[0], accelerationsProchaines[i][1] + vecteurIProchain[1]]
            accelerationsProchaines[j] = [accelerationsProchaines[j][0] + vecteurJProchain[0], accelerationsProchaines[j][1] + vecteurJProchain[1]]
        
            couples_appliques += [[i, j]]

    for i in range(len(bodies)):
        bodies[i].momentum = [bodies[i].momentum[0] + 0.5 * (accelerations[i][0] + accelerationsProchaines[i][0]),
                              bodies[i].momentum[1] + 0.5 * (accelerations[i][1] + accelerationsProchaines[i][1])]
    

    return bodies, accelerationsProchaines