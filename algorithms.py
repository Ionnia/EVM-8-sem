from graph import Graph
from itertools import combinations      # Нужно для получения всех перестановок групп
from math import sqrt, pow
import copy


def get_max_index(arr):
    max_index = 0
    for i in range(1, len(arr)):
        if arr[i] is not None and arr[max_index] is not None:
            if arr[i] > arr[max_index]:
                max_index = i
        else:
            if arr[max_index] is None:
                max_index = i
    return max_index

def get_all_max_indicies(arr):
    max_index = get_max_index(arr)
    max_indicies = []
    for i in range(0, len(arr)):
        if arr[i] == arr[max_index]:
            max_indicies.append(i)
    return max_indicies

def get_min_index(arr):
    min_index = 0
    for i in range(1, len(arr)):
        if arr[i] is not None and arr[min_index] is not None:
            if arr[i] < arr[min_index]:
                min_index = i
        else:
            if arr[min_index] is None:
                min_index = i
    return min_index

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
            print("STEP #%d" % (k+1), "----------------------")
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
            print("x%5s %4d | " % ( (str(group1[i]+1) + "_" + str(group2[j]+1)), b[i][j]), end='')
        print()

# Итерационный алгоритм компоновки
# Возвращает двумерный массив, в котором первое измерение это "группы", а второе элементы этих групп
def iterative_algorithm(graph, groups, info = True):
    # Создаём итератор, который даёт нам все перестановки по две группы
    combs = combinations(range(0, len(groups)), 2)
    # Number of iterations
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
                print("Pair of groups are %2d and %2d %s" % (pair[0], pair[1], '-'*40))
                print("Group #%2d: " % (pair[0]+1), group1)
                print("Group #%2d: " % (pair[1]+1), group2)
                print("Alpha #%2d: " % (pair[0]+1), alpha1)
                print("Alpha #%2d: " % (pair[1]+1), alpha2)
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
                    print("Change x%d and x%d %s" % (group1[group1_index], group2[group2_index], '-'*20))
                    print("Alpha #%2d: " % (pair[0]+1), alpha1)
                    print("Alpha #%2d: " % (pair[1]+1), alpha2)
                    print_b(b, group1, group2)
    except StopIteration:
        pass
    return groups


# Вычисляет значение целевой функции (число связей между группами)
def calculate_Q(graph, groups):
    result = 0
    used_verticies = graph.get_used_verticies()
    graph.clear_used_verticies()
    for i in range(0, len(groups)):
        for j in range(0, len(groups[i])):
            all_adjacent_verticies = graph.get_all_adjacent_verticies(groups[i][j])
            for k in range(0, len(all_adjacent_verticies)):
                if(all_adjacent_verticies[k] not in groups[i]):
                    result += graph.get_num_of_edges(all_adjacent_verticies[k], groups[i][j])
    graph.add_to_used_verticies(used_verticies)
    return int(result/2)

def get_min_value_greater_than_x(matrix, x):
    min_value = 9999999999
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[i])):
            if matrix[i][j] > x and matrix[i][j] < min_value:
                min_value = matrix[i][j]
    return min_value

def get_all_coords_with_value(matrix, value):
    result = []
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[i])):
            if matrix[i][j] == value:
                result.append([i, j])
    return result

# Вычисляет последовательность координат для расположения элементов
def get_list_of_coordinates(dimensions):
    positions = []
    result = []
    for i in range(0, dimensions[0]):
        positions.append([0] * dimensions[1])
        for j in range(0, dimensions[1]):
            positions[i][j] = sqrt(pow(i, 2) + pow(j, 2))
    min_value = 0
    result += get_all_coords_with_value(positions, min_value)
    while len(result) < dimensions[0] * dimensions[1]:
        min_value = get_min_value_greater_than_x(positions, min_value)
        result += get_all_coords_with_value(positions, min_value)
    return result

# Последовательный алгоритм размещения
def sequential_positioning_algorithm(graph, dimensions, info = True):
    pos_matrix = []
    for i in range(0, dimensions[0]):
        pos_matrix.append([None] * dimensions[1])
    # Последовательность координат для размещения
    coordinates_sequence = get_list_of_coordinates(dimensions)
    # Разместим элемент x1 на плате
    pos_matrix[0][0] = 0
    graph.add_to_used_verticies([0])
    connectivity = graph.get_connectivity_with_used_verticies()
    # Очередь на размещение
    positioning_queue = get_all_max_indicies(connectivity)
    if info:
        print("Число связей для каждого элемента: ", graph.get_all_local_degrees())
        print("Коэффициенты связности: ", connectivity)
    for i in range(1, dimensions[0] * dimensions[1]):
        positioning_element = positioning_queue[0]
        positioning_queue = positioning_queue[1:]
        # Размещаем positioning_element
        x, y = coordinates_sequence[i]
        pos_matrix[x][y] = positioning_element
        graph.add_to_used_verticies([positioning_element])
        if len(positioning_queue) == 0:
            connectivity = graph.get_connectivity_with_used_verticies()
            positioning_queue = get_all_max_indicies(connectivity)           
        if info:
            print("ШАГ #%d" % (i) + "-"*40)
            print("Коэффициенты связности: ", connectivity)
            print("Выбираем для размещения элемент x%d" % (positioning_element+1))
    return pos_matrix

