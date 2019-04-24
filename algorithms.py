from graph import Graph
from itertools import combinations      # Нужно для получения всех перестановок групп


def get_max_index(arr):
    max_index = 0
    for i in range(1, len(arr)):
        if arr[i] > arr[max_index]:
            max_index = i
    return max_index


def get_all_sigmas(graph, group, v_index):
    verticies = [v for v in group if v is not v_index]
    result = []
    for i in range(0, len(verticies)):
        sigma = graph.px[verticies[i]]
        for j in range(0, len(group)):
            if  group[j] != verticies[i]:
                sigma -= 2 * graph.get_num_of_edges(group[j], verticies[i])
        result.append(sigma)
    return result, verticies


# Последовательный алгоритм компоновки.
# Возвращает двумерный массив, в котором первое измерение это "группы", а второе элементы этих групп
def sequential_algorithm(graph, group_sizes, info = True):
    # Проверка
    if graph.size != sum(group_sizes):
        raise Exception("Sum of group sizes not equal to number of verticies")
    # Элементы массива result -- это массивы, содержащие индесы вершин, которые находятся в одной группе
    result = []
    # Основной цикл метода
    for k in range(0, len(group_sizes)):
        # Получаем массив индексов вершин с минимальной локальной степенью
        min_local_degree_verticies = graph.get_min_local_degrees()
        # Получаем массив индексов с наибольшим числом кратных рёбер
        best_verticies = graph.get_best_verticies(min_local_degree_verticies)
        # Выбранная вершина
        v_index = best_verticies[0]
        # Новая группа
        group = [v_index] + graph.get_all_adjacent_verticies(v_index)
        # Вывод информации
        if info:
            print("STEP #%d" % k, "----------------------")
            graph.print_info()
            print("Minimal local degree: ", min_local_degree_verticies)
            print("Best verticies: ", best_verticies)
            print("Group: ", group)
        # print("All verticies adjacent to first with min local degree: ", [min_local[0]] + g.get_all_adjacent_verticies(min_local[0]))
        # Возможны три случая
        while len(group) != group_sizes[k]:
            if len(group) > group_sizes[k]:
                # Получаем все сигмы для вершин в verticies
                sigmas, verticies = get_all_sigmas(graph, group, v_index)
                # Получаем индекс вершины с максимальной сигмой
                max_sigma_index = get_max_index(sigmas)
                v_index_max_sigma = verticies[max_sigma_index]
                # Вывод информации
                if info:
                    print("Deleting x%d" % (v_index_max_sigma), "vertex from a group")
                # Удаляем эту вершину из группы
                group.remove(v_index_max_sigma)
            elif len(group) < group_sizes[k]:
                graph.add_to_used_verticies(group)
                min_local_degree_verticies = graph.get_min_local_degrees()
                best_verticies = graph.get_best_verticies(min_local_degree_verticies)
                # Вывод информации
                if info:
                    print("Adding more verticies!")
                # Добавляем в группу новые вершины
                group += [best_verticies[0]] + graph.get_all_adjacent_verticies(best_verticies[0])
            if info:
                print("Group update: ", group)
        graph.add_to_used_verticies(group)
        result.append(group)
    return result

# Возвращает значение alpha
def get_alpha(graph, v_index, group1, group2):
    alpha = 0
    for i in range(0, len(group2)):
        if v_index != group2[i]:
            alpha += graph.get_num_of_edges(v_index, group2[i])
    for i in range(0, len(group1)):
        if v_index != group1[i]:
            alpha -= graph.get_num_of_edges(v_index, group1[i])
    if v_index in group2:
        alpha *= -1
    return alpha

# Возвращает двумерный массив со значениями b между соответствующими вершинами
def get_b(graph, alpha1, alpha2, group1, group2):
    b = []
    for i in range(0, len(alpha1)):
        tmp = []
        for j in range(0, len(alpha2)):
            b_value = alpha1[i] + alpha2[j] - 2 * graph.get_num_of_edges(group1[i], group2[j])
            tmp.append(b_value)
        b.append(tmp)
    return b

# Функция находит и возвращает индекс максимального элемента в двумерном массиве b
def get_max_b_indicies(b):
    group1_index = 0
    group2_index = 0
    for i in range(0, len(b)):
        for j in range(0, len(b[i])):
            if b[group1_index][group2_index] < b[i][j]:
                group1_index, group2_index = i, j
    return group1_index, group2_index

# Функция возвращает True, если согласно матрице b существуют две вершины, которые
# выгодно поменять местами
def swap_is_profitable(b):
    result = False
    for i in range(0, len(b)):
        for j in range(0, len(b[i])):
            if b[i][j] > 0:
                result = True
                break
    return result

# Вывод матрицы b
def print_b(b, group1, group2):
    print("B: ")
    for i in range(0, len(b)):
        print("| ", end='')
        for j in range(0, len(b[i])):
            print("x%d%d %4d | " % (group1[i], group2[j], b[i][j]), end='')
        print()

# Итерационный алгоритм компоновки
# Возвращает двумерный массив, в котором первое измерение это "группы", а второе элементы этих групп
def iterative_algorithm(graph, groups, info = True):
    # Создаём итератор, который даёт нам все перестановки по две группы
    combs = combinations(range(0, len(groups)), 2)
    # Пока не закончатся все перестановки
    try:
        while True:
            # Получаем новую пару групп
            pair = next(combs)
            group1 = groups[pair[0]]
            group2 = groups[pair[1]]
            # Высчитываем характеристику alpha первой группы
            alpha1 = []
            for i in range(0, len(group1)):
                alpha1.append( get_alpha(graph, group1[i], group1, group2))
            # Высчитываем характеристику alpha второй группы
            alpha2 = []
            for i in range(0, len(group2)):
                alpha2.append( get_alpha(graph, group2[i], group1, group2))
            # Вычисление характеристики b
            b = get_b(graph, alpha1, alpha2, group1, group2)
            if info:
                # Вывод дополнительной информации
                print("Pair of groups are %2d and %2d" % (pair[0], pair[1]))
                print("Group #%2d: " % (pair[0]), group1)
                print("Group #%2d: " % (pair[1]), group2)
                print("Alpha #%2d: " % (pair[0]), alpha1)
                print("Alpha #%2d: " % (pair[1]), alpha2)
                print_b(b, group1, group2)
            while swap_is_profitable(b):
                # Нахождение индексов вершин для перестановки в массивах group1, group2
                group1_index, group2_index = get_max_b_indicies(b)
                # Меняем местами вершины в группах
                group1[group1_index], group2[group2_index] = group2[group2_index], group1[group1_index]
                # Высчитываем характеристику alpha первой группы
                alpha1 = []
                for i in range(0, len(group1)):
                    alpha1.append( get_alpha(graph, group1[i], group1, group2))
                # Высчитываем характеристику alpha второй группы
                alpha2 = []
                for i in range(0, len(group2)):
                    alpha2.append( get_alpha(graph, group2[i], group1, group2))
                # Заново вычисляем характеристику b
                b = get_b(graph, alpha1, alpha2, group1, group2)
                if info:
                    print("Change x%d and x%d" % (group1[group1_index], group2[group2_index]))
                    print_b(b, group1, group2)
    except StopIteration:
        pass
    return groups