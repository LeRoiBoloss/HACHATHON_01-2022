from random import randint
from random import choice
import pygame as pg

# Initialisation
pg.font.init()
myfont = pg.font.SysFont('Alerte', 75)
screen = pg.display.set_mode((600, 600))
clock = pg.time.Clock()


# Les variables utiles
noir = (0, 0, 0)
blanc = (255, 255, 255)
jaune = (255, 255, 0)
gris = (211, 211, 211)
bleu = (0, 0, 255)
rouge = (255, 0, 0)
vert = (0, 128, 0)
LEVEL = 1
GOLD = 0
ARMOR = 5


def interieur_carre(x1, y1, x2, y2):
    inte = []
    for i in range(x1+1, x2):
        for j in range(y1+1, y2):
            inte.append((i, j))
    return inte


def contour_carre(x1, y1, x2, y2):
    gauche = [(x1, i) for i in range(y1, y2+1)]
    droite = [(x2, i) for i in range(y1, y2+1)]
    haut = [(i, y1) for i in range(x1, x2+1)]
    bas = [(i, y2) for i in range(x1, x2+1)]
    return gauche + droite + haut + bas


def trace_rect(a, b, color, width=10, height=10):
    rect = pg.Rect(a*10, b*10, width, height)
    pg.draw.rect(screen, color, rect)


def gen_dj():
    salles = [(5, 5, 30, 20), (45, 10, 55, 20), (25, 25, 35, 40),
              (5, 30, 15, 40), (10, 45, 35, 55), (45, 45, 55, 55)]
    cont = []
    inte = []
    for salle in salles:
        cont = cont + contour_carre(*salle)
        inte = inte + interieur_carre(*salle)
    return cont, inte


def couloir():
    coul = [(27, i) for i in range(20, 26)]
    coul = coul + [(12, i) for i in range(40, 46)]
    coul = coul + [(30, i) for i in range(40, 46)]
    coul = coul + [(i, 30) for i in range(35, 51)]
    coul = coul + [(50, i) for i in range(20, 46)]
    return coul


def combat(Arm, lvl, Gld):
    lup = False
    if (x, y) in mechants:
        mechants.remove((x, y))
        damage = randint(0, 3)
        Arm -= damage
        if Arm <= 0:
            return 0, False, Gld
        elif randint(1, lvl) == 1:
            lup = True
            Arm = lvl + 4
        Gld += randint(1, 5)
    return Arm, lup, Gld


# Génère le donjon
contours, interieurs = gen_dj()
couloirs = couloir()


# Coord perso
trace_rect(10, 10, jaune)
x, y = 10, 10


# Placement des méchants
nb = randint(5, 15)
choix = interieurs.copy()
choix.remove((10, 10))
mechants = []
for _ in range(nb):
    mechant = choice(choix)
    choix.remove(mechant)
    mechants.append(choice(choix))


# Le rendu
running = True
time = 30
lvlup = False
while running:
    clock.tick(30)
    # 1. lecture des évênements
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    # 2. actions
        elif event.type == pg.KEYDOWN:
            # si la touche est "Q" on veut quitter le programme
            if event.key == pg.K_q:
                running = False
            else:

                # Déplacement
                if event.key == pg.K_i:
                    if (x, y-1) in interieurs or (x, y-1) in couloirs:
                        y -= 1
                elif event.key == pg.K_k:
                    if (x, y+1) in interieurs or (x, y+1) in couloirs:
                        y += 1
                        trace_rect(x, y, jaune)
                elif event.key == pg.K_j:
                    if (x-1, y) in interieurs or (x-1, y) in couloirs:
                        x -= 1
                elif event.key == pg.K_l:
                    if (x+1, y) in interieurs or (x+1, y) in couloirs:
                        x += 1

    # 3. rendu
    trace_rect(0, 0, noir, width=600, height=600)

    for contour in contours:
        trace_rect(*contour, blanc)

    for interieur in interieurs:
        trace_rect(interieur[0]+0.5, interieur[1]+0.5,
                   blanc, width=2, height=2)

    for couloir in couloirs:
        trace_rect(*couloir, gris)

    trace_rect(x, y, jaune)

    for k, mechant in enumerate(mechants):
        trace_rect(*mechant, rouge)

    caracteristiques = f"Level: {LEVEL}, Gold: {GOLD}, Armor: {ARMOR}"
    pg.display.set_caption(caracteristiques)

    ARMOR, lvlup, GOLD = combat(ARMOR, LEVEL, GOLD)

    if ARMOR == 0 or not mechants:
        running = False

    if lvlup and running:
        time = 0
        LEVEL += 1
        lvlup = False
    if time < 30:
        textsurface = myfont.render('LEVEL UP!', False, vert)
        screen.blit(textsurface, (175, 275))
    time += 1

    pg.display.update()

# Message de fin de jeu
if mechants:
    textsurface = myfont.render('GAME OVER...', False, rouge)
    screen.blit(textsurface, (135, 275))
else:
    textsurface = myfont.render('VICTORY', False, vert)
    screen.blit(textsurface, (200, 275))
pg.display.update()

# Quitter le jeu
quitting = True
while quitting:
    clock.tick(30)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quitting = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                quitting = False

pg.quit()
