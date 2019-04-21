# Первое домашнее задание по ЭВМ. Последовательный и параллельный алгоритм.

from graph import Graph
from algorithms import sequential_algorithm

# Матрица смежности
matrix = [
    [0, 1, 1, 1, 0, 1, 2, 1],
    [1, 0, 0, 0, 1, 1, 1, 0],
    [1, 0, 0, 0, 1, 0, 1, 0],
    [1, 0, 0, 0, 1, 1, 0, 0],
    [0, 1, 1, 1, 0, 1, 0, 1],
    [1, 1, 0, 1, 1, 0, 1, 1],
    [2, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 0]
]
graph = Graph(matrix)
# g.print_info()
# min_local = g.get_min_local_degrees()

groups = sequential_algorithm(graph, [3, 3, 2])
print("GROUPS: ")
for i in range(0, len(groups)):
    groups[i].sort()
    print("Group #", i+1)
    print(groups[i])