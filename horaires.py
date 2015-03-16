#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import sqlite3
import re

#   Pour passer à python 3, il suffit de changer Tkinter en tkinter.
#   On donne l'alias tk pour qu'il n'y ait rien à modifier ailleurs dans le code.

# Ajouter le package : sudo apt-get install python-imaging-tk
import Tkinter as tk
from PIL import Image, ImageTk

try:
    import Tkinter
    import tkFont
except ImportError: # py3k
    import tkinter as Tkinter
    import tkinter.font as tkFont

import ttk

import autocompletion
import calendar_test

#  Il faudra rajouter des fonctions à sqlite. Elles seront importées ici. On suppose ici que le fichier s'appelle mes_fonctions.py 
# (il peut prendre n'importe quel nom)

#import mes_fonctions

class Horaires_tk(tk.Tk):

    def __init__(self, parent, emplacement, escale):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.emplacement = emplacement
        self.escale = escale
        self.initialize()

    def ferme_fichier(self, event):
        self.conn.close()

    def initialize(self):
        # Ouverture du fichier sqlite, il est supposé ici s'appeler vols.sqlite.
        # Noter que si le fichier n'existe pas il n'y aura pas d'erreur à l'ouverture, il sera automatiquement créé, mais il ne contiendra évidemment rien.
        self.conn = sqlite3.connect(os.path.join(self.emplacement, 'flights_test2.db'))

        #  Ajouter ici les fonctions nécessaires à sqlite
        #self.conn.create_function("nom_table dans SQLite", nbre_de_parametres, fonction_python)

        # ==========================================================
        # Interface graphique. On crée une "grille" qui permet de placer ses éléments façon bataille navale, en spécifiant ligne et colonne (numérotées à partir de 0).
        # On crée deux "Frames" (conteneurs d'autres éléments graphiques), une pour la saisie des données de recherche
        # (formulaire) et l'autre pour afficher la liste qui contiendra les éléments retrouvés de la base (résultat)
        # ==========================================================
        self.grid()

        # Le premier paramètre est le parent (l'élément conteneur) du nouvel élément graphique.
        # padx/pady spécifient la marge entre la bordure de l'élément graphique et les éléments qui sont dedans.
        # On crée l'élément, puis on le place en invoquant sa méthode grid().
        self.formulaire = tk.Frame(self, padx=10, pady=50)
        self.formulaire.grid(column=0, row=0)

        #root = Tkinter.Tk()
        self.inputDepart = autocompletion.launchDAuto(self.formulaire)
        self.inputDepart.focus_set()
        self.inputArrivee = autocompletion.launchAuto(self.formulaire)
        #self.inputtest.grid(row=0, column=0)
        #tk.Button(text='nothing').grid(row=1, column=0)

        self.formulaire_img = tk.Frame(self, padx=10, pady=50)
        self.formulaire_img.grid(column=1, row=0)

        #  On attache à l'évènement <Destroy> (fermeture de la fenêtre) la méthode ferme_fichier() qui, comme son nom l'indique, ferme proprement le fichier sqlite.
        #  La méthode est associée au formulaire plutôt qu'à la fenêtre principale parce que sinon toute fermeture de fenêtre fermerait le fichier, y compris pour une 
        #  fenêtre d'erreur que l'on voudrait voir apparaître. Quand le formulaire disparaît, c'est que le programme est vraiment terminé.
        self.formulaire.bind("<Destroy>", self.ferme_fichier)

        #back : self
        resultat = tk.Frame(padx=0, pady=0)
        resultat.grid(column=0, row=1)
        #resultat.pack(side=tk.LEFT)

        resultat2 = tk.Frame(padx=0, pady=0)
        resultat2.grid(column=1, row=1)

        # -----------------------------------------------------
        # "formulaire" contient sa propre grille. A l'intérieur, on place des étiquettes (Label), des zones de saisie (Entry), des boutons (Button). 
        # A chaque fois, le premier paramètre spécifie l'élément parent.
        # Input "De : "
        tk.Label(self.formulaire, text='Départ de').grid(column=2, row=2, pady=0)
        #self.depart = tk.Entry(self.formulaire)
        #self.depart.grid(column=5, row=3)

        # Input "A : "
        tk.Label(self.formulaire, text='A destination de').grid(column=3, row=2)
        #self.arrivee = tk.Entry(self.formulaire)
        #self.arrivee.grid(column=3, row=3)

        # Input "Correspondance : "
        # tk.Label(self.formulaire, text='Correspondance avec : ').grid(column=2, row=0)
        # self.correspondance = tk.Entry(self.formulaire)
        # self.correspondance.grid(column=2, row=1)

        # Input "Départ le : ". Par défaut les éléments sont centrés. Le paramètre optionnel "sticky" permet de modifier l'alignement, avec des références aux points cardinaux. 
        # N = vers le haut, S = vers le bas, W = à gauche, E = à droite.
        tk.Label(self.formulaire, text='Date de départ : ').grid(column=2, row=4, sticky=tk.E, pady=15)

        # Le paramètre optionel 'width' limite le nombre de caractères à entrer et 'font' spécifie la police de caractères.
        # Le reste est plus délicat:
        # Par défaut, on met le modèle de 'format de date' attendu (AAAAMMJJ, on peut choisir autre chose). 
        # Pour que l'utilisateur comprenne bien que c'est un modèle, on le met en gris (paramètre 'fg', pour 'ForeGround color'. 
        # L'ennui, c'est que l'on voudra revenir au noir quand l'utilisateur tape sa date. On ne peut pas changer la couleur avant que la fenêtre soit affichée. 
        # On triche en disant qu'il faut appeler une méthode à un instant précis, et c'est cette méthode qui fera le boulot; 
        # 'validate' précise quand la fonction sera appelée ('focusin' = quand on se positionne dans la zone) et 'validatecommand' quelle est cette fonction.
        self.date_depart = tk.Entry(self.formulaire, width=10, fg='darkgray', font=("Courier", "10"), validate='focusin', validatecommand=self.prepare_date)

        # Input date - Affichage du format idéal pour guider l'utilisateur :
        #self.date_depart.insert(0, 'JJ/MM/AAAA')
        #self.date_depart.grid(column=3, row=4, sticky=tk.W, pady=15)

        # Bouton recherche
        self.bouton_recherche = tk.Button(self.formulaire,
                                            text="Rechercher",
                                            command=self.recherche)
        self.bouton_recherche.grid(column=2, row=5, padx=10, pady=15)

        # Bouton de reset de formulaire
        self.bouton_RAZ = tk.Button(self.formulaire,
                                         text="Nouvelle Recherche",
                                         state=tk.DISABLED,
                                         command=self.remise_a_zero)
        self.bouton_RAZ.grid(column=3, row=5, padx=10, pady=15)

        self.escale = tk.IntVar()
        self.checkbox = tk.Checkbutton(self.formulaire, text="Avec une correspondance", variable=self.escale)
        self.checkbox.grid(column=4, row=3, padx=0, pady=0)

        self.escaleCarrier = tk.IntVar()
        self.checkbox = tk.Checkbutton(self.formulaire, text="Même compagnie", variable=self.escaleCarrier)
        self.checkbox.grid(column=5, row=3, padx=0, pady=0)

        # -----------------------------------------------------
        decalage = '10.10s'

        # Affichage du premier vol - On prépare l'emplacement des résultats, avec un en-tête et une liste que l'on pourra faire dérouler
        entete = tk.Label(resultat,
                            text=format(format('', '1.1s') + ' ' + format('N° Vol', decalage)
                                + ' ' + format('Départ', decalage)
                                + ' ' + format('Arrivée', decalage)
                                + ' ' + format('Durée', decalage)
                                + ' ' + format('Compagnie aérienne', decalage)),
                            anchor='w',
                            width=60,
                            font=('Courier', '12', 'bold'),
                            bg='MidnightBlue',
                            fg='White')
        entete.pack(side=tk.TOP)

        # Pour balayer les résultats
        ascenseur = tk.Scrollbar(resultat)
        ascenseur.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox Pour recevoir le résultat de la requête | Listbox : liste_de_vols
        self.donnees = tk.StringVar()
        self.liste_de_vols = tk.Listbox(resultat,
                                       yscrollcommand=ascenseur.set,
                                       bg='lightgray',
                                       height=15,
                                       width=60,
                                       font=("Courier", "12"),
                                       listvariable=self.donnees)
        #back : heigth = 15, width = 115

        #back : self.liste_de_vols.pack(side=tk.LEFT, fill=tk.BOTH)
        self.liste_de_vols.pack(side=tk.LEFT)
        ascenseur.config(command=self.liste_de_vols.yview)
    
        # fin premier Vol

        # Affichage des information du second vol
        entete2 = tk.Label(resultat2,
                            text=format(format('Correspondance', '18.18s') + ' ' + format('N° Vol', decalage)
                                + ' ' + format('Départ', decalage)
                                + ' ' + format('Arrivée', decalage)
                                + ' ' + format('Durée', decalage)
                                + ' ' + format('Compagnie aérienne', decalage)),
                            anchor='w',
                            width=80,
                            font=('Courier', '12', 'bold'),
                            bg='MidnightBlue',
                            fg='White')
        entete2.pack(side=tk.TOP)

        # Ascenseur Pour balayer les résultats
        ascenseur2 = tk.Scrollbar(resultat2)
        ascenseur2.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox Pour recevoir le résultat de la requête | Listbox : liste_de_vols
        self.donnees2 = tk.StringVar()
        self.liste_de_vols2 = tk.Listbox(resultat2,
                                       yscrollcommand=ascenseur2.set,
                                       bg='lightgray',
                                       height=15,
                                       width=80,
                                       font=("Courier", "12"),
                                       listvariable=self.donnees2)

        # Listbox conf.
        self.liste_de_vols2.pack(side=tk.RIGHT)
        ascenseur2.config(command=self.liste_de_vols2.yview)
    
        # fin cstr de la structure resultats pour le second vol

        # Lorsqu'un élément est ajouté au formulaire on doit ajouter "self." et la méthode .grid(...)
        # Lorsqu'un élément est ajouté au resultats on doit ajouter la méthode .pad(...)
        imageFile = "logo160.png"
        img = ImageTk.PhotoImage(Image.open(imageFile))
        self.panel_ = tk.Label(self.formulaire, image=img)
        self.panel_.grid(column=2, row=0, padx=0, pady=30)
        self.panel_.image = img

        imageFile = "aero.jpg"
        img = ImageTk.PhotoImage(Image.open(imageFile))
        self.panel_ = tk.Label(self.formulaire_img, image=img)
        self.panel_.grid(column=2, row=0, padx=0, pady=30)
        self.panel_.image = img

        # Bouton d'appel au calendrier
        self.buttonCalendar = tk.Button(self.formulaire,
                                    text="Choisir une date",
                                    command=self.functionCalendar)
        self.buttonCalendar.grid(column=3, row=4, padx=10, pady=15)

        # Diverses opérations définissant si l'on peut redimensionner la fenêtre, etc.
        self.resizable(True, False)
        self.update()
        self.geometry(self.geometry())

        # Focus Inputs départ du vol :
        #self.depart.focus_set()
        #self.depart.selection_range(0, tk.END)
        #self.date_depart.config(fg='black')

    def functionCalendar(test):
        print "truc"
        calendar_test.lancement()

    def getDate(self):
        premierJourAnnee = "mercredi"
        tabNomJour = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
        tabJoursByMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        anneeInitiale = 2014

        f = open('search', 'r')
        day = int(f.readline())
        month = int(f.readline())
        year = int(f.readline())

        # Test
        """print "calendar_test.getYear() : " + calendar_test.calendar.getYear()
        year = int(calendar_test.getYear())
        month = int(calendar_test.getMonth())
        day = int(calendar_test.getDay())"""

        """date_depart_choisie = self.date_depart.get().strip().title()
        date_depart_choisie = str(date_depart_choisie)
        year = int(date_depart_choisie[4:])
        day_and_month = date_depart_choisie[:4]
        month = int(day_and_month[2:])
        day = int(day_and_month[:2])"""

        decalageTotalDay = 0
        if year > anneeInitiale:
            decalageTotalDay = (year - anneeInitiale) * 365 + decalageTotalDay
        if month > 2:
            compteur = month - 1
            for i in range(0, compteur):
                #print "nbjours:" + str(tabJoursByMonth[i]) + "\n"
                #print "compteur:" + str(i) + "\n"
                decalageTotalDay = tabJoursByMonth[i] + decalageTotalDay
        if day > 2:
            decalageTotalDay = (day - 1) + decalageTotalDay

        jourADecaler = decalageTotalDay % 7
        jourRecherche = 0
        print "decalageTotalDay : " + str(decalageTotalDay)
        print "jourADecaler : " + str(jourADecaler)
        for i in range(0, 6):
            if premierJourAnnee == tabNomJour[i]:
                jourRecherche = i + jourADecaler
                # 6 équivaut à la longueur max du tableau des jours
                if jourRecherche > 6:
                    # 7 équivaut au nombre de jour
                    jourRecherche = jourRecherche - 7

        # tabNomJour[jourRecherche] # nom du jour
        return (jourRecherche + 1)

    def prepare_date(self):
        # Fonction appelée quand on se positionne sur la zone où l'on saisit la date de départ. 
        # D'abord on efface le contenu (qui peut n'être que le format de date attendu), puis on passe en noir (la zone est créée en gris)
        #self.depart.delete(0, tk.END)
        self.date_depart.delete(0, tk.END)
        self.date_depart.config(fg='black')

    def recherche(self):
        # On commencera par récupérer le contenu des champs de saisie, vérifier au passage qu'ils sont bien dans le format attendu (date) ou 
        # éventuellement les transformer pour qu'ils soient comparables (majuscules/minuscules, etc) à ce qui est dans les tables 
        # (ce genre de transformation se fait au choix dans le langage de programmation ou en SQL)
        #airport_depart = self.depart.get().strip().title()
        airport_depart = self.inputDepart.get().strip().title()        
        #airport_arrivee = self.arrivee.get().strip().title()
        airport_arrivee = self.inputArrivee.get().strip().title()
        #correspondance = self.correspondance.get().strip().title()
        date_depart_choisie = self.date_depart.get().strip().title()

        numeroJour = self.getDate()

        debutCompteurSQL = str(numeroJour)
        finCompteurSQL = str(numeroJour + 1)
        numeroJour = str(numeroJour)

        lendemain = int(numeroJour) + 1
        lendemain = str(lendemain)

        # test initial
        #query = """SELECT flightnum, dep_time, duration, airline_code FROM flight, airline_has_flight WHERE id_flight = 2 AND id_flight = airline_id_flight"""

        # Requête sans correspondances :
        query_wo_escale = """
                    SELECT distinct id_flight, flightnum, dep_time, duration, airline, arrival 
                    FROM flight WHERE 1 = 1 
                    AND departure IN (SELECT airport FROM allairports WHERE city_fr = ?  GROUP BY airport)
                    AND arrival IN (SELECT airport FROM allairports WHERE city_fr = ? GROUP BY airport) 
                    AND day_op LIKE '%""" + numeroJour + """%'
                """

        #  #first_flight.id_flight AS numero_vol_flight1, 
        #second_flight.id_flight AS numero_vol_flight2,
        #first_flight.day_op,
        #first_flight.city_departure, 
        #first_flight.departure, 
        #first_flight.first_city_arrival,
        #second_flight.dep_time, 
        #second_flight.day_op, 
        #city_fr AS city_arrival, 
        #second_flight.arrival, 
        #(CAST(SUBSTR(second_flight.dep_time, 1, 2) AS integer) - CAST(SUBSTR(first_flight.dep_time, 1, 2) AS integer)) AS delay


        # Requête avec correspondances :
        # [1erpoint]    Les points d'interrogation signifie l'insertion de la premiere ville ( Paris ), le second '?' représente la seconde ville de destination 
        # ( Londres ) pour que cela fonctionne il faut aussi insérer dans la liste 'parameters' les valeurs enregistrées par l'utilisateur, cela est en quelque
        # sorte une requête dynamique.
        #
        # [2epoint]     Les variables Python dans la requête (numeroJour,..) sont des valeurs de jour calculées ( dans la fonction getDate() ) en fonction des entrées données 
        # par l'utilisateur.

        # Escale et de compagnies différentes
        query_w_escale_diff_carrier = """
                SELECT
                        DISTINCT first_flight.id_flight,
                        first_flight.flightnum,                            
                        first_flight.dep_time,
                        first_flight.duration,
                        first_flight.airline,                            
                        first_flight.arrival,

                        second_flight.id_flight,
                        second_flight.flightnum,                            
                        second_flight.dep_time,
                        second_flight.duration,
                        second_flight.airline,                            
                        second_flight.arrival,

                        first_flight.first_city_departure,
                        first_flight.first_city_arrival,
                        city_fr,
                        first_flight.carrier,
                        second_flight.carrier
                FROM

                    (SELECT id_flight, flightnum, dep_time, duration, airline, day_op, departure, arrival, carrier, first_city_departure, city_fr AS first_city_arrival
                       FROM 
                          (SELECT id_flight, flightnum, dep_time, duration, airline, day_op, departure, carrier, arrival, city_fr AS first_city_departure
                          FROM flight, allairports
                          WHERE 1 = 1 
                          AND departure IN
                             (SELECT airport
                              FROM allairports
                              WHERE city_fr = ?
                              GROUP BY airport)
                          AND CAST(day_op AS text) LIKE '%""" + numeroJour + """%'
                          AND airport = departure) 
                       AS temp, allairports
                       WHERE airport = arrival
                       GROUP BY id_flight)

                AS first_flight, flight AS second_flight, allairports
                WHERE 1 = 1
                AND first_flight.arrival = second_flight.departure
                AND second_flight.arrival = allairports.airport
                AND first_flight.first_city_departure != allairports.city_fr
                AND first_flight.carrier != second_flight.carrier
                AND allairports.city_fr = ?
                AND 
                (
                    CAST(second_flight.day_op AS text) LIKE '%""" + numeroJour + """%'
                    OR
                    CAST(second_flight.day_op AS text) LIKE '%""" + lendemain + """%'
                )
                  
                AND CAST(SUBSTR(first_flight.dep_time, 1, 2) AS integer) < CAST(SUBSTR(second_flight.dep_time, 1, 2) AS integer)

                AND CAST(SUBSTR(first_flight.dep_time, 1, 2) AS integer)*60 + first_flight.duration + CAST(SUBSTR(first_flight.dep_time, 2, 4) AS integer)
                < CAST(SUBSTR(second_flight.dep_time, 1, 2) AS integer)*60 + CAST(SUBSTR(second_flight.dep_time, 1, 2) AS integer)

                GROUP BY second_flight.id_flight, first_flight.id_flight
                HAVING 1 = 1                    
                AND 
                (
                    (
                        (CAST(SUBSTR(second_flight.dep_time, 1, 2) AS integer) - CAST(SUBSTR(first_flight.dep_time, 1, 2) AS integer) ) <= 5
                            AND CAST(second_flight.day_op AS text) LIKE '%""" + numeroJour + """%'
                    )
                    OR
                    (
                        (24 - CAST(SUBSTR(second_flight.dep_time, 1, 2) AS integer) + CAST(SUBSTR(first_flight.dep_time, 1, 2) AS integer) ) <= 5
                        AND CAST(second_flight.day_op AS text) LIKE '%""" + lendemain + """%'
                    )
                )
        """

        # Escale et même compagnie
        query_same_carrier = """
            SELECT
                        DISTINCT first_flight.id_flight,
                        first_flight.flightnum,                            
                        first_flight.dep_time,
                        first_flight.duration,
                        first_flight.airline,                            
                        first_flight.arrival,

                        second_flight.id_flight,
                        second_flight.flightnum,                            
                        second_flight.dep_time,
                        second_flight.duration,
                        second_flight.airline,                            
                        second_flight.arrival,

                        first_flight.first_city_departure,
                        first_flight.first_city_arrival,
                        city_fr,
                        first_flight.carrier,
                        second_flight.carrier
                FROM

                    (SELECT id_flight, flightnum, dep_time, duration, airline, day_op, departure, arrival, first_city_departure, carrier, city_fr AS first_city_arrival
                       FROM 
                          (SELECT id_flight, flightnum, dep_time, duration, airline, day_op, departure, arrival, carrier, city_fr AS first_city_departure
                          FROM flight, allairports
                          WHERE 1 = 1 
                          AND departure IN
                             (SELECT airport
                              FROM allairports
                              WHERE city_fr = ?
                              GROUP BY airport)      
                          AND CAST(day_op AS text) LIKE '%""" + numeroJour + """%'
                          AND airport = departure) 
                       AS temp, allairports
                       WHERE airport = arrival
                       GROUP BY id_flight)
                AS first_flight, flight AS second_flight, allairports
                WHERE 1 = 1
                AND first_flight.arrival = second_flight.departure
                AND second_flight.arrival = allairports.airport
                AND first_flight.carrier = second_flight.carrier
                AND first_flight.airline = second_flight.airline
                AND first_flight.first_city_departure != allairports.city_fr
                AND allairports.city_fr = ?
                AND 
                (
                    CAST(second_flight.day_op AS text) LIKE '%""" + numeroJour + """%'
                    OR
                    CAST(second_flight.day_op AS text) LIKE '%""" + lendemain + """%'
                )
                  
                AND CAST(SUBSTR(first_flight.dep_time, 1, 2) AS integer) < CAST(SUBSTR(second_flight.dep_time, 1, 2) AS integer)

                AND CAST(SUBSTR(first_flight.dep_time, 1, 2) AS integer)*60 + first_flight.duration + CAST(SUBSTR(first_flight.dep_time, 2, 4) AS integer)
                < CAST(SUBSTR(second_flight.dep_time, 1, 2) AS integer)*60 + CAST(SUBSTR(second_flight.dep_time, 1, 2) AS integer)

                GROUP BY second_flight.id_flight, first_flight.id_flight
                HAVING 1 = 1                    
                AND 
                (
                    (
                        (CAST(SUBSTR(second_flight.dep_time, 1, 2) AS integer) - CAST(SUBSTR(first_flight.dep_time, 1, 2) AS integer) ) <= 5
                            AND CAST(second_flight.day_op AS text) LIKE '%""" + numeroJour + """%'
                    )
                    OR
                    (
                        (24 - CAST(SUBSTR(second_flight.dep_time, 1, 2) AS integer) + CAST(SUBSTR(first_flight.dep_time, 1, 2) AS integer) ) <= 5
                        AND CAST(second_flight.day_op AS text) LIKE '%""" + lendemain + """%'
                    )
                )
        """

        # Escale par défaut
        query_w_escale = """
            SELECT
                        DISTINCT first_flight.id_flight,
                        first_flight.flightnum,                            
                        first_flight.dep_time,
                        first_flight.duration,
                        first_flight.airline,                            
                        first_flight.arrival,

                        second_flight.id_flight,
                        second_flight.flightnum,                            
                        second_flight.dep_time,
                        second_flight.duration,
                        second_flight.airline,                            
                        second_flight.arrival,

                        first_flight.first_city_departure,
                        first_flight.first_city_arrival,
                        city_fr
                FROM

                    (SELECT id_flight, flightnum, dep_time, duration, airline, day_op, departure, arrival, first_city_departure, carrier, city_fr AS first_city_arrival
                       FROM 
                          (SELECT id_flight, flightnum, dep_time, duration, airline, day_op, departure, arrival, carrier, city_fr AS first_city_departure
                          FROM flight, allairports
                          WHERE 1 = 1 
                          AND departure IN
                             (SELECT airport
                              FROM allairports
                              WHERE city_fr = ?
                              GROUP BY airport)      
                          AND CAST(day_op AS text) LIKE '%""" + numeroJour + """%'
                          AND airport = departure) 
                       AS temp, allairports
                       WHERE airport = arrival
                       GROUP BY id_flight)
                AS first_flight, flight AS second_flight, allairports
                WHERE 1 = 1
                AND first_flight.arrival = second_flight.departure
                AND second_flight.arrival = allairports.airport
                AND first_flight.first_city_departure != allairports.city_fr
                AND allairports.city_fr = ?
                AND 
                (
                    CAST(second_flight.day_op AS text) LIKE '%""" + numeroJour + """%'
                    OR
                    CAST(second_flight.day_op AS text) LIKE '%""" + lendemain + """%'
                )

                AND CAST(SUBSTR(first_flight.dep_time, 1, 2) AS integer) < CAST(SUBSTR(second_flight.dep_time, 1, 2) AS integer)

                AND CAST(SUBSTR(first_flight.dep_time, 1, 2) AS integer)*60 + first_flight.duration + CAST(SUBSTR(first_flight.dep_time, 2, 4) AS integer)
                < CAST(SUBSTR(second_flight.dep_time, 1, 2) AS integer)*60 + CAST(SUBSTR(second_flight.dep_time, 1, 2) AS integer)

                GROUP BY second_flight.id_flight, first_flight.id_flight
                HAVING 1 = 1                    
                AND 
                (
                    (
                        (CAST(SUBSTR(second_flight.dep_time, 1, 2) AS integer) - CAST(SUBSTR(first_flight.dep_time, 1, 2) AS integer) ) <= 5
                            AND CAST(second_flight.day_op AS text) LIKE '%""" + numeroJour + """%'
                    )
                    OR
                    (
                        (24 - CAST(SUBSTR(second_flight.dep_time, 1, 2) AS integer) + CAST(SUBSTR(first_flight.dep_time, 1, 2) AS integer) ) <= 5
                        AND CAST(second_flight.day_op AS text) LIKE '%""" + lendemain + """%'
                    )
                )
        """

        # Initialisation :
        parameters = []

        # Ajout des mots-clé
        parameters.append(airport_depart)
        parameters.append(airport_arrivee)

        # Exécution de la requête :
        try:
           cursor = self.conn.cursor()
           cursor.arraysize = 20
           print("Chargement..")
           req = open('whatsql', 'w')
           req.write(str(query_wo_escale))
           if self.escale.get() == 0: 
              cursor.execute(query_wo_escale, parameters)
           elif self.escale.get() == 1 and self.escaleCarrier.get() == 1:
              print "enter meme comp"
              cursor.execute(query_same_carrier, parameters)
           elif self.escale.get() == 1 and self.escaleCarrier.get() == 0:
              print "enter diff compagnie"
              cursor.execute(query_w_escale_diff_carrier, parameters)
           
           """if self.escaleCarrier.get() == 1: 
              cursor.execute(query_same_carrier)
           elif self.escaleCarrier.get() == 0:
              cursor.execute(query_w_escale_diff_carrier)"""

           found = 0
           print("Affichage")
           result = cursor.fetchmany()

           # Récupération des résultats :
           while len(result) > 0:
              for row in result:
                idFlight = str(row[0])
                #Champs numéro de vol
                numeroVol = str(row[1])
                # Champs heur de départ
                timeDeparting = str(row[2])

                # Calcul de la durée en heures et minutes et Calcul de l'heure d'arrivée
                jour = 0
                hourInit = int(timeDeparting[:2])
                minuteInit = int(timeDeparting[3:])
                minuteArriving = 0
                hourArriving = 0
                durationHour = 0
                durationMinute = 0

                #Duration
                if row[3] < 60:
                    # duration < 1 heure
                    hourArriving = hourInit
                    minuteArriving = minuteInit + row[3]
                    durationMinute = row[3]
                    # Si dépassement des minutes
                    if minuteArriving >= 60:
                        hourArriving = hourArriving + 1
                        minuteArriving = minuteArriving - 60
                else:
                    # duration > 1 heure
                    durationMinute = int(row[3]%60)
                    durationHour = int(row[3]/60)
                    minuteArriving = durationMinute + minuteInit
                    hourArriving = durationHour + hourInit
                    # Si Temps d'arrivée > 24h
                    if minuteArriving >= 60:
                        hourArriving = hourArriving + 1
                        minuteArriving = minuteArriving - 60
                    if hourArriving >= 24:
                        hourArriving = hourArriving - 24
                        jour = 1

                # Champs heure d'arrivée - Conversions en string
                if hourArriving < 10:
                    hourArriving = "0" + str(hourArriving)
                if minuteArriving < 10:
                    minuteArriving = "0" + str(minuteArriving)
                hourArriving = str(hourArriving)
                minuteArriving = str(minuteArriving)
                timeArriving = str(hourArriving+":"+minuteArriving)

                # Champs durée
                if durationHour < 10:
                    durationHour = "0" + str(durationHour)
                if durationMinute < 10:
                    durationMinute = "0" + str(durationMinute)
                duration = str(durationHour) + ":" + str(durationMinute)

                #Airline
                airline = str(row[4])

                idFlight2 = ""
                numeroVol2 = ""
                timeDeparting2 = ""
                timeArriving2 = ""
                duration2 = ""
                airline2 = ""
                villeEscale = ""

                if self.escale.get() == 1:
                    idFlight2 = str(row[6])
                    #Champs numéro de vol
                    numeroVol2 = str(row[7])
                    # Champs heur de départ
                    timeDeparting2 = str(row[8])

                    # Calcul de la durée en heures et minutes et Calcul de l'heure d'arrivée
                    jour2 = 0
                    hourInit2 = int(timeDeparting2[:2])
                    minuteInit2 = int(timeDeparting2[3:])
                    minuteArriving2 = 0
                    hourArriving2 = 0
                    durationHour2 = 0
                    durationMinute2 = 0

                    #Duration
                    if row[9] < 60:
                        # duration < 1 heure
                        hourArriving2 = hourInit2
                        durationMinute2 = row[9]
                        minuteArriving2 = minuteInit2 + row[9]
                        # Si dépassement des minutes
                        if minuteArriving2 >= 60:
                            hourArriving2 = hourArriving2 + 1
                            minuteArriving2 = minuteArriving2 - 60
                    else:
                        # duration > 1 heure
                        durationMinute2 = int(row[9]%60)
                        durationHour2 = int(row[9]/60)
                        minuteArriving2 = durationMinute2 + minuteInit2
                        hourArriving2 = durationHour2 + hourInit2
                        # Si Temps d'arrivée > 24h
                        if minuteArriving2 >= 60:
                            hourArriving2 = hourArriving2 + 1
                            minuteArriving2 = minuteArriving2 - 60
                        if hourArriving2 >= 24:
                            hourArriving2 = hourArriving2 - 24
                            jour2 = 1

                    # Champs heure d'arrivée - Conversions en string
                    if hourArriving2 < 10:
                        hourArriving2 = "0" + str(hourArriving2)
                    if minuteArriving2 < 10:
                        minuteArriving2 = "0" + str(minuteArriving2)
                    hourArriving2 = str(hourArriving2)
                    minuteArriving2 = str(minuteArriving2)
                    timeArriving2 = str(hourArriving2 + ":" + minuteArriving2)

                    # Champs durée
                    if durationHour2 < 10:
                        durationHour2 = "0" + str(durationHour2)
                    if durationMinute2 < 10:
                        durationMinute2 = "0" + str(durationMinute2)
                    duration2 = str(durationHour2) + ":" + str(durationMinute2)

                    #Airline
                    airline2 = str(row[10])

                    villeEscale = str(row[13])

                decalage = '10.10s'

                self.liste_de_vols.insert(tk.END, format('', '2.2s') +
                              ' ' + format(numeroVol, decalage) 
                            + ' ' + format(timeDeparting, decalage)
                            + ' ' + format(timeArriving, decalage)
                            + ' ' + format(duration, '14.14s')
                            + ' ' + format(airline, decalage))

                self.liste_de_vols2.insert(tk.END, format('', '1.1s') +
                              ' ' + format(villeEscale, '18.18s')
                            + ' ' + format(numeroVol2, decalage)
                            + ' ' + format(timeDeparting2, decalage)
                            + ' ' + format(timeArriving2, decalage)
                            + ' ' + format(duration2, '13.13s')
                            + ' ' + format(airline2, decalage))

                found = 1
                result = cursor.fetchmany()
           if found == 0:
              self.liste_de_vols.insert(tk.END, '*** Aucun vol trouvé ! ***\n***Aucun vol n\'est disponible pour cette recherche***')
              self.liste_de_vols2.insert(tk.END, '*** Aucun vol trouvé ! ***\n***Aucun vol n\'est disponible pour cette recherche***')
        except:
            print("Unexpected error:" + str(sys.exc_info()))

        #self.liste_de_vols.insert(tk.END, "test")

        # Après avoir affiché, on récupère tous les sous-éléments du formulaire pour les désactiver. On réactive ensuite le bouton "Nouvelle Recherche"
        for element in self.formulaire.children.values():
            element.config(state = tk.DISABLED)
        self.bouton_RAZ.config(state = tk.NORMAL)

    def remise_a_zero(self):
        # Préparation pour une nouvelle recherche..
        # On efface d'abord le résultat précédent.
        self.liste_de_vols.delete(0, tk.END)
        self.liste_de_vols2.delete(0, tk.END)
        # On ré-active tous les éléments du formulaire
        for element in self.formulaire.children.values():
            element.config(state = tk.NORMAL)

        # On efface le contenu des champs, et on remet le format en gris pour la date.
        self.inputDepart.delete(0, tk.END)
        self.inputArrivee.delete(0, tk.END)
        self.date_depart.delete(0, tk.END)
        self.date_depart.config(fg='darkgray')
        self.date_depart.insert(0, 'AAAAMMJJ')
        # Désactive la checkbox
        self.checkbox.deselect()

        # Il faut réactiver ce qui efface le modèle et passé en noir, cela ne fonctionne qu'une fois sinon.
        self.date_depart.config(validate='focusin')
        self.date_depart.config(validatecommand=self.prepare_date)
        # On désactive le bouton "Nouvelle Recherche"
        self.bouton_RAZ.config(state = tk.DISABLED)
        # On positionne dans le champ correspondant à l'aéroport de départ.
        self.inputDepart.focus_set()

if __name__ == "__main__":
    # On suppose que le fichier sqlite est dans le même répertoire que ce programme.
    emplacement = os.path.dirname(sys.argv[0])    
    app = Horaires_tk(None, emplacement, 1)
    # Titre de l'app
    app.title('AirDALM')

    # A ne pas supprimer
    app.mainloop()
