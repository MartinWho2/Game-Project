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
        self.rect_1 = pygame.rect.Rect(0, self.tabs[0].h, bg.w / 8, bg.w / 8)
        self.rect_4 = pygame.rect.Rect(bg.w / 8, self.tabs[0].h + 2 * 1 * bg.w / 8 + bg.w / 8, bg.w / 8, bg.w / 8)
        self.rect_3 = pygame.rect.Rect(0, self.tabs[0].h + 2 * 1 * bg.w / 8, bg.w / 8, bg.w / 8)
        self.rect_6 = pygame.rect.Rect(bg.w / 8, self.tabs[0].h + 2 * 2 * bg.w / 8 + bg.w / 8, bg.w / 8, bg.w / 8)
        self.rect_5 = pygame.rect.Rect(0, self.tabs[0].h + 2 * 2 * bg.w / 8, bg.w / 8, bg.w / 8)
        self.rect_2 = pygame.rect.Rect(bg.w / 8, self.tabs[0].h + bg.w / 8, bg.w / 8, bg.w / 8)
        self.rect_list = [self.rect_1, self.rect_2, self.rect_3, self.rect_4, self.rect_5, self.rect_6]
        self.buying = False
        self.image_buying = (0, 0)
        self.bg = bg
        self.dict = {"Maison": (0, 0), "Tank Factory": (0, 1)}
        self.prices = {"Maison": (-10, -50)}

    def draw_shop(self, win, w, h):
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
                image_maison = pygame.transform.scale(pygame.image.load('Images/Maison.png'), (int(w / 8), int(w / 8)))
                win.blit(image_maison, (0, self.tabs[0].h))
                win.blit(image_maison, (int(w / 8), int(self.tabs[0].h + w / 8)))
                win.blit(image_maison, (0, int(self.tabs[0].h + 2 * w / 8)))
                win.blit(image_maison, (int(w / 8), int(self.tabs[0].h + 3 * w / 8)))
                win.blit(image_maison, (0, int(self.tabs[0].h + 4 * w / 8)))
                win.blit(image_maison, (int(w / 8), int(self.tabs[0].h + 5 * w / 8)))
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
            original_image = pygame.image.load("Images/Maison.png")
            image = pygame.transform.scale(original_image, (math.floor(original_image.get_width() * self.bg.zoom),
                                                            math.floor(original_image.get_height() * self.bg.zoom)))
            self.buying_x = round(
                (pygame.mouse.get_pos()[0] - image.get_width() / 2) / (25 * self.bg.zoom)) * 25 * self.bg.zoom + (
                                        (self.bg.x / (25 * self.bg.zoom)) % 1) * 25 * self.bg.zoom
            self.buying_y = round(
                (pygame.mouse.get_pos()[1] - image.get_height() / 2) / (25 * self.bg.zoom)) * 25 * self.bg.zoom + (
                                        (self.bg.y / (25 * self.bg.zoom)) % 1) * 25 * self.bg.zoom
            win.blit(image, (self.buying_x, self.buying_y))
