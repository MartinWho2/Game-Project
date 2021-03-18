import pygame
import math
import os
import pickle
from shop import Shop
from Langues import Language
from jauge import Jauge
from images import Images
from building import Building
from background import Background
from Menu import Menu
from Encode import encode, get_words, decoding


class Game:
    def __init__(self, win):
        # Définit la fenêtre, un dictionnaire avec les images, le background, le menu, si le shop est ouvert, si l'objet en cours d'achat est positionnable, le shop
        self.win = win
        self.pictures = self.loading()
        self.bg = Background(win, Language(), self.pictures['Maison 3'])
        self.dict_loading = {'A':'Caserne','B': 'Tank_factory','C':'Centrale_electrique','D':'Hopital',
                          'E':'Repos','F':'Plane_factory', 'G': 'Usine', 'H': 'Laboratoire', 'I': 'Tour',
                          'J':'Radio','K':'Mur','L':'Tranchee','M': 'Barbele', 'N': 'Mine', 'O':'Route',
                           'P':'Immeuble', 'Q': 'Immeuble_2','R': 'Immeuble_3', 'S': 'Townhall',
                          'T':'Eglise', 'U': 'Banque', 'V': 'Maison', 'W':'Maison2','X':'Maison_3'}
        self.menu = Menu(self.bg)
        self.shop_open = False
        self.shop_opening = 0
        self.placeable = True
        self.shop = Shop(self.bg, self.pictures['Caserne'], self.pictures['Maison2'], self.pictures['Usine'],
                         self.pictures['Eglise'])
        self.True_dict = {'a': True, 1: True, 'b': False, 2: False}
        # Définit un groupe de sprite, une jauge pour l'or, une jauge pour le matériel,
        # un dictionnaire pour les touches pressées
        self.buildings = pygame.sprite.Group()
        self.gold = Jauge(self.pictures['Pièce'], 1, 10000, self.bg.h, self.bg.w)
        self.stuff = Jauge(self.pictures['Matériel'], 2, 50000000, self.bg.h, self.bg.w)
        self.keys = {}
        # Définit les tabs permettant d'accéder au magasin/projets/recherches/doctrines
        self.tabs = pygame.transform.scale(self.pictures['Onglets'],
                                           (int(36 * (self.bg.h / 1080)), int(1080 * (self.bg.h / 1080))))
        # Définit une variable permettant de ne pas ouvrir l'interface d'un bâtiment au moment où on l'achète
        self.bought = False
        self.interface_on = False
        # Définit si le jeu tourne, si le jeu est en pause, si le menu save/load est ouvert,
        # si le choix dans le menu save/load est vrai ou faux
        self.run = True
        self.pause = False
        self.s_l = False
        self.s_l_choice = False
        # Définit 4 couleurs
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        # Définit les boutons pressés de la souris, 2 polices d'écriture,
        # affiche une première fois les textes des tabs pour ouvrir le menu
        self.buttons = (0, 0, 0)
        self.font_1 = pygame.font.SysFont('comicsans', int(self.bg.w / 10))
        self.font_2 = pygame.font.SysFont("Rockwell", int(self.bg.w / 40))
        self.write_text()

    def loading(self):
        # définit un pourcentage de chargement, la liste de toutes les images
        percent, list = 0, os.listdir("Images")
        n, img = len(list), {}
        # importation de toutes les images, affichage de la barre de téléchargement
        for i in list:
            img[str(i)[:-4]] = pygame.image.load("Images/" + i)
            percent += 1 / n
            pygame.draw.rect(self.win, (255, 255, 255),
                             pygame.rect.Rect(0, round(self.win.get_height() * 2 / 3),
                                              round(self.win.get_width() * percent),
                                              round(self.win.get_height() / 6)))
            pygame.display.flip()
        return img

    def write_text(self):
        # fonction pour afficher le noms des tabs permettant d'accéder au magasin/projets/recherches/doctrines
        for i in range(4):
            setattr(self, ("tab_text_" + str(i)),
                    pygame.transform.rotate((self.font_2.render(self.bg.l.vocab[i], True, self.red)), -90))
            setattr(self, ("tab_text_rect_" + str(i)), getattr(self, ("tab_text_" + str(i))).get_rect())
            getattr(self, ("tab_text_rect_" + str(i))).center = (18 * self.bg.prop_h, (2 * i + 1) * self.bg.h / 8)

    def update(self):
        # remplit la fenêtre
        self.win.fill((0, 0, 0))
        self.buttons = pygame.mouse.get_pressed(num_buttons=3)
        # permet de déplacer le background avec les touches
        if not self.buttons[0]:
            v = pygame.math.Vector2()
            v.xy = 0, 0
            if self.keys.get(pygame.K_s):
                v.y -= self.bg.factor
            if self.keys.get(pygame.K_w):
                v.y += self.bg.factor
            if self.keys.get(pygame.K_a):
                v.x += self.bg.factor
            if self.keys.get(pygame.K_d):
                v.x -= self.bg.factor
            if v.length() > self.bg.factor:
                v.scale_to_length(self.bg.factor)
            self.bg.x += v.x
            self.bg.y += v.y
        # définit si un bâtiment peut être placé
        self.placeable = True
        # affiche le background
        self.win.blit(pygame.transform.scale(self.bg.image, (
            math.floor(self.bg.image.get_width() * self.bg.zoom),
            math.floor(self.bg.image.get_height() * self.bg.zoom))),
                      (math.floor(self.bg.x), math.floor(self.bg.y)))
        # affiche tous les sprites
        self.buildings.draw(self.win)
        # replace tous les sprites si un déplacement ou un zoom a lieu,
        # vérifie si les sprites ne touchent pas l'objet qui va être construit
        for sprite in self.buildings:
            sprite.replace()
            if self.shop_open:
                if pygame.Rect.colliderect(sprite.rect, self.shop.rect_buying):
                    self.placeable = False
            if sprite.bool_interface:
                sprite.update_interface(self.win)

        # affiche les jauges
        self.stuff.display(self.win)
        self.gold.display(self.win)
        # affiche les tabs permettants d'accéder au shop
        if not self.shop_open and not self.shop_opening:
            self.win.blit(self.tabs, (0, 0))
            for i in range(4):
                self.win.blit(getattr(self, ("tab_text_" + str(i))), getattr(self, ("tab_text_rect_" + str(i))))
        if self.shop_opening:
            if self.shop_opening == 1:
                a = self.shop.open(self.win)
            else:
                a = self.shop.close(self.win)
            if a:
                self.shop_opening = 0
                self.shop_open = self.True_dict[a]
                print(f"[EVENT] Shop {self.shop_open}")
        # affiche le shop
        if self.shop_open:
            self.shop.draw_shop(self.win, self.bg.w, self.bg.h, self.placeable)

    def save_load(self):
        # crée le menu save/load (couleurs, textes, coordonnées des textes, afficher les couleurs, afficher les textes)
        self.win.fill(self.red)
        pygame.draw.rect(self.win, self.blue, pygame.Rect(0, 0, int(self.bg.w / 2), self.bg.h))
        save = self.font_1.render("SAVE", True, (0, 0, 0))
        load = self.font_1.render("LOAD", True, (0, 0, 0))
        saveRect, loadRect = save.get_rect(), load.get_rect()
        saveRect.center, loadRect.center = (int(self.bg.w / 4), int(self.bg.h / 2)), (
            int(self.bg.w * 3 / 4), int(self.bg.h / 2))
        self.win.blit(save, saveRect)
        self.win.blit(load, loadRect)

    def save_load_events(self):
        for e in pygame.event.get():
            # quitter le jeu de force
            if e.type == pygame.QUIT:
                self.run = False
                pygame.quit()
            # récupérer les coordonnées de clic de la souris
            if e.type == pygame.MOUSEBUTTONDOWN:
                x = pygame.mouse.get_pos()[0]
                # False to save and True to load
                if x < self.bg.w / 2:
                    self.s_l_choice = False
                else:
                    self.s_l_choice = True
            # vérification du point de relâchement du clic de la souris
            if e.type == pygame.MOUSEBUTTONUP:
                x = pygame.mouse.get_pos()[0]
                # charger les données de sauvegarde
                if self.s_l_choice and x > self.bg.w / 2:
                    infos = decoding()
                    print(infos)
                    self.buildings.empty()
                    self.gold.quantity, self.stuff.quantity = infos[0]
                    self.gold.add(0, self.bg.w)
                    self.stuff.add(0,self.bg.w)
                    self.bg.x,self.bg.y, self.bg.zoom = infos[1]
                    for b in infos[2]:
                        type = self.dict_loading[b[0][0]]
                        image = self.pictures[type]
                        batiment = Building(image,b[1],b[2],self.bg,type)
                        self.buildings.add(batiment)
                    self.s_l = False
                    self.win.fill((0, 0, 0))
                # sauvegarder les données de sauvegarde
                elif not self.s_l_choice and x < self.bg.w / 2:
                    resources = [self.gold.quantity, self.stuff.quantity]
                    building = []
                    for b in self.buildings:
                        building.append([b.type,b.gap_x,b.gap_y])
                    data = [resources,[self.bg.x,self.bg.y,self.bg.zoom], building]
                    encode(data)
                    self.s_l = False
                    self.win.fill((0, 0, 0))
            # si la touche escape est pressée, le menu save/load est fermé
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.s_l = False
                    self.win.fill((0, 0, 0))

    def menu_events(self):
        # affichage des textes du menu
        self.win.blit(self.menu.resume, self.menu.resumeRect)
        self.win.blit(self.menu.save, self.menu.saveRect)
        self.win.blit(self.menu.quit, self.menu.quitRect)
        # vérification de tous les événements dans le menu
        for e in pygame.event.get():
            # si le jeu est quitté, tout s'arrête
            if e.type == pygame.QUIT:
                self.run = False
                pygame.quit()
            # si le jeu détecte un mouvement de souris
            if e.type == pygame.MOUSEMOTION:
                if not self.menu.clicked:
                    # si la souris n'est pas appuyée, récupération de ses coordonnées
                    x, y = pygame.mouse.get_pos()
                    # vérification d'une éventuelle collision avec un des textes
                    for rectangle in self.menu.rects:
                        if rectangle.collidepoint(x, y) and self.menu.selected != self.menu.rects.index(rectangle):
                            # à vérifier                mise en évidence du texte sous la souris
                            self.menu.selected = self.menu.rects.index(rectangle)
                            setattr(self.menu, 'color_' + str(self.menu.selected), self.green)
                            setattr(self.menu, 'color_' + str((self.menu.selected - 1) % 3), self.white)
                            setattr(self.menu, 'color_' + str((self.menu.selected - 2) % 3), self.white)
                            setattr(self.menu, 'font_' + str(self.menu.selected),
                                    pygame.font.SysFont('comicsans', int(self.bg.w / 9)))
                            setattr(self.menu, 'font_' + str((self.menu.selected - 1) % 3),
                                    pygame.font.SysFont('comicsans', int(self.bg.w / 10)))
                            setattr(self.menu, 'font_' + str((self.menu.selected - 2) % 3),
                                    pygame.font.SysFont('comicsans', int(self.bg.w / 10)))
                            self.menu.event_happens = True
                            self.win.fill((0, 0, 0))
            # si la souris est pressée, récupération des coordonnées
            if e.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # si il y a une collision avec un des textes du menu, ouverture de la page correspondante

                if self.menu.rects[self.menu.selected].collidepoint(x, y):
                    self.menu.clicked = self.menu.selected + 1
            # si la souris est relachée, récupération des coordonnées
            if e.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                # si les coordonnées sont les mêmes, exécution de l'action concernée
                if self.menu.rects[self.menu.clicked - 1].collidepoint(x, y):
                    if self.menu.clicked == 1:
                        self.pause = False
                    if self.menu.clicked == 2:
                        self.s_l = True
                    if self.menu.clicked == 3:
                        self.run = False
                        pygame.quit()
                self.menu.clicked = 0
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.pause = False

    def events(self):
        # vérification de tous les événements (pas dans le menu)
        for e in pygame.event.get():
            # si le jeu est quitté, tout fermer
            if e.type == pygame.QUIT:
                self.run = False
                pygame.quit()
            # si une touche est pressée
            elif e.type == pygame.KEYDOWN:
                # ajout dans le dictionnaire des touches
                self.keys[e.key] = True
                # touche de développeur
                if e.key == pygame.K_SPACE:
                    self.gold.add(1000, self.bg.w)
                # touche pour le menu
                if e.key == pygame.K_ESCAPE:
                    self.pause = True
                    self.win.fill((0, 0, 0))
                # touche pour le shop
                if e.key == pygame.K_k:
                    if self.shop_open:
                        self.shop_opening = 2
                        self.shop.loading_rect_width = round(self.bg.w / 4)
                        self.shop_open = False
                    else:
                        self.shop_opening = 1
                    self.shop.buying = False
                # touches pour les langues
                if e.key == pygame.K_1:
                    self.bg.l.change_language(1, self.bg, self.shop)
                    self.write_text()
                if e.key == pygame.K_2:
                    self.bg.l.change_language(2, self.bg, self.shop)
                    self.write_text()
                if e.key == pygame.K_3:
                    self.bg.l.change_language(3, self.bg, self.shop)
                    self.write_text()
            # si une touche est relachée
            elif e.type == pygame.KEYUP:
                # retrait du dictionnaire des touches
                self.keys[e.key] = False

            # si un bouton de la souris est pressé
            elif e.type == pygame.MOUSEBUTTONDOWN:
                # si c'est le boutton 1
                if e.button == 1:
                    # récupération de la position et du temps de click
                    self.pos = pygame.mouse.get_pos()
                    self.down_click = pygame.time.get_ticks()
                    # Si une interface est ouverte et qu'on clique sur la croix, ferme l'interface
                    if round(self.bg.w * 7 / 8) <= self.pos[0] <= round(self.bg.w * 109 / 120) and round(
                            self.bg.h * 2 / 3) <= self.pos[1] <= (round(self.bg.h * 2 / 3) + round(self.bg.w / 30)):
                        for building in self.buildings:
                            if building.bool_interface:
                                building.bool_interface = False
                    # si le shop est ouvert
                    if self.shop_open:
                        # si un bâtiment est en train d'être acheté, achat du bâtiment sélectionné, ajout dans le groupe des sprites, retrait des ressources de constructions
                        if self.shop.buying and self.gold.quantity + self.shop.what_buying[2][0] >= 0 and self.stuff.quantity + self.shop.what_buying[2][1] >= 0 and self.placeable:
                            surface = self.shop.what_buying[0]
                            batiment = Building(surface, (self.shop.buying_x - self.bg.x) / self.bg.zoom,
                                                (self.shop.buying_y - self.bg.y) / self.bg.zoom,
                                                self.bg, self.shop.what_buying[1])
                            self.buildings.add(batiment)
                            self.gold.add(self.shop.what_buying[2][0], self.bg.w)
                            self.stuff.add(self.shop.what_buying[2][1], self.bg.w)
                            self.shop.buying = False
                            # Permet de ne pas ouvrir le menu du bâtiment immédiatement
                            self.bought = True
                            self.shop.bought = 0
                        # si le shop est ouvert
                        elif not self.shop.buying:
                            # vérification du point d'impact sur les images des bâtiments
                            if self.pos[0] <= self.bg.w / 4:
                                continu = True
                                for i in range(0, 3):
                                    if self.shop.tabs[i].collidepoint(self.pos[0], self.pos[1]):
                                        self.shop.tab_open = i
                                        continu = False
                                        break

                                # calcul du bâtiment sélectionné en fonction du point d'impact,
                                if continu:
                                    row = math.ceil((self.pos[1] - self.bg.h / 14) / (self.bg.w / 8))
                                    x = 2 * row - 2
                                    if self.pos[0] <= self.bg.w / 8:
                                        x += 1
                                    else:
                                        x += 2
                                    self.shop.what_buying = (
                                        self.shop.buying_image[int(x)], self.shop.buying_name[int(x)],
                                        self.shop.buying_prices[int(x)])
                                    self.shop.buying = True
                    # vérification du point d'impact sur les tabs
                    elif self.pos[0] <= self.bg.w * 3 / 160:
                        # si une collision est détectée
                        tab = self.shop.check_collision_tabs(math.floor(4 * self.pos[1] / self.bg.h), self.pos)
                        # exécution de l'action concernée
                        if tab == 1:
                            self.shop_opening = 1
                        elif tab == 2:
                            print("Projets = True")
                        elif tab == 3:
                            print("Recherches = True")
                        elif tab == 4:
                            print("Doctrines = True")

            elif e.type == pygame.MOUSEBUTTONUP:
                # Si on ne vient pas d'acheter un bâtiment
                if not self.bought:
                    # Récupération de la position de la souris et création d'un vecteur entre le clic et le déclic
                    up_pos = pygame.mouse.get_pos()
                    vector = pygame.math.Vector2(up_pos[0] - self.pos[0], up_pos[1] - self.pos[1])
                    # Si le vecteur est petit
                    if vector.length() < 15:
                        # Pour chaque bâtiment
                        for building in self.buildings:
                            # Si le bâtiment est visible à l'écran
                            if not self.shop.buying and 0 <= self.bg.x + building.gap_x < self.bg.w and 0 <= self.bg.y + building.gap_y < self.bg.h:
                                # Si on a cliqué dessus
                                if building.rect.collidepoint(up_pos[0], up_pos[1]):
                                    # Ouvre l'interface du bâtiment et définit qu'un interface est ouverte
                                    if self.interface_on:
                                        for chose in self.buildings:
                                            if chose.bool_interface:
                                                chose.bool_interface = False
                                                break
                                    building.open_interface()
                                    self.interface_on = True
                                    break
                else:
                    self.bought = False

            # permet de bouger le background avec la souris
            elif e.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_rel()
                if self.buttons[0] and (self.shop_open is False or pygame.mouse.get_pos()[0] > self.bg.w / 4):
                    self.bg.x += mx
                    self.bg.y += my
            # permet de zoomer avec la molette
            elif e.type == pygame.MOUSEWHEEL:
                rx, ry = pygame.mouse.get_pos()
                if self.shop_open is False or pygame.mouse.get_pos()[0] > self.bg.w / 4:
                    for i in range(int(math.fabs(e.y))):
                        factor = e.y / math.fabs(e.y) * 0.225 + 1.025
                        if not (self.bg.zoom > 3.5 and factor > 1) and not (self.bg.zoom < 0.2 and factor < 1):
                            self.bg.zoom = self.bg.zoom * factor
                            self.bg.x = rx + (self.bg.x - rx) * factor
                            self.bg.y = ry + (self.bg.y - ry) * factor
