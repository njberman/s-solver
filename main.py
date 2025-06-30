import numpy as np

DIGITS = [n for n in range(1, 10)]
s = [[0 for _ in range(9)] for _ in range(9)]
s = [
    [9, 0, 3, 4, 2, 0, 0, 6, 8],
    [0, 5, 0, 0, 0, 0, 1, 9, 0],
    [6, 0, 7, 0, 1, 5, 3, 0, 0],
    [0, 7, 0, 0, 3, 0, 6, 8, 0],
    [1, 0, 0, 0, 0, 8, 7, 0, 0],
    [0, 0, 8, 0, 6, 0, 0, 1, 9],
    [0, 9, 1, 2, 5, 0, 4, 7, 3],
    [3, 0, 5, 0, 0, 1, 0, 0, 0],
    [7, 0, 6, 0, 0, 0, 0, 5, 0],
]

def calculate_possible(s, i, j):
    # Figure out what it can be from it's row (i)
    row = s[i]
    col = [s[y][j] for y in range(9)]
    square = [s[x][y] for x in range(j - j % 3, j - j % 3 + 3) for y in range(i - i % 3, i - i % 3 + 3)]

    possible_from_row = [n for n in DIGITS if n not in row]
    possible_from_col = [n for n in DIGITS if n not in col]
    possible_from_square = [n for n in DIGITS if n not in square]

    possible = min(possible_from_row, possible_from_col, possible_from_square)

    return possible

calculate_possible(s, 5, 4)

entropies = [[0 for _ in range(9)] for _ in range(9)]
for i in range(9):
    for j in range(9):
        entropies[i][j] = len(calculate_possible(s, i, j))


print(np.array(s))
print(np.array(entropies))
