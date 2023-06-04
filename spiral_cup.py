import rhinoscriptsyntax as rs
import Rhino.Geometry as geom
import math
import extruder_turtle
from extruder_turtle import *

# to do
# - vary spacing between bumps (every bump, second bump, fourth, etc)
# - dynamically scale the number of bumps

t = ExtruderTurtle() # print lines

def square(layer_height, radius, bump_height, bump_width, offset):
    v = 1
    for k in range (0, layer_height):
        i = 0
        while i < 360:
            x = radius * math.cos(math.radians(i))
            y = radius * math.sin(math.radians(i))
            t.set_position(x, y)
            t.lift(0.01)
            if i==v:
                # make a bump
                t.right(90)
                t.forward(bump_height)
                t.left(90)
                r_prime = radius + bump_height
                for j in range (0, bump_width):
                    x = r_prime * math.cos(math.radians(i+j))
                    y = r_prime * math.sin(math.radians(i+j))
                    t.set_position(x, y)
                i += bump_width - 1
                t.left(90)
                t.forward(bump_height)
                t.right(90)
                continue
            i += 1  
            
        v += offset

def triangle(layer_height, radius, bump_height, bump_width, offset):
    v = 1
    for k in range (0, layer_height):
        i = 0
        while i < 360:
            x = radius * math.cos(math.radians(i))
            y = radius * math.sin(math.radians(i))
            t.set_position(x, y)
            t.lift(0.01)
            if i==v:
                # make a bump
                t.right(60)
                t.forward(bump_height)
                t.left(120)
                t.forward(bump_height)
                t.right(120)
                i += bump_width - 1
                continue
            i += 1
        v += offset

# def bump(layer_height, radius, bump_height, bump_width, offset, shape_type):
#     if shape_type == 0:
#         square(layer_height, radius, bump_height, bump_width, offset)
#     elif shape_type == 1:
#         triangle(layer_height, radius, bump_height, bump_width, offset)
#     elif shape_type == 2:
#         loop(layer_height, radius, bump_height, bump_width, offset)
#     else:
#         print(f'Invalid shape_type: {shape_type}')

def loop(layer_height, radius, bump_height, bump_width, offset):
    v = 1
    for k in range (0, layer_height):
        i = 0
        while i < 360:
            x = radius * math.cos(math.radians(i))
            y = radius * math.sin(math.radians(i))
            t.set_position(x, y)
            t.lift(0.01)
            if i==v:
                # make a bump
                t.right(45)
                t.forward(math.sqrt(2) * bump_height)
                t.right(90)               
                r_prime = radius + bump_height
                for j in range (0, bump_width):
                    x = r_prime * math.cos(math.radians(i-j))
                    y = r_prime * math.sin(math.radians(i-j))
                    t.set_position(x, y)
                i += bump_width + 1
                t.right(135)
                t.forward(math.sqrt(2) * bump_height)
                t.right(90)
                continue
            i += 1  
            
        v += offset    
            
lines = t.get_lines()
# turtle = t.draw_turtle()