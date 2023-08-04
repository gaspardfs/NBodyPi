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

def Jeu(variable1):
    # VARIABLES DU JEU
    appDimensions = [600, 400]

    # CAMERA
    CameraMoveSpeed = 10
    CameraScrollSpeed = 300

    # SIMULATION
    stepSize = 100000000000
    stepSpeed = 0.2 # makes a step every 0.2 seconds
    etat = 2
    # etat -1: arret, etat 0: nul, etat 1: edition, etat 2: simulation
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
    background.fill("gray")
    pygame.mouse.set_visible(1)
    pygame.display.set_caption("Simulation Gravitationelle (Q/Esc pour sortir)")


    # LISTE DE RENDERIZATION ET SIMULATION
    Bodies = []
    Renderer = []

    '''
    # Orbite
    body1 = Body([1, 1], [0, 0], 20999.0, "Sprites/PlanetRed.png", 66, 212, 245)
    body2 = Body([0, -3000], [250, 0], 999.0, "Sprites/PlanetRed.png", 66, 245, 66)
    Bodies.append(body1)
    Bodies.append(body2)
    '''

    '''
    # Caos
    body1 = Body([1, 1], [0, 0], 20999.0, "Sprites/PlanetRed.png", 66, 212, 245)
    body2 = Body([0, -3000], [250, 0], 999.0, "Sprites/PlanetRed.png", 66, 245, 66)
    body3 = Body([0, -7000], [100, 0], 999.0, "Sprites/PlanetRed.png", 245, 179, 66) 
    body4 = Body([0, 7000], [100, 0], 500.0, "Sprites/PlanetRed.png", 168, 50, 155)
    body5 = Body([0, 1500], [300, 0], 500.0, "Sprites/PlanetRed.png", 64, 50, 168)
    body6 = Body([0, 10000], [0, 50], 500.0, "Sprites/PlanetRed.png", 168, 166, 50)

    Bodies.append(body1)
    Bodies.append(body2)
    Bodies.append(body3)
    Bodies.append(body4)
    Bodies.append(body5)
    Bodies.append(body6)
    '''

    '''
    # Collisions
    body1 = Body([1500, -1000], [15, 3], 1000.0, "Sprites/PlanetRed.png", 0, 0, 255)
    body2 = Body([-2500, 0], [10, 0], 3000.0, "Sprites/PlanetRed.png", 255, 0, 0)
    body3 = Body([-4500, -1000], [-15, 3], 1000.0, "Sprites/PlanetRed.png", 0, 255, 0)

    Bodies.append(body1)
    Bodies.append(body2)
    Bodies.append(body3)
    '''
    
    # Simulation debut systeme solaire
    for i in range(100):
        pos = [random.randint(-5000, 5000), random.randint(-5000, 5000)]
        momentum = [random.randint(-300, 300), random.randint(-300, 300)]
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        corps = Body(pos, momentum, 300, "Sprites/PlanetRed.png", r, g, b)
        Bodies.append(corps)
    

    
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

    
    # Main game loop: edition
    while etat == 1:
        clock.tick(60)
        mainScreen.screen.blit(background, (0, -2))
        EventHandler()

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

    lastPerformanceUpdate = 0
    updatePerformance = True

    while etat == 2:
        clock.tick(60)
        mainScreen.screen.blit(background, (0, -2))

        
        if time.time() - lastStep > stepSpeed:
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