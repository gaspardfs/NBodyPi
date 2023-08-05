import tkinter as tk
import tkinter.filedialog as filed

def Interface(queue):
    fenetre = tk.Tk()
    fenetre.title("Home")
    

    fenetre.geometry("400x400")

    #Création des bouttons
    btn_regles = tk.Button(fenetre, text ="Règles")
    btn_regles.grid(column = 0, row = 0)

    btn_edit = tk.Button(fenetre, text = "Edit")
    btn_edit.grid(column = 1, row = 0)

    btn_sim = tk.Button(fenetre, text = "Sim")
    btn_sim.grid(column = 2, row = 0)

    # champ_vitesse = tk.Entry(fenetre, width = 50)
    # champ_vitesse.grid(column = , row =)

# Création des widgets globales

    widget_regles = None  
    widget_edit = None  
    widget_sim = None  

# Multiprocessing

    def multiprocessingIntake():
            # Chaque element de queue est ue liste de 0: la valeur a changer et 1: la nouvelle valeur
            while not queue.empty():
                valeur = queue.get()
                if valeur[0] == 0: etat = valeur[1]
                elif valeur[0] == 1: pass
                elif valeur[0] == 2: pass
        
    def envoyerValeurMultiprocessing(valeur, n):
        queue.put([n, valeur])

#Conséquence d'appuyer sur les buttons

    def appuyer_chargerPreset(event):
        directoire = filed.askopenfilename(defaultextension="/Presets")
        if directoire != None:
            envoyerValeurMultiprocessing(directoire, 1)

    
    def appuyer_sauvegarderPreset(event):
        directoire = filed.asksaveasfile(defaultextension="")
        if directoire != None:
            envoyerValeurMultiprocessing(directoire.name, 2)
        

    def appuyer_regles(event):
        etat = 1
        global widget_regles, widget_edit, widget_sim  
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
        etat = 1
        global widget_regles, widget_edit, widget_sim  
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
    
        btn_base = tk.Button(widget_edit, text = "base") 
        btn_base.grid(column = 0, row = 20)

        btn_chargerPreset = tk.Button(widget_edit, text = "Charger preset") 
        btn_chargerPreset.grid(column = 0, row = 21)
        btn_chargerPreset.bind("<Button-1>", appuyer_chargerPreset)

        btn_sauvegarderPreset = tk.Button(widget_edit, text = "Sauvegarder preset") 
        btn_sauvegarderPreset.grid(column = 1, row = 21)
        btn_sauvegarderPreset.bind("<Button-1>", appuyer_sauvegarderPreset)
        
    
        label_pos = tk.Label(widget_edit, text = "Position")
        label_pos.grid(column = 0, row = 2)
    
        label_direction = tk.Label(widget_edit, text = "Direction")
        label_direction.grid(column = 0, row = 1)
    
        label_vitesse = tk.Label(widget_edit, text = "Vitesse")
        label_vitesse.grid(column = 0, row = 2)
    
        entree_pos = tk.Entry(widget_edit, width = 50)
        entree_pos.grid(column = 1, row = 0)
    
        entree_direction = tk.Entry(widget_edit, width = 50)
        entree_direction.grid(column = 1, row = 1)
    
        entree_vitesse = tk.Entry(widget_edit, width = 50)
        entree_vitesse.grid(column = 1, row = 2)
        
    
        widget_edit.grid(column = 0, row = 60, columnspan = 3)
        
    def appuyer_sim(event):
        global widget_regles, widget_edit, widget_sim  
        hide_frames()
        
        try:
            widget_regles.grid_forget()
        except:
            pass
        
        try:
            widget_edit.grid_forget()
        except:
            pass
        
        widget_sim = tk.Frame(fenetre)
        
        btn_base = tk.Button(widget_sim, text = "base")
        btn_base.grid(column = 5, row = 5)
        
        widget_sim.grid(column = 0, row = 3)
    
        
    def hide_frames():
        nonlocal widget_regles, widget_edit, widget_sim
        frames = [widget_regles, widget_edit, widget_sim]
        for frame in frames:
            if frame is not None:
                frame.grid_forget()

    btn_regles.bind("<Button-1>", appuyer_regles)
    btn_edit.bind("<Button-1>", appuyer_edit)
    btn_sim.bind("<Button-1>", appuyer_sim)

    fenetre.mainloop()