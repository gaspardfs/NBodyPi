import tkinter as tk

def Interface(variable1):
    fenetre = tk.Tk()
    fenetre.title("Home")

    fenetre.geometry("400x400")

    btn_regles = tk.Button(fenetre, text ="Règles")
    btn_regles.place(x = 10, y = 0)

    btn_edit = tk.Button(fenetre, text = "Edit")
    btn_edit.place(x = 60, y = 0)

    btn_sim = tk.Button(fenetre, text = "Sim")
    btn_sim.place(x = 100, y = 0)

    champ_vitesse = tk.Entry(fenetre, width = 50)
    champ_vitesse.place()

    def appuyer_regles(event):
        guide = ""
        
        label_guide = tk.Label(fenetre, text = "")
        label_guide.config(text = guide)
        label_guide.place(x = 200, y = 200)

    def appuyer_edit(event):
        
        widget_edit = tk.Frame(fenetre)
        
        label_pos = tk.Label(widget_edit, text = "Position")
        label_pos.place(x = 0, y = 200)
        
        label_direction = tk.Label(widget_edit, text = "Direction")
        label_direction.place(x = 0, y = 250)
        
        label_vitesse = tk.Label(widget_edit, text = "Vitesse")
        label_vitesse.place(x = 0, y = 300)
        
        entree_pos = tk.Entry(widget_edit, width = 50)
        entree_pos.place(x = 55, y = 200)
        
        entree_direction = tk.Entry(widget_edit, width = 50)
        entree_direction.place(x = 55, y = 250)
        
        entree_vitesse = tk.Entry(widget_edit, width = 50)
        entree_vitesse.place(x = 55, y = 300)

        
        widget_edit.grid(column = 0, row = 3)
        
        
    def appuyer_sim(event):
        
        btn_base = tk.Button(fenetre, text = "base")
        btn_base.grid(column = 5, row = 5)
        
        guide = ""
        
        label_guide = tk.Label(fenetre, text = "")
        label_guide.config(text = guide)
        label_guide.place(x = 200, y = 200)

    btn_regles.bind("<Button-1>", appuyer_regles)
    btn_edit.bind("<Button-1>", appuyer_edit)
    btn_sim.bind("<Button-1>", appuyer_sim)

    fenetre.mainloop()
