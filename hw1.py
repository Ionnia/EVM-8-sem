# Первое домашнее задание по ЭВМ. Последовательный и параллельный алгоритм.

from graph import Graph
from algorithms import sequential_algorithm, iterative_algorithm

# # Матрица смежности
# matrix1 = [
#     [0, 1, 1, 1, 0, 1, 2, 1],
#     [1, 0, 0, 0, 1, 1, 1, 0],
#     [1, 0, 0, 0, 1, 0, 1, 0],
#     [1, 0, 0, 0, 1, 1, 0, 0],
#     [0, 1, 1, 1, 0, 1, 0, 1],
#     [1, 1, 0, 1, 1, 0, 1, 1],
#     [2, 1, 1, 0, 0, 1, 0, 1],
#     [1, 0, 0, 0, 1, 1, 1, 0]
# ]

# matrix2 = [
#     [0, 1, 2, 0, 0, 1, 0, 1, 0, 0],
#     [1, 0, 1, 0, 2, 2, 0, 0, 0, 0],
#     [2, 1, 0, 2, 0, 0, 2, 1, 0, 0],
#     [0, 0, 2, 0, 0, 0, 1, 0, 1, 1],
#     [0, 2, 0, 0, 0, 1, 0, 1, 1, 0],
#     [1, 2, 0, 0, 1, 0, 0, 0, 0, 1],
#     [0, 0, 2, 1, 0, 0, 0, 1, 0, 0],
#     [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
#     [0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
#     [0, 0, 0, 1, 0, 1, 0, 0, 1, 0]
# ]

# graph = Graph(matrix1)
# # g.print_info()
# # min_local = g.get_min_local_degrees()

# groups = sequential_algorithm(graph, [3, 3, 2], info=False)

# Тест итерационного алгоритма
matrix = [
    [0, 0, 0, 1, 1, 0, 2],
    [0, 0, 2, 0, 3, 0, 0],
    [0, 2, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 2, 1],
    [1, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 1],
    [2, 0, 1, 1, 0, 1, 0]
]

graph = Graph(matrix)

groups = [
    [0, 4, 6],
    [1, 2],
    [5, 3]
]

print("GROUPS: ")
for i in range(0, len(groups)):
    groups[i].sort()
    print("Group #", i)
    print(groups[i])

groups = iterative_algorithm(graph, groups, info=False)

print("GROUPS ITERATIVE: ")
for i in range(0, len(groups)):
    groups[i].sort()
    print("Group #", i)
    print(groups[i])