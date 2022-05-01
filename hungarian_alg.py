class Whatever:
    def __init__(self, m):
        self.matrix = m

    def zeroCover(self):
        self.assigned = []  # starred zeros
        self.markedRows = []  # row with starred zero
        self.markedCols = []  # col with starred zero
        self.coveredCols = []  # line covering col
        self.coveredRows = []  # line covering row
        self.primedZeros = []  # primed zero
        self.assign()
        self.cover()
        self.nCover()
        # self.coveredRows = []
        # self.coveredCols = []
        self.assign()
        self.coverStar()
        self.cover()

        return f"starred: {self.assigned} cRow: {self.coveredRows}  cCol: {self.coveredCols} primed: {self.primedZeros}"

    def assign(self):
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix)):
                # starring zero and covering columns
                if (row not in self.markedRows) and (col not in self.markedCols) and (self.matrix[row][col] == 0):
                    self.assigned.append((row, col))
                    self.markedRows.append(row)
                    self.markedCols.append(col)
                    self.coveredCols.append(col)

    def cover(self):
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix)):
                if (row not in self.coveredRows) and (col not in self.coveredCols) and (row in self.markedRows) and ((row, col) not in self.assigned) and (self.matrix[row][col] == 0):
                    self.primedZeros.append((row, col))
                    self.coveredRows.append(row)
                    for i in self.assigned:
                        if i[0] == row and i[1] in self.coveredCols:
                            self.coveredCols.remove(i[1])

    def nCover(self):
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix)):
                if (row not in self.coveredRows) and (col not in self.coveredCols) and (row not in self.markedRows) and (self.matrix[row][col] == 0):
                    if col in self.markedCols:
                        for star in self.assigned:
                            if star[1] == col:
                                for prime in self.primedZeros:
                                    if prime[0] == star[0]:
                                        self.assigned.remove(
                                            (star[0], star[1]))
                                        self.primedZeros.remove(
                                            (prime[0], prime[1]))
                                        self.assigned.append(
                                            (prime[0], prime[1]))
                                        if star[0] in self.coveredRows:
                                            self.coveredRows.remove(star[0])
                                        else:
                                            self.coveredCols.remove(star[1])
                                        if star[0] in self.markedRows:
                                            self.markedRows.remove(star[0])
                                            self.markedRows.append(prime[0])
                                        if star[1] in self.markedCols:
                                            self.markedCols.remove(star[1])
                                            self.markedCols.append(prime[1])

    def coverStar(self):
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix)):
                if (row not in self.coveredRows) and (col not in self.coveredCols) and ((row, col) in self.assigned):
                    self.coveredCols.append(col)

# mat = [
#     [0, 4, 2, 7, 0, 1],
#     [5, 2, 8, 1, 0, 2],
#     [7, 3, 0, 7, 1, 0],
#     [8, 5, 1, 0, 6, 8],
#     [0, 5, 2, 7, 0, 4],
#     [1, 4, 0, 5, 2, 0]
# ]


mat = [
    [0, 1, 0, 1],
    [1, 0, 1, 0],
    [0, 1, 1, 1],
    [0, 1, 1, 1]
]


a = Whatever(mat)
print(a.zeroCover())
