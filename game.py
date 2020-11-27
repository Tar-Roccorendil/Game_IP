import pygame as pg
from pygame import mixer
import player as pl
import mapa as mp
import inimigo as ini

# initialize Pygame
pg.init()


#Música_de_Fundo
mixer.init()
mixer.music.load("song.mp3")
mixer.music.set_volume(0.7)
mixer.music.play()


# dimenções da janela
WINDOW_WIDTH = 672
WINDOW_HEIGHT = 672

# setup da tela
win = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("Unitled Wizard Game")

# setup icone da tela
icon = pg.image.load('images/wizard.png')
pg.display.set_icon(icon)

# cria o jogador no centro da tela
king = pl.player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 32, 32, win, WINDOW_WIDTH, WINDOW_HEIGHT)

# cria o mapa
mapa = mp.mapa(0, 0, win)

# cria lista que vai guardar todos inimigos
zombies = []



# roda o jogo
def main():
    ticks_last_frame = 0
    ticks_last_enemy = 0


    # mude para true para ver o fps
    show_fps = True
    if show_fps:
        font = pg.font.Font(None, 30)
        clock = pg.time.Clock()

    while True:
        # permite fechar a janela
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
        # fechar a janela apretando esc
        if pg.key.get_pressed()[pg.K_ESCAPE]:
            pg.quit()

        # Calcula delta time, usado pra fazer o movimento continuo
        t = pg.time.get_ticks()
        dt = (t - ticks_last_frame)
        ticks_last_frame = t

        # responsavel por spawnar os inimigos
        dt_enemy = t - ticks_last_enemy
        if dt_enemy > 1000:
            zombies.append(ini.inimigo(0, WINDOW_HEIGHT // 2, 32, 32, win, WINDOW_WIDTH, WINDOW_HEIGHT))
            ticks_last_enemy = t

        # update o jogador e as balas
        king.update(dt, mapa)

        for bullet in king.bullets:
            killed = bullet.check_enemy(zombies)
            if killed != -1:
                zombies.pop(zombies.index(killed))
        
        # king.check_enemy(zombies)
                
        # update do inimigo
        for zombie in zombies:
            zombie.update(king.x, king.y, dt, mapa)

        # desenha tudo 
        draw_all()

        # mostra o fps do jogo
        if show_fps:
            fps = font.render(str(int(clock.get_fps())), True, pg.Color('White'))
            win.blit(fps, (50, 50))
            pg.display.flip()
            clock.tick(120)

        # update diplay
        pg.display.update()


#  desenha tudo
def draw_all():
    # desenha o mapa
    mapa.draw()

    #desenhar inimigos
    for zombie in zombies:
        zombie.draw()

    # desenha o jogador e as suas balas 
    king.draw()

    # faz update da tela
    pg.display.update()


main()
