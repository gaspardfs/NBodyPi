import tkinter as tk
import tkinter.filedialog as filed
from tkinter import ttk
from tkinter.colorchooser import askcolor
import Classes
import copy
import sys

def Interface(queueToInterface, queueToJeu):
    fenetre = tk.Tk()
    fenetre.title("Home")
    

    fenetre.geometry("750x300")

    #Création des bouttons
    btn_edit = tk.Button(fenetre, text = "Edit", width=46)
    btn_edit.grid(column = 1, row = 0)

    btn_sim = tk.Button(fenetre, text = "Sim", width=46)
    btn_sim.grid(column = 2, row = 0)

    etat = 1
    steps = 0
    stepSpeed = 0.2
    pause = True
    nbEtapes = 1000
    reference = None
    
    Bodies = []
    combo_box_bodies = None
    rentree_combo_body = tk.StringVar()
    champ_etapes = tk.StringVar()
    i = None
    trajectoires_visibles = False

    # display
    displayPos = None
    displayMom = None
    displayMass = None

# Création des widgets globales

    widget_edit = None  
    widget_sim = None  


# Multiprocessing

    def preparePickling(Bodies):
        nouvBodies = []
        for body in Bodies:
            nouvBody = copy.copy(body)
            nouvBody.sprite = copy.copy(body.sprite)
            nouvBody.sprite.image = None
            nouvBodies += [nouvBody]
        return nouvBodies
    
    def envoyerValeurMultiprocessing(valeur, n):
        queueToJeu.put([n, valeur])
        
    def multiprocessingIntake():
        nonlocal etat, steps, stepSpeed, Bodies
        nouvellesCommandes = []
        # Chaque element de queue est que liste de 0: la valeur a changer et 1: la nouvelle valeur
        while not queueToInterface.empty():
            valeur = queueToInterface.get()
            if valeur[0] == 0: etat = valeur[1]
            elif valeur[0] == 1: pass
            elif valeur[0] == 2: pass
            elif valeur[0] == 3: 
                steps = valeur[1]
            elif valeur[0] == 4: stepSpeed = valeur[1]
            elif valeur[0] == 7: 
                Bodies = valeur[1]

        for commande in nouvellesCommandes:
            envoyerValeurMultiprocessing(commande[0], commande[1])
    
    def envoyerListeBodies():
        nonlocal Bodies
        envoyerValeurMultiprocessing(preparePickling(Bodies), 7)

#Conséquence d'appuyer sur les buttons

    def onKeyPress(event):
        envoyerValeurMultiprocessing(5, True)

    def appuyer_chargerPreset(event):
        directoire = filed.askopenfilename()
        if directoire != "":
            envoyerValeurMultiprocessing(directoire, 1)
            multiprocessingIntake()
            while queueToInterface.empty():
                continue
            multiprocessingIntake()
            appuyer_edit(None)
            

    def appuyer_sauvegarderPreset(event):
        directoire = filed.asksaveasfile(defaultextension="")
        if directoire != "":
            envoyerValeurMultiprocessing(directoire.name, 2)

    def actualiserSimulation(stepSpeedA):
        try:
            stepSpeedA = float(stepSpeedA)
        except:
            print("Valeur invalide!")
            return None
        envoyerValeurMultiprocessing(stepSpeedA, 4)
        stepSpeed = stepSpeedA

    def pausePlay():
        nonlocal pause
        if pause:
            pause = False
            envoyerValeurMultiprocessing(False, 5)
        else:
            pause = True
            envoyerValeurMultiprocessing(True, 5)
    
    def actualiser_trajectoires(etapes):
        nonlocal nbEtapes
        try:
            nbEtapes = int(etapes)
            envoyerValeurMultiprocessing(nbEtapes, 10)
        except:
            print("Valeur(s) invalides.")

    def montrer_cacher_trajectoires(event):
        nonlocal trajectoires_visibles 
        trajectoires_visibles = not trajectoires_visibles
        envoyerValeurMultiprocessing(trajectoires_visibles, 9)

    
    def selectionner_combo_box(event):
        nonlocal i
        i = int([str(elt) for elt in rentree_combo_body.get()][-1])
        appuyer_edit(None)
    
    def appuyer_actualiser(position, momentum, mass, name, r, g, b):
        try:
            Bodies[i].position = [float(position[0]), float(position[1])]
            Bodies[i].momentum =  [float(momentum[0]), float(momentum[1])]
            Bodies[i].setMass(float(mass))
            Bodies[i].r1 = int(r)
            Bodies[i].g1 = int(g)
            Bodies[i].b1 = int(b)
            Bodies[i].name = name


            envoyerListeBodies()
        except:
            print("Valeur(s) invalide(s)!")

    def appuyer_ajouter(event):
        nouveau_corps = Classes.Body()
        Bodies.append(nouveau_corps)
        appuyer_edit(None)  

    def appuyer_enlever(event):
        nonlocal i
        try:
            Bodies.pop(i)
            i = None
            appuyer_edit(None)
        except:
            print("Erreur de suprimement")

    def appuyer_reference(event):
        nonlocal i
        try:
            reference = Bodies[i]
            envoyerValeurMultiprocessing(reference, 11)
        except:
            print("Erreur de référence", file=sys.stderr)

    def choisir_couleur():
