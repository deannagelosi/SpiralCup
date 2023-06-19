import rhinoscriptsyntax as rs
import Rhino.Geometry as geom
import math

# sources:
#  - https://dev.to/taarimalta/how-to-draw-a-spiral-with-python-turtle-2n5c

class SpiralCup:
    def __init__(self, t):
        self.t = t

    def bump(self, layer_height, radius, bump_height, bump_width, offset, shape_type):                
        bottom_lift = 1.6 # as of Friday 7/9, last tested on 1.2
        # print(bottom_lift)
        
        # Create spiral outwards and get its last position
        curr_x, curr_y = self.spiral_bottom(radius, self.t.get_extrude_width())
        self.t.lift(bottom_lift)
        # print(self.t.get_layer_height())

        # Offset for the second layer
        self.t.left(90)
        radial_offset = self.t.get_extrude_width() / 2
        self.t.forward(radial_offset)
        # self.t.left(90)

        # Calculate offset angle for the second layer
        increment_angle = -1  # change direction of spiral
        extrude_width = self.t.get_extrude_width()
        curr_x, curr_y = self.spiral_bottom(radius - radial_offset, extrude_width, increment_angle, 0)
        self.t.lift(bottom_lift)

        # Third pass similar to first pass, spiraling outwards
        increment_angle = 1
        curr_x, curr_y = self.spiral_bottom(radius, self.t.get_extrude_width(), increment_angle)

        # Set the position to the last position of the spiral
        self.t.set_position(x = curr_x, y = curr_y)

        shape_object = None
        if shape_type == "Triangle":
            shape_object = Triangle(self.t, bump_height, bump_width)
        elif shape_type == "Loop":
            shape_object = Loop(self.t, bump_height, bump_width, radius)
        elif shape_type == "Square":
            shape_object = Square(self.t, bump_height, bump_width, radius)
        else:
            raise ValueError("Invalid shape_type: " + shape_type)

        self.spiral(radius, shape_object, offset, layer_height)

    def spiral_bottom(self, radius, extrude_width, increment_angle=1, start_angle=0):
        angle = start_angle
        total_rotations = radius / extrude_width  # total rotations in the spiral

        # If spiraling inwards
        if increment_angle < 0:  
            x = radius
            y = 0
        else:  # spiraling outwards
            x = 0
            y = 0

        max_angle_position_reached = False
        min_angle_position_reached = False

        while not (max_angle_position_reached or min_angle_position_reached):
            # Continue with the spiral
            curr_radius = abs(angle) * extrude_width / 360  # current radius based on angle

            # For spiraling inwards, reduce the radius as angle increases
            if increment_angle < 0:
                curr_radius = radius - curr_radius

            x = curr_radius * math.cos(math.radians(angle))
            y = curr_radius * math.sin(math.radians(angle))
            self.t.set_position(x, y)

            max_angle_position_reached = increment_angle > 0 and x >= radius and y <= 0 and angle >= 360 * total_rotations
            min_angle_position_reached = increment_angle <= 0 and x <= 0 and y >= 0 and angle <= -360 * total_rotations
                
            angle += increment_angle

        return x, y

    def spiral(self, radius, shape_object, offset, layer_height):
        i = 0
        while i < 360 * layer_height:
            x = radius * math.cos(math.radians(i))
            y = radius * math.sin(math.radians(i))
            self.t.set_position(x, y)
            lift = self.t.get_layer_height() / 360.0
            self.t.lift(lift)
            if i % offset == 0:
                i += shape_object.generate(i)
            else:
                i += 1  
        return self.t

class Shape:
    def __init__(self, t, bump_height, bump_width):
        self.t = t
        self.bump_height = bump_height
        self.bump_width = bump_width

class Triangle(Shape):
    def __init__(self, t, bump_height, bump_width):
        Shape.__init__(self, t, bump_height, bump_width)
        
    def generate(self, i):
        self.t.right(60)
        self.t.forward(self.bump_height)
        self.t.left(120)
        self.t.forward(self.bump_height)
        self.t.right(120)

        return self.bump_width - 1

class Loop(Shape):
    def __init__(self, t, bump_height, bump_width, radius):
        Shape.__init__(self, t, bump_height, bump_width)
        self.radius = radius

    def generate(self, i):
        self.t.right(45)
        self.t.forward(math.sqrt(2) * self.bump_height)
        self.t.right(90)               
        r_prime = self.radius + self.bump_height
        for j in range (0, self.bump_width):
            x = r_prime * math.cos(math.radians(i-j))
            y = r_prime * math.sin(math.radians(i-j))
            self.t.set_position(x, y)
        self.t.right(135)
        self.t.forward(math.sqrt(2) * self.bump_height)
        self.t.right(90)

        return self.bump_width + 1
    
class Square(Shape):
    def __init__(self, t, bump_height, bump_width, radius):
        Shape.__init__(self, t, bump_height, bump_width)
        self.radius = radius
    
    def generate(self, i):
        self.t.right(90)
        self.t.forward(self.bump_height)
        self.t.left(90)
        r_prime = self.radius + self.bump_height
        for j in range (0, self.bump_width):
            x = r_prime * math.cos(math.radians(i+j))
            y = r_prime * math.sin(math.radians(i+j))
            self.t.set_position(x, y)
        self.t.left(90)
        self.t.forward(self.bump_height)
        self.t.right(90)

        return self.bump_width + 1