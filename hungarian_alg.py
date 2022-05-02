from cmath import inf


class Hungarian:
    def __init__(self, matrix):
        self.matrix = matrix  # matrix[task][machine] = cost
        self.theta = 0  # total matrix reduction
        self.ind_zeros = []  # independent zeros (starring)
        self.dep_zeros = []  # dependent zeros  (primed)
        self.cross_row = []  # crossed row
        self.cross_col = []  # crossed column

    def reduce_matrix(self):  # method subtracting lowest values from rows and columns
        # rows:
        for i, _ in enumerate(self.matrix):
            self.theta += min(self.matrix[i])
            self.matrix[i] = [elem - min(self.matrix[i])
                              for elem in self.matrix[i]]
        # cols:
        for j, _ in enumerate(self.matrix):
            min_col_val = inf
            for i, _ in enumerate(self.matrix[j]):  # find minimal value
                if self.matrix[i][j] < min_col_val:
                    min_col_val = self.matrix[i][j]

            self.theta += min_col_val

            for i, _ in enumerate(self.matrix[j]):  # subtract minimal value
                self.matrix[i][j] -= min_col_val

    def assign(self):
        ind_zeros = []
        dep_zeros = []
        size = len(self.matrix)
        # Pierwsza iteracja w celu znalezienia pojedynczych zer niezależnych w wierszu
        for idx, row in enumerate(self.matrix):
            if row.count(0) == 0:
                continue
            elif row.count(0) == 1:
                for idy, col in enumerate(row):
                    if col == 0 and idy not in [el[1] for el in ind_zeros]:
                        ind_zeros.append((idx, idy))

        # Kolejna iteracja w celu znalezienia zera niezależnego w wierszach z większą ilością zer
        for number in range(2, size):
            for idx, row in enumerate(self.matrix):
                if row.count(0) == number:
                    added = False
                    for idy, col in enumerate(row):
                        if col == 0 and not added and idy not in [el[1] for el in ind_zeros]:
                            another_zero_in_col = False
                            for row_in_col in range(size):
                                if self.matrix[row_in_col][idy] == 0 and row_in_col != row:
                                    another_zero_in_col = True
                            if not another_zero_in_col:
                                added = True
                                ind_zeros.append((idx, idy))

                    if not added:
                        for idy, col in enumerate(row):
                            if col == 0 and idy not in [el[1] for el in ind_zeros]:
                                ind_zeros.append((idx, idy))
                                break

            for row in range(size):
                for col in range(size):
                    if self.matrix[row][col] == 0 and (row, col) not in ind_zeros:
                        dep_zeros.append((row, col))

        self.ind_zeros = ind_zeros
        self.dep_zeros = dep_zeros

    def zero_crossing(self):
        select_row = [i for i in range(len(self.matrix))]
        select_col = []
        # Oznaczyć symbolem x każdy wiersz nie posiadający niezależnego zera
        for el in self.ind_zeros:
            select_row.remove(el[0])

        while True:
            selected = False
            # Oznaczyć symbolem x każda kolumnę mającą zero zależne 0 w oznaczonym wierszu
            for row in select_row:
                # for col in matrix[row]:
                for col in range(len(self.matrix[row])):
                    for zero in self.dep_zeros:
                        if zero[0] == row and zero[1] == col:
                            if col not in select_col:
                                select_col.append(col)
                                selected = True

            # Oznaczyć symbolem x każdy wiersz mający w oznakowanej kolumnie niezależne zero
            for col in select_col:
                for row in range(len(self.matrix)):
                    for zero in self.ind_zeros:
                        if zero[0] == row and zero[1] == col:
                            if row not in select_row:
                                select_row.append(row)
                                selected = True
            if not selected:
                break

        # Poszukiwanie minimalnego pokrycia wierzchołkowego.
        cross_col = select_col
        cross_col.sort()
        cross_row = []
        for i in range(len(self.matrix)):
            if i not in select_row:
                cross_row.append(i)
        cross_row.sort()
        self.cross_row = cross_row
        self.cross_col = cross_col

    # method for further matrix reduction
    def get_more_independent_zeros(self):
        min_matrix_val = inf
        # find minimal value uncrossed value in matrix
        for i, _ in enumerate(self.matrix):
            for j, _ in enumerate(self.matrix[i]):
                if i not in self.cross_row and j not in self.cross_col and self.matrix[i][j] < min_matrix_val:
                    min_matrix_val = self.matrix[i][j]
        # add minval
        # subtract minimal value from uncrossed elems
        for i, _ in enumerate(self.matrix):
            for j, _ in enumerate(self.matrix[i]):
                if i in self.cross_row and j not in self.cross_col:
                    continue
                if i in self.cross_row and j in self.cross_col:
                    # add minimal value to double crossed elements
                    self.matrix[i][j] += min_matrix_val
                if j in self.cross_col:
                    continue
                self.matrix[i][j] -= min_matrix_val
        self.theta += min_matrix_val

    def algorithm(self):
        print("Macierz wejściowa:")
        for row in self.matrix:
            print(row)
        print()

        self.reduce_matrix()
        print("Macierz po początkowej redukcji")
        for row in self.matrix:
            print(row)
        print("Wielkość redukcji macierzy: {}\n".format(self.theta))

        while True:
            self.assign()
            print("Wyznaczone zera:")
            print("Współrzędne zer niezależnych: {}".format(self.ind_zeros))
            print("Współrzędne zer zależnych: {}\n".format(self.dep_zeros)) if self.dep_zeros else print()
            if len(self.ind_zeros) == len(self.matrix):
                break

            self.zero_crossing()
            print("Wiersze do wykreślenia: {}".format(self.cross_row))
            print("Kolumny do wykreślenia: {}\n".format(self.cross_col))

            # if len(self.cross_col) + len(self.cross_row) == len(self.matrix):
            #     break
            self.get_more_independent_zeros()
            print("Macierz po powiększeniu zbioru zer niezależnych")
            for row in self.matrix:
                print(row)
            print("Wielkość redukcji macierzy: {}\n".format(self.theta))

        print("Macierz końcowa")
        for row in self.matrix:
            print(row)
        print()

        result = [[0 for i in range(len(self.matrix))] for j in range(len(self.matrix))]
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                for z in self.ind_zeros:
                    if z[0] == i and z[1] == j:
                        result[i][j] = 1

        print("Rozwiązanie optymalne")
        for row in result:
            print(row)
        print("Wartość funkcji kryterialnej: {}\n".format(self.theta))


matrix_e = [
    [5, 2, 3, 2, 7],
    [6, 8, 4, 2, 5],
    [6, 4, 3, 7, 2],
    [6, 9, 0, 4, 0],
    [4, 1, 2, 4, 0]
]

matrix_2 = [
    [3, 2, 4, 5, 2, 1],
    [7, 3, 4, 5, 1, 1],
    [2, 2, 3, 3, 5, 6],
    [1, 3, 4, 5, 6, 2],
    [2, 1, 3, 3, 4, 5],
    [1, 0, 2, 4, 2, 3]
]

m = Hungarian(matrix_2)
m.algorithm()
