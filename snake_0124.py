import pygame
from pygame.locals import *
import random

BLOCK_SIZE = 10
SCREEN_SIZE_X = 60
SCREEN_SIZE_Y = 40
BLUE = (47, 86, 233)
RED = (255, 106, 106)
BLACK = (0, 0, 0)
VEL = [1, 0]
TEXT_DEAD = None
TEXT_DEAD_X = 0
TEXT_DEAD_Y = 0

snake_body = []
food_loc = []

SCREEN = pygame.display.set_mode((SCREEN_SIZE_X*BLOCK_SIZE, SCREEN_SIZE_Y*BLOCK_SIZE))
MAIN_CLOCK = pygame.time.Clock()


def initializing():
    global TEXT_DEAD, TEXT_DEAD_X, TEXT_DEAD_Y
    pygame.init()
    snake_init_len = 6
    snake_init_x, snake_init_y = 1, 10
    snake_body.extend([[x, snake_init_y] for x in range(snake_init_x, snake_init_x+snake_init_len)])
    FONT1 = pygame.font.SysFont('arial', 56, 1)
    TEXT_DEAD = FONT1.render('DEAD!!', True, BLACK)
    TEXT_DEAD_X = (SCREEN_SIZE_X * BLOCK_SIZE - TEXT_DEAD.get_width()) // 2
    TEXT_DEAD_Y = (SCREEN_SIZE_Y * BLOCK_SIZE - TEXT_DEAD.get_height()) // 2


def keyboard_events():
    global pause, VEL, ACC
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            key = event.key
            if key == K_SPACE:
                pause = not pause
                break

            d0, d1 = 0, 0
            if key == K_RIGHT:
                d0, d1 = 1, 0
            elif key == K_UP:
                d0, d1 = 0, -1
            elif key == K_LEFT:
                d0, d1 = -1, 0
            elif key == K_DOWN:
                d0, d1 = 0, 1
            if [d0, d1] == VEL:
                ACC = 4
            if d0 != VEL[0] and d1 != VEL[1]:
                VEL[0], VEL[1] = d0, d1


def snake():
    global ACC
    head = snake_body[-1]
    for n in range(1, ACC+1):
        new_head = [head[0]+n*VEL[0], head[1]+n*VEL[1]]
        snake_body.append(new_head)


def food():
    while True:
        x = random.randrange(0, SCREEN_SIZE_X-1)
        y = random.randrange(0, SCREEN_SIZE_Y-1)
        if (x, y) not in snake_body:
            break
    food_loc.extend([x, y])


def eat_check():
    global food_ct
    for n in range(0, ACC):
        if food_loc != snake_body[-1-n]:
            snake_body.pop(0)
        else:
            food_loc.clear()
            food_ct += 1


def boundary_check():
    global dead
    head = snake_body[-1]
    if head[0] > SCREEN_SIZE_X or head[0] < 0 or head[1] > SCREEN_SIZE_Y or head[1] < 0 or head in snake_body[0:-1]:
        dead = True


if __name__ == '__main__':

    # initialization
    initializing()
    dead = False
    pause = False
    fps = 1
    food_ct = 0

    while True:
        if food_ct >= fps:
            fps *= 2
        MAIN_CLOCK.tick(fps)
        ACC = 1
        # keyboard events
        keyboard_events()

        # food

        if not pause:
            # snake
            snake()
            # boundary
            boundary_check()
            # eat food
            eat_check()

        if not food_loc:
            food()

        if dead:
            SCREEN.fill(RED)
            SCREEN.blit(TEXT_DEAD, (TEXT_DEAD_X, TEXT_DEAD_Y))
            pygame.display.update()
            continue

        # update
        SCREEN.fill(BLACK)
        for sec in snake_body:
            loc = (sec[0]*BLOCK_SIZE, sec[1]*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, BLUE, loc)
        if food_loc:
            loc = (food_loc[0]*BLOCK_SIZE+BLOCK_SIZE//2, food_loc[1]*BLOCK_SIZE+BLOCK_SIZE//2)
            pygame.draw.circle(SCREEN, RED, loc, BLOCK_SIZE//2)
        pygame.display.update()

