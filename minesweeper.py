#########
# TO DO #
#########
"""
- When I click on "number", it clears if "number" amount of flags are in it's vicinity
- Make better bomb and flag icons
- Make X number of bombs per difficulty
    - Make an list of each coordinate (x, y)
    - For each bomb, pick a coordinate randomly from that list and place it there
- Make bottom bar with:
    - Bomb count
    - Timer
    - Game status text
        - Game over :(
    - Restart button
    - Menu button
- Menu screen
    - Pick between easy, medium, and hard
"""


###########
# IMPORTS #
###########
from pygame import * 
import random
import time as t
import math as m

#############
# GAME INFO #
#############
""" 
Legend for graphic_boxes
------------------------
0 = touched 0 bombs near
1 = touched 1 bomb near
2 = touched 2 bombs near
 = touched 3 bombs near
4 = touched 4 bombs near
5 = touched 5 bombs near
6 = touched 6 bombs near
7 = touched 7 bombs near
8 = touched 8 bombs near
9 = untouched
10 = bomb
11 = flag
"""

##############
# GAME SETUP #
##############
# Variables
num_bombs = 50
num_flags = 0

game_font_size = 27
menu_font_size = 40

box_size = 20
num_boxes = 25
border_width = 30
menu_height = 40

game_width = box_size*num_boxes + 1
game_height = box_size*num_boxes + 1
screen_width = game_width + border_width*2
screen_height = game_width + border_width*3 + menu_height

bomb_count_width = 70
timer_width = 70
game_status_width = game_width - border_width*2 - bomb_count_width - timer_width
# Game
init()
screen = display.set_mode((screen_width, screen_height))
clock = time.Clock()
running = True
start_time = t.time()
timer = m.floor(t.time() - start_time)
# Font
font.init()
game_font = font.SysFont("consolas.ttf", game_font_size)
menu_font = font.SysFont("consolas.ttf", menu_font_size)

box_colour = {
    0:"light grey", # Empty
    1:"light grey", # 1
    2:"light grey", # 2
    3:"light grey", # 3
    4:"light grey", # 4
    5:"light grey", # 5
    6:"light grey", # 6
    7:"light grey", # 7
    8:"light grey", # 8
    9:"dark grey",  # Untouched
    10:"dark red",  # Bomb
    11:"orange"     # Flag
}
text_colour = {
    0:"light grey", # Empty
    1:"blue",       # 1
    2:"dark green", # 2
    3:"red",        # 3
    4:"dark blue",  # 4
    5:"dark red",   # 5
    6:"teal",       # 6
    7:"black",      # 7
    8:"grey",       # 8
    9:"dark grey",  # Untouched
    10:"black",     # Bomb
    11:"white"      # Flag
}
icon = {
    0:"",   # Empty
    1:"1",  # 1
    2:"2",  # 2
    3:"3",  # 3
    4:"4",  # 4
    5:"5",  # 5
    6:"6",  # 6
    7:"7",  # 7
    8:"8",  # 8
    9:"",   # Untouched
    10:"X", # Bomb
    11:"!", # Flag
}

bombs = [] # bomb locations
# Create bomb list
for i in range(num_boxes):
    bombs.append([])
    for j in range(num_boxes):
        bombs[i].append(0)
possible_locations = []
# Create linear list of locations
for i in range(num_boxes):
    for j in range(num_boxes):
        possible_locations.append((i, j))
# Select bomb locations
for i in range(num_bombs):
    index = random.randrange(len(possible_locations))
    coord = possible_locations.pop(index)
    bombs[coord[0]][coord[1]] = 1

graphic_boxes = [] # graphics
for i in range(num_boxes):
    graphic_boxes.append([])
    for j in range(num_boxes):
        graphic_boxes[i].append(9)

