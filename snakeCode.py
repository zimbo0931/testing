# On importe les fonctions necessaires

from tkinter import *
from random import randrange


# Fonction la plus compliqu�e permettant le d�placement du serpent
def deplacement():
    global a, b, z, y, lu, lv, score, serpent, j, m
    c = len(serpent)
    c = c - 1
    # Chaque carr� reprend la coordonn�e du pr�c�dent dans la liste (serpent)
    while c != 0:
        lu[c] = lu[c - 1]
        lv[c] = lv[c - 1]
        c += -1
    # On change les coordon�es du premier carr�
    lu[0] += a
    lv[0] += b
    c = 0
    # On applique les nouvelles coordonn�es aux carr�s correspondant
    while c != len(serpent):
        can.coords(serpent[c], lu[c], lv[c], lu[c] + 10, lv[c] + 10)
        c += 1
    c = 1
    # Si les coordonn�es du premier carr� sont �gales � celle d'un autre le jeu s'arr�tera
    while c != len(serpent):
        if lu[c] == lu[0] and lv[c] == lv[0]:
            j = 1
            score = 'Perdu  avec  ' + str(score * 10)
            scores.set(score)
            break
        c += 1
    # Si le serpent est mord un cot� il ressort de l'autre
    # La valeur 'd' sert � empecher un bug empechant la transfert du serpent de l'autre cot� du canvevas
    d = 1
    if lu[0] == 600:
        lu[0], d = 10, 0
    if lu[0] == 0 and d == 1:
        lu[0] = 600
    if lv[0] == 600:
        lv[0], d = 10, 0
    if lv[0] == 0 and d == 1:
        lv[0] = 600
    d = 0
    # Si le carr� de t�te recoupe le cercle, le score augmente et un nouveau cercle apparait al�atoirement
    if z - 7 <= lu[0] <= z + 7 and y - 7 <= lv[0] <= y + 7:
        score += 1
        scores.set(str(score * 10))
        bestiole()
    if j != 1 and m != 1:
        fen.after(100, deplacement)


# Cette fonction cr�e un cercle de coordon�e multiple de 10 pour �viter que le cercle soit partiellement coup� par le serpent

def bestiole():
    global z, y, n, lu, lv, serpent, a, b
    z = randrange(2, 18)
    y = randrange(2, 18)
    z = z * 10
    y = y * 10
    can.coords(cercle, z, y, z + 5, y + 5)
    # On ajoute un carr� hors du canevas (pour all�ger le code) qui se rajoutera � la suite
    serpents = can.create_rectangle(300, 300, 310, 310, fill='green')
    serpent.append(serpents)
    lu.append(lu[n] + 12 + a)
    lv.append(lv[n] + 12 + b)
    n += 1


# Ces quatres fonctions permettent le d�placement dans quatres directions du serpent
# Grace aux modifications successives des coordon�es du premier carr�e grave au valeur a et b
# La valeur s permet de ne pas accelerer la vitesse du serpent ou � modifier ca direction
# en appuyant successivement sur Haut/Bas/Gauche/Droite

def gauche(event):
    global a, b, s
    a = -10
    b = 0
    if s == 0:
        s = 1
        deplacement()


def droite(event):
    global a, b, s
    a = 10
    b = 0
    if s == 0:
        s = 1
        deplacement()


def haut(event):
    global a, b, s
    a = 0
    b = -10
    if s == 0:
        s = 1
        deplacement()


def bas(event):
    global a, b, s
    a = 0
    b = 10
    if s == 0:
        s = 1
        deplacement()


# Cette fonction permet d'arr�ter le serpent

def pause(event):
    global j, a, b, m, enpause
    t = 0
    if a == b:
        t = 1
    if j != 1:
        # Affichage ou Effacage du texte 'PAUSE'
        # Et arr�t du serpent
        if m != 1:
            m = 1
            can.coords(enpause, 100, 100)
        else:
            m = 0
            can.coords(enpause, 300, 300)
            if t != 1:
                deplacement()


# Cette fonction r�initialise toutes les valeurs et recr��e le serpent de base ainsi que le premier repas

def recommencer(event):
    global z, y, lu, lv, score, serpent, j, m, s, n, a, b, cercle
    if j != 1:
        print
        'Le suicide est puni'
    can.delete(ALL)
    s = score = j = m = a = b = 0
    z = y = 50
    lu, lv, serpent = [100, 112], [100, 112], []
    n = 1
    tete = can.create_rectangle(100, 100, 110, 110, fill='dark green')
    carre = can.create_rectangle(112, 100, 122, 110, fill='green')
    cercle = can.create_oval(z, y, z + 5, y + 5, fill='red')
    serpent.append(tete)
    serpent.append(carre)
    scores.set('0')


# On d�finit les valeurs initiales

s = score = j = m = t = a = b = 0
z = y = 50
lu, lv, serpent = [100, 112], [100, 112], []
n = 1

print
' ' * 35 + 'Les fleches pour bouger'
print
' ' * 35 + 'P pour mettre/enlever la pause'
print
' ' * 35 + 'Entree pour recommencer, attention au suicide'

# On cr�e un canevas tout gris

fen = Tk()
can = Canvas(fen, width=600, height=600, bg='gray')
can.grid(row=1, column=0, columnspan=3)

enpause = can.create_text(300, 300, text="PAUSE")

# On cr�e la base du serpent ainsi que le premier repas

tete = can.create_rectangle(100, 100, 110, 110, fill='dark green')
carre = can.create_rectangle(112, 100, 122, 110, fill='green')
cercle = can.create_oval(z, y, z + 5, y + 5, fill='red')

print(tete)
print(carre)
print(serpent)
serpent.append(tete)
serpent.append(carre)
print(serpent)

# On cr�e les commandes au clavier

can.bind_all('<Up>', haut)
can.bind_all('<Down>', bas)
can.bind_all('<Left>', gauche)
can.bind_all('<Right>', droite)
can.bind_all('<Return>', recommencer)
can.bind_all('p', pause)

# L'affichage du score

Label(fen, text='Score:  ').grid(row=0, column=0)

scores = StringVar()
Score = Entry(fen, textvariable=scores)
Score.grid(row=0, column=1)
scores.set('0')

fen.mainloop()