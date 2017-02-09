#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys,random
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util
import math
import re
from pymunk import vec2d

def init():
    pygame.init()
    screen=pygame.display.set_mode((600,600))
    pygame.display.set_caption("Joints.Just wait ant the L will tips over")
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = (0.0,0.0)
    return screen,clock,space

def add_ball(space,x):
    mass=10
    radius=14
    inetia = pymunk.moment_for_circle(mass,0,radius,(0,0))
    body = pymunk.Body(mass,inetia)
    #x = random.randint(120,380)
    body.position = x,550
    body.torque = 5000
    shape = pymunk.Circle(body,radius,(0,0))
    space.add(body,shape)
    return shape

def add_joint(space,a,b):
    #l = a.position.get_distance(b.position) * 0.9
    #stiffness = 500.
    #damping=10
    #a0=10*math.pi/180.0
    #b0=3500*math.pi/180.0
    #print("a0={} b0={}".format(a0,b0))
    #j2 = pymunk.constraint.RotaryLimitJoint(a,b, b0,a0)
    #space.add(j2)

    #j = pymunk.DampedSpring(a, b, (0,0), (0,0), rl, stiffness, damping)
    #j.max_bias=100
    #space.add(j)
    #rest_angle=0
    #j2 = pymunk.constraint.RotaryLimitJoint(a,b, 1.0,100.0)
    #space.add(j2)
    #j3 = pymunk.constraint.PinJoint(a,b,(0,0),(0,0))
    #j3.collide_bodies=False
    #j3.max_force=1000
    #space.add(j3)
    #j = pymunk.constraint.DampedRotarySpring(a,b,0,100,100)
    #xdiff=a.position.x - b.position.x
    #print("xdiff={}".format(xdiff))
    #space.add(j)
    #pass
    #j4 = pymunk.constraint.SimpleMotor(a,b,0)
    #j4.collide_bodies=False
    #j4.max_force=1000
    #space.add(j4)
    l = a.position.get_distance(b.position) * 0.9
    stiffness = 500.
    damping=400.
    j3 = pymunk.constraint.DampedSpring(a,b,(0,0),(0,0),l,stiffness,damping)
    j3.collide_bodies=False
    j3.max_force=1000
    space.add(j3)


def show_binfo(i,b):
    for k in dir(b):
        if re.search("^[^_]",k):
            try:
                v=getattr(b,k)
                print("i={} k={} v={}".format(i,k,v))
            except AttributeError as err:
                print("k={} erro={}".format(k,err))
def show_const(i,c):
    for k in dir(c):
        if re.search("^[^_]",k):
            try:
                v=getattr(c,k)
                print("i={} k={} v={}".format(i,k,v))
            except AttributeError as err:
                print("k={} erro={}".format(k,err))

def show_v(i,b):
    av=b.angular_velocity
    print("i={} av={}".format(i,av))

def main():
    (screen,clock,space) = init()
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    add_ball(space,300)
    add_ball(space,200)
    add_ball(space,150)
    add_ball(space,100)

    bodies=space.bodies
    bodies=sorted(bodies,key=lambda x:x.position.x,reverse=True)
    for i,a in enumerate(bodies):
        if i+1<len(bodies):
            b=bodies[i+1]
            add_joint(space,a,b)
    running=True
    is_interactive = False
    constraints = space.constraints
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
        #for i,b in enumerate(bodies):
            #show_binfo(i,b)
         #   show_v(i,b)
       #for i,c in enumerate(constraints):
        #    show_const(i,c)
        space.step(1/50.0)
        screen.fill((255,255,255))
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(50)


if __name__=='__main__':
    sys.exit(main())
