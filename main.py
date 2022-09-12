import pygame
import random
import sys

# initializing display
running = True
dead = False
window = pygame.display.set_mode((800,800))
# defining constants
black = 0x000000
white = 0xffffff
green = 0x60a05b
light_green = 0xa1c89e
red = 0xff4d4d
blue = 0x5b84b1
purple = 0x9c03c8
moves = ('R','L','D','U')


# starting variables
direction = ''
moveQueue = ''
snek_len = 2
snek_color = red
# making a 'grid' of values that will be used to create the snake and the apple
grid = []
for i in range(441):
    grid.append(i)
# 220 is the point (10,10), and is the initial starting point of the snake
grid.append(grid.pop(grid.index(220)))
# chooses a random point that is not (10,10) in order to choose a point for the apple to be located
grid.insert(0,grid.pop(random.randint(0,439)))
appel = grid[0]

# board reset
def start():
    global direction, moveQueue, snek_len, snek_color, grid, appel, dead
    direction = ''
    moveQueue = ''
    snek_len = 2
    snek_color = red
    grid = []
    for i in range(441):
        grid.append(i)
    grid.append(grid.pop(grid.index(220)))
    grid.insert(0,grid.pop(random.randint(0,439)))
    appel = grid[0]
    dead = False
    return

# used to create game ticks see line 
mvt_clock = pygame.time.Clock()

while running:
    eat = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        # denotes keypresses
        if event.type == pygame.KEYDOWN:
            # determines what key is pressed and does the appropriate action
            if event.key >= pygame.K_RIGHT and event.key <= pygame.K_UP:
                this_move = moves[event.key - pygame.K_RIGHT]
                moveQueue += this_move
            # press g to grow the snake, used only for testing purposes
            if event.key == pygame.K_g:
                snek_len += 1
                eat = True
            # reset with the r key
            if event.key == pygame.K_r:
                start()
    if moveQueue:
        direction = moveQueue[-1]
    # if a move is not pressed, the direction is automatically the direction 
    if len(moveQueue) < snek_len:
        moveQueue += direction
    # print(moveQueue) # used for testing purposes
    window.fill(white)
    # drawing the checkerboard pattern for the snake
    for i in range(21):
        for j in range(21):
            if (i + j) % 2: pygame.draw.rect(window,green,pygame.Rect(85+30*i,85+30*j,30,30))
            else: pygame.draw.rect(window,light_green,pygame.Rect(85+30*i,85+30*j,30,30))
    # moving the snake in a direction
    if len(moveQueue) >= snek_len:
        # take the last value in the grid(the current position of the head)
        next_square = grid[-1]    
        # calculate the location of the next square to find
        if moveQueue[snek_len-1] == 'U': next_square -= 21
        if moveQueue[snek_len-1] == 'R': 
            # check if snake has collided with right wall
            if next_square % 21 == 20:
                dead = True
            else: next_square += 1
        if moveQueue[snek_len-1] == 'L': 
            if next_square % 21 == 0:
                dead = True
            else: next_square -= 1
        if moveQueue[snek_len-1] == 'D': next_square += 21
        if next_square < 0 or next_square > 440:
            dead = True
        # check if snake collides with itself
        if not dead and grid.index(next_square) >= len(grid) - snek_len:
            dead = True
        # check if snake has eaten the apple
        if next_square == appel:
            snek_len += 1
            grid.append(grid.pop(grid.index(next_square)))
            appel = -1
            eat = True
        if not dead: grid.append(grid.pop(grid.index(next_square)))
        else: snek_color = purple # ded snek purple
    elif moveQueue:
        next_square = grid[-1]    
        if moveQueue[-1] == 'U': next_square -= 21
        if moveQueue[-1] == 'R': next_square += 1
        if moveQueue[-1] == 'L': next_square -= 1
        if moveQueue[-1] == 'D': next_square += 21
        grid.append(grid.pop(grid.index(next_square)))
    
    # draw the snek
    for num in grid[-snek_len:]:
        pygame.draw.rect(window,snek_color,pygame.Rect(90+30*(num%21),90+30*(num//21),20,20))
    
    # checks if the appel has been eaten
    if(appel != -1):
        pygame.draw.rect(window,blue,pygame.Rect(90+30*(appel % 21), 90 + 30*(appel//21),20,20))
    else: # generates a new location for the appel
        grid.insert(0,grid.pop(random.randint(0,len(grid)-snek_len)))
        appel = grid[0]
    if eat:
        # end of snake stays same since the snake len increases
        moveQueue = moveQueue[:snek_len+1]
    else:
        # the last end of the snake is taken out
        moveQueue = moveQueue[1:snek_len+1]
    # used to generate ticks in the animation
    pygame.display.update()
    mvt_clock.tick(10)