import pygame
import sys
from pygame.locals import *
from Classes import *
from Functions import *
from Regles import LoiGravitation
import time
import Trajectoires
import copy

def Jeu(variable1):
    # VARIABLES DU JEU
    appDimensions = [600, 400]

    # CAMERA
    CameraMoveSpeed = 10
    CameraScrollSpeed = 300

    # SIMULATION
    stepSize = 100000000000
    stepSpeed = 0.1 # makes a step every 0.2 seconds
    etat = 1
    # etat -1: arret, etat 0: nul, etat 1: edition, etat 2: simulation

    # Edition
    dessinerTrajectoires = True
    nombreSteps = 1000
    multiplicateurTrajectoire = 1 # Le plus grand c'est, le moins precis la trajectoire devient mais augmente la quantite projetee


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


    sprite1 = Body([1, 1], [0, 0], 20999.0, "Sprites/PlanetRed.png", 255, 255, 255)

    sprite2 = Body([0, -3000], [250, 0], 999.0, "Sprites/PlanetRed.png", 0, 0, 0)
    #sprite1.sprite.setScale(10.0)

    #sprite3 = Body([0, 500], [20, 0], 1, "Sprites/PlanetRed.png")

    #sprite4 = Body([-200, 100], [0, 0], 1, "Sprites/PlanetRed.png")


    Bodies.append(sprite1)
    Bodies.append(sprite2)
    #Bodies.append(sprite3)
    #Bodies.append(sprite4)


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


        # print(sprite1.position)


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

    while etat == 2:
        clock.tick(60)
        mainScreen.screen.blit(background, (0, -2))

        
        if time.time() - lastStep > stepSpeed:
            lastStep = time.time()
            # Bodies
            # Applies the law for all the bodies
            Bodies = LoiGravitation.apply(Bodies, stepSize)
            for body in Bodies:
                body.position = [body.position[0] + body.momentum[0], body.position[1] + body.momentum[1]]




        EventHandler()

        # print(sprite1.position)

        # Body renderer
        for body in Bodies:
            body.draw(mainScreen)

        # Renderer
        for sprite in Renderer:
            sprite.draw(mainScreen)


        pygame.display.update()