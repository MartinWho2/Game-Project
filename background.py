import pygame, math

# Class for the background
class Background:
    def __init__(self, screen,language,image):
        #définit les caractéristiques du background: son image, ses coordonnées, son zoom, sa hauteur, sa largeur, ses coefficients de proportionnalité en fonction de la taille de la fenêtre, son facteur de taille, son langage
        self.image = image
        self.x = 0
        self.y = 0
        self.zoom = 1
        self.h = screen.get_height()
        self.w = screen.get_width()
        self.prop_w = self.w / 1920
        self.prop_h = self.h / 1080
        self.factor = (self.h + self.w) / 600
        self.l = language