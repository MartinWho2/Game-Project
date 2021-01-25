import pygame
import math


# Create a subclass for all sprites
class Images(pygame.sprite.Sprite):
    def __init__(self, image, gap_x, gap_y, bg):
        super().__init__()
        self.bg = bg
        self.image = image
        self.original_image = image
        self.rect = self.image.get_rect()
        self.gap_x = gap_x
        self.gap_y = gap_y

    # Function to place them correctly if you moved the screen
    def replace(self):
        self.image = pygame.transform.scale(self.original_image, (
            math.floor(self.original_image.get_width() * self.bg.zoom),
            math.floor(self.original_image.get_height() * self.bg.zoom)))
        self.rect=self.image.get_rect()
        self.rect.x = math.floor(self.bg.x + self.bg.zoom * self.gap_x)
        self.rect.y = math.floor(self.bg.y + self.bg.zoom * self.gap_y)
