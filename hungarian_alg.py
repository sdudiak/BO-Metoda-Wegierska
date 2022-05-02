from cmath import inf


class Hungarian:
    def __init__(self, matrix):
        self.matrix = matrix  # matrix[task][machine] = cost
        self.theta = 0  # total matrix reduction
        self.ind_zeros = []  # współrzędne zer niezależnych
        self.dep_zeros = []  # współrzędne zer zależnych
        self.cross_row = []  # wiersze do przekreślenia
        self.cross_col = []  # kolumny do przekreślenia

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
        ind_zeros = []  # współrzędne zer niezależnych
        dep_zeros = []  # współrzędne zer zależnych
        size = len(self.matrix)  # rozmiar macierzy

        for number in range(1, size):  # Dla liczby zer w wierszu
            for idx, row in enumerate(self.matrix):  # dla każdego wiersza macierzy
                if row.count(0) == number:  # jeśli liczba zer w wierszu wynosi number
                    added = False  # zmienna do sprawdzania czy znaleziono zero niezalezne
                    for idy, col in enumerate(row):  # dla każdej kolumny
                        # jeśli znaleziono zero, nie jest to zero niezależne i kolumna nie jest już w innym zerze
                        if col == 0 and not added and idy not in [el[1] for el in ind_zeros]:
                            another_zero_in_col = False  # zmiienna do spradzania większej ilości zer w kolumnie
                            for row_in_col in range(size):  # dla każdego wiersza w kolumnie
                                # jeśli znaleziono zero i nie jest to wiersz row
                                if self.matrix[row_in_col][idy] == 0 and row_in_col != row:
                                    another_zero_in_col = True  # znaleziono zero
                            if not another_zero_in_col:  # jeśli nie znaleziono więcej zer
                                added = True  # znaleziono zero niezalezne
                                ind_zeros.append((idx, idy))  # dodaj współrzędną do zer niezależnych

                    if not added:  # jeśli nie znaleziono zera niezależnego
                        for idy, col in enumerate(row):  # dla każdej kolumny macierzy
                            #  znajdź pierwsze zero, którego kolumna nie jest już w zerach niezaleznych
                            if col == 0 and idy not in [el[1] for el in ind_zeros]:
                                ind_zeros.append((idx, idy))  # dodaj do zer niezależnych
                                break

        # dodanie zer zależnych
        for row in range(size):  # dla każdego wiersza
            for col in range(size):  # dla każdej kolumny
                # jeśli znaleziono zero i nie jest to zero niezależne lub niezależne
                if self.matrix[row][col] == 0 and (row, col) not in ind_zeros:
                    dep_zeros.append((row, col))  # znaleziono zero zależne

        self.ind_zeros = ind_zeros
        self.dep_zeros = dep_zeros

    def zero_crossing(self):
        select_row = [i for i in range(len(self.matrix))]  # tablica na zaznaczone wiersze
        select_col = []  # tablica na zaznaczone kolumny
        # Oznaczyć symbolem x każdy wiersz nie posiadający niezależnego zera
        for el in self.ind_zeros:  # dla każdego elementu w tablicy zer niezależnych
            select_row.remove(el[0])  # usuń wiersz z tablicy zaznaczonych, w którym jest zero niezależne

        while True:  # do póki znajdowane są nowe zaznaczenia
            selected = False  # zmienna do sprawdzania czy znaleziono nowe zaznaczenia

            # Oznaczyć symbolem x każda kolumnę mającą zero zależne 0 w oznaczonym wierszu
            for row in select_row:  # dla każdego wiersza w zaznaczonych wierszach
                for col in range(len(self.matrix[row])):  # dla każdej kolumny macierzy
                    # for zero in self.dep_zeros:  # dla każdego zera zależnego
                    #     if zero[0] == row and zero[1] == col:
                    if (row, col) in self.dep_zeros:  # jeśli współrzędne są równe współrzędnym zera zależnego
                        if col not in select_col:  # jeśli kolumna nie jest w zaznaczonych kolumnach
                            select_col.append(col)  # dodaj do zaznaczonych kolumn
                            selected = True  # zaznaczono

            # Oznaczyć symbolem x każdy wiersz mający w oznakowanej kolumnie niezależne zero
            for col in select_col:  # dla każdej kolumny w zaznaczonych kolumnach
                for row in range(len(self.matrix)):  # dla każdego wiersza macierzy
                    # for zero in self.ind_zeros:
                    #     if zero[0] == row and zero[1] == col:
                    if (row, col) in self.ind_zeros:  # jeśli współrzędne są równe współrzędnym zera niezależnego
                        if row not in select_row:  # jeśli wiersz nie jest w zaznaczonych wierszach
                            select_row.append(row)  # dodaj do zaznaczonych wierszy
                            selected = True  # zaznaczono
            if not selected:  # jeśli nie zaznaczono
                break  # przerwij

        # Poszukiwanie minimalnego pokrycia wierzchołkowego.
        cross_col = select_col  # tablica kolumn do skreślenia jest równa tablicy zaznaczonych kolumn
        cross_col.sort()  # posortuj tablice kolumn
        cross_row = []  # tablica kolumn do skreślenia
        for i in range(len(self.matrix)):  # dla każdego wiersza macierzy
            if i not in select_row:  # jeśli wiersz nie jest zaznaczony
                cross_row.append(i)  # dodaj wiersz do skreślenia
        cross_row.sort()  # posortuj tablice wierszy
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

        self.reduce_matrix()  # zredukowanie macierzy
        print("Macierz po początkowej redukcji")
        for row in self.matrix:
            print(row)
        print("Wielkość redukcji macierzy: {}\n".format(self.theta))

        while True:
            self.assign()  # wyznaczenie zer niezaleznych i zależnych
            print("Wyznaczone zera:")
            print("Współrzędne zer niezależnych: {}".format(self.ind_zeros))
            print("Współrzędne zer zależnych: {}\n".format(self.dep_zeros)) if self.dep_zeros else print()
            if len(self.ind_zeros) == len(self.matrix):
                break

            self.zero_crossing()  # wyznaczenie wierszy i kolumn do zakreślenia
            print("Wiersze do wykreślenia: {}".format(self.cross_row))
            print("Kolumny do wykreślenia: {}\n".format(self.cross_col))

            # if len(self.cross_col) + len(self.cross_row) == len(self.matrix):
            #     break
            self.get_more_independent_zeros()  # wyznaczenie wiecej zer niezależnych
            print("Macierz po powiększeniu zbioru zer niezależnych")
            for row in self.matrix:
                print(row)
            print("Wielkość redukcji macierzy: {}\n".format(self.theta))

        print("Macierz końcowa")
        for row in self.matrix:
            print(row)
        print()

        # stworzenie tablicy rozwiązania optymalnego
        result = [[0 for i in range(len(self.matrix))] for j in range(len(self.matrix))]  # stworzenie macierzy zer
        for row in range(len(self.matrix)):  # dla każdego wiersza
            for col in range(len(self.matrix)):  # dla każdej  kolumny
                if (row, col) in self.ind_zeros:  # jesli współrzędne to współrzędne zera niezależnego
                    result[row][col] = 1  # zmień zero na 1

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

matrix = [
    [3, 2, 4, 5, 2, 1],
    [7, 3, 4, 5, 1, 1],
    [2, 2, 3, 3, 5, 6],
    [1, 3, 4, 5, 6, 2],
    [2, 1, 3, 3, 4, 5],
    [1, 0, 2, 4, 2, 3]
]

m = Hungarian(matrix)
m.algorithm()
