import rhinoscriptsyntax as rs
import Rhino.Geometry as geom
import math
from extruder_turtle import ExtruderTurtle

# Grasshopper Python Script Editor code
#
# import rhinoscriptsyntax as rs
# import sys
# import operator as op
# from spiral_cup import SpiralCup   # file

# to_delete = list()
# for module in sys.modules:
#     if "spiral_cup" in module:
#       to_delete.append(module)
# for module in to_delete:
#     sys.modules.pop(module)

# s = SpiralCup()

# lines = s.bump(layer_height, radius, bump_height, bump_width, offset, shape_type)

class SpiralCup:
    def __init__(self):
        self.t = ExtruderTurtle() # print lines

    def bump(self, layer_height, radius, bump_height, bump_width, offset, shape_type):
        if shape_type == "Square":
            lines = self.square(layer_height, radius, bump_height, bump_width, offset)
            return lines 
        elif shape_type == "Triangle":
            lines = self.triangle(layer_height, radius, bump_height, bump_width, offset)
            return lines 
        elif shape_type == "Loop":
            lines = self.loop(layer_height, radius, bump_height, bump_width, offset)
            return lines 
        else:
            print("Invalid shape_type: " + str(shape_type))

    def square(self, layer_height, radius, bump_height, bump_width, offset):
        v = 1
        for k in range (0, layer_height):
            i = 0
            while i < 360:
                x = radius * math.cos(math.radians(i))
                y = radius * math.sin(math.radians(i))
                self.t.set_position(x, y)
                self.t.lift(0.01)
                if i==v:
                    # make a bump
                    self.t.right(90)
                    self.t.forward(bump_height)
                    self.t.left(90)
                    r_prime = radius + bump_height
                    for j in range (0, bump_width):
                        x = r_prime * math.cos(math.radians(i+j))
                        y = r_prime * math.sin(math.radians(i+j))
                        self.t.set_position(x, y)
                    i += bump_width - 1
                    self.t.left(90)
                    self.t.forward(bump_height)
                    self.t.right(90)
                    continue
                i += 1  
                
            v += offset
        lines = self.t.get_lines()
        return lines
            
    def triangle(self, layer_height, radius, bump_height, bump_width, offset):
        v = 1
        for k in range (0, layer_height):
            i = 0
            while i < 360:
                x = radius * math.cos(math.radians(i))
                y = radius * math.sin(math.radians(i))
                self.t.set_position(x, y)
                self.t.lift(0.01)
                if i==v:
                    # make a bump
                    self.t.right(60)
                    self.t.forward(bump_height)
                    self.t.left(120)
                    self.t.forward(bump_height)
                    self.t.right(120)
                    i += bump_width - 1
                    continue
                i += 1
            v += offset
        lines = self.t.get_lines()
        return lines

    def loop(self, layer_height, radius, bump_height, bump_width, offset):
        v = 1
        for k in range (0, layer_height):
            i = 0
            while i < 360:
                x = radius * math.cos(math.radians(i))
                y = radius * math.sin(math.radians(i))
                self.t.set_position(x, y)
                self.t.lift(0.01)
                if i==v:
                    # make a bump
                    self.t.right(45)
                    self.t.forward(math.sqrt(2) * bump_height)
                    self.t.right(90)               
                    r_prime = radius + bump_height
                    for j in range (0, bump_width):
                        x = r_prime * math.cos(math.radians(i-j))
                        y = r_prime * math.sin(math.radians(i-j))
                        self.t.set_position(x, y)
                    i += bump_width + 1
                    self.t.right(135)
                    self.t.forward(math.sqrt(2) * bump_height)
                    self.t.right(90)
                    continue
                i += 1  
            v += offset
        lines = self.t.get_lines()
        return lines