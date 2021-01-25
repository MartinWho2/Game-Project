import pygame, math

# Class for the background
class Background:
    def __init__(self, screen,language):
        self.image = pygame.image.load("Images/Maison 3.png")
        #self.image= pygame.transform.scale(self.image, (25, 25))
        self.x = 0
        self.y = 0
        self.zoom = 1
        self.h = screen.get_height()
        self.w = screen.get_width()
        self.factor = (self.h + self.w) / 600
        self.l = language