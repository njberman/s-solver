import numpy as np
import pygame
import time
import random

DIGITS = [n for n in range(1, 10)]
s = [[0 for _ in range(9)] for _ in range(9)]
s = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0]
]
def calculate_possible(s, i, j):
    # Figure out what it can be from it's row (i)
    row = s[i]
    col = [s[y][j] for y in range(9)]
    square = [s[y][x] for x in range(j - j % 3, j - j % 3 + 3) for y in range(i - i % 3, i - i % 3 + 3)]

    possible_from_row = [n for n in DIGITS if n not in row]
    possible_from_col = [n for n in DIGITS if n not in col]
    possible_from_square = [n for n in DIGITS if n not in square]

    possible = list(set(possible_from_row) & set(possible_from_col) & set(possible_from_square))

    return possible


possibilities = [[[] for _ in range(9)] for _ in range(9)]
for i in range(9):
    for j in range(9):
        possible = calculate_possible(s, i, j)
        possibilities[i][j] = possible

        possible = []


saved = []
saved_counts = []
saved_idx = -1

def solve(n=1):
    for i in range(9):
        for j in range(9):
            if s[i][j] != 0: continue

            possible = calculate_possible(s, i, j)
            possibilities[i][j] = possible


            if len(possible) == n:
                s[i][j] = possible[random.randint(0, n - 1)]

                if n > 1:
                    saved.append([s.copy(), possibilities.copy(), i, j])
                    saved_counts.append(0)
                return

    # All entropies are bigger than one
    return solve(n=n+1)



pygame.init()
screen = pygame.display.set_mode((1000, 700))
width, height = screen.get_size()
clock = pygame.time.Clock()
running = True

font = pygame.font.SysFont("Caskaydia Cove Mono", int((height - 100)/9))
smaller_font = pygame.font.SysFont("Caskaydia Cove Mono", 30)

hover = False

def draw_sudoku():
    for i in range(9):
        for j in range(9):
            if s[i][j] == 0:
                for x in range(len(possibilities[i][j])):
                    possible = possibilities[i][j][x]

                    text_surface = smaller_font.render(str(possible), False, "white")
                    screen.blit(text_surface, (50 + ((height - 100)/9)*j + 15 * x + 3, 50 + ((height - 100)/9)*i + 3))
                continue

            text_surface = font.render(str(s[i][j]), False, "white")
            screen.blit(text_surface, (50 + (height - 100) / 27 + ((height - 100)/9) * j, 50 + (height - 100) / 36 + ((height - 100)/9) * i))



while running:
    (mousex, mousey) = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP and hover:
            solve()
            for i in range(9):
                for j in range(9):
                    if len(possibilities[i][j]) == 0 and s[i][j] == 0:
                        saved_s, saved_p, x, y = saved[saved_idx]
                        if saved_counts[saved_idx] < len(saved_p[x][y]):
                            s = saved_s.copy()
                            saved_val = s[x][y]

                            while s[x][y] == saved_val:
                                s[x][y] = saved_p[x][y][random.randint(0, len(saved_p[x][y]) - 1)]
                                solve()
                        else:
                            saved.pop()
                            saved_counts.pop()
                            saved_s, saved_p, x, y = saved[saved_idx]
                            if saved_counts[saved_idx] < len(saved_p[x][y]):
                                s = saved_s.copy()
                                saved_val = s[x][y]

                                while s[x][y] == saved_val:
                                    s[x][y] = saved_p[x][y][random.randint(0, len(saved_p[x][y]) - 1)]
                                    solve()




    screen.fill("black")


    pygame.draw.line(screen, "white", (50, 50), (50, height - 50))

    for i in range(10):
        pygame.draw.line(screen, "white", (50 + ((height - 100)/9) * i, 50), (50 + ((height - 100)/9) * i, 650), width=(3 if i % 3 == 0 else 1))
        pygame.draw.line(screen, "white", (50, 50 + ((height - 100)/9) * i), (650, 50 + ((height - 100)/9) * i), width=(3 if i % 3 == 0 else 1))

    draw_sudoku()

    pygame.draw.rect(screen, "white" if not hover else "gray", (height, height / 2 - 25, width - height - 50, 50), border_radius=2)
    text_surface = font.render("Solve", False, "black")
    screen.blit(text_surface, (height + (1/4) * (width - height - 50), height / 2 - 25 + (1/6)*50))

    if height <= mousex and mousex <= (width - 50) and (height / 2 - 25) <= mousey and mousey <= (height / 2 + 25):
        hover = True
    else:
        hover = False

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