#        global couleur_hex
#        couleur_hex = None
        couleur = askcolor(title="Choisir une couleur")
        tab_couleur = list(couleur)
        couleur_hex = str(tab_couleur[1])
        val_rgb = list(couleur[0])
        if i != None:
            Bodies[i].r1 = val_rgb[0]
            Bodies[i].g1 = val_rgb[1]
            Bodies[i].b1 = val_rgb[2]
            appuyer_edit(None)
        label_couleur1.config(bg=couleur_hex)
        
    def appuyer_edit(event):
        nonlocal combo_box_bodies, rentree_combo_body
        etat = 1
        envoyerValeurMultiprocessing(1, 0)
        nonlocal widget_edit, widget_sim, Bodies
        hide_frames()
        
        try:
            widget_sim.grid_forget()
        except:
            pass
        
    
        widget_edit = tk.Frame(fenetre)
        
        btn_ajouter= tk.Button(widget_edit, text = '+', width = 10)
        btn_ajouter.grid(column = 2, row = 2)
        btn_ajouter.bind("<Button-1>", appuyer_ajouter)

        btn_enlever= tk.Button(widget_edit, text = '-', width = 10)
        btn_enlever.bind("<Button-1>", appuyer_enlever)
        btn_enlever.grid(column = 3, row = 2)

        btn_reference = tk.Button(widget_edit, text = "Utiliser référence", width = 10)
        btn_reference.grid(column = 4, row = 2)
        btn_reference.bind("<Button-1>", appuyer_reference)

        
        combo_box_bodies = ttk.Combobox(widget_edit, textvariable = rentree_combo_body, values = Bodies, state = "readonly")
        combo_box_bodies.bind('<<ComboboxSelected>>', selectionner_combo_box)
        combo_box_bodies['values'] = tuple([[Bodies[i].name, i] for i in range(len(Bodies))])
        combo_box_bodies.grid(column = 1, row = 2)
    
        label_pos = tk.Label(widget_edit, text = "Position")
        label_pos.grid(column = 0, row = 5)
        
        label_x = tk.Label(widget_edit, text = "x")
        label_x.grid(column = 1, row = 5)
        
        label_y = tk.Label(widget_edit, text = "y")
        label_y.grid(column = 3, row = 5)
    
        label_momentum = tk.Label(widget_edit, text = "Momentum")
        label_momentum.grid(column = 0, row = 6)
        
        label_mom_x = tk.Label(widget_edit, text = "x")
        label_mom_x.grid(column = 1, row = 6)
        
        label_mom_y = tk.Label(widget_edit, text = "y")
        label_mom_y.grid(column = 3, row = 6)
        
        label_masse = tk.Label(widget_edit, text = "Masse")
        label_masse.grid(column = 0, row = 8)
        
        label_etapes = tk.Label(widget_edit, text = "Nb d'étapes")
        label_etapes.grid(column = 0, row = 14)

        label_nom = tk.Label(widget_edit, text = "Nom")
        label_nom.grid(column = 0, row = 9)

        label_couleur = tk.Label(widget_edit, text = "Couleur (r,v,b)")
        label_couleur.grid(column = 0, row = 10)

        label_config_trajectoires = tk.Label(widget_edit, text = "Configuration des trajectoires")
        label_config_trajectoires.grid(column = 2, row = 13)

        entree_pos_x = tk.Entry(widget_edit, width = 10)
        entree_pos_x.grid(column = 2, row = 5)
        
        entree_pos_y = tk.Entry(widget_edit, width = 10)
        entree_pos_y.grid(column = 4, row = 5)
    
        entree_momentum_x = tk.Entry(widget_edit, width = 10)
        entree_momentum_x.grid(column = 2, row = 6)
    
        entree_momentum_y = tk.Entry(widget_edit, width = 10)
        entree_momentum_y.grid(column = 4, row = 6)
        
        entree_masse = tk.Entry(widget_edit, width = 10, )
        entree_masse.grid(column = 1, row = 8)

        entree_nom = tk.Entry(widget_edit, width = 10, )
        entree_nom.grid(column = 1, row = 9)

        btn_slc_couleurs = tk.Button(widget_edit, text="Choisir une couleur", width=15, command=choisir_couleur)
        btn_slc_couleurs.grid(column = 4, row = 10)

        entree_r = tk.Entry(widget_edit, width = 10, )
        entree_r.grid(column = 1, row = 10)

        entree_v = tk.Entry(widget_edit, width = 10, )
        entree_v.grid(column = 2, row = 10)

        entree_b = tk.Entry(widget_edit, width = 10, )
        entree_b.grid(column = 3, row = 10)

        global label_couleur1
        label_couleur1 = tk.Label(widget_edit, bg=None, width=10)
        label_couleur1.grid(column = 2, row = 11)

        if i != None:
            combo_box_bodies.state = [Bodies[i].name, i]
            entree_masse.insert(0, Bodies[i].mass)
            entree_pos_x.insert(0, Bodies[i].position[0])
            entree_pos_y.insert(0, Bodies[i].position[1])
            entree_momentum_x.insert(0, Bodies[i].momentum[0])
            entree_momentum_y.insert(0, Bodies[i].momentum[1])
            entree_nom.insert(0, Bodies[i].name)
            entree_r.insert(0, Bodies[i].r1)
            entree_v.insert(0, Bodies[i].g1)
            entree_b.insert(0, Bodies[i].b1)
            

        
        champ_etapes = tk.Entry(widget_edit, width=10)
        champ_etapes.insert(0, str(nbEtapes)) 
        champ_etapes.grid(column=1, row=13)

        btn_act_trajectoires = tk.Button(widget_edit, text="Actualiser trajectoires", command= lambda: actualiser_trajectoires(champ_etapes.get()))
        btn_act_trajectoires.grid(column=2, row=14)

        btn_montrer_trajectoires = tk.Button(widget_edit, text="Montrer/Cacher trajectoires")
        btn_montrer_trajectoires.grid(column=3, row=14)
        btn_montrer_trajectoires.bind("<Button-1>", montrer_cacher_trajectoires)

       
        btn_chargerPreset = tk.Button(widget_edit, text = "Charger preset") 
        btn_chargerPreset.grid(column = 0, row = 0)
        btn_chargerPreset.bind("<Button-1>", appuyer_chargerPreset)

        btn_sauvegarderPreset = tk.Button(widget_edit, text = "Sauvegarder preset") 
        btn_sauvegarderPreset.grid(column = 1, row = 0)
        btn_sauvegarderPreset.bind("<Button-1>", appuyer_sauvegarderPreset)
        
        btn_actualiser = tk.Button(widget_edit, text = "Actualiser", background="green",command= lambda: 
                                   appuyer_actualiser([entree_pos_x.get(), entree_pos_y.get()], 
                                                      [entree_momentum_x.get(), entree_momentum_y.get()], entree_masse.get(), entree_nom.get(),
                                                      entree_r.get(), entree_v.get(), entree_b.get())) 
        btn_actualiser.grid(column = 2, row = 12)
       
        widget_edit.grid(column = 0, row = 60, columnspan = 3)
        
    def appuyer_sim(event):
        nonlocal widget_edit, widget_sim, etat
        etat = 2
        envoyerValeurMultiprocessing(2, 0)
        hide_frames()
        
        try:
            widget_edit.grid_forget()
        except:
            pass
        
        widget_sim = tk.Frame(fenetre, width = 18 * 3)
        widget_sim.grid(row=1, column=0, columnspan = 3)
        
        #btn_base = tk.Button(widget_sim, text = "base")
        #btn_base.grid(column = 0, row = 0)
        labelStepSpeed = tk.Label(widget_sim, text="Vitesse des pas (s)")
        entreeStepSpeed = tk.Entry(widget_sim)
        entreeStepSpeed.insert(0, str(stepSpeed))
        labelStepSpeed.grid(row = 1, column=0)
        entreeStepSpeed.grid(row = 1, column=1)

        btnActualiserValeurs = tk.Button(widget_sim, text="Actualiser simulation", background="green",
                                          command= lambda: actualiserSimulation(entreeStepSpeed.get()))
        btnActualiserValeurs.grid(row=2, column=1)

        btnPause = tk.Button(widget_sim, text="Pause/Play", command= lambda: pausePlay())
        btnPause.grid(row=3, column=0)
        btnNouvEtape = tk.Button(widget_sim, text="+Etape", command= lambda: envoyerValeurMultiprocessing(True, 6))
        btnNouvEtape.grid(row=3, column=1)


        #btnActualiserValeurs.bind("<Button-1>", lambda event, stepSpeedA=float(entreeStepSpeed.get()), n=4: envoyerValeurMultiprocessingEvent(event, n, stepSpeedA))

        
        
    def hide_frames():
        nonlocal widget_edit, widget_sim

        # actualise les valeurs du multiprocessing
        multiprocessingIntake()
        frames = [widget_edit, widget_sim]
        for frame in frames:
            if frame is not None:
                frame.grid_forget()

    btn_edit.bind("<Button-1>", appuyer_edit)
    btn_sim.bind("<Button-1>", appuyer_sim)

    fenetre.mainloop()