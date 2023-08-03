import tkinter as tk

def Interface(variable1):
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

#Conséquence d'appuyer sur les buttons
    def appuyer_regles(event):
        
        widget_regles = tk.Frame(fenetre)
        
        btn_base = tk.Button(widget_regles, text = "base")
        btn_base.grid(column = 0, row = 20)
    
        guide = "hello"
    
        label_guide = tk.Label(widget_regles, text = "")
        label_guide.config(text = guide)
        label_guide.grid(column = 0, row = 200)
        
        widget_regles.grid(column = 0, row = 3)
        
    def appuyer_edit(event):
    
        widget_edit = tk.Frame(fenetre)
    
        btn_base = tk.Button(widget_edit, text = "base") 
        btn_base.grid(column = 0, row = 20)
    
        label_pos = tk.Label(widget_edit, text = "Position")
        label_pos.grid(column = 0, row = 0)
    
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
        
        widget_sim = tk.Frame(fenetre)
        
        btn_base = tk.Button(widget_sim, text = "base")
        btn_base.grid(column = 5, row = 5)
        
        widget_sim.grid(column = 0, row = 3)

    btn_regles.bind("<Button-1>", appuyer_regles)
    btn_edit.bind("<Button-1>", appuyer_edit)
    btn_sim.bind("<Button-1>", appuyer_sim)

    fenetre.mainloop()
