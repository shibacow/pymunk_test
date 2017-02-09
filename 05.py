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
import json

def init():
    pygame.init()
    screen=pygame.display.set_mode((600,600))
    pygame.display.set_caption("Joints.Just wait ant the L will tips over")
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = (0.0,0.0)
    return screen,clock,space



def up_position(body,dt):
    print("body={} dt={}".format(body,dt))
def get_resource(space):
    o=json.load(open('out.json'))
    maxx=10
    radius=14
    #inetia = pymunk.moment_for_segment(maxx,0,radius,(0,0))
    #body = pymunk.Body(mass,0,body_type=pymunk.Body.DYNAMIC)
    body = pymunk.Body(10,10000)
    #pa=pymunk.autogeometry.PolylineSet()
    #body=pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position=(300,300)
    body.velocity=vec2d.Vec2d(-100.0,0.0)
    body.update_position=up_position
    vec=[(float(x['x']),float(x['y'])) for x in o]
    poly = pymunk.Poly(body,vec)
    space.add(poly,body)
    #for i,k in enumerate(o[:-1]):
    #    p1=k
    #    p2=o[i+1]
     #   x1=float(p1['x'])
     #   y1=float(p1['y'])
     #   x2=float(p2['x'])
     #   y2=float(p2['y'])
        #pa.collect_segment((x1,y1),(x2,y2))
        #l=pymunk.Segment(body,(x1,y1),(x2,y2),1)
        #space.add(l)
        #print("i={} k={}".format(i,k))
    return poly
def add_ball(space,x):
    mass=10
    radius=14
    inetia = pymunk.moment_for_circle(mass,0,radius,(0,0))
    body = pymunk.Body(mass,inetia)
    #x = random.randint(120,380)
    body.position = x,350
    #body.torque = 5000
    shape = pymunk.Circle(body,radius,(0,0))
    space.add(body,shape)
    return shape
def static_ball(space,b):
    def mk_static_body(b,x,y):
        static_body = pymunk.Body(body_type = pymunk.Body.STATIC)
        static_body.position = vec2d.Vec2d(x,y)
        l = static_body.position.get_distance(b.position) * 0.9
        damping=15
        stiffness=20
        j = pymunk.DampedSpring(static_body, b, (0,0), (0,0), l,stiffness,damping)
        space.add(j)
    x=b.position.x
    y=b.position.y-200
    mk_static_body(b,x,y)
    y2=b.position.y+200
    mk_static_body(b,x,y2)

    #static_body.position
    #j = pymunk.PivotJoint(static_body, b, static_body.position)


def add_joint(space,a,b):
    j3 = pymunk.constraint.PinJoint(a,b,(0,0),(0,0))
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

def move_it(space,x):
    for b in space.bodies:
        b.position.x=b.position.x-x
    #for s in space.shapes:
        #s.position.x=s.position.x-x
        #print("shape={}".format(s))


def main():
    (screen,clock,space) = init()
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    add_ball(space,400)
    add_ball(space,350)
    add_ball(space,300)
    add_ball(space,250)
    add_ball(space,200)
    add_ball(space,150)
    add_ball(space,100)


    bodies=space.bodies
    bodies=sorted(bodies,key=lambda x:x.position.x,reverse=True)
    for i,a in enumerate(bodies):
        if i+1<len(bodies):
            b=bodies[i+1]
            add_joint(space,a,b)
    for a in bodies:
        static_ball(space,a)
    running=True
    is_interactive = False
    constraints = space.constraints
    back_recouce=get_resource(space)
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
        #back_recouce.position.x=back_recouce.position.x - 10.0
        #ax=back_recouce.position.x
        #ay=back_recouce.position.y
        #back_recouce.position.x=ax-100
        #print("ax={} ay={}".format(ax,ay))
        move_it(space,10)
        space.step(1/50.0)
        screen.fill((255,255,255))
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(50)


if __name__=='__main__':
    sys.exit(main())
