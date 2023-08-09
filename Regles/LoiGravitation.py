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

                vectorItoJ = math.atan2(y, x)
                vectorJtoI = vectorItoJ - math.pi
                
                bodies[i].apply_force(force * stepSize, vectorItoJ)
                bodies[j].apply_force(force * stepSize, vectorJtoI)
                couples_appliques += [[i, j]]
    return bodies