class Graph:
    def __init__(self, matrix):
        self.matrix = matrix            # Матрица смежности
        self.px = []                    # Локальная степень каждой вершины
        self.size = len(self.matrix)    # Размерность матрицы
        self.used_verticies = set()     # Уже использованные для распределения вершины
        print("Set size ", len(self.used_verticies))
        for i in range(0, self.size):
            self.px.append(0)
            for j in range(0, self.size):
                self.px[i] += self.matrix[i][j]
        self.update_min_local_degrees()
        return
    
    def print_info(self):
        print('%3s|' % (''), end='')
        for i in range(0, self.size):
            if i not in self.used_verticies:
                print('%3s ' % ('x' + str(i)), end='')
        print('| %3s' % ('px'))
        for i in range(0, self.size):
            if i not in self.used_verticies:
                print('%3s|' % ('x' + str(i)), end='')
                for j in range(0, self.size):
                    if j not in self.used_verticies:
                        print('%3d ' % ( self.matrix[i][j] ), end='')
                print('| %3d' % (self.px[i]))

    def update_min_local_degrees(self):
        for i in range(0, self.size):
            self.px[i] = 0
            for j in range(0, self.size):
                if j not in self.used_verticies:
                    self.px[i] += self.matrix[i][j]

    # Возвращает list, в котором хранятся индексы всех вершин с минимальной локальной степенью
    def get_min_local_degrees(self):
        self.update_min_local_degrees()
        # Находим минимальную локальную степень
        min = self.px[0]
        for i in range(1, self.size):
            if (i not in self.used_verticies) and (self.px[i] < min):
                min = self.px[i]

        result = []     # Здесь хранятся индексы вершин
        # Находим все индексы вершин с минимальной локальной степенью
        for i in range(0, self.size):
            if (i not in self.used_verticies) and (self.px[i] == min):
                result.append(i)
        
        return result

    # Возвращает массив с индексами элементов, у которых наибольшее количество кратных рёбер
    def get_best_verticies(self, min_local_degree_verticies):
        # Массив содержащий количество кратных рёбер у вершины с индексами из min_local_degree_verticies
        num_of_multiple_edges = []
        for i in range(0, len(min_local_degree_verticies)):
            counter_of_multiple_edges = 0
            for j in range(0, self.size):
                if self.matrix[min_local_degree_verticies[i]][j] == 2:
                    counter_of_multiple_edges += 1
            num_of_multiple_edges.append(counter_of_multiple_edges)
        # Массив результата. Содержит индексы всех вершин с наибольшим колчеством кратных рёбер и
        # входящих в min_local_degree_verticies
        result = []
        # Максимальное количество кратных рёбер
        max_edges = num_of_multiple_edges[0]
        for i in range(1, len(num_of_multiple_edges)):
            if num_of_multiple_edges[i] > max_edges:
                max_edges = num_of_multiple_edges[i]
        # Находим все вершины с наибольшим количеством кратных рёбер
        for i in range(0, len(num_of_multiple_edges)):
            if num_of_multiple_edges[i] == max_edges:
                result.append(min_local_degree_verticies[i])
        return result

    # Получаем массив индексов всех вершин, смежных с вершиной v_index
    def get_all_adjacent_verticies(self, v_index):
        # list с индексами всех вершин, смежных с этой
        result = []
        for i in range(0, self.size):
            if (i not in self.used_verticies) and (self.matrix[v_index][i] > 0):
                result.append(i)
        return result
    
    def get_num_of_edges(self, v_index1, v_index2):
        return self.matrix[v_index1][v_index2]

    def add_to_used_verticies(self, arr):
        self.used_verticies.update(arr)
