import random
import math
from PIL import Image, ImageDraw

# Display image
class PixelDisplay:
    gridcolor = (0, 0, 0)
    sky_color = (0, 222, 255)

    def __init__(self, sx, sy):
        self.image = None
        self.set_size(sx, sy)

    def set_size(self, sx, sy):
        self.image = Image.new("RGB", (sx * 10, sy * 10), color=PixelDisplay.gridcolor)

        for x in range(0, sx):
            for y in range(0, sy):
                self.draw_pixel(x, y, PixelDisplay.sky_color, False)

    def draw_pixel(self, x, y, color, on=True):
        draw = ImageDraw.Draw(self.image)
        draw.rectangle((x * 10, y * 10, x * 10 + 8, y * 10 + 8), color if on else PixelDisplay.sky_color)

    def display(self):
        transposed = self.image.transpose(method=Image.FLIP_TOP_BOTTOM)
        transposed.show()

# Constants
X = 2000
Y = 150
num_trees = math.floor(X/10)
house_distance = 10
y = 60 # Starting y pos

# Initialize screen
screen = PixelDisplay(X, Y)

# Colors
green = (0, 255, 0)
brown = (76, 45, 28)
blue = (68, 85, 90)
light_brown = (245, 222, 179)
door_brown = (139, 69, 19)

# Draw house
def draw_house(x, y):
    # Draw the base
    for width in range(5):
        screen.draw_pixel(x+width, y, green)
        for height in range(4):
            screen.draw_pixel(x+width, y+height+1, light_brown)
        for y0 in range(y):
            screen.draw_pixel(x+width, y0, brown)
        if width == 2:
            screen.draw_pixel(x+width, y+1, door_brown)
            screen.draw_pixel(x+width, y+2, door_brown)

    # Draw the roof
    roof = -3
    for width in range(-1, 3):
        screen.draw_pixel(x+width, y+ 7 + roof, door_brown)
        roof += 1
    for width in range(-1, 3):
        screen.draw_pixel(x+width+3, y+ 8 - roof, door_brown)
        roof += 1
    for inside_x in range(1, 4):
        screen.draw_pixel(x+inside_x, y+5, door_brown)
        screen.draw_pixel(x+inside_x, y+6, door_brown)

# Draw tree
def draw_tree(x, y):
    # Draw the trunk
    height = random.randint(5, 8)
    for h in range(height):
        screen.draw_pixel(x, y+h, brown)
    # Draw the leaves
    screen.draw_pixel(x+1, height+y, green)
    screen.draw_pixel(x-1, height+y, green)
    screen.draw_pixel(x, height+y, green)
    screen.draw_pixel(x, height+y+1, green)

# Generate probability distribution array
probabilities = [20, 20, 20, 1] # [up, down, horizontal, house]
cases = []
i = 0
for p in probabilities:
    i+=1
    for n in range(p):
        cases.append(i)

# Variables
tree_count = 0
last_tree = 0
house_x_count = 0
last_house = 0

# Generate the terrain
for x in range(X):
    if house_x_count != 0:
        house_x_count -= 1
        pass
    else:
        # Choose random direction
        r = random.randint(0, len(cases)-1)
        case = cases[r]

        # Up, down, straight or house, according to probability
        if case == 1:
            # Up
            y += 1
            screen.draw_pixel(x, y, green)
            for y0 in range(y):
                screen.draw_pixel(x, y0, brown)
        elif case == 2:
            # Down
            y -= 1
            screen.draw_pixel(x, y, green)
            for y0 in range(y):
                screen.draw_pixel(x, y0, brown)
        elif case == 3:
            # Straight
            screen.draw_pixel(x, y, green)
            for y0 in range(y):
                screen.draw_pixel(x, y0, brown)
        house_dx = abs(x - last_house)
        if case == 4:
            # House
            if house_dx > 20:
                last_house = x
                draw_house(x, y)
                house_x_count += 4
            else:
                screen.draw_pixel(x, y, green)
                for y0 in range(y):
                    screen.draw_pixel(x, y0, brown)
        # Create tree
        t = random.randint(1, 10) # Probability
        tree_dx = abs(x-last_tree) 
        if y > 0 and tree_count < num_trees + 1 and t > 9 and tree_dx > 10 and house_dx > 20:
            last_tree = x
            tree_count += 1
            draw_tree(x+1, y)

screen.display()