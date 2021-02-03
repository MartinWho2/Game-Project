import pygame
import math


class Shop:
    def __init__(self, bg,*arg):
        self.surface = pygame.rect.Rect(0, 0, bg.w / 4, bg.h)
        self.tabs = [pygame.rect.Rect(0, 0, bg.w / 12, bg.h / 14),pygame.rect.Rect(bg.w / 12, 0, bg.w / 12, bg.h / 14),pygame.rect.Rect(bg.w / 6, 0, bg.w / 12, bg.h / 14)]
        self.shop_tabs = []
        self.tab_open = 0
        self.shop_tab_open = 0
        self.buying = False
        self.image_buying = (0, 0)
        self.bg = bg
        self.what_buying = 0
        self.buying_name = {
            1: "Maison",
            2: "Maison2",
            3: "Usine",
            4: "Eglise"
            }
        self.buying_prices = {1:(-10,-50),2: (-50,-20),3:(-20,-20), 4:(-40,-20)}
        self.a = 1
        for i in arg:
            setattr(self, ("image_" + self.buying_name[self.a]),pygame.transform.scale(i,(int(bg.w / 8), int(bg.w / 8))))
            self.a += 1
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
                win.blit(self.image_Maison, (0, self.tabs[0].h))
                win.blit(self.image_Maison2, (int(w / 8), self.tabs[0].h))
                win.blit(self.image_Eglise, (0, int(self.tabs[0].h + w / 8)))
                win.blit(self.image_Usine, (int(w / 8), int(self.tabs[0].h + w / 8)))
                win.blit(self.image_Maison, (0, self.tabs[0].h + w / 4))
                win.blit(self.image_Maison2, (int(w / 8), self.tabs[0].h + w / 4))
                win.blit(self.image_Eglise, (0, int(self.tabs[0].h + 3 * w / 8)))
                win.blit(self.image_Usine, (int(w / 8), int(self.tabs[0].h + 3 * w / 8)))
                pygame.draw.rect(win, (150, 150, 150), self.tabs[0])
                pygame.draw.rect(win, (160, 160, 160), self.tabs[1])
                pygame.draw.rect(win, (150, 150, 150), self.tabs[2])
                font = pygame.font.SysFont("arial", round(w / 85))
                for i in range(3):
                    text = font.render(self.bg.l.vocab[i+4], True, pygame.Color('black'))
                    text_rect = text.get_rect()
                    text_rect.center = (i * w / 12 + w / 24), h / 28
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

    def open(self,win):
        for i in range (1,51):
            rect = pygame.rect.Rect(0,0,round(self.bg.w/200*i),self.bg.h)
            print(rect)
            pygame.draw.rect(win,(150,150,150),rect)
    def check_collision_tabs(self,tab_nmbr,pos):
        p = self.bg.prop_h
        if pos[1] <= p * (35 + 270 * tab_nmbr) and pos[1] <= pos[0] :
            return False
        elif pos[1] >= p * (235 + 270 * tab_nmbr) and pos[1] - 235 * p >= 35 * p - pos[0]:
           return False
        else: return tab_nmbr + 1