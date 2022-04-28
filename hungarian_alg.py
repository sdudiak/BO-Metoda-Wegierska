from cmath import inf


class Hungarian:
    def __init__(self, matrix):
        self.matrix = matrix  # matrix[task][machine] = cost
        self.theta = 0  # total matrix reduction

    def reduce_matrix(self):  # method subtracting lowest values from rows and columns
        # rows:
        for i, _ in enumerate(self.matrix):
            self.theta += min(self.matrix[i])
            self.matrix[i] = [elem - min(self.matrix[i]) for elem in self.matrix[i]]
        # cols:
        for j, _ in enumerate(self.matrix):
            min_col_val = inf
            for i, _ in enumerate(self.matrix[i]):  # find minimal value
                if self.matrix[i][j] < min_col_val: min_col_val = self.matrix[i][j]

            self.theta += min_col_val

            for i, _ in enumerate(self.matrix[i]):  # subtract minimal value
                self.matrix[i][j] -= min_col_val


matrix_example = [
    [0, 0, 1, 0, 5],
    [1, 6, 2, 0, 3],
    [1, 2, 1, 5, 0],
    [3, 9, 0, 4, 0],
    [1, 1, 2, 4, 0]
]

independent_zeros = [(0, 0), (1, 3), (2, 4), (3, 2)]
dependent_zeros = [(0, 1), (0, 3), (3, 4), (4, 4)]


def zero_crossing(matrix, ind_zeros, dep_zeros):
    select_row = [i for i in range(len(matrix))]
    select_col = []
    # Oznaczyć symbolem x każdy wiersz nie posiadający niezależnego zera
    for el in ind_zeros:
        select_row.remove(el[0])

    while True:
        selected = False
        # Oznaczyć symbolem x każda kolumnę mającą zero zależne 0 w oznaczonym wierszu
        for row in select_row:
            # for col in matrix[row]:
            for col in range(len(matrix[row])):
                for zero in dep_zeros:
                    if zero[0] == row and zero[1] == col:
                        if col not in select_col:
                            select_col.append(col)
                            selected = True

        # Oznaczyć symbolem x każdy wiersz mający w oznakowanej kolumnie niezależne zero
        for col in select_col:
            for row in range(len(matrix)):
                for zero in ind_zeros:
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
    for i in range(len(matrix)):
        if i not in select_row:
            cross_row.append(i)
    cross_row.sort()
    return cross_row, cross_col


print(zero_crossing(matrix_example, independent_zeros, dependent_zeros))
