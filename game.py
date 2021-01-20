import pygame
import math
from shop import Shop
from Langues import Language
from jauge import Jauge
from images import Images
from background import Background


class Game:
    def __init__(self, win):
        self.bg = Background(win, Language())
        self.shop_open = False
        self.shop = Shop(self.bg)
        self.group = pygame.sprite.Group()
        self.gold = Jauge(pygame.image.load('Images/Pièce.png'), 1, 100000000, self.bg.h, self.bg.w)
        self.stuff = Jauge(pygame.image.load('Images/Matériel.png'), 2, 50000000, self.bg.h, self.bg.w)
        self.keys = {}
        self.win = win
        self.run = True
        self.buttons = (0, 0, 0)

    def update(self):
        self.buttons = pygame.mouse.get_pressed(num_buttons=3)
        # you can also move it with keys
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
        # move and display all sprites and background
        for sprite in self.group:
            sprite.replace()

        self.win.fill((0, 0, 0))
        self.win.blit(pygame.transform.scale(self.bg.image, (
            math.floor(self.bg.image.get_width() * self.bg.zoom),
            math.floor(self.bg.image.get_height() * self.bg.zoom))),
                      (math.floor(self.bg.x), math.floor(self.bg.y)))
        self.group.draw(self.win)
        self.stuff.display(self.win)
        self.gold.display(self.win)
        if self.shop_open:
            self.shop.draw_shop(self.win, self.bg.w, self.bg.h)

    def events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.run = False
                pygame.quit()
            elif e.type == pygame.KEYDOWN:
                self.keys[e.key] = True
                if e.key == pygame.K_SPACE:
                    self.stuff.add(1000, self.bg.w)
                if e.key == pygame.K_ESCAPE:
                    self.run = False
                    pygame.quit()
                if e.key == pygame.K_k:
                    self.shop_open = not self.shop_open
                    self.shop.buying = False
                if e.key == pygame.K_1:
                    self.bg.l.change_language(1, self.bg, self.shop)
                if e.key == pygame.K_2:
                    self.bg.l.change_language(2, self.bg, self.shop)
                if e.key == pygame.K_3:
                    self.bg.l.change_language(3, self.bg, self.shop)
            elif e.type == pygame.KEYUP:
                self.keys[e.key] = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    pos = pygame.mouse.get_pos()
                    egal = False
                    if self.shop.buying and self.gold.quantity + self.shop.prices["Maison"][
                        0] >= 0 and self.stuff.quantity + \
                            self.shop.prices["Maison"][1] >= 0:
                        surface = pygame.image.load('Images/Maison.png')
                        a = Images(surface, (self.shop.buying_x - self.bg.x) / self.bg.zoom,
                                   (self.shop.buying_y - self.bg.y) / self.bg.zoom, self.bg)
                        self.group.add(a)
                        self.gold.add(self.shop.prices["Maison"][0], self.bg.w)
                        self.stuff.add(self.shop.prices["Maison"][1], self.bg.w)
                        self.shop.buying = False
                        egal = True
                        self.shop.bought = 0
                        # print(self.shop.buying_x, self.shop.buying_y, self.bg.x / self.bg.zoom,
                        #      self.bg.y / self.bg.zoom)
                    if self.shop_open and not self.shop.buying and not egal:
                        for i in range(0, 4):
                            if self.shop.tabs[i].collidepoint(pos[0], pos[1]):
                                self.shop.tab_open = i
                        for i in range(0, 6):
                            if self.shop.rect_list[i].collidepoint(pos[0], pos[1]) and not self.shop.buying:
                                self.shop.buying = True

            elif e.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_rel()
                if self.buttons[0] and (self.shop_open is False or pygame.mouse.get_pos()[0] > self.bg.w / 4):
                    self.bg.x += mx
                    self.bg.y += my
            # function for zooming
            elif e.type == pygame.MOUSEWHEEL:
                rx, ry = pygame.mouse.get_pos()
                if self.shop_open is False or pygame.mouse.get_pos()[0] > self.bg.w / 4:
                    factor = e.y * 0.225 + 1.025
                    if not (self.bg.zoom > 3.5 and factor > 1) and not (self.bg.zoom < 0.2 and factor < 1):
                        self.bg.zoom = self.bg.zoom * factor
                        self.bg.x = rx + (self.bg.x - rx) * factor
                        self.bg.y = ry + (self.bg.y - ry) * factor
