import pygame
import random
from images import Images


class Building(Images):
    def __init__(self, image, gap_x, gap_y, bg, genre):
        super().__init__(image, gap_x, gap_y, bg)
        # Type de bâtiment

        self.dict_type = {'Caserne': 'A', 'Tank_factory': 'B', 'Centrale_electrique': 'C', 'Hopital': 'D',
                          'Repos': 'E', 'Plane_factory': 'F', 'Usine': 'G', 'Laboratoire': 'H', 'Tour': 'I',
                          'Radio': 'J','Mur': 'K','Tranchee': 'L', 'Barbele': 'M','Mine': 'N', 'Route': 'O',
                          'Immeuble': 'P', 'Immeuble_2': 'Q','Immeuble_3': 'R', 'Townhall': 'S',
                          'Eglise': 'T', 'Banque': 'U', 'Maison': 'V', 'Maison2': 'W','Maison_3': 'X'}
        self.type = (self.dict_type[genre], 100, 100)
        print(self.type)
        # Ouvert ou non
        self.bool_interface = False
        # Définit la surface de l'interface
        self.interface = pygame.Surface((round(self.bg.w / 8), round(self.bg.h / 3)))
        self.interface.set_alpha(120)
        self.interface.fill((150,150,150))
        # Croix pour fermer
        self.croix = pygame.Surface((round(self.bg.w / 30), round(self.bg.w / 30)))
        self.croix.fill((255, 0, 0))
        self.font = pygame.font.SysFont(None, round(self.bg.w / 20))
        self.x = self.font.render('x', True, pygame.Color('white'))
        self.x_x = round((round(self.bg.w / 30) - self.x.get_width()) / 2) + (round(self.bg.w * 7 / 8))
        self.x_y = round((round(self.bg.w / 30) - self.x.get_height()) / 2) + round(self.bg.h * 2 / 3)

    def open_interface(self):
        self.bool_interface = True

    def update_interface(self, win):
        win.blit(self.interface, (round(self.bg.w * 7 / 8), round(self.bg.h * 2 / 3)))
        win.blit(self.croix, (round(self.bg.w * 7 / 8), round(self.bg.h * 2 / 3)))
        win.blit(self.x, (self.x_x, self.x_y))
