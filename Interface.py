import tkinter as tk
from tkinter import filedialog
import os


def Interface(variable1):

    fenetre = tk.Tk()
    fenetre.title("Home")

    fenetre.geometry("800x600")

    btn_regles = tk.Button(fenetre, text ="Règles")
    btn_regles.place(x = 350, y = 300)

    btn_edit = tk.Button(fenetre, text = "Edit")
    btn_edit.place(x = 440, y = 300)

    btn_sim = tk.Button(fenetre, text = "Sim")
    btn_sim.place(x = 400, y = 300)

    champ_vitesse = tk.Entry(fenetre, width = 50)
    champ_vitesse.place()

    def appuyer_regles(event):
        btn_regles.place(x = 10, y = 0)
        btn_edit.place(x = 60, y = 0)
        btn_sim.place(x = 100, y = 0)
        
        guide = ""
        
        label_guide = tk.Label(fenetre, text = "")
        label_guide.config(text = guide)
        label_guide.place(x = 200, y = 200)

    def appuyer_edit(event):
        def appuyer_presets(event):
            """Opens NBodyPi\Presets"""
            filename = filedialog.askopenfilename(initialdir="Presets")
            with open(filename) as charged_preset:
                lines = charged_preset.readlines()
            print(lines)

        def sauver(event):
            position = entree_position.get()
            direction = entree_direction.get()
            vitesse = entree_vitesse.get()


        btn_regles.place(x = 10, y = 0)
        btn_edit.place(x = 60, y = 0)
        btn_sim.place(x = 100, y = 0)

        btn_presets = tk.Button(fenetre, text = "Charger un preset")
        btn_presets.place(x = 200, y = 150)

        label_pos = tk.Label(fenetre, text = "Position")
        label_pos.place(x = 200, y = 200)
        
        label_direction = tk.Label(fenetre, text = "Direction")
        label_direction.place(x = 200, y = 250)
        
        label_vitesse = tk.Label(fenetre, text = "Vitesse")
        label_vitesse.place(x = 200, y = 300)
        
        entree_pos = tk.Entry(fenetre, width = 50)
        entree_pos.place(x = 255, y = 200)
        
        entree_direction = tk.Entry(fenetre, width = 50)
        entree_direction.place(x = 255, y = 250)
        
        entree_vitesse = tk.Entry(fenetre, width = 50)
        entree_vitesse.place(x = 255, y = 300)

        btn_save = tk.Button(fenetre, text = "Sauver")
        btn_save.place(x = 255, y = 350)

        btn_save.bind("<Button-1>", sauver)
        btn_presets.bind("<Button-1>", appuyer_presets)
        

    # def appuyer_sim():

    btn_regles.bind("<Button-1>", appuyer_regles)
    btn_edit.bind("<Button-1>", appuyer_edit)
    # btn_sim.bind("<Button-1>", appuyer_sim)

    fenetre.mainloop()