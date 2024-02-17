import sys
sys.path.append("..")
from Classes import *
import math

# Original
G_constant = 0.000000066743

# Modifie
#G_constant = 0.000000066743

def apply(corps : list, taillePas) -> list:
    couples_appliques = []
    for i in range(len(corps)):
        for j in range(len(corps)):
            if i == j:
                continue
            if not [j, i] in couples_appliques and not [i, j] in couples_appliques:
                # Calcule la distance entre I et J
                distance = math.sqrt(abs(corps[i].position[0] - corps[j].position[0])**2 + 
                                    abs(corps[i].position[1] - corps[j].position[1])**2)
                
                # Calcule la force gravitationelle entre I et J
                try:
                    force = G_constant * ((corps[i].masse * corps[j].masse) / distance**2)
                except:
                    force = 0
                x = corps[j].position[0] - corps[i].position[0]
                y = corps[j].position[1] - corps[i].position[1]

                vectorItoJ = math.atan2(y, x)
                vectorJtoI = vectorItoJ - math.pi
                
                corps[i].apply_force(force * taillePas, vectorItoJ)
                corps[j].apply_force(force * taillePas, vectorJtoI)
                couples_appliques += [[i, j]]
    return corps