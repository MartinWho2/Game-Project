import pygame
from game import Game

pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
game = Game(win)


# afficher les fps
def display_fps():
    "Data that will be rendered and blitted in display"
    font = pygame.font.SysFont(None ,(50))
    text = font.render(str(int(clock.get_fps())),True,(255,255,255))
    win.blit(text,(0,0))


def main():

    while game.run:
        clock.tick(60)
    # afficher le jeu
        if not game.pause:
            game.update()
            display_fps()
            pygame.display.flip()
            game.events()
            
        else:
            # afficher le menu du jeu
            if not game.s_l:
                game.menu.menu()
                pygame.display.flip()
                game.menu_events()
            else:
                # afficher le menu de sauvegarde
                game.save_load()
                pygame.display.flip()
                game.save_load_events()


main()
