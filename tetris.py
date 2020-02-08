import pygame
from pygame.locals import *
import random
from numpy import rot90

BLOCK_SIZE = 30
SCREEN_SIZE_X = 10
SCREEN_SIZE_Y = 20

SCREEN = pygame.display.set_mode((SCREEN_SIZE_X*BLOCK_SIZE, SCREEN_SIZE_Y*BLOCK_SIZE))
MAIN_CLOCK = pygame.time.Clock()

P_I = \
        [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0]]

P_J = \
    [[0, 1, 0],
     [0, 1, 0],
     [1, 1, 0]]

P_L = \
    [[1, 1, 0],
     [0, 1, 0],
     [0, 1, 0]]

P_S = \
    [[1, 0, 0],
     [1, 1, 0],
     [0, 1, 0]]

P_T = \
    [[0, 1, 0],
     [1, 1, 0],
     [0, 1, 0]]

P_Z = \
    [[0, 1, 0],
     [1, 1, 0],
     [1, 0, 0]]

P_O = \
    [[1, 1],
     [1, 1]]

BLUE = (47, 86, 233)
RED = (255, 106, 106)
BLACK = (0, 0, 0)


def initializing():
    pygame.init()


def keyboard_events():
    global flag_key_down
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            key = event.key
            if key == K_RIGHT:
                cur_piece[0][0] += 1
                if collision(cur_piece, accu_pieces):
                    cur_piece[0][0] -= 1
            elif key == K_LEFT:
                cur_piece[0][0] -= 1
                if collision(cur_piece, accu_pieces):
                    cur_piece[0][0] += 1
            elif key == K_UP:
                cur_piece[1] = rot90(cur_piece[1], k=-1)
                if collision(cur_piece, accu_pieces):
                    cur_piece[1] = rot90(cur_piece[1], k=1)
            elif key == K_DOWN:
                flag_key_down = True


def generate_piece():
    lst = [P_I, P_J, P_L, P_S, P_T, P_Z, P_O]
    n = random.randrange(0, 7)
    p = lst[n]
    pp = [[4, -1], p]
    return pp


def rotate_piece(pp):
    return pp


def locate_piece(pp):
    ppl = []
    i0, j0 = pp[0]
    for i in range(len(pp[1])):
        for j in range(len(pp[1][0])):
            if pp[1][j][i]:
                ppl.append([i+i0, j+j0])
    return ppl


def collision(pp, ppc):
    for k in locate_piece(pp):
        if (k in ppc) or (k[1] >= 20) or (k[0] < 0) or (k[0] > 9):
            return True
    return False


def flag_clear_lines(ppc):
    cts = {}
    for k in ppc:
        if k[1] not in cts.keys():
            cts[k[1]] = 1
        else:
            cts[k[1]] += 1
        if cts[k[1]] >= 10:
            return True
    return False


def clear_lines(ppc):
    cts = {}
    for k in ppc:
        if k[1] not in cts.keys():
            cts[k[1]] = [k]
        else:
            cts[k[1]].append(k)

    for key, val in sorted(cts.items()):
        if len(val) == 10:
            for v in val:
                ppc.remove(v)
            for p in ppc:
                if p[1] < key:
                    p[1] += 1

    return ppc


def update_screen():
    SCREEN.fill(BLACK)
    for sec in locate_piece(cur_piece) + accu_pieces:
        loc = (sec[0] * BLOCK_SIZE, sec[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(SCREEN, BLUE, loc)
    for j in range(1, 20):
        pygame.draw.line(SCREEN, RED, (0 * BLOCK_SIZE, j * BLOCK_SIZE), (11 * BLOCK_SIZE, j * BLOCK_SIZE))
    for i in range(1, 10):
        pygame.draw.line(SCREEN, RED, (i * BLOCK_SIZE, 0 * BLOCK_SIZE), (i * BLOCK_SIZE, 21 * BLOCK_SIZE))
    pygame.display.update()


if __name__ == '__main__':

    initializing()
    fps = 24
    dps = 2
    flag_new_piece = True
    flag_piece_drop = True
    flag_piece_rotate = True
    ct = 0
    accu_pieces = []

    while True:
        flag_key_down = False
        MAIN_CLOCK.tick(fps)
        ct += 1

        keyboard_events()

        if flag_new_piece:
            cur_piece = generate_piece()
            flag_new_piece = False

        if flag_piece_drop and (ct == fps//dps or flag_key_down):
            cur_piece[0][1] += 1
            ct = 0

        if collision(cur_piece, accu_pieces):
            cur_piece[0][1] -= 1
            accu_pieces.extend(locate_piece(cur_piece))
            flag_new_piece = True

        # screen update
        update_screen()

        # clear if full
        if not flag_clear_lines(accu_pieces):
            continue
        accu_pieces = clear_lines(accu_pieces)
        update_screen()
