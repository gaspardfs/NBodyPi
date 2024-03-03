import tkinter as tk
import tkinter.filedialog as filed
from tkinter import ttk
from tkinter.colorchooser import askcolor
import Classes
import copy
import sys

def Interface(queuePourInterface, queuePourJeu):
    fenetre = tk.Tk()
    fenetre.title("Home")
    

    fenetre.geometry("750x300")

    #Création des boutons
    btn_edit = tk.Button(fenetre, text = "Edition", width=46)
    btn_edit.grid(column = 1, row = 0)

    btn_sim = tk.Button(fenetre, text = "Simulation", width=46)
    btn_sim.grid(column = 2, row = 0)

    etat = 1
    pas = 0
    vitessePas = 0.2
    pause = True
    nbEtapes = 1000
    reference = None
    nNouvCorp = 1
    
    Corps = []
    combo_box_corps = None
    rentree_combo_corp = tk.StringVar(value="Selectionner un corps")
    champ_etapes = tk.StringVar()
    i = None
    trajectoires_visibles = False

    # Affichage
    affichePos = None
    afficheMom = None
    afficheMasse = None

# Création des widgets globales

    edition_widget = None  
    simulation_widget = None  


# Multiprocessing

    def preparePickling(Corps):
        nouvCorps = []
        for corp in Corps:
            nouvCorp = copy.copy(corp)
            nouvCorp.sprite = copy.copy(corp.sprite)
            nouvCorp.sprite.image = None
            nouvCorps += [nouvCorp]
        return nouvCorps
    
    def envoyerValeurMultiprocessing(valeur, n):
        queuePourJeu.put([n, valeur])
        
    def recevoirMultiprocessing():
        nonlocal etat, pas, vitessePas, Corps
        nouvellesCommandes = []
        # Chaque element de queue est que liste de 0: la valeur a changer et 1: la nouvelle valeur
        while not queuePourInterface.empty():
            valeur = queuePourInterface.get()
            if valeur[0] == 0: etat = valeur[1]
            elif valeur[0] == 1: pass
            elif valeur[0] == 2: pass
            elif valeur[0] == 3: 
                pas = valeur[1]
            elif valeur[0] == 4: vitessePas = valeur[1]
            elif valeur[0] == 7: 
                Corps = valeur[1]

        for commande in nouvellesCommandes:
            envoyerValeurMultiprocessing(commande[0], commande[1])
    
    def envoyerListeCorps():
        nonlocal Corps
        envoyerValeurMultiprocessing(preparePickling(Corps), 7)

