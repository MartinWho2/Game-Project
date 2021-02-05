import pygame
import math


class Jauge:
    def __init__(self, image, y, amount, h, w):
        #définit l'image de la jauge, ses coordonnées, sa quantité, le texte de l'affichage de sa quantité
        self.image = image
        self.image = pygame.transform.scale(self.image, (math.floor(w / 50), math.floor(h / 25)))
        self.rect = self.image.get_rect()
        self.quantity = amount
        self.rect.x = round(w - self.rect.w - w / 200)
        self.rect.y = w * (y * 50 - 30) / 1920
        self.font = pygame.font.SysFont('comicsans', round(w / 50))
        self.text = self.font.render(str(amount), True, pygame.Color(255, 255, 255))
        self.rectText = self.text.get_rect()
        self.rectText.x = self.rect.x - self.text.get_width()-10
        self.rectText.top = self.rect.y + 0.25 * math.floor(h / 25)
#fonction pour ajouter ou enlever une certaine quantité  
    def add(self, amount, w):
        self.quantity += amount
        self.text = self.font.render(str(self.quantity), True, pygame.Color(255, 255, 255))
        self.rectText.x = self.rect.x - self.text.get_width()-10
#affiche la jauge
    def display(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))
        win.blit(self.text, self.rectText)
