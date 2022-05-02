class Whatever:
    def __init__(self, m):
        self.matrix = m

    def zeroCover(self):
        self.assigned = []  # starred zeros
        self.markedRows = []  # row with starred zero
        self.markedCols = []  # col with starred zero
        self.primedZeros = []  # primed zero
        self.assign()

        return f"starred: {self.assigned} primed: {self.primedZeros}"

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


# mat = [
#     [0, 4, 2, 7, 0, 1],
#     [5, 2, 8, 1, 0, 2],
#     [7, 3, 0, 7, 1, 0],
#     [8, 5, 1, 0, 6, 8],
#     [0, 5, 2, 7, 0, 4],
#     [1, 4, 0, 5, 2, 0]
# ]


# mat = [
#     [0, 1, 0, 1],
#     [1, 0, 1, 0],
#     [0, 1, 1, 1],
#     [0, 1, 1, 1]
# ]

# mat = [
#     [0, 0, 1, 0, 6],
#     [1, 6, 2, 0, 4],
#     [0, 1, 0, 4, 0],
#     [3, 9, 0, 4, 1],
#     [0, 0, 1, 3, 0]
# ]

mat = [
    [0, 0, 1, 0, 5],
    [1, 6, 2, 0, 3],
    [1, 2, 1, 5, 0],
    [3, 9, 0, 4, 0],
    [1, 1, 2, 4, 0]
]


a = Whatever(mat)
print(a.zeroCover())
