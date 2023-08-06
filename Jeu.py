import pygame
import sys
from pygame.locals import *
from Classes import *
from Functions import *
from Regles import LoiGravitation
import time
import Trajectoires
import copy
import Collisions
import random
import FonctionsPreset as Presets

def Jeu(queueToInterface, queueToJeu):
    # VARIABLES DU JEU
    appDimensions = [600, 400]
    etat = 2
    # etat -1: arret, etat 0: nul, etat 1: edition, etat 2: simulation

    # CAMERA
    CameraMoveSpeed = 10
    CameraScrollSpeed = 300

    # SIMULATION
    stepSize = 100000000000
    stepSpeed = 0.2 # makes a step every 0.2 seconds
    stepCount = 0
    newStep = False
    pause = True
    collisions = True
    merge = True

    # Edition
    dessinerTrajectoires = True
    nombreSteps = 500
    multiplicateurTrajectoire = 1 # Le plus grand c'est, le moins precis la trajectoire devient mais augmente la quantite projetee

    # Statistique
    intervaleDePerformanceUpdate = 10 # Temps en seconde entre evaluations de performance


    # FIN DES VARIABLES / DEBUT PROGRAMME
    ######################################

    
    # VARIABLES DU PROGRAMME
    actualizerPositions = True
    trajectoirePositions = None
    couleurs = None

    mainScreen = Screen(appDimensions[0], appDimensions[1])
    pygame.init()
    clock = pygame.time.Clock()

    background = pygame.Surface((1920, 1080))
    background.fill("black")
    pygame.mouse.set_visible(1)
    pygame.display.set_caption("NBodyPi (Q/Esc pour sortir)")


    # LISTE DE RENDERIZATION ET SIMULATION
    Bodies = []
    Renderer = []

    def EventHandler():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.quit()
            if event.type == pygame.MOUSEWHEEL:
                mainScreen.camera.AddZoom(event.y * -CameraScrollSpeed)

        # Keyboard movement
        keys = pygame.key.get_pressed()
        if keys[K_w] or keys[K_UP]:
            mainScreen.camera.position[1] -= CameraMoveSpeed * mainScreen.camera.scale
        if keys[K_s] or keys[K_DOWN]:
            mainScreen.camera.position[1] += CameraMoveSpeed * mainScreen.camera.scale
        if keys[K_a] or keys[K_LEFT]:
            mainScreen.camera.position[0] -= CameraMoveSpeed * mainScreen.camera.scale
        if keys[K_d] or keys[K_RIGHT]:
            mainScreen.camera.position[0] += CameraMoveSpeed * mainScreen.camera.scale

    lastStep = time.time()

    def envoyerValeurMultiprocessing(valeur, n):
        queueToInterface.put([n, valeur])
        
    def preparePickling(Bodies):
        nouvBodies = []
        for body in Bodies:
            nouvBody = copy.copy(body)
            nouvBody.sprite = copy.copy(body.sprite)
            nouvBody.sprite.image = None
            nouvBodies += [nouvBody]
        return nouvBodies
        
    def multiprocessingIntake():
        nonlocal etat, stepCount, stepSpeed, actualizerPositions, Bodies, pause, newStep, Bodies, actualizerPositions, dessinerTrajectoires
        nouvellesCommandes = []
        # Chaque element de queue est ue liste de 0: la valeur a changer et 1: la nouvelle valeur
        while not queueToJeu.empty():
            valeur = queueToJeu.get()
            if valeur[0] == 0: etat = valeur[1]
            elif valeur[0] == 1:
                Bodies = Presets.ChargerPreset(valeur[1])
                nouvellesCommandes += [[preparePickling(Bodies), 7]]
            elif valeur[0] == 2: Presets.SauverPreset(valeur[1], Bodies)
            elif valeur[0] == 3: stepCount = valeur[1]
            elif valeur[0] == 4: 
                stepSpeed = valeur[1]
                nouvellesCommandes += [[stepSpeed, 4]]
            elif valeur[0] == 5: pause = valeur[1]
            elif valeur[0] == 6: newStep = valeur[1]
            elif valeur[0] == 7: 
                Bodies = valeur[1]
                for body in Bodies:
                    body.reloadSprite()
            elif valeur[0] == 8: actualizerPositions = True
            elif valeur[0] == 9: dessinerTrajectoires = True

        
        for commande in nouvellesCommandes:
            envoyerValeurMultiprocessing(commande[0], commande[1])
    
    lastPerformanceUpdate = 0
    updatePerformance = True

    while True:
        # Main game loop: edition
        if etat == 1:
            clock.tick(60)
            mainScreen.screen.blit(background, (0, -2))
            EventHandler()
            multiprocessingIntake()


            # Trajectories Renderer       
            if dessinerTrajectoires and actualizerPositions:
                startTime = time.time()

                # Copie les corps individuelement (sinon il ne marche pas)
                nouveauBodies = []
                for body in Bodies:
                    nouveauBodies += [copy.copy(body)]

                trajectoirePositions = Trajectoires.calculerPositions(nouveauBodies, stepSize * multiplicateurTrajectoire, nombreSteps)
                couleurs = [(body.r1, body.g1, body.b1) for body in Bodies]
                actualizerPositions = False

                print(f"{nombreSteps} positions calculees pour {len(Bodies)} corps en {time.time() - startTime}s.")
            
            if dessinerTrajectoires:
                Trajectoires.dessinerLignes(trajectoirePositions, mainScreen, couleurs)

            # Body renderer
            for body in Bodies:
                body.draw(mainScreen)

            # Renderer
            for sprite in Renderer:
                sprite.draw(mainScreen)

            pygame.display.update()

        # Main game loop: simulation
        elif etat == 2:
            clock.tick(60)
            mainScreen.screen.blit(background, (0, -2))
            multiprocessingIntake()

            if (time.time() - lastStep > stepSpeed and not pause) or newStep:
                newStep = False
                stepCount += 1
                lastStep = time.time()
                if time.time() - lastPerformanceUpdate > intervaleDePerformanceUpdate:
                    lastPerformanceUpdate = time.time()
                    updatePerformance = True
                # Bodies
                # Applies the law for all the bodies
                Bodies = LoiGravitation.apply(Bodies, stepSize)
                for body in Bodies:
                    body.position = [body.position[0] + body.momentum[0], body.position[1] + body.momentum[1]]
                if updatePerformance:
                    updatePerformance = False
                    print(f"PERFORMANCE UPDATE: Temps de calcul = {time.time() - lastPerformanceUpdate}s, {(time.time() - lastPerformanceUpdate) / stepSpeed * 100}% de temps de calcul utilisee.")

                # Sisteme de colision et merge
                if collisions:
                    Bodies = Collisions.collisions(Bodies, merge)


            EventHandler()


            # Body renderer
            for body in Bodies:
                body.draw(mainScreen)

            # Renderer
            for sprite in Renderer:
                sprite.draw(mainScreen)


            pygame.display.update()