def calculate_bombs_around(x, y):
    num_bombs = 0
    
    # o++
    # +++
    # +++
    if x != 0 and y != 0:
        if bombs[x-1][y-1] == 1:
            num_bombs += 1
    # +o+
    # +++
    # +++
    if y != 0:
        if bombs[x][y-1] == 1:
            num_bombs += 1
    # ++o
    # +++
    # +++
    if x != 24 and y != 0:
        if bombs[x+1][y-1] == 1:
            num_bombs += 1
    # +++
    # o++
    # +++
    if x != 0:
        if bombs[x-1][y] == 1:
            num_bombs += 1
    # +++
    # ++o
    # +++
    if x != 24:
        if bombs[x+1][y] == 1:
            num_bombs += 1
    # +++
    # +++
    # o++
    if x != 0 and y != 24:
        if bombs[x-1][y+1] == 1:
            num_bombs += 1
    # +++
    # +++
    # +o+
    if y != 24:
        if bombs[x][y+1] == 1:
            num_bombs += 1
    # +++
    # +++
    # ++o
    if x != 24 and y != 24:
        if bombs[x+1][y+1] == 1:
            num_bombs += 1
    
    return num_bombs

def get_num_around(number, x, y):
    amount = 0
    
    # o++
    # +++
    # +++
    if x != 0 and y != 0:
        if graphic_boxes[x-1][y-1] == number:
            amount += 1
    # +o+
    # +++
    # +++
    if y != 0:
        if graphic_boxes[x][y-1] == number:
            amount += 1
    # ++o
    # +++
    # +++
    if x != 24 and y != 0:
        if graphic_boxes[x+1][y-1] == number:
            amount += 1
    # +++
    # o++
    # +++
    if x != 0:
        if graphic_boxes[x-1][y] == number:
            amount += 1
    # +++
    # ++o
    # +++
    if x != 24:
        if graphic_boxes[x+1][y] == number:
            amount += 1
    # +++
    # +++
    # o++
    if x != 0 and y != 24:
        if graphic_boxes[x-1][y+1] == number:
            amount += 1
    # +++
    # +++
    # +o+
    if y != 24:
        if graphic_boxes[x][y+1] == number:
            amount += 1
    # +++
    # +++
    # ++o
    if x != 24 and y != 24:
        if graphic_boxes[x+1][y+1] == number:
            amount += 1
    
    return amount

def draw_screen():
    # Background
    screen.fill("darkseagreen")
    
    # Bottom Buttons
    # Bombs left
    draw.rect(screen, "black", [border_width, game_height + border_width*2, bomb_count_width, menu_height], 2, 5)
    screen.blit(menu_font.render("X " + str(num_bombs-num_flags), False, "black"), (border_width + 7, game_height + border_width*2 + 8))
    # Game over message
    draw.rect(screen, "black", [border_width + bomb_count_width + border_width, game_height + border_width*2, game_status_width, menu_height], 2, 5)
    screen.blit(menu_font.render("Minesweeper", False, "black"), (border_width*2 + bomb_count_width + 65, game_height + border_width*2 + 8))
    # Timer
    draw.rect(screen, "black", [screen_width - border_width - timer_width, game_height + border_width*2, bomb_count_width, menu_height], 2, 5)
    screen.blit(menu_font.render(str(timer), False, "black"), (screen_width - border_width - timer_width + 10, game_height + border_width*2 + 7))
    
    # Draw boxes
    for x in range(25):
        for y in range(25):
            draw.rect(screen, box_colour[graphic_boxes[x][y]], [x*box_size + border_width, y*box_size + border_width, box_size, box_size])  # Box fill
            draw.rect(screen, "black", [x*box_size + border_width, y*box_size + border_width, box_size+1, box_size+1], 1)                   # Box border
            screen.blit(game_font.render(icon[graphic_boxes[x][y]], False, text_colour[graphic_boxes[x][y]]), (x*20 + border_width + 5, y*20 + border_width + 2))    # Box number
    
    draw.rect(screen, "black", [border_width, border_width, game_width+1, game_height+1], 2) # Bombs left

    # Draw grid
    # for i in range(num_boxes + 1):
    #     draw.line(screen, "black", (0 + border_width, i*20 + border_width), (500 + border_width, i*20 + border_width))
    #     draw.line(screen, "black", (i*20 + border_width, 0 + border_width), (i*20 + border_width, 500 + border_width))