def get_l(pos_matrix, v1, v2):
    v1_i, v1_j = 0, 0
    v2_i, v2_j = 0, 0
    for i in range(0, len(pos_matrix)):
        for j in range(0, len(pos_matrix[i])):
            if pos_matrix[i][j] == v1:
                v1_i, v1_j = i, j
            elif pos_matrix[i][j] == v2:
                v2_i, v2_j = i, j
    return abs(v1_i - v2_i) + abs(v1_j - v2_j)

def get_Y_X_distance(pos_matrix, v1, v2):
    v1_i, v1_j = 0, 0
    v2_i, v2_j = 0, 0
    for i in range(0, len(pos_matrix)):
        for j in range(0, len(pos_matrix[i])):
            if pos_matrix[i][j] == v1:
                v1_i, v1_j = i, j
            elif pos_matrix[i][j] == v2:
                v2_i, v2_j = i, j
    return abs(v1_i - v2_i), abs(v1_j - v2_j)

def get_l_array(graph, pos_matrix):
    l = []
    for i in range(0, graph.get_number_of_verticies()):
        tmp_list = []
        for j in range(0, graph.get_number_of_verticies()):
            if graph.get_num_of_edges(i, j) == 0:
                tmp_list.append(None)
            else:
                tmp_list.append( get_l(pos_matrix, i, j) )
        l.append(tmp_list)
    return l

# Вычисление целевой функции для задачи размещения
def calculate_Q_positioning(graph, l_arr):
    Q = 0
    for i in range(0, graph.get_number_of_verticies()):
        for j in range(0, graph.get_number_of_verticies()):
            if l_arr[i][j] is not None:
                Q += l_arr[i][j] * graph.get_num_of_edges(i, j)
    return int(Q/2)

# Вычисление средних расстояний между одним и остальными элементами
def get_L_array(graph, l_arr):
    L = []
    local_degrees = graph.get_all_local_degrees()
    for i in range(0, graph.get_number_of_verticies()):
        all_adjacent_verticies = graph.get_all_adjacent_verticies(i)
        L_value = 0
        for j in range(0, len(all_adjacent_verticies)):
            L_value += graph.get_num_of_edges(i, all_adjacent_verticies[j]) * l_arr[i][all_adjacent_verticies[j]]
        L.append(L_value/local_degrees[i])
    return L

def print_arr(arr, string = None):
    if string is not None:
        print(string)
    for i in range(0, len(arr)):
        print('|', end='')
        for j in range(0, len(arr[i])):
            print(" %4s " % arr[i][j], end='')
        print('|')

def calculate_Xc(graph, pos_matrix, v_index):
    all_adjacent_verticies = graph.get_all_adjacent_verticies(v_index)
    X_coords = []
    for i in range(0, len(all_adjacent_verticies)):
        _, xd = get_all_coords_with_value(pos_matrix, all_adjacent_verticies[i])[0]
        X_coords.append(xd)
    sum = 0    
    for i in range(0, len(all_adjacent_verticies)):
        sum += graph.get_num_of_edges(v_index, all_adjacent_verticies[i]) * X_coords[i]
    return sum/graph.get_local_degree(v_index)

def calculate_Yc(graph, pos_matrix, v_index):
    all_adjacent_verticies = graph.get_all_adjacent_verticies(v_index)
    Y_coords = []
    for i in range(0, len(all_adjacent_verticies)):
       yd, _ = get_all_coords_with_value(pos_matrix, all_adjacent_verticies[i])[0]
       Y_coords.append(yd)
    sum = 0    
    for i in range(0, len(all_adjacent_verticies)):
        sum += graph.get_num_of_edges(v_index, all_adjacent_verticies[i]) * Y_coords[i]
    return sum/graph.get_local_degree(v_index)

def get_elements_by_coords(graph, pos_matrix, v_index, xc, yc):
    v_y, v_x = get_all_coords_with_value(pos_matrix, v_index)[0]
    x_is_greater = xc > v_x
    y_is_greater = yc > v_y
    elements = []
    if x_is_greater and y_is_greater:
        for i in range(v_y, len(pos_matrix)):
            for j in range(v_x, len(pos_matrix[i])):
                if graph.get_num_of_edges(v_index, pos_matrix[i][j]) > 0:
                    elements.append(pos_matrix[i][j])
    elif x_is_greater and not y_is_greater:
        for i in range(0, v_y):
            for j in range(v_x, len(pos_matrix[i])):
                if graph.get_num_of_edges(v_index, pos_matrix[i][j]) > 0:
                    elements.append(pos_matrix[i][j])
    elif not x_is_greater and y_is_greater:
        for i in range(v_y, len(pos_matrix)):
            for j in range(0, v_x):
                if graph.get_num_of_edges(v_index, pos_matrix[i][j]) > 0:
                    elements.append(pos_matrix[i][j])
    else:
        for i in range(0, v_y):
            for j in range(0, v_x):
                if graph.get_num_of_edges(v_index, pos_matrix[i][j]) > 0:
                    elements.append(pos_matrix[i][j])
    return elements


