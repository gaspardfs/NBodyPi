import tkinter as tk
import tkinter.filedialog as filed
from tkinter import ttk
import Classes
import copy

def Interface(queueToInterface, queueToJeu):
    fenetre = tk.Tk()
    fenetre.title("Home")
    

    fenetre.geometry("400x400")

    #Création des bouttons
    btn_regles = tk.Button(fenetre, text ="Règles", width=18)
    btn_regles.grid(column = 0, row = 0)

    btn_edit = tk.Button(fenetre, text = "Edit", width=18)
    btn_edit.grid(column = 1, row = 0)

    btn_sim = tk.Button(fenetre, text = "Sim", width=18)
    btn_sim.grid(column = 2, row = 0)

    # champ_vitesse = tk.Entry(fenetre, width = 50)
    # champ_vitesse.grid(column = , row =)

    etat = 1
    steps = 0
    stepSpeed = 0.2
    pause = True
    
    Bodies = []
    combo_box_bodies = None
    rentree_combo_body = tk.StringVar()
    i = None

    # display
    displayPos = None
    displayMom = None
    displayMass = None

# Création des widgets globales

    widget_regles = None  
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

    def appuyer_chargerPreset(event):
        directoire = filed.askopenfilename(defaultextension="/Presets")
        if directoire != None:
            envoyerValeurMultiprocessing(directoire, 1)
            while queueToInterface.empty():
                continue
            multiprocessingIntake()
            appuyer_edit(None)
            

    def appuyer_sauvegarderPreset(event):
        directoire = filed.asksaveasfile(defaultextension="")
        if directoire != None:
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
    
    def selectionner_combo_box(event):
        nonlocal i
        i = int([str(elt) for elt in rentree_combo_body.get()][-1])
        appuyer_edit(None)


    
    def appuyer_actualiser(position, momentum, mass):
        Bodies[i].position = [float(position[0]), float(position[1])]
        Bodies[i].momentum =  [float(momentum[0]), float(momentum[1])]
        Bodies[i].setMass(float(mass))
        envoyerListeBodies()

    def appuyer_ajouter(event):
        nouveau_corps = Classes.Body()
        Bodies.append(nouveau_corps)
        appuyer_edit(None)  
    
    def appuyer_regles(event):
        nonlocal widget_regles, widget_edit, widget_sim, etat
        print("Etat edition.")
        etat = 1
        envoyerValeurMultiprocessing(1, 0)
        hide_frames()
        try:
            widget_sim.grid_forget()
        except:
            pass
        
        try:
            widget_edit.grid_forget()
        except:
            pass
        
        widget_regles = tk.Frame(fenetre)
        
        btn_base = tk.Button(widget_regles, text = "base")
        btn_base.grid(column = 0, row = 20)
    
        guide = "hello"
    
        label_guide = tk.Label(widget_regles, text = "")
        label_guide.config(text = guide)
        label_guide.grid(column = 0, row = 200)
        
        widget_regles.grid(column = 0, row = 3)
        
    def appuyer_edit(event):
        nonlocal combo_box_bodies, rentree_combo_body
        etat = 1
        envoyerValeurMultiprocessing(1, 0)
        print("Etat edition.")
        nonlocal widget_regles, widget_edit, widget_sim, Bodies
        hide_frames()
        
        try:
            widget_regles.grid_forget()
        except:
            pass
        
        try:
            widget_sim.grid_forget()
        except:
            pass
        
    
        widget_edit = tk.Frame(fenetre)
        
        btn_ajouter= tk.Button(widget_edit, text = '+', width = 10)
        btn_ajouter.grid(column = 0, row = 0)
        btn_ajouter.bind("<Button-1>", appuyer_ajouter)
        
        combo_box_bodies = ttk.Combobox(widget_edit, textvariable = rentree_combo_body, values = Bodies, state = "readonly")
        combo_box_bodies.bind('<<ComboboxSelected>>', selectionner_combo_box)
        combo_box_bodies['values'] = tuple([[Bodies[i].name, i] for i in range(len(Bodies))])
        combo_box_bodies.grid(column = 0, row = 2)
    
        label_pos = tk.Label(widget_edit, text = "Position")
        label_pos.grid(column = 0, row = 5)
        
        label_x = tk.Label(widget_edit, text = "x")
        label_x.grid(column = 1, row = 5)
        
        label_y = tk.Label(widget_edit, text = "y")
        label_y.grid(column = 5, row = 5)
    
        label_direction = tk.Label(widget_edit, text = "Direction")
        label_direction.grid(column = 0, row = 6)
    
        label_vitesse = tk.Label(widget_edit, text = "Vitesse")
        label_vitesse.grid(column = 0, row = 7)
        
        label_masse = tk.Label(widget_edit, text = "Masse")
        label_masse.grid(column = 0, row = 8)

        entree_pos_x = tk.Entry(widget_edit, width = 5)
        entree_pos_x.grid(column = 2, row = 5)
        
        entree_pos_y = tk.Entry(widget_edit, width = 5)
        entree_pos_y.grid(column = 6, row = 5)
    
        entree_momentum_x = tk.Entry(widget_edit, width = 10)
        entree_momentum_x.grid(column = 1, row = 6)
    
        entree_momentum_y = tk.Entry(widget_edit, width = 10)
        entree_momentum_y.grid(column = 1, row = 7)
        
        entree_masse = tk.Entry(widget_edit, width = 10, )
        entree_masse.grid(column = 1, row = 8)

        if i != None:
            combo_box_bodies.state = [Bodies[i].name, i]
            entree_masse.insert(0, Bodies[i].mass)
            entree_pos_x.insert(0, Bodies[i].position[0])
            entree_pos_y.insert(0, Bodies[i].position[1])
            entree_momentum_x.insert(0, Bodies[i].momentum[0])
            entree_momentum_y.insert(0, Bodies[i].momentum[1])

        
       
        btn_chargerPreset = tk.Button(widget_edit, text = "Charger preset") 
        btn_chargerPreset.grid(column = 0, row = 21)
        btn_chargerPreset.bind("<Button-1>", appuyer_chargerPreset)

        btn_sauvegarderPreset = tk.Button(widget_edit, text = "Sauvegarder preset") 
        btn_sauvegarderPreset.grid(column = 1, row = 21)
        btn_sauvegarderPreset.bind("<Button-1>", appuyer_sauvegarderPreset)
        
        btn_actualiser = tk.Button(widget_edit, text = "Actualiser", command= lambda: 
                                   appuyer_actualiser([entree_pos_x.get(), entree_pos_y.get()], [entree_momentum_x.get(), entree_momentum_y.get()], entree_masse.get())) 
        btn_actualiser.grid(column = 0, row = 30)
       
        widget_edit.grid(column = 0, row = 60, columnspan = 3)
        
    def appuyer_sim(event):
        nonlocal widget_regles, widget_edit, widget_sim, etat
        print("Etat simulation.")
        etat = 2
        envoyerValeurMultiprocessing(2, 0)
        hide_frames()
        try:
            widget_regles.grid_forget()
        except:
            pass
        
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
        nonlocal widget_regles, widget_edit, widget_sim

        # actualise les valeurs du multiprocessing
        multiprocessingIntake()
        frames = [widget_regles, widget_edit, widget_sim]
        for frame in frames:
            if frame is not None:
                frame.grid_forget()

    btn_regles.bind("<Button-1>", appuyer_regles)
    btn_edit.bind("<Button-1>", appuyer_edit)
    btn_sim.bind("<Button-1>", appuyer_sim)

    fenetre.mainloop()