bombs_around = [] # for logic
for i in range(num_boxes):
    bombs_around.append([])
    for j in range(num_boxes):
        bombs_around[i].append(0)
        if bombs[i][j] == 1:
            bombs_around[i][j] = 10
        else:
            bombs_around[i][j] = calculate_bombs_around(i, j)

def propagate(x, y):
    # o++
    # +++
    # +++
    if x != 0 and y != 0:
        reveal(x-1, y-1)
    # +o+
    # +++
    # +++
    if y != 0:
        reveal(x, y-1)
    # ++o
    # +++
    # +++
    if x != 24 and y != 0:
        reveal(x+1, y-1)
    # +++
    # o++
    # +++
    if x != 0:
        reveal(x-1, y)
    # +++
    # ++o
    # +++
    if x != 24:
        reveal(x+1, y)
    # +++
    # +++
    # o++
    if x != 0 and y != 24:
        reveal(x-1, y+1)
    # +++
    # +++
    # +o+
    if y != 24:
        reveal(x, y+1)
    # +++
    # +++
    # ++o
    if x != 24 and y != 24:
        reveal(x+1, y+1)
            
# def reveal_radius(x, y):
    # o++
    # +++
    # +++
    if x != 0 and y != 0 and bombs[x-1][y-1] != 1:
        reveal(x-1, y-1)
    # +o+
    # +++
    # +++
    if y != 0 and bombs[x][y-1] != 1:
        reveal(x, y-1)
    # ++o
    # +++
    # +++
    if x != 24 and y != 0 and bombs[x+1][y-1] != 1:
        reveal(x+1, y-1)
    # +++
    # o++
    # +++
    if x != 0 and bombs[x-1][y] != 1:
        reveal(x-1, y)
    # +++
    # ++o
    # +++
    if x != 24 and bombs[x+1][y] != 1:
        reveal(x+1, y)
    # +++
    # +++
    # o++
    if x != 0 and y != 24 and bombs[x-1][y+1] != 1:
        reveal(x-1, y+1)
    # +++
    # +++
    # +o+
    if y != 24 and bombs[x][y+1] != 1:
        reveal(x, y+1)
    # +++
    # +++
    # ++o
    if x != 24 and y != 24 and bombs[x+1][y+1] != 1:
        reveal(x+1, y+1)

def reveal(x, y):
    # FOR VISUALIZING THE PROPOGATION ALGORITHM #
    ################
    # draw_screen()
    # display.flip()
    # time.delay(1)
    ################
    if graphic_boxes[x][y] == 9:
        graphic_boxes[x][y] = bombs_around[x][y]
        if graphic_boxes[x][y] == 0:
            propagate(x, y)

# Main loop
draw_screen()
display.flip()
while running:
    timer = m.floor(t.time() - start_time)
    for e in event.get():
        if e.type == QUIT:  # Quit game
            running = False
        if e.type == MOUSEBUTTONDOWN:
            x = (e.__dict__["pos"][0] - border_width) // box_size
            y = (e.__dict__["pos"][1] - border_width) // box_size
            if x < num_boxes and x >= 0 and y < num_boxes and y >= 0:
                if e.__dict__["button"] == 1: # Left mouse button
                    if graphic_boxes[x][y] == 9:
                        reveal(x, y)
                    if graphic_boxes[x][y] >= 1 and graphic_boxes[x][y] <= 8:
                        if get_num_around(11, x, y) == graphic_boxes[x][y]:
                            propagate(x, y)
                if e.__dict__["button"] == 3: # Right mouse button
                    match graphic_boxes[x][y]:
                        case 9: # Untouched, place flag
                            if num_flags < num_bombs:
                                graphic_boxes[x][y] = 11
                                num_flags += 1
                        case 11: # Flagged, remove flag
                            graphic_boxes[x][y] = 9
                            num_flags -= 1
        
    # Update screen
    draw_screen()
    display.flip()
    clock.tick(60)  # limits FPS to 60

quit()
