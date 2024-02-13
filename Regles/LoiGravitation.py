import sys
sys.path.append("..")
from Classes import *
import math

# Original
G_constant = 0.000000066743

# Modifie
#G_constant = 0.000000066743

def apply(bodies : list, stepSize) -> list:
    couples_appliques = []
    for i in range(len(bodies)):
        for j in range(len(bodies)):
            if i == j:
                continue
            if not [j, i] in couples_appliques and not [i, j] in couples_appliques:
                # Calcule la distance entre I et J
                distance = math.sqrt(abs(bodies[i].position[0] - bodies[j].position[0])**2 + 
                                    abs(bodies[i].position[1] - bodies[j].position[1])**2)
                
                # Calcule la force gravitationelle entre I et J
                try:
                    force = G_constant * ((bodies[i].mass * bodies[j].mass) / distance**2)
                except:
                    force = 0
                x = bodies[j].position[0] - bodies[i].position[0]
                y = bodies[j].position[1] - bodies[i].position[1]

                accelerationI = force * stepSize / bodies[i].mass
                accelerationJ = force * stepSize / bodies[j].mass
                try:
                    vecteurI = [x * (accelerationI / distance), y * (accelerationI / distance)]
                    vecteurJ = [-x * (accelerationJ / distance), -y * (accelerationJ / distance)]
                except:
                    vecteurI = [0, 0]
                    vecteurJ = [0, 0]

                bodies[i].momentum = [bodies[i].momentum[0] + vecteurI[0],
                                      bodies[i].momentum[1] + vecteurI[1]]
                bodies[j].momentum = [bodies[j].momentum[0] + vecteurJ[0],
                                      bodies[j].momentum[1] + vecteurJ[1]]
                
                bodies[i].position = [bodies[i].position[0] + bodies[i].momentum[0],
                                      bodies[i].position[1] + bodies[i].momentum[1]]
                bodies[j].position = [bodies[j].position[0] + bodies[j].momentum[0],
                                      bodies[j].position[1] + bodies[j].momentum[1]]
                                      

                #vectorItoJ = math.atan2(y, x)
                #vectorJtoI = vectorItoJ - math.pi
                
                #bodies[i].apply_force(force * stepSize, vectorItoJ)
                #bodies[j].apply_force(force * stepSize, vectorJtoI)
                    
                
                couples_appliques += [[i, j]]
    return bodies