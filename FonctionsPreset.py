import pickle
import copy
import time
import pygame

def SauverPreset(directoire, Bodies) -> None:
    # En premier il faut faire une copie a un deuxieme niveau de "Bodies"
    nouvBodies = []
    for body in Bodies:
        nouvBody = copy.copy(body)
        nouvBody.sprite = copy.copy(body.sprite)
        nouvBody.sprite.scale = [nouvBody.sprite.image.get_width(), nouvBody.sprite.image.get_height()]
        nouvBody.sprite.image = None
        # pickle ne peut pas pickler les images pygame, donc on doit les enlever
        # pour apres les reconstituer avec le chemin de l'image et de son echelle
        nouvBodies += [nouvBody]

    with open(directoire, "wb") as f:
        pickle.dump(nouvBodies, f)

def ChargerPreset(directoire) -> list:
    '''Retourne la liste Bodies'''
    
    '''
    try:
        with open(directoire) as f:
            data = pickle.load(f)
    except:
        data = []
        print("Erreur de chargement.")
    return data
    '''
    with open(directoire, "rb") as f:
        startTime = time.time()
        Bodies = pickle.load(f)
        for body in Bodies:
            body.reloadSprite()
        print(f"Temps de chargement {time.time() - startTime}s.")
    return Bodies
    