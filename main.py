import pygame
from game import Game

pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

game = Game(win)

def main():

    while game.run:
        clock.tick(60)
        if not game.pause:
            game.update()
            pygame.display.flip()
            game.events()
        else:
            if not game.s_l:
                game.menu.menu()
                pygame.display.flip()
                game.menu_events()
            else:
                game.save_load()
                pygame.display.flip()
                game.save_load_events()

main()
