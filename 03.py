#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys,random
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util

def init():
    pygame.init()
    screen=pygame.display.set_mode((600,600))
    pygame.display.set_caption("Joints.Just wait ant the L will tips over")
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = (0.0,0.0)
    return screen,clock,space

def add_ball(space):
    mass=100
    radius=14
    inetia = pymunk.moment_for_circle(mass,0,radius,(0,0))
    body = pymunk.Body(mass,inetia)
    x = random.randint(120,380)
    body.position = x,550
    shape = pymunk.Circle(body,radius,(0,0))
    space.add(body,shape)
    return shape

def add_joint(space,a,b):
    rl = a.position.get_distance(b.position) * 0.9
    stiffness = 500.
    damping=10
    j = pymunk.DampedSpring(a, b, (0,0), (0,0), rl, stiffness, damping)
    j.max_bias=100
    space.add(j)
    #rest_angle=0
    #j2 = pymunk.constraint.RotaryLimitJoint(a,b, 0.0,0.0)
    #space.add(j2)
def main():
    (screen,clock,space) = init()
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    print(draw_options)
    add_ball(space)
    add_ball(space)
    add_ball(space)
    add_ball(space)
    add_ball(space)
    add_ball(space)
    bodies=space.bodies
    bodies=sorted(bodies,key=lambda x:x.position.x,reverse=True)
    for i,a in enumerate(bodies):
        if i+1<len(bodies):
            b=bodies[i+1]
            add_joint(space,a,b)
    running=True
    is_interactive = False
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)
            elif event.type ==  MOUSEBUTTONDOWN and not is_interactive:
                is_interactive = True
            elif event.type == MOUSEBUTTONUP:
                is_interactive = False
        if is_interactive:
            mouse_pos = pymunk.pygame_util.get_mouse_pos(screen)
            bd = space.point_query_nearest(mouse_pos, 10, pymunk.ShapeFilter())
            if bd:
                bd.shape.body.position=mouse_pos
        space.step(1/50.0)
        screen.fill((255,255,255))
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(50)


if __name__=='__main__':
    sys.exit(main())
