from cmath import inf


class Hungarian:
    def __init__(self, matrix):
        self.matrix = matrix  # matrix[task][machine] = cost
        self.theta = 0  # total matrix reduction
        self.ind_zeros = []  # independent zeros (starring)
        self.dep_zeros = []  # dependent zeros  (primed)
        self.cross_row = []  # crossed row
        self.cross_col = []  # crossed column
        self.assigned = []  # starred zeros
        self.markedRows = []  # row with starred zero
        self.markedCols = []  # col with starred zero
        self.primedZeros = []  # primed zero

    def reduce_matrix(self):  # method subtracting lowest values from rows and columns
        # rows:
        for i, _ in enumerate(self.matrix):
            self.theta += min(self.matrix[i])
            self.matrix[i] = [elem - min(self.matrix[i]) for elem in self.matrix[i]]
        # cols:
        for j, _ in enumerate(self.matrix):
            min_col_val = inf
            for i, _ in enumerate(self.matrix[j]):  # find minimal value
                if self.matrix[i][j] < min_col_val: min_col_val = self.matrix[i][j]

            self.theta += min_col_val

            for i, _ in enumerate(self.matrix[j]):  # subtract minimal value
                self.matrix[i][j] -= min_col_val

    def zeroCover(self):
        self.assigned = []  # starred zeros
        self.markedRows = []  # row with starred zero
        self.markedCols = []  # col with starred zero
        self.primedZeros = []  # primed zero
        self.assign()
        # return f"starred: {self.assigned} primed: {self.primedZeros}"
        self.ind_zeros = self.assigned
        self.dep_zeros = self.primedZeros

    def assign(self):
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix)):
                # starring zero and covering columns
                if (row not in self.markedRows) and (col not in self.markedCols) and (self.matrix[row][col] == 0):
                    self.assigned.append((row, col))
                    self.markedRows.append(row)
                    self.markedCols.append(col)
                if ((row, col) not in self.assigned) and (self.matrix[row][col] == 0):
                    self.primedZeros.append((row, col))

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

    def get_more_independent_zeros(self):  # method for further matrix reduction
        min_matrix_val = inf
        for i, _ in enumerate(self.matrix):  # find minimal value uncrossed value in matrix
            for j, _ in enumerate(self.matrix[i]):
                if i not in self.cross_row and j not in self.cross_col and self.matrix[i][j] < min_matrix_val:
                    min_matrix_val = self.matrix[i][j]
        # add minval
        for i, _ in enumerate(self.matrix):  # subtract minimal value from uncrossed elems
            for j, _ in enumerate(self.matrix[i]):
                if i in self.cross_row and j not in self.cross_col: continue
                if i in self.cross_row and j in self.cross_col:
                    self.matrix[i][j] += min_matrix_val  # add minimal value to double crossed elements
                if j in self.cross_col: continue
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
            self.zeroCover()
            print("Wyznaczone zera:")
            print("Współrzędne zer niezależnych: {}".format(self.ind_zeros))
            print("Współrzędne zer zależnych: {}\n".format(self.dep_zeros))
            # if len(self.ind_zeros) == len(self.matrix):
            #     return self.ind_zeros

            self.zero_crossing()
            print("Wiersze do wykreślenia: {}".format(self.cross_row))
            print("Kolumny do wykreślenia: {}\n".format(self.cross_col))

            if len(self.cross_col) + len(self.cross_row) == len(self.matrix):
                return self.ind_zeros
            self.get_more_independent_zeros()
            print("Macierz po powiększeniu zbioru zer niezależnych")
            for row in self.matrix:
                print(row)
            print("Wielkość redukcji macierzy: {}\n".format(self.theta))


matrix_e = [
    [5, 2, 3, 2, 7],
    [6, 8, 4, 2, 5],
    [6, 4, 3, 7, 2],
    [6, 9, 0, 4, 0],
    [4, 1, 2, 4, 0]
]

m = Hungarian(matrix_e)
m.algorithm()
