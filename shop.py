import pygame
import math


class Shop:
    def __init__(self, bg,*arg):
        # définit le rectangle du shop, les tabs du shop, le dictionnaire des tabs du shop, le tab ouvert actuellement, si un achat est en train d'être fait, récupère le bg, dictionnaire des images du shop, numéro de l'objet en cours d'achat
        self.surface = pygame.rect.Rect(0, 0, bg.w / 4, bg.h)
        self.loading_rect = pygame.rect.Rect(0,0,0, bg.h)
        self.loading_rect_width = 0
        self.tabs = [pygame.rect.Rect(0, 0, bg.w / 12, bg.h / 14),pygame.rect.Rect(bg.w / 12, 0, bg.w / 12, bg.h / 14),pygame.rect.Rect(bg.w / 6, 0, bg.w / 12, bg.h / 14)]
        self.shop_tabs = []
        self.tab_open = 0
        self.shop_tab_open = 0 #utilité à vérifier
        self.buying = False
        self.bg = bg
        self.what_buying = 0
        # dictionnaire des noms des bâtiments, dictionnaire des prix des bâtiments
        self.buying_name = {
            1: "Caserne",
            2: "Maison2",
            3: "Usine",
            4: "Eglise"
            }
        self.buying_prices = {1:(-10,-50),2: (-50,-20),3:(-20,-20), 4:(-40,-20)}
        # importation des différentes images
        self.a = 1
        self.buying_image = {}
        for i in arg:
            setattr(self, ("shop_" + self.buying_name[self.a]),pygame.transform.scale(i,(int(bg.w / 8), int(bg.w / 8))))
            setattr(self, ("buying_" + self.buying_name[self.a]),i)
            self.buying_image[self.a] = getattr(self,("buying_" + self.buying_name[self.a]))
            self.a += 1
        
    # affichage du shop
    def draw_shop(self, win, w, h, placeable):
        # si pas en achat
        if not self.buying:
            # action en fonction du tab ouvert
            if self.shop_tab_open == 0:
                pass
            elif self.tab_open == 1:
                pass
            elif self.tab_open == 2:
                pass
            else:
                pass
            if self.tab_open == 0:
                # affichage des bâtiments dans le shop
                win.blit(self.shop_Caserne, (0, self.tabs[0].h))
                win.blit(self.shop_Maison2, (int(w / 8), self.tabs[0].h))
                win.blit(self.shop_Eglise, (0, int(self.tabs[0].h + w / 8)))
                win.blit(self.shop_Usine, (int(w / 8), int(self.tabs[0].h + w / 8)))
                win.blit(self.shop_Caserne, (0, self.tabs[0].h + w / 4))
                win.blit(self.shop_Maison2, (int(w / 8), self.tabs[0].h + w / 4))
                win.blit(self.shop_Eglise, (0, int(self.tabs[0].h + 3 * w / 8)))
                win.blit(self.shop_Usine, (int(w / 8), int(self.tabs[0].h + 3 * w / 8)))
                # affichage des tabs dans le shop
                pygame.draw.rect(win, (150, 150, 150), self.tabs[0])
                pygame.draw.rect(win, (160, 160, 160), self.tabs[1])
                pygame.draw.rect(win, (150, 150, 150), self.tabs[2])
                # affichage du nom des tabs dans le shop
                font = pygame.font.SysFont("arial", round(w / 85))
                for i in range(3):
                    text = font.render(self.bg.l.vocab[i+4], True, pygame.Color('black'))
                    text_rect = text.get_rect()
                    text_rect.center = (i * w / 12 + w / 24), h / 28
                    win.blit(text, text_rect)

        else:
            # définit l'image du bâtiment en cours d'achat, ses coordonnées
            original_image = self.what_buying[0]
            image = pygame.transform.scale(original_image, (math.floor(original_image.get_width() * self.bg.zoom),
                                                            math.floor(original_image.get_height() * self.bg.zoom)))
            self.buying_x = round(
                (pygame.mouse.get_pos()[0] - image.get_width() / 2) / (25 * self.bg.zoom)) * 25 * self.bg.zoom + (
                                        (self.bg.x / (25 * self.bg.zoom)) % 1) * 25 * self.bg.zoom
            self.buying_y = round(
                (pygame.mouse.get_pos()[1] - image.get_height() / 2) / (25 * self.bg.zoom)) * 25 * self.bg.zoom + (
                                        (self.bg.y / (25 * self.bg.zoom)) % 1) * 25 * self.bg.zoom
            self.rect_buying = image.get_rect()
            self.rect_buying.x = self.buying_x
            self.rect_buying.y = self.buying_y
            # affichage du bâtiment en cours d'achat
            win.blit(image, (self.buying_x, self.buying_y))
            # affichage d'une bordure rouge en cas d'achat irréalisable
            if not placeable:
                original_imp_action_image = pygame.image.load("Images/Inachetable.png")
                imp_action_image=pygame.transform.scale(original_imp_action_image,(image.get_width(),image.get_height()))
                win.blit(imp_action_image,(self.buying_x,self.buying_y))

    # animation d'ouverture du shop
    def open(self, win):
        if self.loading_rect.width >= self.bg.w/4:
            self.loading_rect = pygame.rect.Rect(0,0,0,self.bg.h)
            self.loading_rect_width = 0
            return 1
        self.loading_rect_width += self.bg.w/40
        self.loading_rect.width = round(self.loading_rect_width)
        pygame.draw.rect(win,(150,150,150),self.loading_rect)
        
    def close(self, win):
        if self.loading_rect_width <= 0:
            return 'b'
        self.loading_rect.width = round(self.loading_rect_width)
        self.loading_rect_width -= self.bg.w/40
        pygame.draw.rect(win, (150, 150, 150), self.loading_rect)

    # vérification des collisions avec les tabs pour ouvrir le shop
    def check_collision_tabs(self, tab_nmbr, pos):
        p = self.bg.prop_h
        if pos[1] <= p * (35 + 270 * tab_nmbr) and pos[1] <= pos[0] :
            return False
        elif pos[1] >= p * (235 + 270 * tab_nmbr) and pos[1] - 235 * p >= 35 * p - pos[0]:
           return False
        else:
            return tab_nmbr + 1