"""Showcase what the output of pymunk.pygame_util draw methods will look like.

See pyglet_util_demo.py for a comparison to pyglet.
"""

__docformat__ = "reStructuredText"

import sys

import pygame
from pygame.locals import *

import pymunk
from pymunk.vec2d import Vec2d
import pymunk.pygame_util

import shapes_for_draw_demos

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000,700))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)

    space = pymunk.Space()
    captions = shapes_for_draw_demos.fill_space(space)


    options = pymunk.pygame_util.DrawOptions(screen)
    is_interactive = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or \
                event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):
                return
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(screen, "pygame_util_demo.png")
            elif event.type ==  MOUSEBUTTONDOWN and not is_interactive:
                is_interactive = True
            elif event.type == MOUSEBUTTONUP:
                is_interactive = False
        if is_interactive:
            mouse_pos = pymunk.pygame_util.get_mouse_pos(screen)
            bd = space.point_query_nearest(mouse_pos, 10, pymunk.ShapeFilter())
            if bd:
                print(bd)
                bd.shape.body.position=mouse_pos
        space.step(1/50.0)
        ### Draw it
        screen.fill(pygame.color.THECOLORS["white"])
        space.debug_draw(options)
    #pymunk.pygame_util.draw(screen, space)

    # Info
        color = pygame.color.THECOLORS["black"]
        screen.blit(font.render("Demo example of pygame_util.DrawOptions()", 1, color), (205, 680))
        for caption in captions:
            x, y = caption[0]
            y = 700 - y
            screen.blit(font.render(caption[1], 1, color), (x,y))
        pygame.display.flip()
        clock.tick(10)

if __name__ == '__main__':
    sys.exit(main())