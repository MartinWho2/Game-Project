import pygame
import math


# Create a subclass for all sprites
class Images(pygame.sprite.Sprite):
    def __init__(self, image, gap_x, gap_y, bg, immobile=True):
        super().__init__()
        #importe le background, définit l'image du sprite, ses coordonnées
        self.bg = bg
        self.image = image
        self.original_image = image
        self.width = self.original_image.get_width()
        self.height = self.original_image.get_height()
        self.immobile = immobile
        self.rect = self.image.get_rect()
        # Distance x et y entre l'image et le bg afin de la replacer correctement
        self.gap_x = gap_x
        self.gap_y = gap_y

    # Function to place them correctly if you moved the screen
    def replace(self):
        # modifie la taille de l'image en fonction du zoom
        self.image = pygame.transform.scale(self.original_image, (
            round(self.width * self.bg.zoom),
            round(self.height * self.bg.zoom)))
        # redéfinit ses coordonnées en fonction du zoom
        self.rect = self.image.get_rect()
        self.rect.x = round(self.bg.x + self.bg.zoom * self.gap_x)
        self.rect.y = round(self.bg.y + self.bg.zoom * self.gap_y)

    def move(self):
        if not self.immobile:
            vector = pygame.math.Vector2()
            vector.xy = self.gap_x, self.gap_y
            if vector.length_squared() <=2:
                return "REMOVE"
            vector.scale_to_length(round(1/self.bg.zoom))
            print(f"[VECTOR] The vector is {vector.x, vector.y}; The zoom factor is {self.bg.zoom}")
            self.gap_x, self.gap_y = (self.rect.x - vector.x - self.bg.x) / self.bg.zoom, (self.rect.y - vector.y - self.bg.y) / self.bg.zoom
