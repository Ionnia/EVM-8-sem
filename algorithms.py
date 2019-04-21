from graph import Graph


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
def sequential_algorithm(graph, group_sizes):
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
        print("Step #", k)
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
                # Удаляем эту вершину из группы
                group.remove(v_index_max_sigma)
            elif len(group) < group_sizes[k]:
                graph.add_to_used_verticies(group)
                min_local_degree_verticies = graph.get_min_local_degrees()
                best_verticies = graph.get_best_verticies(min_local_degree_verticies)
                # Добавляем в группу новые вершины
                group += [best_verticies[0]] + graph.get_all_adjacent_verticies(best_verticies[0])
        graph.add_to_used_verticies(group)
        result.append(group)
    return result