# Итерационный алгоритм размещения
def iterative_positioning_algorithm(graph, pos_matrix, info = True):
    graph.clear_used_verticies()
    # l = get_l_array(graph, pos_matrix)
    # print_arr(l, "Matrix of l ------------------------")
    # L = get_L_array(graph, l)
    # print(L)
    # max_index = get_max_index(L)
    # print("Choose x%d" % (max_index+1))
    # X_c = calculate_Xc(graph, pos_matrix, max_index)
    # print("Xc: ", X_c)
    # Y_c = calculate_Yc(graph, pos_matrix, max_index)
    # print("Yc: ", Y_c)
    # print("Choosing from elements: ")
    # elements = get_elements_by_coords(graph, pos_matrix, max_index, X_c, Y_c)
    # print(elements)
    # Q = calculate_Q_positioning(graph, l)
    # print("Q = ", calculate_Q_positioning(graph, l))
    # Qs = []
    # for i in range(0, len(elements)):
    #     tmp_pos_matrix = copy.deepcopy(pos_matrix)
    #     v_y, v_x = get_all_coords_with_value(pos_matrix, max_index)[0]
    #     y, x = get_all_coords_with_value(pos_matrix, elements[i])[0]
    #     tmp_pos_matrix[v_y][v_x], tmp_pos_matrix[y][x] = tmp_pos_matrix[y][x], tmp_pos_matrix[v_y][v_x]
    #     Qs.append(calculate_Q_positioning(graph, get_l_array(graph, tmp_pos_matrix)))

    # print("New Qs: ", Qs)
    # # Выбираем перестановку основываясь на целевой функции
    # min_index = get_min_index(Qs)
    # if Qs[min_index] < Q:
    #     v_y, v_x = get_all_coords_with_value(pos_matrix, max_index)[0]
    #     y, x = get_all_coords_with_value(pos_matrix, elements[min_index])[0]
    #     pos_matrix[v_y][v_x], pos_matrix[y][x] = pos_matrix[y][x], pos_matrix[v_y][v_x]

    counter = 1
    continue_iterations = True
    while continue_iterations:
        # Вычисляем длину проводника
        l = get_l_array(graph, pos_matrix)
        # Вычисляем средние расстояния
        L = get_L_array(graph, l)
        # Находим лучшего кандидата для перестановки
        max_index = get_max_index(L)
        # В какую сторону переставлять
        X_c = calculate_Xc(graph, pos_matrix, max_index)
        Y_c = calculate_Yc(graph, pos_matrix, max_index)
        # Находим подходящие элементы
        elements = get_elements_by_coords(graph, pos_matrix, max_index, X_c, Y_c)
        # Находим текущее значение целевой функции
        Q = calculate_Q_positioning(graph, l)
        # Находим потенциальные значения целевой функции после перестановки
        Qs = []
        for i in range(0, len(elements)):
            tmp_pos_matrix = copy.deepcopy(pos_matrix)
            v_y, v_x = get_all_coords_with_value(pos_matrix, max_index)[0]
            y, x = get_all_coords_with_value(pos_matrix, elements[i])[0]
            tmp_pos_matrix[v_y][v_x], tmp_pos_matrix[y][x] = tmp_pos_matrix[y][x], tmp_pos_matrix[v_y][v_x]
            Qs.append(calculate_Q_positioning(graph, get_l_array(graph, tmp_pos_matrix)))
        # Выбираем перестановку основываясь на минимизации целевой функции
        min_index = get_min_index(Qs)
        continue_iterations = Qs[min_index] < Q
        if continue_iterations:
            v_y, v_x = get_all_coords_with_value(pos_matrix, max_index)[0]
            y, x = get_all_coords_with_value(pos_matrix, elements[min_index])[0]
            pos_matrix[v_y][v_x], pos_matrix[y][x] = pos_matrix[y][x], pos_matrix[v_y][v_x]
        # Вывод промежуточной информации
        if info:
            print("ШАГ #", counter, "="*40)
            print_arr(l, "Длины проводника: l ------------------------")
            print("Средние расстояния: ", L)
            print("Выбранная для перестановки вершина x%d" % (max_index+1))
            print("Xc: ", X_c)
            print("Yc: ", Y_c)
            print("Значение целевой функции: ", Q)
            print("Потенциальные элементы для перестановки: ", elements)
            print("Потенциальные значения цел. функ. после перестановки: ", Qs)
            if continue_iterations:
                print("[!]Меняем местами x" + str(max_index+1) + " и x" + str(elements[min_index]+1))
        counter += 1
    return pos_matrix