# Conséquence d'appuyer sur les buttons

    def boutonAppuye(event):
        envoyerValeurMultiprocessing(5, True)

    def appuyer_chargerPreset(event):
        nonlocal i, rentree_combo_corp
        directoire = filed.askopenfilename(defaultextension="/Presets")
        if directoire != "":
            envoyerValeurMultiprocessing(directoire, 1)
            envoyerValeurMultiprocessing(0, 8)
            recevoirMultiprocessing()
            while queuePourInterface.empty():
                continue
            i = None
            rentree_combo_corp = tk.StringVar(value="Selectionner un corps")
            recevoirMultiprocessing()
            appuyer_edit(None)
            

    def appuyer_sauvegarderPreset(event):
        directoire = filed.asksaveasfile(defaultextension="/Presets")
        if directoire != "":
            envoyerValeurMultiprocessing(directoire.name, 2)

    def actualiserSimulation(vitessePasA):
        recevoirMultiprocessing()
        try:
            vitessePasA = float(vitessePasA)
        except:
            print("Valeur invalide!")
            return None
        envoyerValeurMultiprocessing(vitessePasA, 4)
        vitessePas = vitessePasA

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
        nonlocal i, Corps
        for j in range(len(Corps)):
            if Corps[j].nom == rentree_combo_corp.get():
                i = j
        appuyer_edit(None)
    
    def appuyer_actualiser(position, momentum, masse, nom, rouge, vert, bleu):
        nonlocal Corps
        recevoirMultiprocessing()
        try:
            Corps[i].position = [float(position[0]), float(position[1])]
            Corps[i].momentum =  [float(momentum[0]), float(momentum[1])]
            Corps[i].definirMasse(float(masse))
            Corps[i].couleur = (int(rouge), int(vert), int(bleu))
            if nom not in [Corps[i].nom for i in range(len(Corps))]:
                Corps[i].nom = nom
            else:
                print("Nom déjà")


            envoyerListeCorps()
        except:
            print("Valeur(s) invalide(s)!")

    def appuyer_ajouter(event):
        nonlocal nNouvCorp, i, rentree_combo_corp
        recevoirMultiprocessing()
        nouveau_corps = Classes.Corp()
        nouveau_corps.nom = f"Corp {nNouvCorp}"
        rentree_combo_corp = tk.StringVar(value=nouveau_corps.nom)
        Corps.append(nouveau_corps)
        i = len(Corps) - 1
        nNouvCorp += 1
        appuyer_edit(None)  

    def appuyer_enlever(event):
        recevoirMultiprocessing()
        nonlocal i
        try:
            Corps.pop(i)
            i = None
            appuyer_edit(None)
        except:
            print("Erreur de suprimement")

    def appuyer_reference(event):
        recevoirMultiprocessing()
        nonlocal i
        try:
            reference = Corps[i]
            envoyerValeurMultiprocessing(reference, 11)
        except:
            print("Erreur de référence", file=sys.stderr)

    def choisir_couleur():
        recevoirMultiprocessing()
        couleur = askcolor(title="Choisir une couleur")
        tab_couleur = list(couleur)
        couleur_hex = str(tab_couleur[1])
        val_rgb = list(couleur[0])
        if i != None:
            Corps[i].couleur = (val_rgb[0], val_rgb[1], val_rgb[2])
            appuyer_edit(None)
        label_couleur1.config(bg=couleur_hex)
        
    def appuyer_edit(event):
        nonlocal combo_box_corps, rentree_combo_corp, Corps
        etat = 1
        envoyerValeurMultiprocessing(1, 0)
        envoyerValeurMultiprocessing(0, 8)

        nonlocal edition_widget, simulation_widget
        cacher_frames()
        
        try:
            simulation_widget.grid_forget()
        except:
            pass
        
    
        edition_widget = tk.Frame(fenetre)
        
        btn_ajouter= tk.Button(edition_widget, text = '+', width = 10)
        btn_ajouter.grid(column = 2, row = 2)
        btn_ajouter.bind("<Button-1>", appuyer_ajouter)

        btn_enlever= tk.Button(edition_widget, text = '-', width = 10)
        btn_enlever.bind("<Button-1>", appuyer_enlever)
        btn_enlever.grid(column = 3, row = 2)

        btn_reference = tk.Button(edition_widget, text = "Utiliser référence", width = 10)
        btn_reference.grid(column = 4, row = 2)
        btn_reference.bind("<Button-1>", appuyer_reference)

        
        combo_box_Corps = ttk.Combobox(edition_widget, textvariable = rentree_combo_corp, values = Corps, state = "readonly")
        combo_box_Corps.bind('<<ComboboxSelected>>', selectionner_combo_box)
        combo_box_Corps['values'] = tuple([Corps[i].nom for i in range(len(Corps))])
        combo_box_Corps.grid(column = 1, row = 2)
    
        label_pos = tk.Label(edition_widget, text = "Position")
        label_pos.grid(column = 0, row = 5)
        
        label_x = tk.Label(edition_widget, text = "x")
        label_x.grid(column = 1, row = 5)
        
        label_y = tk.Label(edition_widget, text = "y")
        label_y.grid(column = 3, row = 5)
    
        label_momentum = tk.Label(edition_widget, text = "Momentum")
        label_momentum.grid(column = 0, row = 6)
        
        label_mom_x = tk.Label(edition_widget, text = "x")
        label_mom_x.grid(column = 1, row = 6)
        
        label_mom_y = tk.Label(edition_widget, text = "y")
        label_mom_y.grid(column = 3, row = 6)
        
        label_masse = tk.Label(edition_widget, text = "Masse")
        label_masse.grid(column = 0, row = 8)
        
        label_etapes = tk.Label(edition_widget, text = "Nb d'étapes")
        label_etapes.grid(column = 0, row = 14)

        label_nom = tk.Label(edition_widget, text = "Nom")
        label_nom.grid(column = 0, row = 9)

        label_couleur = tk.Label(edition_widget, text = "Couleur (r,v,b)")
        label_couleur.grid(column = 0, row = 10)

        label_config_trajectoires = tk.Label(edition_widget, text = "Configuration des trajectoires")
        label_config_trajectoires.grid(column = 2, row = 13)

        entree_pos_x = tk.Entry(edition_widget, width = 10)
        entree_pos_x.grid(column = 2, row = 5)
        
        entree_pos_y = tk.Entry(edition_widget, width = 10)
        entree_pos_y.grid(column = 4, row = 5)
    
        entree_momentum_x = tk.Entry(edition_widget, width = 10)
        entree_momentum_x.grid(column = 2, row = 6)
    
        entree_momentum_y = tk.Entry(edition_widget, width = 10)
        entree_momentum_y.grid(column = 4, row = 6)
        
        entree_masse = tk.Entry(edition_widget, width = 10, )
        entree_masse.grid(column = 1, row = 8)

        entree_nom = tk.Entry(edition_widget, width = 10, )
        entree_nom.grid(column = 1, row = 9)

        btn_slc_couleurs = tk.Button(edition_widget, text="Choisir une couleur", width=15, command=choisir_couleur)
        btn_slc_couleurs.grid(column = 4, row = 10)

        entree_r = tk.Entry(edition_widget, width = 10, )
        entree_r.grid(column = 1, row = 10)

        entree_v = tk.Entry(edition_widget, width = 10, )
        entree_v.grid(column = 2, row = 10)

        entree_b = tk.Entry(edition_widget, width = 10, )
        entree_b.grid(column = 3, row = 10)

        global label_couleur1
        label_couleur1 = tk.Label(edition_widget, bg=None, width=10)
        label_couleur1.grid(column = 2, row = 11)

        if i != None:
            combo_box_Corps.state = [Corps[i].nom, i]
            entree_masse.insert(0, Corps[i].masse)
            entree_pos_x.insert(0, Corps[i].position[0])
            entree_pos_y.insert(0, Corps[i].position[1])
            entree_momentum_x.insert(0, Corps[i].momentum[0])
            entree_momentum_y.insert(0, Corps[i].momentum[1])
            entree_nom.insert(0, Corps[i].nom)
            entree_r.insert(0, Corps[i].couleur[0])
            entree_v.insert(0, Corps[i].couleur[1])
            entree_b.insert(0, Corps[i].couleur[2])
            envoyerValeurMultiprocessing(12, Corps[i].id)
            

        
        champ_etapes = tk.Entry(edition_widget, width=10)
        champ_etapes.insert(0, str(nbEtapes)) 
        champ_etapes.grid(column=1, row=13)

        btn_act_trajectoires = tk.Button(edition_widget, text="Actualiser trajectoires", command= lambda: actualiser_trajectoires(champ_etapes.get()))
        btn_act_trajectoires.grid(column=2, row=14)

        btn_montrer_trajectoires = tk.Button(edition_widget, text="Montrer/Cacher trajectoires")
        btn_montrer_trajectoires.grid(column=3, row=14)
        btn_montrer_trajectoires.bind("<Button-1>", montrer_cacher_trajectoires)

       
        btn_chargerPreset = tk.Button(edition_widget, text = "Charger preset") 
        btn_chargerPreset.grid(column = 0, row = 0)
        btn_chargerPreset.bind("<Button-1>", appuyer_chargerPreset)

        btn_sauvegarderPreset = tk.Button(edition_widget, text = "Sauvegarder preset") 
        btn_sauvegarderPreset.grid(column = 1, row = 0)
        btn_sauvegarderPreset.bind("<Button-1>", appuyer_sauvegarderPreset)
        
        btn_actualiser = tk.Button(edition_widget, text = "Actualiser", background="green",command= lambda: 
                                   appuyer_actualiser([entree_pos_x.get(), entree_pos_y.get()], 
                                                      [entree_momentum_x.get(), entree_momentum_y.get()], entree_masse.get(), entree_nom.get(),
                                                      entree_r.get(), entree_v.get(), entree_b.get())) 
        btn_actualiser.grid(column = 2, row = 12)
       
        edition_widget.grid(column = 0, row = 60, columnspan = 3)
        
    def appuyer_sim(event):
        nonlocal edition_widget, simulation_widget, etat
        etat = 2
        envoyerValeurMultiprocessing(2, 0)
        cacher_frames()
        
        try:
            edition_widget.grid_forget()
        except:
            pass
        
        simulation_widget = tk.Frame(fenetre, width = 18 * 3)
        simulation_widget.grid(row=1, column=0, columnspan = 3)
        
        #btn_base = tk.Button(simulation_widget, text = "base")
        #btn_base.grid(column = 0, row = 0)
        labelVitessePas = tk.Label(simulation_widget, text="Vitesse des pas (s)")
        entreeVitessePas = tk.Entry(simulation_widget)
        entreeVitessePas.insert(0, str(vitessePas))
        labelVitessePas.grid(row = 1, column=0)
        entreeVitessePas.grid(row = 1, column=1)

        btnActualiserValeurs = tk.Button(simulation_widget, text="Actualiser simulation", background="green",
                                          command= lambda: actualiserSimulation(entreeVitessePas.get()))
        btnActualiserValeurs.grid(row=2, column=1)

        btnPause = tk.Button(simulation_widget, text="Pause/Play", command= lambda: pausePlay())
        btnPause.grid(row=3, column=0)
        btnNouvEtape = tk.Button(simulation_widget, text="+Etape", command= lambda: envoyerValeurMultiprocessing(True, 6))
        btnNouvEtape.grid(row=3, column=1)


        #btnActualiserValeurs.bind("<Button-1>", lambda event, vitessePasA=float(entreeVitessePas.get()), n=4: envoyerValeurMultiprocessingEvent(event, n, vitessePasA))

        
        
    def cacher_frames():
        nonlocal edition_widget, simulation_widget

        # actualise les valeurs du multiprocessing
        recevoirMultiprocessing()
        frames = [edition_widget, simulation_widget]
        for frame in frames:
            if frame is not None:
                frame.grid_forget()

    btn_edit.bind("<Button-1>", appuyer_edit)
    btn_sim.bind("<Button-1>", appuyer_sim)

    fenetre.mainloop()