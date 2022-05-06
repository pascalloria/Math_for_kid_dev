import random
import sqlite3
from timeit import default_timer as timer  # ( on renome timeit.default_timer par timer)
from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, Clock
from kivy.uix.relativelayout import RelativeLayout

Builder.load_file("menu.kv")
Builder.load_file("reponse.kv")
Builder.load_file("nom_score.kv")

""" Version Avec Score Base de donné"""


# difficulté devient un parametre de trie dans la base

# Programme de caclul
# mesure le temps de l'utilisateur : OK
# Donne une note : OK
# empeche la saisie de lettre pour reponse au calcul : OK
# Demande le nom et voir enregistre le scord : dabord dans un fichier txt OK ! puis dans une base de donnée ok !
# 3 niveau de difficulté : OK
# interface Graphique : OK

# Améliorer l'affichage du tableau des scores : OK
# Aligner le tout (BoxLayout Horizontal  ??): OK

# Son : OK
# bouton restart : OK


# voir pour limiter le temps par question / session):

class MainWidget(RelativeLayout):
    nb_question = NumericProperty(1)  # Numero actuel de la question
    NOMBRE_QUESTION = NumericProperty(1)  # Nombre max de question
    question = StringProperty("")  # calcul à éfféctuer
    text_imput_state_validate = BooleanProperty(False)  # Un valeur a été validé dans la zone de texte

    OPR = 0  # Variable pour le choix de l'opérateur + ou *
    NOMBRE_MAX = 10  # Plus grand nombre possible dans le calcul
    NOMBRE_MIN = 1  # Plus petit nombre possible dans le calcul
    DIFF = None  # Variable qui stock la difficulté choisit

    nb_points = 0  # compteur de point
    temps = None  # variable de temps
    nom = None  # variable pour le nom de l'utilisateur
    o = None  # operateur
    a = None  # nombre 1 du calcul
    b = None  # nombre 2 du calcul

    reponse_str = "None"  # variable qui stock la réponse
    reponse_int = None  # int de la réponse

    start = None  # début du timer
    end = None  # fin du timer

    valider_reponse = StringProperty("Reponse")
    score_afficher = StringProperty("Votre score")
    'State of game ( run or menu)'
    game_state = False

    tables = []
    tables_names = []
    tables_difficulte = []
    tables_score = []
    tables_temps = []
    tables_join = StringProperty('')
    tables_names_join = StringProperty('')
    tables_difficulte_join = StringProperty('')
    tables_score_join = StringProperty('')
    tables_temps_join = StringProperty('')

    'Play musique when the game start'
    sound = SoundLoader.load('audio/music1.wav')
    sound.play()
    sound.volume = .5  # volume de la musique de 0 à 1

    """def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.init_audio()
        self.sound.play()

    def init_audio(self):
        self.sound = SoundLoader.load('audio/music1.wav')"""

    def on_press_facile(self):
        self.NOMBRE_QUESTION = 4
        self.OPR = 0
        self.NOMBRE_MAX = 10
        self.DIFF = "Facile"
        self.menu_principal.opacity = 0
        self.afficher_la_question()
        # intialise le timer
        self.start = timer()
        self.game_state = True

    def on_press_moyen(self):
        self.NOMBRE_QUESTION = 20
        self.OPR = 1
        self.NOMBRE_MAX = 10
        self.DIFF = "Moyen"
        self.menu_principal.opacity = 0
        self.afficher_la_question()
        self.start = timer()
        self.game_state = True

    def on_press_difficile(self):
        self.NOMBRE_QUESTION = 20
        self.OPR = 2
        self.NOMBRE_MAX = 100
        self.DIFF = "Difficile"
        self.menu_principal.opacity = 0
        self.afficher_la_question()
        self.start = timer()
        self.game_state = True

    def afficher_la_question(self):
        Clock.schedule_once(self.hide_reponse_view, .5)
        self.a = random.randint(self.NOMBRE_MIN, self.NOMBRE_MAX)
        self.b = random.randint(self.NOMBRE_MIN, self.NOMBRE_MAX)
        opr_str = "+"
        if self.OPR == 1:
            opr_str = "*"
            self.o = 1
        elif self.OPR == 2:
            self.o = random.randint(0, 1)
            if self.o == 1:
                opr_str = "*"
        self.question = f"Calculer {self.a} {opr_str} {self.b} ?"

    def hide_reponse_view(self, dt):
        self.reponse_view.opacity = 0

    def on_text_validate(self, widget):
        self.reponse_str = widget.text
        try:
            self.reponse_int = int(self.reponse_str)
            self.text_imput_state_validate = True
            """self.verifier_la_reponse()

            if self.nb_question < self.NOMBRE_QUESTION:
                self.afficher_la_question()
                self.nb_question += 1
            else:
                print('le jeux est fini')
                self.end = timer()
                print(f"L'exercice à duré : {int(self.end - self.start)} s")
                self.temps = int(self.end - self.start)
                self.nom_score()"""
        except:
            self.valider_reponse = "Veuillez entrer un nombre"
            self.reponse_view.opacity = 1
            Clock.schedule_once(self.hide_reponse_view, .5)  # permet de masquer le widget de reponse en x seconde

    def on_press_validate(self):
        if self.text_imput_state_validate:
            # print(self.reponse_str)
            self.text_imput_state_validate = False
            self.verifier_la_reponse()
            if self.nb_question < self.NOMBRE_QUESTION:
                self.afficher_la_question()
                self.nb_question += 1
            else:
                self.end = timer()
                self.temps = int(self.end - self.start)
                self.reponse_view.opacity = 0
                self.nom_score_view.opacity = 1

    def verifier_la_reponse(self):
        calcul = self.a + self.b
        if self.o == 1:
            calcul = self.a * self.b
        if self.reponse_int == calcul:
            self.valider_reponse = "BONNE REPONSE"
            self.reponse_view.opacity = 1
            self.nb_points += 1
        else:
            self.valider_reponse = "MAUVAISE REPONSE"
            self.reponse_view.opacity = 1

    def on_name_validate(self, widget):
        self.nom = widget.text
        self.nom_score()

    def nom_score(self):
        self.score_afficher = f"{self.nom} votre score est de : {self.nb_points}/{self.NOMBRE_QUESTION} en {self.temps} s "
        self.sauvegarde_score()
        self.game_state = False

    'Enregistre le score dans une base de donné SQLITE'

    def sauvegarde_score(self):
        filename = 'Score_Jeux_de_Math.db'
        con = sqlite3.connect(filename)
        cur = con.cursor()
        try:
            cur.execute('''CREATE TABLE Score
            (
                nom VARCHAR(100), 
                difficulte VARCHAR(100),
                score INT,
                Temps INT
                )''')
        except:
            pass
        cur.execute("INSERT INTO Score VALUES (?, ?, ?,?)", (self.nom, self.DIFF, self.nb_points, self.temps))
        con.commit()
        for row in cur.execute('SELECT * FROM Score ORDER BY score DESC'):
            self.tables.append(row)

        for e in self.tables:
            self.tables_names.append(e[0])
            self.tables_difficulte.append(e[1])
            self.tables_score.append(e[2])
            self.tables_temps.append(e[3])

        self.tables_names_join = "\n".join(map(str, self.tables_names))
        self.tables_difficulte_join = "\n".join(map(str, self.tables_difficulte))
        self.tables_score_join = "\n".join(map(str, self.tables_score))
        self.tables_temps_join = "\n".join(map(str, self.tables_temps))

    def on_press_restart_button(self):
        self.nom_score_view.opacity = 0
        self.menu_principal.opacity = 1
        self.start = None
        self.end = None
        self.nb_points = 0
        self.nb_question = 1
        self.tables = []
        self.tables_names = []
        self.tables_difficulte = []
        self.tables_score = []
        self.tables_temps = []


class MathApp(App):
    pass


MathApp().run()

