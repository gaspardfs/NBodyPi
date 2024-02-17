import pygame
import sys
from pygame.locals import *
from Classes import *
from Regles import LoiGravitation
import time
import Trajectoires
import copy
import Collisions
import random
import FonctionsPreset as Presets
import Interface

def Jeu(queuePourInterface, queuePourJeu):
    # VARIABLES DU JEU
    appDimensions = [600, 400]
    etat = 2
    # etat -1: arret, etat 0: nul, etat 1: edition, etat 2: simulation

    # CAMERA
    VitesseMouvementCamera = 10
    VitesseScrollCamera = 300

    # SIMULATION
    taillePas = 100000000000
    vitessePas = 0.2 # Prend un pas tous les 0.2 secondes
    compteurPas = 0
    nouveauPas = False
    pause = True
    collisions = True
    fusionner = True

    # Edition
    dessinerTrajectoires = False
    nombrePas = 1000
    multiplicateurTrajectoire = 1 # Le plus grand c'est, le moins precis la trajectoire devient mais augmente la quantite projetee
    dessinerVecteursVitesse = True

    lastMousPos = None
    glissement = None
    dragCheck = False
    flecheglissementCorpsId = None

    # Statistique
    intervaleDePerformanceUpdate = 10 # Temps en seconde entre evaluations de performance


    # FIN DES VARIABLES / DEBUT PROGRAMME
    ######################################

    
    # VARIABLES DU PROGRAMME
    actualizerPositions = True
    trajectoirePositions = None
    couleurs = None

    ecranPrincipal = Screen(appDimensions[0], appDimensions[1])
    pygame.init()
    horloge = pygame.time.Clock()

    arriere_plan = pygame.Surface((1920, 1080))
    arriere_plan.fill("black")
    pygame.mouse.set_visible(1)
    pygame.display.set_caption("Gravi Sim (Q/Esc pour sortir)")


    # LISTE DE RENDERIZATION ET SIMULATION
    Corps = []
    Renderer = []
    Fleches = {}
    reference = None

    def envoyerValeurMultiprocessing(valeur, n):
            queuePourInterface.put([n, valeur])

    def gestionnaireEvenements():
        nonlocal glissement, lastMousPos, actualizerPositions, dragCheck, flecheglissementCorpsId
        nonlocal pause
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.quit()
            if event.type == pygame.MOUSEWHEEL:
                ecranPrincipal.camera.AddZoom(event.y * -VitesseScrollCamera)

            if pygame.mouse.get_pressed()[0] == True and glissement == None and not dragCheck and etat == 1:
                colisionFleche = False
                dragCheck = True
                for fleche in Fleches.keys():
                    try:
                        if Fleches[fleche].PointDansFleche(ecranPrincipal, event.pos) == True:
                            flecheglissementCorpsId = fleche
                            lastMousPos = event.pos
                            colisionFleche = True
                    except:
                        pass
                
                if not colisionFleche:
                    for Corp in Corps:
                        position = Corp.sprite.realPosition
                        rayon = Corp.sprite.realRayon
                        rect = pygame.Rect(position[0], position[1], rayon * 2, rayon * 2)
                        try:
                            if rect.collidepoint(event.pos):
                                glissement = Corp.id 
                                lastMousPos = event.pos
                        except:
                            pass

            if event.type == MOUSEBUTTONUP:
                glissement = None
                dragCheck = False
                flecheglissementCorpsId = None

        # Mouvement par le clavier
        keys = pygame.key.get_pressed()
        if keys[K_w] or keys[K_UP]:
            ecranPrincipal.camera.position[1] -= VitesseMouvementCamera * ecranPrincipal.camera.echelle
        if keys[K_s] or keys[K_DOWN]:
            ecranPrincipal.camera.position[1] += VitesseMouvementCamera * ecranPrincipal.camera.echelle
        if keys[K_a] or keys[K_LEFT]:
            ecranPrincipal.camera.position[0] -= VitesseMouvementCamera * ecranPrincipal.camera.echelle
        if keys[K_d] or keys[K_RIGHT]:
            ecranPrincipal.camera.position[0] += VitesseMouvementCamera * ecranPrincipal.camera.echelle

        # Keyboard shortcuts
        if keys[K_SPACE]:
            if pause == pause:
                pause = not pause
            else:
                pause = pause
            
            
    dernierPas = time.time()

    def preparePickling(Corps):
        nouvCorps = []
        for corp in Corps:
            nouvCorp = copy.copy(corp)
            nouvCorp.sprite = copy.copy(corp.sprite)
            nouvCorp.sprite.image = None
            nouvCorps += [nouvCorp]
        return nouvCorps
        
    def recevoirMultiprocessing():
        nonlocal etat, compteurPas, vitessePas, actualizerPositions, Corps, pause, nouveauPas, Corps, actualizerPositions, dessinerTrajectoires
        nonlocal reference
        nonlocal nombrePas
        nouvellesCommandes = []
        # Chaque element de queue est une liste de 0: la valeur a changer et 1: la nouvelle valeur
        while not queuePourJeu.empty():
            valeur = queuePourJeu.get()
            if valeur[0] == 0: etat = valeur[1]
            elif valeur[0] == 1:
                Corps = Presets.ChargerPreset(valeur[1])
                nouvellesCommandes += [[preparePickling(Corps), 7]]
            elif valeur[0] == 2: Presets.SauverPreset(valeur[1], Corps)
            elif valeur[0] == 3: compteurPas = valeur[1]
            elif valeur[0] == 4: 
                vitessePas = valeur[1]
                nouvellesCommandes += [[vitessePas, 4]]
            elif valeur[0] == 5: pause = not pause
            elif valeur[0] == 6: nouveauPas = valeur[1]
            elif valeur[0] == 7: 
                Corps = valeur[1]
                for corp in Corps:
                    corp.rechargerSprite()
                actualizerPositions = True
                dessinerTrajectoires = True
            elif valeur[0] == 8: actualizerPositions = True
            elif valeur[0] == 9: dessinerTrajectoires = valeur[1]
            elif valeur[0] == 10: 
                nombrePas = valeur[1]
                actualizerPositions = True
            elif valeur[0] == 11:
                reference = valeur[1]
        
                
        for commande in nouvellesCommandes:
            envoyerValeurMultiprocessing(commande[0], commande[1])
    
    dernierePerformanceUpdate = 0
    updatePerformance = True

    while True:
        # Loop principal de l'édition

        if etat == 1:
            horloge.tick(60)
            ecranPrincipal.screen.blit(arriere_plan, (0, -2))
            gestionnaireEvenements()
            recevoirMultiprocessing()

            #pygame.draw.polygon(ecranPrincipal.screen, (255, 255, 255), ((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)))
        
            
            if glissement:
                pos = pygame.mouse.get_pos()
                for corp in Corps:
                    if corp.id == glissement:
                        corp.position = [corp.position[0] + (pos[0] - lastMousPos[0]) * ecranPrincipal.camera.echelle, corp.position[1] + (pos[1] - lastMousPos[1]) * ecranPrincipal.camera.echelle]
                lastMousPos = pos
                actualizerPositions = True
            
            if flecheglissementCorpsId:
                pos = pygame.mouse.get_pos()
                for corp in Corps:
                    if corp.id == flecheglissementCorpsId:
                        corp.momentum = [corp.momentum[0] + (pos[0] - lastMousPos[0]) * ecranPrincipal.camera.echelle, corp.momentum[1] + (pos[1] - lastMousPos[1]) * ecranPrincipal.camera.echelle]
                lastMousPos = pos
                actualizerPositions = True

            
            # Trajectories Renderer       
            if dessinerTrajectoires and actualizerPositions:
                momentDemarrage = time.time()

                # Copie les corps individuelement (sinon il ne marche pas)
                nouveauCorps = []
                for corp in Corps:
                    nouveauCorps += [copy.copy(corp)]

                trajectoirePositions, couleurs, marquesCollisions = Trajectoires.calculerPositions(nouveauCorps, taillePas * multiplicateurTrajectoire, nombrePas)
                #couleurs = [(corp.rouge1, corp.vert1, corp.bleu1) for corp in Corps]
                actualizerPositions = False

                print(f"{nombrePas} positions calculees pour {len(Corps)} corps en {time.time() - momentDemarrage}s.")
            
            if dessinerTrajectoires:
                Trajectoires.dessinerLignes(trajectoirePositions, ecranPrincipal, couleurs, marquesCollisions, reference)

            # Corp renderer
            for corp in Corps:
                corp.draw(ecranPrincipal)

            # Renderer
            for sprite in Renderer:
                sprite.draw(ecranPrincipal)

            # Affichage fleches
            if dessinerVecteursVitesse:
                corpsExistants = set()
                for corp in Corps:
                    if corp.id in Fleches:
                        Fleches[corp.id].debut = corp.position
                        if reference == None:
                            Fleches[corp.id].fin = [corp.position[0] + corp.momentum[0], corp.position[1] + corp.momentum[1]]
                        else:
                            Fleches[corp.id].fin = [corp.position[0] + corp.momentum[0] - reference.momentum[0], corp.position[1] + corp.momentum[1] - reference.momentum[1]]
                    else:
                        if reference == None:
                            fleche = Fleche(corp.position, [corp.position[0] + corp.momentum[0], corp.position[1] + corp.momentum[1]], 10,
                                        (abs(corp.rouge1 -255), abs(corp.vert1 -255), abs(corp.bleu1 -255)), 15)
                        else:
                            fleche = Fleche(corp.position, [corp.position[0] + corp.momentum[0] - reference.momentum[0], corp.position[1] + corp.momentum[1] - reference.momentum[1]], 10,
                                        (abs(corp.rouge1 -255), abs(corp.vert1 -255), abs(corp.bleu1 -255)), 15)
                        Fleches[corp.id] = fleche
                            
                    corpsExistants.add(corp.id)
                
                flechesToPop = []
                for fleche in Fleches.keys():
                    if fleche not in corpsExistants:
                        flechesToPop.append(fleche)
                for fleche in flechesToPop:
                    Fleches.pop(fleche)

                for fleche in Fleches.values():
                    fleche.draw(ecranPrincipal)

            pygame.display.update()

        # Loop principal de la simulation
        elif etat == 2:
            horloge.tick(60)
            ecranPrincipal.screen.blit(arriere_plan, (0, -2))
            recevoirMultiprocessing()

            if (time.time() - dernierPas > vitessePas and not pause) or nouveauPas:
                nouveauPas = False
                compteurPas += 1
                dernierPas = time.time()
                if time.time() - dernierePerformanceUpdate > intervaleDePerformanceUpdate:
                    dernierePerformanceUpdate = time.time()
                    updatePerformance = True
                # Corps
                # Applique la loi pour tous les corps
                Corps = LoiGravitation.apply(Corps, taillePas)
                #for corp in Corps:
                #    corp.position = [corp.position[0] + corp.momentum[0], corp.position[1] + corp.momentum[1]]
                if updatePerformance:
                    updatePerformance = False
                    print(f"PERFORMANCE UPDATE: Temps de calcul = {time.time() - dernierePerformanceUpdate}s, {(time.time() - dernierePerformanceUpdate) / vitessePas * 100}% de temps de calcul utilisee.")

                # Systeme de colision et fusion
                if collisions:
                    Corps = Collisions.collisions(Corps, fusionner)


            gestionnaireEvenements()


            # Corp renderer
            for corp in Corps:
                corp.draw(ecranPrincipal)

            # Renderer
            for sprite in Renderer:
                sprite.draw(ecranPrincipal)


            pygame.display.update()
