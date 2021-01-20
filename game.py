import pygame
import math
from shop import Shop
from Langues import Language
from jauge import Jauge
from images import Images
from background import Background
from Menu import Menu
from Encode import encode, decode
class Game:
    def __init__(self, win):
        self.bg = Background(win, Language())
        self.menu = Menu(self.bg)
        self.shop_open = False
        self.shop = Shop(self.bg)
        self.group = pygame.sprite.Group()
        self.gold = Jauge(pygame.image.load('Images/Pièce.png'), 1, 100, self.bg.h, self.bg.w)
        self.stuff = Jauge(pygame.image.load('Images/Matériel.png'), 2, 50000000, self.bg.h, self.bg.w)
        self.keys = {}
        self.win = win

        self.run = True
        self.pause = False
        self.s_l = False
        self.s_l_choice = False

        self.buttons = (0, 0, 0)
        self.font_1 = pygame.font.SysFont('comicsans',int(self.bg.w/10))

        self.white = (255,255,255)
        self.green = (0,255,0)
        self.blue = (0,0,255)
        self.red = (255,0,0)

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

    def save_load(self):
        self.win.fill(self.red)
        pygame.draw.rect(self.win, self.blue, pygame.Rect(0, 0, int(self.bg.w/2), self.bg.h))
        save = self.menu.font.render("SAVE", True, (0, 0, 0))
        load = self.menu.font.render("LOAD", True, (0, 0, 0))
        saveRect, loadRect = save.get_rect(), load.get_rect()
        saveRect.center, loadRect.center = (int(self.bg.w/4),int(self.bg.h/2)),(int(self.bg.w * 3 / 4),int(self.bg.h/2))
        self.win.blit(save, saveRect)
        self.win.blit(load, loadRect)

    def save_load_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.run = False
                pygame.quit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                x = pygame.mouse.get_pos()[0]
                # False to save and True to load
                if x < self.bg.w/2:
                    self.s_l_choice = False
                else:
                    self.s_l_choice = True
            if e.type == pygame.MOUSEBUTTONUP:
                x = pygame.mouse.get_pos()[0]
                if self.s_l_choice and x > self.bg.w/2:
                    self.gold.quantity = int(decode())
                    self.gold.add(0,self.bg.w)
                    self.s_l = False
                    self.win.fill((0,0,0))
                elif not self.s_l_choice and x < self.bg.w/2:
                    encode(str(self.gold.quantity))
                    self.s_l = False
                    self.win.fill((0,0,0))
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.s_l = False




    def menu_events(self):
        self.win.blit(self.menu.resume, self.menu.resumeRect)
        self.win.blit(self.menu.save, self.menu.saveRect)
        self.win.blit(self.menu.quit, self.menu.quitRect)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.run = False
                pygame.quit()
            if e.type == pygame.MOUSEMOTION:
                if not self.menu.clicked:
                    x, y = pygame.mouse.get_pos()
                    for rectangle in self.menu.rects:
                        if rectangle.collidepoint(x, y):
                            self.menu.selected = self.menu.rects.index(rectangle)
                            setattr(self.menu, 'color_' + str(self.menu.selected), self.green)
                            setattr(self.menu, 'color_' + str((self.menu.selected - 1) % 3), self.white)
                            setattr(self.menu, 'color_' + str((self.menu.selected - 2) % 3), self.white)
                            self.menu.event_happens = True

            if e.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if self.menu.rects[self.menu.selected].collidepoint(x,y):
                    self.menu.clicked = self.menu.selected+1
            if e.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                if self.menu.rects[self.menu.clicked-1].collidepoint(x, y):
                    if self.menu.clicked == 1:
                        self.pause = False
                    if self.menu.clicked == 2:
                        self.s_l = True
                    if self.menu.clicked == 3:
                        self.run = False
                        pygame.quit()
                self.menu.clicked = 0




    def events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.run = False
                pygame.quit()
            elif e.type == pygame.KEYDOWN:
                self.keys[e.key] = True
                if e.key == pygame.K_SPACE:
                    self.gold.add(1000, self.bg.w)
                if e.key == pygame.K_ESCAPE:
                    self.pause = True
                    self.win.fill((0,0,0))
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
