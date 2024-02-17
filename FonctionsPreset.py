import pickle
import copy
import time
import pygame

def SauverPreset(directoire, Corps) -> None:
    # En premier il faut faire une copie a un deuxieme niveau de "Corps"
    nouvCorps = []
    for corp in Corps:
        nouvCorp = copy.copy(corp)
        nouvCorp.sprite = copy.copy(corp.sprite)
        nouvCorp.sprite.echelle = [nouvCorp.sprite.image.get_width(), nouvCorp.sprite.image.get_height()]
        nouvCorp.sprite.image = None
        # pickle ne peut pas pickler les images pygame, donc on doit les enlever
        # pour apres les reconstituer avec le chemin de l'image et de son echelle
        nouvCorps += [nouvCorp]

    with open(directoire, "wb") as f:
        pickle.dump(nouvCorps, f)

def ChargerPreset(directoire) -> list:
#    try:
    with open(directoire, "rb") as f:
        momentDemarrage = time.time()
        Corps = pickle.load(f)
        for corp in Corps:
            corp.rechargerSprite()
            corp.id = -1 # compatibilité avec ancien presets
        print(f"Temps de chargement {time.time() - momentDemarrage}s.")
#    except:
#       Corps = []
#       print("Erreur de chargement")
    return Corps
    