# Второе домашнее задание по ЭВМ. Задача размещения.

from graph import Graph
from algorithms import sequential_positioning_algorithm

# Вариант 1
matrix = [
    [0, 1, 0, 3, 2, 0, 2, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2, 4, 2, 3, 0, 2, 3, 2, 2, 3],
    [1, 0, 4, 4, 3, 0, 0, 2, 0, 0, 0, 0, 3, 4, 0, 0, 2, 0, 0, 2, 4, 2, 1, 0, 1, 3, 2, 2, 0, 0],
    [0, 4, 0, 2, 0, 0, 1, 0, 3, 0, 0, 0, 0, 3, 0, 0, 3, 2, 0, 0, 0, 3, 3, 2, 0, 1, 2, 4, 1, 0],
    [3, 4, 2, 0, 1, 0, 3, 0, 0, 1, 0, 4, 0, 0, 0, 0, 3, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0],
    [2, 3, 0, 1, 0, 2, 0, 1, 0, 3, 2, 0, 2, 0, 0, 0, 0, 0, 1, 0, 4, 4, 3, 4, 1, 3, 3, 2, 1, 3],
    [0, 0, 0, 0, 2, 0, 3, 0, 4, 4, 0, 0, 4, 0, 4, 0, 2, 0, 3, 2, 1, 3, 0, 0, 3, 2, 0, 1, 4, 0],
    [2, 0, 1, 3, 0, 3, 0, 4, 0, 4, 0, 0, 1, 0, 0, 0, 0, 3, 0, 1, 3, 1, 1, 2, 1, 4, 1, 1, 0, 3],
    [3, 2, 0, 0, 1, 0, 4, 0, 2, 4, 0, 0, 1, 1, 4, 0, 0, 2, 0, 0, 4, 2, 3, 0, 2, 0, 2, 0, 4, 0],
    [3, 0, 3, 0, 0, 4, 0, 2, 0, 0, 0, 4, 1, 3, 4, 0, 0, 1, 0, 2, 3, 0, 2, 2, 4, 0, 0, 0, 4, 0],
    [0, 0, 0, 1, 3, 4, 4, 4, 0, 0, 0, 0, 0, 1, 1, 3, 0, 2, 3, 0, 2, 0, 3, 0, 1, 3, 0, 3, 0, 3],
    [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 4, 4, 0, 1, 4, 0, 0, 0, 4, 0, 3, 0, 3, 0, 0, 2, 3, 1, 0],
    [0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 4, 0, 0, 3, 0, 0, 2, 0, 2, 1, 1, 2, 0, 0, 0, 3, 0, 2, 2, 0],
    [0, 3, 0, 0, 2, 4, 1, 1, 1, 0, 4, 0, 0, 0, 2, 4, 4, 0, 0, 3, 2, 0, 0, 0, 2, 0, 1, 0, 0, 0],
    [0, 4, 3, 0, 0, 0, 0, 1, 3, 1, 0, 3, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 3, 0, 0],
    [0, 0, 0, 0, 0, 4, 0, 4, 4, 1, 1, 0, 2, 2, 0, 4, 4, 1, 4, 0, 2, 2, 0, 2, 0, 0, 0, 0, 3, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 0, 4, 0, 4, 0, 0, 0, 4, 3, 0, 2, 1, 4, 0, 4, 0, 0, 0, 2],
    [0, 2, 3, 3, 0, 2, 0, 0, 0, 0, 0, 2, 4, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 3, 3, 0, 0, 1],
    [0, 0, 2, 0, 0, 0, 3, 2, 1, 2, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 4, 0, 2, 0, 1, 0, 1, 4, 2],
    [3, 0, 0, 0, 1, 3, 0, 0, 0, 3, 0, 2, 0, 1, 4, 4, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0],
    [0, 2, 0, 2, 0, 2, 1, 0, 2, 0, 4, 1, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 3, 4, 0, 0, 2, 3, 0, 0],
    [2, 4, 0, 0, 4, 1, 3, 4, 3, 2, 0, 1, 2, 0, 2, 0, 0, 0, 0, 0, 0, 3, 0, 1, 4, 0, 3, 4, 0, 3],
    [4, 2, 3, 0, 4, 3, 1, 2, 0, 0, 3, 2, 0, 0, 2, 2, 0, 4, 3, 0, 3, 0, 0, 2, 3, 0, 1, 0, 0, 3],
    [2, 1, 3, 4, 3, 0, 1, 3, 2, 3, 0, 0, 0, 2, 0, 1, 1, 0, 0, 3, 0, 0, 0, 0, 2, 0, 0, 0, 4, 0],
    [3, 0, 2, 0, 4, 0, 2, 0, 2, 0, 3, 0, 0, 0, 2, 4, 0, 2, 0, 4, 1, 2, 0, 0, 4, 1, 4, 1, 2, 2],
    [0, 1, 0, 0, 1, 3, 1, 2, 4, 1, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 4, 3, 2, 4, 0, 0, 0, 0, 0, 2],
    [2, 3, 1, 0, 3, 2, 4, 0, 0, 3, 0, 3, 0, 0, 0, 4, 3, 1, 0, 0, 0, 0, 0, 1, 0, 0, 4, 1, 3, 3],
    [3, 2, 2, 0, 3, 0, 1, 2, 0, 0, 2, 0, 1, 1, 0, 0, 3, 0, 0, 2, 3, 1, 0, 4, 0, 4, 0, 3, 0, 1],
    [2, 2, 4, 0, 2, 1, 1, 0, 0, 3, 3, 2, 0, 3, 0, 0, 0, 1, 3, 3, 4, 0, 0, 1, 0, 1, 3, 0, 0, 0],
    [2, 0, 1, 0, 1, 4, 0, 4, 4, 0, 1, 2, 0, 0, 3, 0, 0, 4, 0, 0, 0, 0, 4, 2, 0, 3, 0, 0, 0, 2],
    [3, 0, 0, 0, 3, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 2, 1, 2, 0, 0, 3, 3, 0, 2, 2, 3, 1, 0, 2, 0]
]

graph = Graph(matrix)

pos_matrix = sequential_positioning_algorithm(graph, [6, 5])

for i in range(0, len(pos_matrix)):
    for j in range(0, len(pos_matrix[i])):
        print("%3s " % ("x" + str(pos_matrix[i][j]+1)), end='')
    print()