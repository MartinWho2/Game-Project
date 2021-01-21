import pygame
import math

class Menu:
    def __init__(self,bg):
        self.bg = bg
        self.event_happens = True
        self.font_0 = pygame.font.SysFont('comicsans',int(self.bg.w/9))
        self.font_1 = pygame.font.SysFont('comicsans',int(self.bg.w/10))
        self.font_2 = pygame.font.SysFont('comicsans',int(self.bg.w/10))
        self.color_0 = (0,255,0)
        self.color_1 = (255,255,255)
        self.color_2 = (255,255,255)
        self.selected = 0
        self.clicked = 0

        self.resume = self.font_1.render("Continue", True, self.color_0)
        self.save = self.font_1.render("Save / Load", True, self.color_1)
        self.quit = self.font_1.render("Quit", True, self.color_2)

        self.resumeRect = self.resume.get_rect()
        self.saveRect = self.save.get_rect()
        self.quitRect = self.quit.get_rect()
        self.rects = [self.resumeRect,self.saveRect,self.quitRect]

        self.resumeRect.center = (int(self.bg.w / 2), int(self.bg.h * 2 / 7))
        self.saveRect.center = (int(self.bg.w / 2), int(self.bg.h / 2))
        self.quitRect.center = (int(self.bg.w / 2), int(self.bg.h * 5 / 7))

    def menu(self):
        if self.event_happens:
            self.resume = self.font_0.render("Continue",True,self.color_0)
            self.save = self.font_1.render("Save / Load", True, self.color_1)
            self.quit = self.font_2.render("Quit", True, self.color_2)

            self.resumeRect = self.resume.get_rect()
            self.saveRect = self.save.get_rect()
            self.quitRect = self.quit.get_rect()
            self.rects = [self.resumeRect, self.saveRect, self.quitRect]

            self.resumeRect.center = (int(self.bg.w / 2), int(self.bg.h * 2 / 7))
            self.saveRect.center = (int(self.bg.w / 2), int(self.bg.h / 2))
            self.quitRect.center = (int(self.bg.w / 2), int(self.bg.h * 5 / 7))

            self.event_happens = False


