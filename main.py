import pygame
from game import Game

pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

game = Game(win)


def main():

    while game.run:
        clock.tick(60)
        game.update()
        pygame.display.flip()
        game.events()


main()
