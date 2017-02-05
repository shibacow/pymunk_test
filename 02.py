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
    space.gravity = (0.0,-900.0)
    return screen,clock,space

def add_ball(space):
    mass=1
    radius=14
    inetia = pymunk.moment_for_circle(mass,0,radius,(0,0))
    body = pymunk.Body(mass,inetia)
    x = random.randint(120,380)
    body.position = x,550
    shape = pymunk.Circle(body,radius,(0,0))
    space.add(body,shape)
    return shape

def add_L(space):
    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position=(300,300)
    rotation_limit_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_limit_body.position=(200,300)
    body = pymunk.Body(10,10000)
    body.position = (300,300)
    l1 = pymunk.Segment(body, (-150, 0), (200.0, 0.0), 1)
    l2 = pymunk.Segment(body, (-150.0, 0), (-150.0, 50.0), 5)

    rotation_center_joint = pymunk.PinJoint(body,rotation_center_body,(0,0),(0,0))
    joint_limit = 25
    rotation_limit_joint = pymunk.SlideJoint(body,rotation_limit_body,(-100,0),(0,0),0,joint_limit)
    space.add(l1,l2,body,rotation_center_joint,rotation_limit_joint)
    return l1,l2

def main():
    (screen,clock,space) = init()
    lines = add_L(space)
    balls = []
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    print(draw_options)

    ticks_to_next_ball = 10
    running=True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)
        ticks_to_next_ball -= 1
        if ticks_to_next_ball <=0:
            ticks_to_next_ball = 25
            ball_shape = add_ball(space)
            balls.append(ball_shape)

        balls_to_remove = []
        for ball in balls:
            if ball.body.position.y < 150:
                balls_to_remove.append(ball)
        for ball in balls_to_remove:
            space.remove(ball,ball.body)
            balls.remove(ball)
        space.step(1/50.0)
        screen.fill((255,255,255))
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(50)


if __name__=='__main__':
    sys.exit(main())
