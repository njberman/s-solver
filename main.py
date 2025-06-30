DIGITS = (n for n in range(1, 10))
s = [[0 for _ in range(9)] for _ in range(9)]
s = [
    [0, 0, 6, 0, 0, 1, 0, 0, 7],
    [3, 0, 5, 7, 6, 0, 0, 0, 0],
    [2, 0, 8, 0, 5, 0, 0, 0, 0],
    [6, 0, 9, 0, 0, 0, 0, 7, 0],
    [0, 0, 0, 0, 0, 3, 0, 0, 9],
    [7, 0, 0, 2, 0, 8, 5, 0, 1],
    [0, 0, 0, 5, 1, 7, 0, 0, 0],
    [1, 0, 0, 0, 0, 6, 7, 0, 5],
    [0, 3, 0, 0, 2, 0, 0, 9, 0],
]

def calculate_entropy(s, i, j):
    # Figure out what it can be from it's row (i)
    row = s[i]
    possible_from_row = [n if n not in row else None for n in DIGITS]
    print(possible_from_row)

calculate_entropy(s, 5, 4)
print(s)
