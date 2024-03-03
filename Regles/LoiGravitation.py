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

                if corps[i].masse != 0:
                    accelerationI = force * taillePas / corps[i].masse
                else:
                    accelerationI = 0
                if corps[j].masse != 0:
                    accelerationJ = force * taillePas / corps[j].masse
                else:
                    accelerationJ = 0
                    
                try:
                    vecteurI = [x * (accelerationI / distance), y * (accelerationI / distance)]
                    vecteurJ = [-x * (accelerationJ / distance), -y * (accelerationJ / distance)]
                except:
                    vecteurI = [0, 0]
                    vecteurJ = [0, 0]

                corps[i].momentum = [corps[i].momentum[0] + vecteurI[0],
                                      corps[i].momentum[1] + vecteurI[1]]
                corps[j].momentum = [corps[j].momentum[0] + vecteurJ[0],
                                      corps[j].momentum[1] + vecteurJ[1]]
                
                couples_appliques += [[i, j]]

    for corp in corps:
        corp.position = [corp.position[0] + corp.momentum[0],
                         corp.position[1] + corp.momentum[1]]
    return corps