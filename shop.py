import pygame
import math


class Shop:
    def __init__(self, bg):
        self.surface = pygame.rect.Rect(0, 0, bg.w / 4, bg.h)
        self.tabs_name = bg.l.vocab[0], bg.l.vocab[1], bg.l.vocab[2], bg.l.vocab[3]
        self.tabs = [pygame.rect.Rect(0, 0, bg.w / (len(self.tabs_name) * 4), bg.h / 14),
                     pygame.rect.Rect(bg.w / (len(self.tabs_name) * 4), 0, bg.w / (len(self.tabs_name) * 4), bg.h / 14),
                     pygame.rect.Rect(bg.w / (len(self.tabs_name) * 2), 0, bg.w / (len(self.tabs_name) * 4), bg.h / 14),
                     pygame.rect.Rect(bg.w / (len(self.tabs_name) * 4 / 3), 0, bg.w / (len(self.tabs_name) * 4),
                                      bg.h / 14)]
        self.shop_tabs = []
        self.tab_open = 0
        self.shop_tab_open = 0
        self.buying = False
        self.image_buying = (0, 0)
        self.bg = bg
        self.what_buying = 0
        self.buying_image = {
            1:pygame.image.load("Images/Maison.png"),
            2:pygame.image.load("Images/Maison2.png"),
            3:pygame.image.load("Images/Usine.png"),
            4:pygame.image.load("Images/Eglise.png")
            }
        self.buying_name = {
            1:"Maison",
            2:"Maison2",
            3:"Usine",
            4:"Eglise"
            }
        self.buying_prices = {1:(-10,-50),2: (-50,-20),3:(-20,-20), 4:(-40,-20)}
        self.image_maison = pygame.transform.scale(pygame.image.load("Images/Maison.png"),(int(bg.w / 8), int(bg.w / 8)))
        self.image_maison2 = pygame.transform.scale(pygame.image.load("Images/Maison2.png"),(int(bg.w / 8), int(bg.w / 8)))
        self.image_eglise = pygame.transform.scale(pygame.image.load("Images/Usine.png"),(int(bg.w / 8), int(bg.w / 8)))
        self.image_usine = pygame.transform.scale(pygame.image.load("Images/Eglise.png"),(int(bg.w / 8), int(bg.w / 8)))
    def draw_shop(self, win, w, h, placeable):
        if not self.buying:
            if self.shop_tab_open == 0:
                pass
            elif self.tab_open == 1:
                pass
            elif self.tab_open == 2:
                pass
            else:
                pass
            if self.tab_open == 0:
                win.blit(self.image_maison, (0, self.tabs[0].h))
                win.blit(self.image_maison2, (int(w / 8), self.tabs[0].h))
                win.blit(self.image_eglise, (0, int(self.tabs[0].h + w / 8)))
                win.blit(self.image_usine, (int(w / 8), int(self.tabs[0].h + w / 8)))
                win.blit(self.image_maison, (0, self.tabs[0].h + w / 4))
                win.blit(self.image_maison2, (int(w / 8), self.tabs[0].h + w / 4))
                win.blit(self.image_eglise, (0, int(self.tabs[0].h + 3 * w / 8)))
                win.blit(self.image_usine, (int(w / 8), int(self.tabs[0].h + 3 * w / 8)))
                pygame.draw.rect(win, (150, 150, 150), self.tabs[0])
                pygame.draw.rect(win, (160, 160, 160), self.tabs[1])
                pygame.draw.rect(win, (150, 150, 150), self.tabs[2])
                pygame.draw.rect(win, (150, 160, 150), self.tabs[3])
                font = pygame.font.SysFont("arial", round(w / 85))
                for i in range(0, 4):
                    text = font.render(self.tabs_name[i], True, pygame.Color('black'))
                    text_rect = text.get_rect()
                    text_rect.center = (i * w / (len(self.tabs_name) * 4) + w / (len(self.tabs_name) * 8), h / 28)
                    win.blit(text, text_rect)
                

        else:
            original_image = self.what_buying[0]
            image = pygame.transform.scale(original_image, (math.floor(original_image.get_width() * self.bg.zoom),
                                                            math.floor(original_image.get_height() * self.bg.zoom)))
            self.buying_x = round(
                (pygame.mouse.get_pos()[0] - image.get_width() / 2) / (25 * self.bg.zoom)) * 25 * self.bg.zoom + (
                                        (self.bg.x / (25 * self.bg.zoom)) % 1) * 25 * self.bg.zoom
            self.buying_y = round(
                (pygame.mouse.get_pos()[1] - image.get_height() / 2) / (25 * self.bg.zoom)) * 25 * self.bg.zoom + (
                                        (self.bg.y / (25 * self.bg.zoom)) % 1) * 25 * self.bg.zoom
            self.rect_buying=image.get_rect()
            self.rect_buying.x=self.buying_x
            self.rect_buying.y=self.buying_y
            win.blit(image, (self.buying_x, self.buying_y))
            if not placeable:
                original_imp_action_image = pygame.image.load("Images/Inachetable.png")
                imp_action_image=pygame.transform.scale(original_imp_action_image,(image.get_width(),image.get_height()))
                win.blit(imp_action_image,(self.buying_x,self.buying_y))


    def check_collision_tabs(self,tab_nmbr,pos):
        p = self.bg.prop_h
        if pos[1] <= p * (35 + 270 * tab_nmbr) and pos[1] <= pos[0] :
            return False
        elif pos[1] >= p * (235 + 270 * tab_nmbr) and pos[1] - 235 * p >= 35 * p - pos[0]:
           return False
        else: return True